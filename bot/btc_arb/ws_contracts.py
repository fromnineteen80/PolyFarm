"""
Polymarket WebSocket — real-time BTC contract price streaming.

Two modes:
  SDK mode (live): Uses client.ws.markets() from polymarket-us SDK.
    Auth handled automatically. Same pattern as sports bot ws_markets.py.
    Subscribes via SUBSCRIPTION_TYPE_MARKET_DATA_LITE.

  Fast-poll mode (paper): No SDK client available — falls back to
    REST polling every 2 seconds instead of 30. Not as fast as WS
    but 15x faster than the default scanner interval.

The WS API is v1 only (wss://api.polymarket.us/v1/ws/markets).
There is no v2 WebSocket — v2 is REST-only for discovery.
"""
import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

import httpx

from btc_arb.config import (
    WS_BATCH_SIZE,
    POLYMARKET_PUBLIC_URL,
)
from btc_arb.market_scanner import MarketScanner

if TYPE_CHECKING:
    from polymarket_us import AsyncPolymarketUS

logger = logging.getLogger("btc_arb.ws_contracts")


class ContractWebSocket:
    """
    Real-time Polymarket contract price feed.
    Updates MarketScanner's BTCMarket objects in place.
    """

    def __init__(
        self,
        scanner: MarketScanner,
        client: Optional["AsyncPolymarketUS"] = None,
    ):
        self.scanner = scanner
        self.client = client
        self._running = False
        self._ws = None
        self._subscribed_slugs: set[str] = set()
        self._pending_slugs: set[str] = set()
        self._task: Optional[asyncio.Task] = None
        self._last_heartbeat: Optional[datetime] = None

        # Tracking
        self.updates_received = 0
        self.last_update_ms = 0
        self.mode = "sdk" if client else "fast_poll"

    async def start(self):
        """Start price streaming."""
        self._running = True
        if self.mode == "sdk":
            self._task = asyncio.create_task(self._sdk_loop())
            logger.info(
                "Contract WS starting (SDK mode — real-time)"
            )
        else:
            self._task = asyncio.create_task(self._poll_loop())
            logger.info(
                "Contract WS starting (fast-poll mode — 2s interval)"
            )

    async def stop(self):
        """Stop the price stream."""
        self._running = False
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(
            f"Contract WS stopped ({self.mode}). "
            f"Updates: {self.updates_received}"
        )

    # ─── SDK Mode (live) ──────────────────────────────

    async def _sdk_loop(self):
        """
        Connect via SDK's client.ws.markets() — handles auth.
        Same pattern as bot/core/ws_markets.py.
        """
        reconnect_delay = 5
        while self._running:
            try:
                await self._sdk_connect_and_run()
                reconnect_delay = 5  # reset on clean disconnect
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(
                    f"Contract WS error: {e}. "
                    f"Reconnecting in {reconnect_delay}s"
                )
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 120)

    async def _sdk_connect_and_run(self):
        """Single SDK WebSocket session."""
        self._ws = self.client.ws.markets()
        self._ws.on(
            "market_data_lite", self._on_market_data_lite
        )
        self._ws.on("heartbeat", self._on_heartbeat)
        self._ws.on("error", self._on_ws_error)
        self._ws.on("close", self._on_ws_close)

        await self._ws.connect()
        logger.info("Contract WS connected (SDK)")
        self._subscribed_slugs.clear()

        # Subscribe to all known markets
        slugs = list(self.scanner.markets.keys())
        if slugs:
            await self._subscribe_batch(slugs)

        # Main loop — check for new markets and heartbeat
        self._last_heartbeat = datetime.now(timezone.utc)
        while self._running:
            await asyncio.sleep(5)

            # Subscribe any newly discovered markets
            if self._pending_slugs:
                new = list(self._pending_slugs)
                self._pending_slugs.clear()
                await self._subscribe_batch(new)

            # Heartbeat check
            if self._last_heartbeat:
                age = (
                    datetime.now(timezone.utc) - self._last_heartbeat
                ).total_seconds()
                if age > 30:
                    logger.warning(
                        "Contract WS heartbeat timeout. "
                        "Reconnecting."
                    )
                    await self._ws.close()
                    break

    async def _subscribe_batch(self, slugs: list[str]):
        """Subscribe slugs via SDK WS — batched in groups of 10."""
        if not self._ws:
            return
        new = [s for s in slugs if s not in self._subscribed_slugs]
        if not new:
            return

        ts = int(time.time())
        for i in range(0, len(new), WS_BATCH_SIZE):
            batch = new[i:i + WS_BATCH_SIZE]
            batch_idx = i // WS_BATCH_SIZE
            try:
                await self._ws.subscribe(
                    f"btc-mdl-{batch_idx}-{ts}",
                    "SUBSCRIPTION_TYPE_MARKET_DATA_LITE",
                    batch,
                )
                self._subscribed_slugs.update(batch)
                logger.debug(
                    f"Subscribed batch {batch_idx}: "
                    f"{len(batch)} slugs"
                )
            except Exception as e:
                logger.error(f"Subscribe batch error: {e}")

        logger.info(
            f"Subscribed {len(new)} BTC markets "
            f"(total: {len(self._subscribed_slugs)})"
        )

    def _on_market_data_lite(self, data: dict):
        """
        SDK callback for MARKET_DATA_LITE events.
        Payload: {slug, marketData: {bestBid, bestAsk, currentPx}}
        Each has .value as string.
        """
        slug = data.get("slug", "")
        market_data = data.get("marketData", {})
        if not slug or not market_data:
            return

        mkt = self.scanner.markets.get(slug)
        if not mkt:
            return

        # Extract prices — same parsing as sports bot
        best_bid = market_data.get("bestBid", {})
        best_ask = market_data.get("bestAsk", {})
        current_px = market_data.get("currentPx", {})

        yes_price = 0.0

        # Prefer bid/ask midpoint for accuracy
        if best_bid and best_ask:
            bid = float(best_bid.get("value", 0))
            ask = float(best_ask.get("value", 0))
            if bid > 0 and ask > 0:
                yes_price = (bid + ask) / 2.0

        # Fall back to currentPx
        if yes_price == 0 and current_px:
            yes_price = float(current_px.get("value", 0))

        if yes_price > 0:
            mkt.update_prices(yes_price, 1.0 - yes_price)
            self.updates_received += 1
            self.last_update_ms = int(time.time() * 1000)

    def _on_heartbeat(self, data: dict):
        self._last_heartbeat = datetime.now(timezone.utc)

    def _on_ws_error(self, data: dict):
        logger.error(f"Contract WS error event: {data}")

    def _on_ws_close(self, data: dict):
        logger.warning(f"Contract WS close event: {data}")

    # ─── Fast-Poll Mode (paper) ───────────────────────

    async def _poll_loop(self):
        """
        Paper mode fallback: poll REST every 2 seconds.
        Not as fast as WS but 15x faster than the default 30s scanner.
        """
        async with httpx.AsyncClient(timeout=5) as http:
            while self._running:
                try:
                    await self._poll_prices(http)
                except Exception as e:
                    logger.debug(f"Poll error: {e}")
                await asyncio.sleep(2)

    async def _poll_prices(self, http: httpx.AsyncClient):
        """Fetch latest prices for all tracked markets."""
        for slug, mkt in self.scanner.markets.items():
            try:
                resp = await http.get(
                    f"{POLYMARKET_PUBLIC_URL}/v2/markets/{slug}"
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()

                yes_price = 0.0
                no_price = 0.0

                # marketSides format
                sides = data.get("marketSides", [])
                for side in sides:
                    label = side.get("label", "").lower()
                    price = float(side.get("price", 0))
                    if label == "yes":
                        yes_price = price
                    elif label == "no":
                        no_price = price

                # outcomePrices fallback
                if yes_price == 0:
                    op = data.get("outcomePrices", [])
                    if len(op) >= 2:
                        yes_price = float(op[0])
                        no_price = float(op[1])

                if yes_price > 0:
                    mkt.update_prices(yes_price, no_price)
                    self.updates_received += 1
                    self.last_update_ms = int(time.time() * 1000)

            except Exception as e:
                logger.debug(f"Poll {slug} error: {e}")

    # ─── Shared ───────────────────────────────────────

    async def subscribe_new_markets(self):
        """Notify that scanner found new markets."""
        if self.mode == "sdk":
            new = [
                s for s in self.scanner.markets
                if s not in self._subscribed_slugs
            ]
            if new:
                self._pending_slugs.update(new)
        # In poll mode, new markets are picked up automatically

    async def monitor_loop(self):
        """Health monitoring — check for stale data."""
        while self._running:
            await asyncio.sleep(30)
            try:
                await self.subscribe_new_markets()

                now_ms = int(time.time() * 1000)
                if (
                    self.last_update_ms > 0
                    and (now_ms - self.last_update_ms) > 60_000
                ):
                    logger.warning(
                        f"Contract {self.mode}: "
                        f"no updates in 60s"
                    )
            except Exception as e:
                logger.error(f"WS monitor error: {e}")
