import asyncio
import json
import logging
import websockets
from config import WS_PRIVATE
from core.ws_auth import generate_ws_headers

logger = logging.getLogger("polyfarm.ws_private")

BACKOFF = [1, 2, 4, 8, 16, 32]


class WSPrivate:

    def __init__(self, position_monitor, wallet):
        self.pm = position_monitor
        self.wallet = wallet
        self._ws = None

    async def connect_and_listen(self):
        attempt = 0
        while True:
            try:
                headers = generate_ws_headers(
                    "/v1/ws/private"
                )
                async with websockets.connect(
                    WS_PRIVATE,
                    additional_headers=headers,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    self._ws = ws
                    attempt = 0
                    logger.info(
                        "WS Private connected"
                    )

                    # Subscribe to private channels
                    await ws.send(json.dumps({
                        "type": "subscribe",
                        "channels": [
                            "ORDER",
                            "POSITION",
                            "ACCOUNT_BALANCE",
                        ],
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
                    f"WS Private disconnected: {e}"
                )
            except Exception as e:
                logger.error(
                    f"WS Private error: {e}"
                )

            self._ws = None
            delay = BACKOFF[min(
                attempt, len(BACKOFF) - 1
            )]
            logger.info(
                f"WS Private reconnecting in {delay}s"
            )
            await asyncio.sleep(delay)
            attempt += 1

    async def _handle(self, data: dict):
        channel = data.get("channel") or \
                  data.get("type", "")

        if channel == "ORDER":
            await self._handle_order(data)
        elif channel == "POSITION":
            await self._handle_position(data)
        elif channel == "ACCOUNT_BALANCE":
            await self._handle_balance(data)

    async def _handle_order(self, data: dict):
        status = data.get("status", "")
        if status not in ("FILLED", "PARTIALLY_FILLED"):
            return
        order_id = data.get("order_id", "")
        slug = data.get("market_slug", "")
        fill_price = float(
            data.get("fill_price", 0) or
            data.get("average_price", 0) or 0
        )
        intent = data.get("intent", "")

        if order_id and slug and fill_price > 0:
            await self.pm.on_ws_order_fill(
                order_id, slug, fill_price, intent
            )

    async def _handle_position(self, data: dict):
        slug = data.get("market_slug", "")
        current_price = float(
            data.get("current_price", 0) or 0
        )
        shares = float(
            data.get("size", 0) or 0
        )
        if slug and current_price > 0:
            await self.pm.on_ws_position_update(
                slug, current_price, shares
            )

    async def _handle_balance(self, data: dict):
        balance = data.get("buying_power")
        if balance is not None:
            self.wallet.state.cash_balance = float(
                balance
            )
