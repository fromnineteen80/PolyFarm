import asyncio
import json
import logging
import websockets
from config import WS_MARKETS
from core.ws_auth import generate_ws_headers
from data.database import set_bot_config

logger = logging.getLogger("polyfarm.ws_markets")

BACKOFF = [1, 2, 4, 8, 16, 32]


class WSMarkets:

    def __init__(self, registry, market_loader):
        self.registry = registry
        self.loader = market_loader
        self._subscribed_slugs: set = set()
        self._edge_detector = None
        self._ws = None

    def set_edge_detector(self, ed):
        self._edge_detector = ed

    async def subscribe_slugs(self, slugs: list):
        new = [s for s in slugs
               if s not in self._subscribed_slugs]
        if not new:
            return
        self._subscribed_slugs.update(new)
        if self._ws:
            try:
                await self._ws.send(json.dumps({
                    "type": "subscribe",
                    "channel": "MARKET_DATA_LITE",
                    "markets": new,
                }))
            except Exception as e:
                logger.debug(f"Subscribe error: {e}")

    async def connect_and_listen(self):
        attempt = 0
        while True:
            try:
                headers = generate_ws_headers(
                    "/v1/ws/markets"
                )
                async with websockets.connect(
                    WS_MARKETS,
                    additional_headers=headers,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    self._ws = ws
                    attempt = 0
                    logger.info(
                        "WS Markets connected"
                    )
                    try:
                        await set_bot_config(
                            "ws_markets_status",
                            "CONNECTED"
                        )
                    except Exception:
                        pass

                    # Resubscribe on reconnect
                    if self._subscribed_slugs:
                        await ws.send(json.dumps({
                            "type": "subscribe",
                            "channel": "MARKET_DATA_LITE",
                            "markets": list(
                                self._subscribed_slugs
                            ),
                        }))

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
                    f"WS Markets disconnected: {e}"
                )
            except Exception as e:
                logger.error(
                    f"WS Markets error: {e}"
                )

            self._ws = None
            try:
                await set_bot_config(
                    "ws_markets_status", "DISCONNECTED"
                )
            except Exception:
                pass
            delay = BACKOFF[min(
                attempt, len(BACKOFF) - 1
            )]
            logger.info(
                f"WS Markets reconnecting in {delay}s"
            )
            await asyncio.sleep(delay)
            attempt += 1

    async def _handle(self, data: dict):
        msg_type = data.get("type")

        if msg_type == "MARKET_DATA_LITE" or \
           "market_slug" in data:
            slug = data.get("market_slug")
            yes_price = data.get("yes_price")
            if slug and yes_price is not None:
                # Update registry
                market = await self.registry.get(slug)
                if market:
                    market.yes_price = float(yes_price)
                    await self.registry.update(
                        slug, market
                    )

                # Push to edge detector
                if self._edge_detector:
                    try:
                        self._edge_detector\
                            .price_queue.put_nowait({
                                "market_slug": slug,
                                "yes_price": yes_price,
                            })
                    except asyncio.QueueFull:
                        pass
