"""
Private WebSocket handler using the official
polymarket-us SDK.
Handles order fills, position changes, and
account balance updates.
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from data.database import set_bot_config

if TYPE_CHECKING:
    from polymarket_us import AsyncPolymarketUS

logger = logging.getLogger("polyfarm.ws_private")


class PrivateWebSocket:

    HEARTBEAT_TIMEOUT = 30
    RECONNECT_BASE = 5
    RECONNECT_MAX = 120

    def __init__(self, client, position_monitor, wallet):
        self.client = client
        self.position_monitor = position_monitor
        self.wallet = wallet
        self._ws = None
        self._last_heartbeat = None
        self._reconnect_delay = self.RECONNECT_BASE
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            try:
                await self._connect_and_run()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(
                    f"Private WS error: {e}. "
                    f"Reconnecting in {self._reconnect_delay}s"
                )
                try:
                    await set_bot_config("ws_private_status", "DISCONNECTED")
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
        self._ws = self.client.ws.private()
        self._ws.on("order_snapshot", self._on_order_snapshot)
        self._ws.on("order_update", self._on_order_update)
        self._ws.on("position_snapshot", self._on_position_snapshot)
        self._ws.on("position_update", self._on_position_update)
        self._ws.on("account_balance_snapshot", self._on_balance_snapshot)
        self._ws.on("account_balance_update", self._on_balance_update)
        self._ws.on("heartbeat", self._on_heartbeat)
        self._ws.on("error", self._on_error)
        self._ws.on("close", self._on_close)

        await self._ws.connect()
        self._reconnect_delay = self.RECONNECT_BASE
        logger.info("Private WebSocket connected")
        try:
            await set_bot_config("ws_private_status", "CONNECTED")
        except Exception:
            pass

        await self._ws.subscribe("order-sub-1", "SUBSCRIPTION_TYPE_ORDER")
        await self._ws.subscribe("pos-sub-1", "SUBSCRIPTION_TYPE_POSITION")
        await self._ws.subscribe("balance-sub-1", "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE")

        self._last_heartbeat = datetime.now(timezone.utc)
        while self._running:
            await asyncio.sleep(5)
            if self._last_heartbeat:
                age = (datetime.now(timezone.utc) - self._last_heartbeat).total_seconds()
                if age > self.HEARTBEAT_TIMEOUT:
                    logger.warning("Private WS heartbeat timeout. Reconnecting.")
                    await self._ws.close()
                    break

    def _on_order_snapshot(self, data):
        try:
            orders = data.get("orderSubscriptionSnapshot", {}).get("orders", [])
            logger.debug(f"Order snapshot: {len(orders)} open orders")
        except Exception as e:
            logger.error(f"Order snapshot error: {e}")

    def _on_order_update(self, data):
        try:
            execution = data.get("orderSubscriptionUpdate", {}).get("execution", {})
            exec_type = execution.get("type", "")
            order = execution.get("order", {})
            order_id = order.get("id")
            slug = order.get("marketSlug")
            intent = order.get("intent", "")
            fill_price = float(execution.get("lastPx", {}).get("value", 0) or 0)
            shares = float(execution.get("lastShares", 0) or 0)
            trade_id = execution.get("tradeId")

            if exec_type in ("EXECUTION_TYPE_FILL", "EXECUTION_TYPE_PARTIAL_FILL"):
                logger.info(f"Order fill: {slug} {shares} shares @ {fill_price} [{exec_type}]")
                if hasattr(self.position_monitor, "on_ws_order_fill"):
                    asyncio.create_task(
                        self.position_monitor.on_ws_order_fill(
                            order_id=order_id, slug=slug,
                            fill_price=fill_price, intent=intent,
                        )
                    )
            elif exec_type == "EXECUTION_TYPE_CANCELED":
                logger.debug(f"Order canceled: {order_id} on {slug}")
        except Exception as e:
            logger.error(f"Order update error: {e}")

    def _on_position_snapshot(self, data):
        logger.debug("Position snapshot received")

    def _on_position_update(self, data):
        try:
            pos_data = data.get("positionSubscription", {})
            after = pos_data.get("afterPosition", {})
            net_position = float(after.get("netPosition", 0) or 0)
            cost = float(after.get("cost", {}).get("value", 0) or 0)
            trade_id = pos_data.get("tradeId")
            if hasattr(self.wallet, "on_position_change"):
                asyncio.create_task(
                    self.wallet.on_position_change(
                        net_position=net_position, cost=cost, trade_id=trade_id,
                    )
                )
        except Exception as e:
            logger.error(f"Position update error: {e}")

    def _on_balance_snapshot(self, data):
        try:
            balances = data.get("accountBalancesSnapshot", {}).get("balances", [])
            if balances:
                buying_power = float(balances[0].get("buyingPower", 0) or 0)
                current_balance = float(balances[0].get("currentBalance", 0) or 0)
                logger.info(f"Balance snapshot: BP={buying_power:.2f} Total={current_balance:.2f}")
                self.wallet.state.cash_balance = buying_power
        except Exception as e:
            logger.error(f"Balance snapshot error: {e}")

    def _on_balance_update(self, data):
        try:
            change = data.get("accountBalancesUpdate", {}).get("balanceChange", {})
            after = change.get("afterBalance", {})
            buying_power = float(after.get("buyingPower", 0) or 0)
            self.wallet.state.cash_balance = buying_power
        except Exception as e:
            logger.error(f"Balance update error: {e}")

    def _on_heartbeat(self, data):
        self._last_heartbeat = datetime.now(timezone.utc)

    def _on_error(self, error):
        logger.error(f"Private WS error: {error}")

    def _on_close(self, data):
        logger.warning("Private WS closed. Reconnect loop will restart.")
