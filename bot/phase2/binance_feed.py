import asyncio
import json
import logging
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional
import websockets
from config import PHASE2_ENABLED

logger = logging.getLogger("polyfarm.binance")

BINANCE_WS = "wss://stream.binance.com:9443/ws"
SYMBOLS = ["btcusdt", "ethusdt"]
BACKOFF = [1, 2, 4, 8, 16, 32]


@dataclass
class PriceEvent:
    symbol: str
    price: float
    timestamp: float
    momentum_10s: float
    momentum_30s: float


class BinanceFeed:

    def __init__(self):
        self.price_queue: asyncio.Queue = (
            asyncio.Queue(maxsize=1000)
        )
        self._history: dict[str, deque] = {
            s: deque(maxlen=300)
            for s in SYMBOLS
        }
        self._latest: dict[str, float] = {}

    def _calc_momentum(self, symbol: str,
                        seconds: int) -> float:
        history = self._history.get(symbol)
        if not history or len(history) < 2:
            return 0.0
        now = time.time()
        cutoff = now - seconds
        prices = [
            p for t, p in history
            if t >= cutoff
        ]
        if len(prices) < 2:
            return 0.0
        return (prices[-1] - prices[0]) / prices[0]

    async def stream_loop(self):
        if not PHASE2_ENABLED:
            logger.info(
                "Phase 2 disabled — "
                "Binance feed dormant"
            )
            while True:
                await asyncio.sleep(3600)

        streams = "/".join(
            f"{s}@ticker" for s in SYMBOLS
        )
        url = f"{BINANCE_WS}/{streams}"
        attempt = 0

        while True:
            try:
                async with websockets.connect(
                    url,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    attempt = 0
                    logger.info(
                        "Binance feed connected"
                    )
                    async for raw in ws:
                        try:
                            data = json.loads(raw)
                            await self._handle(data)
                        except json.JSONDecodeError:
                            continue

            except (
                websockets.ConnectionClosed,
                ConnectionError,
                OSError,
            ) as e:
                logger.warning(
                    f"Binance disconnected: {e}"
                )
            except Exception as e:
                logger.error(
                    f"Binance error: {e}"
                )

            delay = BACKOFF[min(
                attempt, len(BACKOFF) - 1
            )]
            await asyncio.sleep(delay)
            attempt += 1

    async def _handle(self, data: dict):
        symbol = data.get("s", "").lower()
        price_str = data.get("c")
        if not symbol or not price_str:
            return

        price = float(price_str)
        now = time.time()
        self._history[symbol].append((now, price))
        self._latest[symbol] = price

        event = PriceEvent(
            symbol=symbol,
            price=price,
            timestamp=now,
            momentum_10s=self._calc_momentum(
                symbol, 10
            ),
            momentum_30s=self._calc_momentum(
                symbol, 30
            ),
        )
        try:
            self.price_queue.put_nowait(event)
        except asyncio.QueueFull:
            pass
