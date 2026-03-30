"""
Markets WebSocket handler using the official
polymarket-us SDK.
Streams real-time BBO price data and trade flow
for active market slugs.
Max 10 slugs per subscription (retail tier).
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from data.database import set_bot_config

if TYPE_CHECKING:
    from polymarket_us import AsyncPolymarketUS

logger = logging.getLogger("polyfarm.ws_markets")


class MarketsWebSocket:

    HEARTBEAT_TIMEOUT = 30
    RECONNECT_BASE = 1
    RECONNECT_MAX = 60
    BATCH_SIZE = 10

    def __init__(self, client, price_queue, trade_queue=None):
        self.client = client
        self.price_queue = price_queue
        self.trade_queue = trade_queue or asyncio.Queue(maxsize=500)
        self._ws = None
        self._subscribed_slugs: set = set()
        self._pending_slugs: set = set()
        self._last_heartbeat = None
        self._reconnect_delay = self.RECONNECT_BASE
        self._running = False
        self._price_history: dict = {}
        self._trade_flow: dict = {}
        self._HISTORY_WINDOW_SECONDS = 1800

    async def start(self):
        self._running = True
        while self._running:
            try:
                await self._connect_and_run()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(
                    f"Markets WS error: {e}. "
                    f"Reconnecting in {self._reconnect_delay}s"
                )
                try:
                    await set_bot_config("ws_markets_status", "DISCONNECTED")
                except Exception:
                    pass
                await asyncio.sleep(self._reconnect_delay)
                self._reconnect_delay = min(
                    self._reconnect_delay * 2, self.RECONNECT_MAX
                )

    async def stop(self):
        self._running = False
        if self._ws:
            await self._ws.close()

    async def _connect_and_run(self):
        self._ws = self.client.ws.markets()
        self._ws.on("market_data_lite", self._on_market_data_lite)
        self._ws.on("trade", self._on_trade)
        self._ws.on("heartbeat", self._on_heartbeat)
        self._ws.on("error", self._on_error)
        self._ws.on("close", self._on_close)

        await self._ws.connect()
        self._reconnect_delay = self.RECONNECT_BASE
        logger.info("Markets WebSocket connected")
        try:
            await set_bot_config("ws_markets_status", "CONNECTED")
        except Exception:
            pass

        if self._subscribed_slugs:
            await self._subscribe_batch(list(self._subscribed_slugs))

        self._last_heartbeat = datetime.now(timezone.utc)
        while self._running:
            await asyncio.sleep(5)
            if self._pending_slugs:
                new = list(self._pending_slugs)
                self._pending_slugs.clear()
                await self._subscribe_batch(new)
            if self._last_heartbeat:
                age = (datetime.now(timezone.utc) - self._last_heartbeat).total_seconds()
                if age > self.HEARTBEAT_TIMEOUT:
                    logger.warning("Markets WS heartbeat timeout. Reconnecting.")
                    await self._ws.close()
                    break

    async def _subscribe_batch(self, slugs):
        added = []
        ts = int(datetime.now().timestamp())
        for i in range(0, len(slugs), self.BATCH_SIZE):
            batch = slugs[i:i + self.BATCH_SIZE]
            batch_idx = i // self.BATCH_SIZE
            try:
                await self._ws.subscribe(
                    f"mdl-sub-{batch_idx}-{ts}",
                    "SUBSCRIPTION_TYPE_MARKET_DATA_LITE",
                    batch
                )
                added.extend(batch)
                logger.debug(f"Subscribed batch {batch_idx}: {len(batch)} slugs")
            except Exception as e:
                logger.error(f"Subscribe batch error: {e}")
        self._subscribed_slugs.update(added)

    async def subscribe_markets(self, slugs):
        new_slugs = [s for s in slugs if s not in self._subscribed_slugs]
        if not new_slugs:
            return
        if self._ws:
            await self._subscribe_batch(new_slugs)
        else:
            self._pending_slugs.update(new_slugs)

    # Backward-compatible alias
    async def subscribe_slugs(self, slugs):
        await self.subscribe_markets(slugs)

    async def unsubscribe_market(self, slug):
        self._subscribed_slugs.discard(slug)

    def get_subscribed_slugs(self):
        return self._subscribed_slugs.copy()

    def _append_price_history(self, slug, price, bid, ask):
        now = datetime.now(timezone.utc)
        entry = {"price": price, "bid": bid, "ask": ask, "timestamp": now.isoformat()}
        if slug not in self._price_history:
            self._price_history[slug] = []
        self._price_history[slug].append(entry)
        cutoff = now.timestamp() - self._HISTORY_WINDOW_SECONDS
        self._price_history[slug] = [
            e for e in self._price_history[slug]
            if datetime.fromisoformat(e["timestamp"]).timestamp() > cutoff
        ]

    def _record_trade_flow(self, slug, price, quantity, taker_intent):
        if slug not in self._trade_flow:
            self._trade_flow[slug] = {
                "buy_volume": 0.0,
                "sell_volume": 0.0,
                "window_start": datetime.now(timezone.utc).isoformat(),
            }
        dollar_volume = price * quantity
        if taker_intent == "ORDER_INTENT_BUY_LONG":
            self._trade_flow[slug]["buy_volume"] += dollar_volume
        else:
            self._trade_flow[slug]["sell_volume"] += dollar_volume

    def get_price_history(self, slug):
        return self._price_history.get(slug, [])

    def get_trade_flow(self, slug):
        return self._trade_flow.get(slug, {})

    def calculate_velocity(self, slug):
        history = self._price_history.get(slug, [])
        if len(history) < 2:
            return 0.0, "stable"
        oldest = history[0]
        newest = history[-1]
        try:
            t0 = datetime.fromisoformat(oldest["timestamp"]).timestamp()
            t1 = datetime.fromisoformat(newest["timestamp"]).timestamp()
            elapsed_minutes = (t1 - t0) / 60
            if elapsed_minutes < 0.1:
                return 0.0, "stable"
            price_change = (newest["price"] - oldest["price"]) * 100
            velocity = price_change / elapsed_minutes
            if velocity < -0.2:
                direction = "falling"
            elif velocity > 0.2:
                direction = "rising"
            else:
                direction = "stable"
            return round(velocity, 3), direction
        except Exception:
            return 0.0, "stable"

    def get_net_buy_pressure(self, slug):
        flow = self._trade_flow.get(slug, {})
        buy = flow.get("buy_volume", 0)
        sell = flow.get("sell_volume", 0)
        total = buy + sell
        if total < 10:
            return 1.0
        if sell == 0:
            return 2.0
        return round(buy / sell, 3)

    def _on_market_data_lite(self, data):
        try:
            d = data.get("marketDataLite", {})
            slug = d.get("marketSlug")
            if not slug:
                return
            bid = float(d.get("bestBid", {}).get("value", 0) or 0)
            ask = float(d.get("bestAsk", {}).get("value", 1) or 1)
            current = float(d.get("currentPx", {}).get("value", bid) or bid)

            event = {
                "market_slug": slug,
                "bid": bid,
                "ask": ask,
                "yes_price": ask,
                "current_px": current,
                "bid_depth": d.get("bidDepth", 0),
                "ask_depth": d.get("askDepth", 0),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            try:
                self.price_queue.put_nowait(event)
            except asyncio.QueueFull:
                try:
                    self.price_queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
                self.price_queue.put_nowait(event)
            self._append_price_history(slug, current, bid, ask)
        except Exception as e:
            logger.error(f"Market data lite error: {e}")

    def _on_trade(self, data):
        try:
            t = data.get("trade", {})
            slug = t.get("marketSlug")
            if not slug:
                return
            price = float(t.get("price", {}).get("value", 0) or 0)
            quantity = float(t.get("quantity", {}).get("value", 0) or 0)
            taker_intent = t.get("taker", {}).get("intent", "")
            try:
                self.trade_queue.put_nowait({
                    "market_slug": slug,
                    "price": price,
                    "quantity": quantity,
                    "trade_time": t.get("tradeTime"),
                })
            except asyncio.QueueFull:
                try:
                    self.trade_queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
                self.trade_queue.put_nowait({
                    "market_slug": slug,
                    "price": price,
                    "quantity": quantity,
                    "trade_time": t.get("tradeTime"),
                })
            self._record_trade_flow(slug, price, quantity, taker_intent)
        except Exception as e:
            logger.error(f"Trade event error: {e}")

    def _on_heartbeat(self, data):
        self._last_heartbeat = datetime.now(timezone.utc)

    def _on_error(self, error):
        logger.error(f"Markets WS error: {error}")

    def _on_close(self, data):
        logger.warning("Markets WS closed. Reconnect loop will restart.")
