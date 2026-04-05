"""
Order Executor — places and manages trades on Polymarket.

Paper mode: simulates fills at market price.
Live mode: uses polymarket-us SDK to place real orders.

Fee optimization:
  - Large lag (>0.5%): post MAKER limit order → earn 0.2% rebate
  - Small lag (<0.5%): take liquidity immediately → pay 0.3% fee
  - If maker order doesn't fill in 3s, convert to taker
  This flips the fee math from -0.3% to +0.2% on ~half of trades.

Execution flow:
  1. LagSignal received
  2. Risk check (can_open?)
  3. Size calculation
  4. Route: maker (large lag, earn rebate) or taker (small lag, speed)
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
    MAKER_REBATE,
    ORDER_TIMEOUT_S,
    MAKER_LAG_THRESHOLD,
    MAKER_FILL_TIMEOUT_MS,
    MAKER_PRICE_OFFSET,
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
        # Fee tracking
        self.maker_fills = 0
        self.taker_fills = 0
        self.total_fees_saved = 0.0

    def _should_use_maker(self, signal: LagSignal) -> bool:
        """
        Decide whether to use maker (limit) or taker (market) order.
        Large lag = we have time to post a limit and earn rebate.
        Small lag = take immediately before it closes.
        """
        return signal.lag_pct >= MAKER_LAG_THRESHOLD

    def _maker_price(self, signal: LagSignal) -> float:
        """
        Calculate maker limit price — slightly inside the spread
        toward fair value, so it fills as the contract catches up.

        Example: contract at 0.60, fair value at 0.66
        Maker posts at 0.655 (fair - offset)
        As market makers reprice toward 0.66, our limit gets hit.
        """
        if signal.side == "YES":
            # We're buying YES — post below fair value
            return signal.fair_value - MAKER_PRICE_OFFSET
        else:
            # We're buying NO — post below fair NO value
            return (1.0 - signal.fair_value) - MAKER_PRICE_OFFSET

    async def execute(self, signal: LagSignal) -> Optional[Position]:
        """
        Execute a trade based on a lag signal.
        Routes to maker or taker based on lag size.
        """
        # Risk gate
        can, reason = self.risk.can_open()
        if not can:
            logger.debug(f"Risk blocked: {reason}")
            return None

        # Route: maker or taker
        use_maker = self._should_use_maker(signal)

        if use_maker:
            entry_price = self._maker_price(signal)
            # Maker gets rebate, so effective fee is negative (savings)
            fee_rate = -MAKER_REBATE
            route = "MAKER"
        else:
            entry_price = signal.contract_price
            fee_rate = TAKER_FEE
            route = "TAKER"

        # Size the position
        cost, shares = self.risk.calculate_size(entry_price)
        if shares <= 0:
            logger.debug("Zero shares — skipping")
            return None

        # Execute
        if PAPER_MODE:
            pos = await self._paper_fill(
                signal, entry_price, shares, cost,
                fee_rate, route
            )
        else:
            if use_maker:
                pos = await self._live_maker_fill(
                    signal, entry_price, shares, cost
                )
            else:
                pos = await self._live_taker_fill(
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
        fee_rate: float,
        route: str,
    ) -> Optional[Position]:
        """Simulate a fill in paper mode with maker/taker routing."""
        fee = cost * fee_rate
        total_cost = cost + fee  # negative fee = cost reduction

        # Track fee savings
        if route == "MAKER":
            self.maker_fills += 1
            taker_cost = cost * TAKER_FEE
            saved = taker_cost + (cost * MAKER_REBATE)  # what we saved
            self.total_fees_saved += saved
        else:
            self.taker_fills += 1

        pos = self.risk.open_position(
            slug=signal.market.slug,
            side=signal.side,
            entry_price=price,
            shares=shares,
            cost_usd=total_cost,
        )
        if pos:
            logger.info(
                f"[PAPER|{route}] Filled {signal.side} "
                f"{signal.market.slug} "
                f"@ {price:.4f} x{shares} "
                f"= ${total_cost:.2f} "
                f"(lag={signal.lag_pct:.3%}, "
                f"edge={signal.net_edge:.4f}, "
                f"fee={'%.1f' % (fee_rate*100)}%)"
            )
        return pos

    async def _live_maker_fill(
        self,
        signal: LagSignal,
        price: float,
        shares: int,
        cost: float,
    ) -> Optional[Position]:
        """
        Post a maker limit order and wait for fill.
        If not filled within MAKER_FILL_TIMEOUT_MS, cancel and
        re-submit as taker at current market price.
        """
        if not self.client:
            logger.error("No SDK client for live trading")
            return None

        try:
            # Post limit order
            order_result = await asyncio.wait_for(
                self.client.orders.create(
                    slug=signal.market.slug,
                    side="buy",
                    outcome=signal.side.lower(),
                    size=shares,
                    price=price,
                    order_type="limit",
                ),
                timeout=ORDER_TIMEOUT_S,
            )
            order_id = order_result.get("id", "")
            logger.info(
                f"[MAKER] Limit posted: {signal.market.slug} "
                f"@ {price:.4f} x{shares} (id={order_id})"
            )

            # Wait for fill
            fill_deadline = time.time() + (MAKER_FILL_TIMEOUT_MS / 1000)
            filled = False
            while time.time() < fill_deadline:
                await asyncio.sleep(0.2)
                # Check if order is filled (via private WS or polling)
                # For now, assume fill after timeout
                # TODO: wire into private WS for real fill detection

            if not filled:
                # Cancel maker, fall back to taker
                try:
                    await self.client.orders.cancel_all()
                except Exception:
                    pass
                logger.info(
                    f"[MAKER] No fill in {MAKER_FILL_TIMEOUT_MS}ms, "
                    f"falling back to taker"
                )
                return await self._live_taker_fill(
                    signal, signal.contract_price, shares, cost
                )

            # Maker filled — earn rebate
            self.maker_fills += 1
            rebate = cost * MAKER_REBATE
            self.total_fees_saved += rebate + (cost * TAKER_FEE)
            pos = self.risk.open_position(
                slug=signal.market.slug,
                side=signal.side,
                entry_price=price,
                shares=shares,
                cost_usd=cost - rebate,
            )
            return pos

        except asyncio.TimeoutError:
            logger.error(f"Maker order timeout for {signal.market.slug}")
            return None
        except Exception as e:
            logger.error(f"Maker order failed: {e}")
            return None

    async def _live_taker_fill(
        self,
        signal: LagSignal,
        price: float,
        shares: int,
        cost: float,
    ) -> Optional[Position]:
        """Place a taker (market/IOC) order for immediate fill."""
        if not self.client:
            logger.error("No SDK client for live trading")
            return None

        try:
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
            logger.info(f"[TAKER] Order filled: {order_result}")

            self.taker_fills += 1
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
                f"Taker order timeout ({ORDER_TIMEOUT_S}s) "
                f"for {signal.market.slug}"
            )
            return None
        except Exception as e:
            logger.error(f"Taker order failed: {e}")
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
        """Close a position. Exits always use taker (IOC) for speed."""
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

    def fee_stats(self) -> dict:
        """Fee optimization statistics."""
        total = self.maker_fills + self.taker_fills
        maker_pct = (
            self.maker_fills / total * 100 if total > 0 else 0
        )
        return {
            "maker_fills": self.maker_fills,
            "taker_fills": self.taker_fills,
            "maker_rate": f"{maker_pct:.0f}%",
            "fees_saved": f"${self.total_fees_saved:.2f}",
        }

    async def start(self):
        self._running = True
        logger.info("Order executor started (maker/taker routing)")

    async def stop(self):
        self._running = False
        for pid, task in self._monitor_tasks.items():
            task.cancel()
        await asyncio.gather(
            *self._monitor_tasks.values(),
            return_exceptions=True,
        )
        self._monitor_tasks.clear()
        logger.info(
            f"Order executor stopped. "
            f"Fee stats: {self.fee_stats()}"
        )
