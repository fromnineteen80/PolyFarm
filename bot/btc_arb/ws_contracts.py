"""
Polymarket WebSocket — real-time BTC contract price streaming.

Replaces the 30-second REST polling in MarketScanner with
sub-second price updates via the Markets WebSocket.

Uses the same WS protocol as the sports bot (ws_markets.py):
  1. Connect to wss://api.polymarket.us/v1/ws/markets
  2. Subscribe to MARKET_DATA_LITE for each BTC market slug
  3. Receive real-time best bid, best ask, current price
  4. Update BTCMarket objects in the scanner instantly

This is critical for a latency arb — if we're blind to
contract price changes for 30 seconds, we miss exits and
enter on stale data.
"""
import asyncio
import json
import logging
import time
from typing import Optional

import websockets

from btc_arb.config import WS_MARKETS_URL, WS_BATCH_SIZE
from btc_arb.market_scanner import MarketScanner

logger = logging.getLogger("btc_arb.ws_contracts")


class ContractWebSocket:
    """
    Real-time Polymarket contract price feed via WebSocket.
    Updates MarketScanner's BTCMarket objects in place.
    """

    def __init__(self, scanner: MarketScanner):
        self.scanner = scanner
        self._running = False
        self._ws = None
        self._subscribed_slugs: set[str] = set()
        self._task: Optional[asyncio.Task] = None
        # Price update tracking
        self.updates_received = 0
        self.last_update_ms = 0

    async def start(self):
        """Start the WebSocket connection loop."""
        self._running = True
        self._task = asyncio.create_task(self._connect_loop())
        logger.info("Contract WebSocket starting")

    async def stop(self):
        """Stop the WebSocket."""
        self._running = False
        if self._ws:
            await self._ws.close()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(
            f"Contract WebSocket stopped. "
            f"Total updates: {self.updates_received}"
        )

    async def _connect_loop(self):
        """Maintain WebSocket connection with auto-reconnect."""
        while self._running:
            try:
                async with websockets.connect(
                    WS_MARKETS_URL,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    self._ws = ws
                    logger.info("Contract WS connected")

                    # Subscribe to all known markets
                    await self._subscribe_all()

                    # Process messages
                    async for msg in ws:
                        if not self._running:
                            break
                        await self._handle_message(msg)

            except websockets.ConnectionClosed:
                logger.warning(
                    "Contract WS disconnected, reconnecting..."
                )
                self._subscribed_slugs.clear()
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Contract WS error: {e}")
                self._subscribed_slugs.clear()
                await asyncio.sleep(2)

    async def _subscribe_all(self):
        """Subscribe to all known BTC market slugs."""
        slugs = list(self.scanner.markets.keys())
        if not slugs:
            logger.info("No BTC markets to subscribe to yet")
            return

        # Batch subscriptions (same pattern as sports bot)
        for i in range(0, len(slugs), WS_BATCH_SIZE):
            batch = slugs[i:i + WS_BATCH_SIZE]
            await self._subscribe_batch(batch)
            if i + WS_BATCH_SIZE < len(slugs):
                await asyncio.sleep(0.1)

    async def _subscribe_batch(self, slugs: list[str]):
        """Subscribe to a batch of market slugs."""
        if not self._ws:
            return

        for slug in slugs:
            if slug in self._subscribed_slugs:
                continue
            try:
                sub_msg = json.dumps({
                    "type": "subscribe",
                    "channel": "MARKET_DATA_LITE",
                    "slug": slug,
                })
                await self._ws.send(sub_msg)
                self._subscribed_slugs.add(slug)
            except Exception as e:
                logger.error(
                    f"Subscribe failed for {slug}: {e}"
                )

        logger.info(
            f"Subscribed to {len(slugs)} BTC markets "
            f"(total: {len(self._subscribed_slugs)})"
        )

    async def subscribe_new_markets(self):
        """
        Called when scanner discovers new markets.
        Subscribes only to markets not already subscribed.
        """
        new_slugs = [
            s for s in self.scanner.markets
            if s not in self._subscribed_slugs
        ]
        if new_slugs and self._ws:
            await self._subscribe_batch(new_slugs)

    async def _handle_message(self, raw: str):
        """
        Parse WS message and update BTCMarket prices.

        Expected format (MARKET_DATA_LITE):
        {
            "type": "market_data",
            "slug": "btc-above-84000-april-5",
            "marketData": {
                "bestBid": {"value": "0.62"},
                "bestAsk": {"value": "0.64"},
                "currentPx": {"value": "0.63"}
            }
        }
        """
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return

        msg_type = data.get("type", "")
        if msg_type not in ("market_data", "MARKET_DATA_LITE"):
            return

        slug = data.get("slug", "")
        market_data = data.get("marketData", {})
        if not slug or not market_data:
            return

        mkt = self.scanner.markets.get(slug)
        if not mkt:
            return

        # Extract prices
        current_px = market_data.get("currentPx", {})
        best_bid = market_data.get("bestBid", {})
        best_ask = market_data.get("bestAsk", {})

        yes_price = 0.0
        no_price = 0.0

        # Current price is our best estimate of YES price
        if current_px:
            yes_price = float(current_px.get("value", 0))
            no_price = 1.0 - yes_price

        # If we have bid/ask, use midpoint for better accuracy
        if best_bid and best_ask:
            bid = float(best_bid.get("value", 0))
            ask = float(best_ask.get("value", 0))
            if bid > 0 and ask > 0:
                yes_price = (bid + ask) / 2.0
                no_price = 1.0 - yes_price

        if yes_price > 0:
            mkt.update_prices(yes_price, no_price)
            self.updates_received += 1
            self.last_update_ms = int(time.time() * 1000)

    async def monitor_loop(self):
        """
        Periodically check for new markets to subscribe to
        and log connection health.
        """
        while self._running:
            await asyncio.sleep(30)
            try:
                # Subscribe to any newly discovered markets
                await self.subscribe_new_markets()

                # Health check
                now_ms = int(time.time() * 1000)
                stale = (
                    self.last_update_ms > 0
                    and (now_ms - self.last_update_ms) > 60_000
                )
                if stale:
                    logger.warning(
                        "Contract WS: no updates in 60s, "
                        "connection may be stale"
                    )
            except Exception as e:
                logger.error(f"WS monitor error: {e}")
