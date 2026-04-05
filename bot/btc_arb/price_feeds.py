"""
Real-time BTC price feeds.

Primary: Binance WebSocket (btcusdt@trade) — sub-10ms latency
Secondary: Coinbase REST spot price — confirmation
Tertiary: CryptoQuant on-chain metrics — momentum signal

The bot uses multiple feeds to build consensus before acting.
"""
import asyncio
import json
import time
import logging
from dataclasses import dataclass, field
from typing import Optional
from collections import deque

import websockets
import httpx

from btc_arb.config import (
    BINANCE_WS_URL,
    COINBASE_TICKER_URL,
    CRYPTOQUANT_API_KEY,
    CRYPTOQUANT_BASE_URL,
    MAX_SPOT_AGE_MS,
)

logger = logging.getLogger("btc_arb.feeds")


@dataclass
class PriceTick:
    price: float
    source: str
    timestamp_ms: int  # unix ms
    volume: Optional[float] = None


@dataclass
class PriceState:
    """Aggregated BTC price state from all feeds."""
    binance_price: Optional[float] = None
    binance_ts: int = 0
    coinbase_price: Optional[float] = None
    coinbase_ts: int = 0
    cryptoquant_signal: Optional[str] = None  # "bullish" / "bearish" / "neutral"
    cryptoquant_ts: int = 0

    # Rolling window for velocity calculation
    price_history: deque = field(
        default_factory=lambda: deque(maxlen=300)
    )

    @property
    def best_price(self) -> Optional[float]:
        """Most recent valid price across all feeds."""
        now_ms = int(time.time() * 1000)
        candidates = []
        if self.binance_price and (now_ms - self.binance_ts) < MAX_SPOT_AGE_MS:
            candidates.append((self.binance_ts, self.binance_price))
        if self.coinbase_price and (now_ms - self.coinbase_ts) < 10_000:
            candidates.append((self.coinbase_ts, self.coinbase_price))
        if not candidates:
            return None
        # Return most recent
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    @property
    def feed_count(self) -> int:
        """How many feeds have recent data."""
        now_ms = int(time.time() * 1000)
        count = 0
        if self.binance_price and (now_ms - self.binance_ts) < MAX_SPOT_AGE_MS:
            count += 1
        if self.coinbase_price and (now_ms - self.coinbase_ts) < 10_000:
            count += 1
        return count

    @property
    def price_velocity(self) -> float:
        """Price change per second over last 5 seconds."""
        if len(self.price_history) < 2:
            return 0.0
        now_ms = int(time.time() * 1000)
        recent = [
            (ts, px) for ts, px in self.price_history
            if (now_ms - ts) < 5_000
        ]
        if len(recent) < 2:
            return 0.0
        oldest_ts, oldest_px = recent[0]
        newest_ts, newest_px = recent[-1]
        dt_s = (newest_ts - oldest_ts) / 1000.0
        if dt_s == 0:
            return 0.0
        return (newest_px - oldest_px) / dt_s


class PriceFeedManager:
    """Manages all BTC price feeds concurrently."""

    def __init__(self):
        self.state = PriceState()
        self._running = False
        self._tasks: list[asyncio.Task] = []
        self._callbacks: list = []

    def on_price(self, callback):
        """Register callback for price updates: callback(PriceTick)"""
        self._callbacks.append(callback)

    async def _notify(self, tick: PriceTick):
        for cb in self._callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(tick)
                else:
                    cb(tick)
            except Exception as e:
                logger.error(f"Price callback error: {e}")

    async def start(self):
        """Start all price feeds."""
        self._running = True
        self._tasks = [
            asyncio.create_task(self._binance_ws()),
            asyncio.create_task(self._coinbase_poll()),
        ]
        if CRYPTOQUANT_API_KEY:
            self._tasks.append(
                asyncio.create_task(self._cryptoquant_poll())
            )
        logger.info(
            f"Price feeds started: binance_ws, coinbase_poll"
            f"{', cryptoquant' if CRYPTOQUANT_API_KEY else ''}"
        )

    async def stop(self):
        """Stop all feeds."""
        self._running = False
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        logger.info("Price feeds stopped")

    # ─── Binance WebSocket ────────────────────────────

    async def _binance_ws(self):
        """
        Binance trade stream — real-time BTC/USDT trades.
        Each message: {"p": "64321.50", "q": "0.001", "T": 1712345678901}
        """
        while self._running:
            try:
                async with websockets.connect(
                    BINANCE_WS_URL,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    logger.info("Binance WS connected")
                    async for msg in ws:
                        if not self._running:
                            break
                        data = json.loads(msg)
                        price = float(data["p"])
                        ts = int(data["T"])
                        volume = float(data.get("q", 0))

                        self.state.binance_price = price
                        self.state.binance_ts = ts
                        self.state.price_history.append((ts, price))

                        tick = PriceTick(
                            price=price,
                            source="binance",
                            timestamp_ms=ts,
                            volume=volume,
                        )
                        await self._notify(tick)

            except websockets.ConnectionClosed:
                logger.warning("Binance WS disconnected, reconnecting...")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Binance WS error: {e}")
                await asyncio.sleep(2)

    # ─── Coinbase REST Poll ───────────────────────────

    async def _coinbase_poll(self):
        """Poll Coinbase spot price every 500ms as secondary confirmation."""
        async with httpx.AsyncClient(timeout=5) as client:
            while self._running:
                try:
                    resp = await client.get(COINBASE_TICKER_URL)
                    if resp.status_code == 200:
                        data = resp.json()
                        price = float(data["data"]["amount"])
                        ts = int(time.time() * 1000)

                        self.state.coinbase_price = price
                        self.state.coinbase_ts = ts

                        tick = PriceTick(
                            price=price,
                            source="coinbase",
                            timestamp_ms=ts,
                        )
                        await self._notify(tick)
                except Exception as e:
                    logger.debug(f"Coinbase poll error: {e}")

                await asyncio.sleep(0.5)

    # ─── CryptoQuant On-Chain Signal ──────────────────

    async def _cryptoquant_poll(self):
        """
        Poll CryptoQuant for on-chain momentum signals.
        Exchange netflow, whale activity — directional bias.
        """
        headers = {"Authorization": f"Bearer {CRYPTOQUANT_API_KEY}"}
        async with httpx.AsyncClient(
            timeout=10, headers=headers
        ) as client:
            while self._running:
                try:
                    # Exchange netflow — negative = bullish (coins leaving exchanges)
                    resp = await client.get(
                        f"{CRYPTOQUANT_BASE_URL}/bitcoin/exchange-flows/netflow",
                        params={"window": "hour", "limit": 1},
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        results = data.get("result", {}).get("data", [])
                        if results:
                            netflow = results[0].get("netflow", 0)
                            if netflow < -100:
                                signal = "bullish"
                            elif netflow > 100:
                                signal = "bearish"
                            else:
                                signal = "neutral"

                            self.state.cryptoquant_signal = signal
                            self.state.cryptoquant_ts = int(
                                time.time() * 1000
                            )
                            logger.debug(
                                f"CryptoQuant signal: {signal} "
                                f"(netflow={netflow:.0f})"
                            )
                except Exception as e:
                    logger.debug(f"CryptoQuant poll error: {e}")

                await asyncio.sleep(60)  # on-chain data updates slowly
