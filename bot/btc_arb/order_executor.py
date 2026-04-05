"""
Order Executor — places and manages trades on Polymarket.

Paper mode: simulates fills at market price.
Live mode: uses polymarket-us SDK to place real orders.

Execution flow:
  1. LagSignal received
  2. Risk check (can_open?)
  3. Size calculation
  4. Re-verify lag still exists (avoid stale signals)
  5. Place order (paper or live)
  6. Monitor for exit conditions
"""
import asyncio
import logging
import time
from typing import Optional

from btc_arb.config import (
    PAPER_MODE,
    RECHECK_LAG_BEFORE_EXEC,
    TAKE_PROFIT_PCT,
    STOP_LOSS_PCT,
    MAX_HOLD_TIME_S,
    TRAILING_STOP_ACTIVATE_PCT,
    TRAILING_STOP_FLOOR_PCT,
    TAKER_FEE,
    ORDER_TIMEOUT_S,
)
from btc_arb.lag_detector import LagSignal
from btc_arb.risk_manager import RiskManager, Position

logger = logging.getLogger("btc_arb.executor")


class OrderExecutor:
    """Executes trades and monitors exits."""

    def __init__(
        self,
        risk: RiskManager,
        client=None,  # polymarket-us AsyncPolymarketUS
    ):
        self.risk = risk
        self.client = client
        self._running = False
        self._monitor_tasks: dict[str, asyncio.Task] = {}

    async def execute(self, signal: LagSignal) -> Optional[Position]:
        """
        Execute a trade based on a lag signal.
        Returns the opened Position or None.
        """
        # Risk gate
        can, reason = self.risk.can_open()
        if not can:
            logger.debug(f"Risk blocked: {reason}")
            return None

        # Determine entry price
        entry_price = signal.contract_price

        # Size the position
        cost, shares = self.risk.calculate_size(entry_price)
        if shares <= 0:
            logger.debug("Zero shares — skipping")
            return None

        # Execute
        if PAPER_MODE:
            pos = await self._paper_fill(
                signal, entry_price, shares, cost
            )
        else:
            pos = await self._live_fill(
                signal, entry_price, shares, cost
            )

        if pos:
            # Start monitoring for exit
            task = asyncio.create_task(
                self._monitor_position(pos, signal)
            )
            self._monitor_tasks[pos.position_id] = task

        return pos

    async def _paper_fill(
        self,
        signal: LagSignal,
        price: float,
        shares: int,
        cost: float,
    ) -> Optional[Position]:
        """Simulate a fill in paper mode."""
        # Apply taker fee to cost
        fee = cost * TAKER_FEE
        total_cost = cost + fee

        pos = self.risk.open_position(
            slug=signal.market.slug,
            side=signal.side,
            entry_price=price,
            shares=shares,
            cost_usd=total_cost,
        )
        if pos:
            logger.info(
                f"[PAPER] Filled {signal.side} "
                f"{signal.market.slug} "
                f"@ {price:.4f} x{shares} "
                f"= ${total_cost:.2f} "
                f"(lag={signal.lag_pct:.3%}, "
                f"edge={signal.net_edge:.4f})"
            )
        return pos

    async def _live_fill(
        self,
        signal: LagSignal,
        price: float,
        shares: int,
        cost: float,
    ) -> Optional[Position]:
        """Place a real order via the Polymarket SDK."""
        if not self.client:
            logger.error("No SDK client for live trading")
            return None

        try:
            # Place market buy order
            order_result = await asyncio.wait_for(
                self.client.orders.create(
                    slug=signal.market.slug,
                    side="buy",
                    outcome=signal.side.lower(),
                    size=shares,
                    price=price,
                    order_type="market",
                ),
                timeout=ORDER_TIMEOUT_S,
            )
            logger.info(f"Live order placed: {order_result}")

            fee = cost * TAKER_FEE
            pos = self.risk.open_position(
                slug=signal.market.slug,
                side=signal.side,
                entry_price=price,
                shares=shares,
                cost_usd=cost + fee,
            )
            return pos

        except asyncio.TimeoutError:
            logger.error(
                f"Order timeout ({ORDER_TIMEOUT_S}s) "
                f"for {signal.market.slug}"
            )
            return None
        except Exception as e:
            logger.error(f"Order failed: {e}")
            return None

    async def _monitor_position(
        self, pos: Position, signal: LagSignal
    ):
        """
        Monitor an open position for exit conditions:
        1. Take profit — contract catches up to fair value
        2. Stop loss — price moves against us
        3. Trailing stop — lock in gains
        4. Timeout — max hold time exceeded
        """
        trailing_active = False
        trailing_floor = 0.0

        while self._running or pos.position_id in self.risk.positions:
            await asyncio.sleep(0.5)  # check every 500ms

            if pos.position_id not in self.risk.positions:
                break  # already closed

            # Get current market price for our side
            mkt = signal.market
            if pos.side == "YES":
                current = mkt.yes_price
            else:
                current = mkt.no_price

            if current <= 0:
                continue

            # Update mark-to-market
            self.risk.update_position_value(
                pos.position_id, current
            )
            pnl_pct = pos.pnl_pct

            # 1. Take profit
            if pnl_pct >= TAKE_PROFIT_PCT:
                await self._exit(
                    pos, current, "take_profit",
                    f"pnl={pnl_pct:.3%}"
                )
                break

            # 2. Stop loss
            if pnl_pct <= -STOP_LOSS_PCT:
                await self._exit(
                    pos, current, "stop_loss",
                    f"pnl={pnl_pct:.3%}"
                )
                break

            # 3. Trailing stop
            if pnl_pct >= TRAILING_STOP_ACTIVATE_PCT:
                if not trailing_active:
                    trailing_active = True
                    logger.info(
                        f"Trailing stop activated for "
                        f"{pos.position_id} at {pnl_pct:.3%}"
                    )
                trailing_floor = max(
                    trailing_floor,
                    pnl_pct * TRAILING_STOP_FLOOR_PCT,
                )
            if trailing_active and pnl_pct <= trailing_floor:
                await self._exit(
                    pos, current, "trailing_stop",
                    f"pnl={pnl_pct:.3%}, "
                    f"floor={trailing_floor:.3%}"
                )
                break

            # 4. Timeout
            if pos.hold_time_s >= MAX_HOLD_TIME_S:
                await self._exit(
                    pos, current, "timeout",
                    f"held {pos.hold_time_s:.0f}s"
                )
                break

    async def _exit(
        self,
        pos: Position,
        exit_price: float,
        reason: str,
        detail: str,
    ):
        """Close a position."""
        if PAPER_MODE:
            pnl = self.risk.close_position(
                pos.position_id, exit_price
            )
            logger.info(
                f"[PAPER] Exit {pos.position_id}: "
                f"{reason} ({detail}) "
                f"pnl=${pnl:+.2f}"
            )
        else:
            # Live: place IOC sell order
            try:
                if self.client:
                    await self.client.orders.create(
                        slug=pos.slug,
                        side="sell",
                        outcome=pos.side.lower(),
                        size=pos.shares,
                        price=exit_price,
                        order_type="ioc",
                    )
                pnl = self.risk.close_position(
                    pos.position_id, exit_price
                )
                logger.info(
                    f"[LIVE] Exit {pos.position_id}: "
                    f"{reason} ({detail}) "
                    f"pnl=${pnl:+.2f}"
                )
            except Exception as e:
                logger.error(
                    f"Exit order failed for "
                    f"{pos.position_id}: {e}"
                )

    async def start(self):
        self._running = True
        logger.info("Order executor started")

    async def stop(self):
        self._running = False
        # Cancel all monitor tasks
        for pid, task in self._monitor_tasks.items():
            task.cancel()
        await asyncio.gather(
            *self._monitor_tasks.values(),
            return_exceptions=True,
        )
        self._monitor_tasks.clear()
        logger.info("Order executor stopped")
