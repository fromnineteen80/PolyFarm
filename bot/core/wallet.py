import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from config import (
    FLOOR_PCT,
    HARVEST_THRESHOLD, PROTECTION_THRESHOLD,
    LOCK_THRESHOLD, PORTFOLIO_TRAIL_REVERT,
    DAILY_LOSS_REDUCE_TIER, DAILY_LOSS_PAUSE_TIER,
    DAILY_LOSS_HALT_TIER,
    BAND_A_POSITION_PCT, BAND_B_POSITION_PCT,
    BAND_C_POSITION_PCT,
    EXCEPTION_MAX_POSITION_PCT,
    FADE_MAX_POSITION_PCT,
    PHASE1B_MAX_POSITION_PCT,
    get_active_strategies,
    logger as config_logger
)
from data.database import (
    log_system_event, set_bot_config,
    write_daily_snapshot
)

logger = logging.getLogger("polyfarm.wallet")

@dataclass
class WalletState:
    # Portfolio values
    cash_balance: float = 0.0
    open_positions_value: float = 0.0
    live_portfolio_value: float = 0.0

    # Session anchors — set once at session_init
    session_start_value: float = 0.0
    floor_value: float = 0.0

    # Daily tracking
    daily_peak_gain: float = 0.0
    daily_gain_pct: float = 0.0
    realized_pnl_today: float = 0.0  # closed trades only

    # Mode state
    profit_mode: str = "NORMAL"
    loss_mode: str = "NORMAL"
    session_locked: bool = False
    entries_halted: bool = False
    new_entries_paused: bool = False
    sizing_reduced: bool = False

    # Counters
    exception_trades_today: int = 0
    fade_trades_today: int = 0
    paper_mode: bool = True

class WalletManager:

    def __init__(self, client, paper_mode: bool):
        self.client = client
        self.paper_mode = paper_mode
        self.state = WalletState(paper_mode=paper_mode)
        self._position_values: dict = {}
        self._alerts = None  # Set by main.py after init
        self._order_manager = None  # Set by main.py

    def set_alerts(self, alerts):
        self._alerts = alerts

    def set_order_manager(self, om):
        self._order_manager = om

    async def session_init(self):
        """
        Called once at startup. Establishes floor.
        Floor is fixed for the entire session.
        """
        from core.market_loader import parse_bbo

        result = await self.client.account.balances()
        balances = result.get("balances", [])
        cash = float(
            balances[0].get("buyingPower", 0) or 0
        ) if balances else 0.0

        pos_result = await self.client.portfolio.positions()
        positions_map = pos_result.get("positions", {})
        pos_value = 0.0

        for slug, pos in positions_map.items():
            try:
                shares = float(pos.get("longShares", 0) or 0)
                if shares <= 0:
                    continue
                bbo = await self.client.markets.bbo(slug)
                bid, ask, cur = parse_bbo(bbo)
                pos_value += bid * shares
                self._position_values[slug] = {
                    "value": bid * shares,
                    "shares": shares,
                    "current_bid": bid,
                }
            except Exception as e:
                logger.warning(
                    f"Could not value position {slug}: {e}"
                )

        total = cash + pos_value
        floor = total * FLOOR_PCT

        self.state.cash_balance = cash
        self.state.open_positions_value = pos_value
        self.state.live_portfolio_value = total
        self.state.session_start_value = total
        self.state.floor_value = floor
        self.state.daily_peak_gain = 0.0

        logger.info(
            f"Session init: wallet=${total:.2f} "
            f"floor=${floor:.2f} "
            f"working=${total - floor:.2f}"
        )

    async def recalculate(self):
        """
        Called every 10 seconds by monitor_loop.
        Updates all portfolio metrics and checks
        all profit and loss tier thresholds.
        """
        try:
            result = await self.client.account.balances()
            balances = result.get("balances", [])
            cash = float(
                balances[0].get("buyingPower", 0) or 0
            ) if balances else 0.0

            # Update position values from WebSocket
            # state (_position_values updated by
            # position_monitor via update_position_value)
            pos_value = sum(
                v["value"]
                for v in self._position_values.values()
            )

            total = cash + pos_value
            self.state.cash_balance = cash
            self.state.open_positions_value = pos_value
            self.state.live_portfolio_value = total

            if self.state.session_start_value > 0:
                gain_pct = (
                    (total - self.state.session_start_value)
                    / self.state.session_start_value
                )
                self.state.daily_gain_pct = gain_pct
                self.state.daily_peak_gain = max(
                    self.state.daily_peak_gain, gain_pct
                )

            await self._check_floor(total)
            await self._check_profit_tiers()
            await self._check_loss_tiers()

        except Exception as e:
            logger.error(f"Wallet recalculate error: {e}")

    def update_position_value(self,
                               slug: str,
                               bid: float,
                               shares: float):
        """Called by position_monitor on price updates."""
        self._position_values[slug] = {
            "value": bid * shares,
            "shares": shares,
            "current_bid": bid,
        }

    def remove_position(self, slug: str, pnl: float = 0.0):
        """Called when a position closes."""
        self._position_values.pop(slug, None)
        self.state.realized_pnl_today += pnl

    async def on_balance_update(self, buying_power, current_balance):
        """Called by private WebSocket on balance change."""
        self.state.cash_balance = buying_power

    async def on_position_change(self, net_position, cost, trade_id):
        """Called by private WebSocket on position change."""
        pass

    async def _check_floor(self, total: float):
        if self.state.session_locked:
            return
        floor = self.state.floor_value
        if floor <= 0:
            return
        gap_pct = (total - floor) / floor

        if total <= floor:
            await self._floor_breach_protocol()
            return

        # Only alert once per level — reset when gap recovers above 15%
        if gap_pct <= 0.05 and self._alerts:
            if not getattr(self, '_floor_critical_sent', False):
                await self._alerts.send_floor_critical(
                    total, floor, gap_pct
                )
                self._floor_critical_sent = True
                self._floor_warning_sent = True
        elif gap_pct <= 0.10 and self._alerts:
            if not getattr(self, '_floor_warning_sent', False):
                await self._alerts.send_floor_warning(
                    total, floor, gap_pct
                )
                self._floor_warning_sent = True
        elif gap_pct > 0.15:
            self._floor_warning_sent = False
            self._floor_critical_sent = False

    async def _check_profit_tiers(self):
        if self.state.session_locked:
            return
        if self.state.loss_mode != "NORMAL":
            return

        gain = self.state.daily_gain_pct
        peak = self.state.daily_peak_gain
        mode = self.state.profit_mode

        # Portfolio trailing stop
        if peak >= PROTECTION_THRESHOLD and \
           gain <= PORTFOLIO_TRAIL_REVERT:
            await self._trigger_lock(
                "PORTFOLIO_TRAILING_STOP"
            )
            return

        # Lock and drain
        if gain >= LOCK_THRESHOLD:
            await self._trigger_lock("DAILY_TARGET_HIT")
            return

        # Protection mode
        if gain >= PROTECTION_THRESHOLD:
            if mode != "PROTECTION":
                self.state.profit_mode = "PROTECTION"
                self.state.sizing_reduced = False
                logger.info("Entered PROTECTION mode")
                if self._alerts:
                    await self._alerts.send_protection_mode(
                        gain, self.state.live_portfolio_value
                    )
            return

        # Harvest mode
        if gain >= HARVEST_THRESHOLD:
            if mode == "NORMAL":
                self.state.profit_mode = "HARVEST"
                logger.info("Entered HARVEST mode")
                if self._alerts:
                    await self._alerts.send_harvest_mode(
                        gain, self.state.live_portfolio_value
                    )
            return

        # Reset to NORMAL if fallen back below harvest
        if gain < HARVEST_THRESHOLD and \
           mode in ("HARVEST", "PROTECTION"):
            self.state.profit_mode = "NORMAL"
            self.state.sizing_reduced = False
            logger.info("Returned to NORMAL profit mode")

    async def _check_loss_tiers(self):
        if self.state.session_locked:
            return
        # Use realized P&L only — unrealized dips on open
        # positions are game volatility, not real losses
        if self.state.session_start_value <= 0:
            return
        pnl_pct = (
            self.state.realized_pnl_today
            / self.state.session_start_value
        )

        # -15%: done for the day
        if pnl_pct <= DAILY_LOSS_HALT_TIER:
            if self.state.loss_mode != "HALT":
                self.state.loss_mode = "HALT"
                self.state.entries_halted = True
                self.state.session_locked = True
                self.state.new_entries_paused = True
                logger.warning("Daily loss limit (-15%) — done for the day")
                if self._alerts:
                    await self._alerts.send_daily_halt(
                        pnl_pct,
                        self.state.live_portfolio_value
                    )
                # Don't emergency exit — let positions settle
            return

        # -10%: pause new entries
        if pnl_pct <= DAILY_LOSS_PAUSE_TIER:
            if self.state.loss_mode not in (
                "PAUSE", "HALT"
            ):
                self.state.loss_mode = "PAUSE"
                self.state.new_entries_paused = True
                self.state.sizing_reduced = False
                logger.warning("Losses at -10% — pausing new trades")
                if self._alerts:
                    await self._alerts.send_daily_pause(
                        pnl_pct,
                        self.state.live_portfolio_value
                    )
            return

        # -5%: reduce position sizes
        if pnl_pct <= DAILY_LOSS_REDUCE_TIER:
            if self.state.loss_mode == "NORMAL":
                self.state.loss_mode = "REDUCE"
                self.state.sizing_reduced = True
                logger.warning("Losses at -5% — reducing position sizes")
                if self._alerts:
                    await self._alerts.send_daily_reduce(
                        pnl_pct,
                        self.state.live_portfolio_value
                    )
            return

        # Recovery: if paused at -10% and recovers to -5%, resume trading
        if self.state.loss_mode == "PAUSE" and \
           pnl_pct > DAILY_LOSS_REDUCE_TIER:
            self.state.loss_mode = "NORMAL"
            self.state.new_entries_paused = False
            self.state.sizing_reduced = False
            logger.info("Recovered from -10% to above -5% — resuming trades")

        # Recovery: if reduced at -5% and recovers above 0%
        elif self.state.loss_mode == "REDUCE" and \
             pnl_pct > 0:
            self.state.loss_mode = "NORMAL"
            self.state.sizing_reduced = False
            logger.info("Recovered to positive — back to normal")

    async def _trigger_lock(self, reason: str):
        self.state.profit_mode = "LOCKED"
        self.state.session_locked = True
        self.state.entries_halted = True
        self.state.new_entries_paused = True
        logger.info(f"Daily target hit — no new trades. Open positions will close naturally.")
        if self._alerts:
            await self._alerts.send_session_locked(
                reason,
                self.state.daily_gain_pct,
                self.state.live_portfolio_value
            )
        # Don't drain — let open positions play out to settlement

    async def _floor_breach_protocol(self):
        self.state.entries_halted = True
        self.state.session_locked = True
        self.state.new_entries_paused = True
        self.state.loss_mode = "FLOOR_BREACH"
        logger.critical("Floor breach — stopping trades for the day. Resets at midnight ET.")
        if self._alerts:
            await self._alerts.send_floor_breach(
                self.state.live_portfolio_value,
                self.state.floor_value
            )
        # Don't emergency exit — let positions settle naturally
        # Midnight reset will unlock for next day
        await log_system_event(
            "floor_breach",
            f"Portfolio fell to floor. Stopped for the day.",
            {
                "floor": self.state.floor_value,
                "portfolio": self.state.live_portfolio_value
            }
        )

    def get_position_size_usd(self,
                               strategy: str) -> float:
        """
        Returns position size in USD for the given
        strategy type given current session state.
        strategy: band_a | band_b | band_c |
                  exception | fade | research
        Returns 0.0 if strategy not active.
        """
        strategies = get_active_strategies(
            self.state.profit_mode,
            self.state.loss_mode
        )
        config = strategies.get(strategy)
        if not config or not config.get("active"):
            return 0.0

        size_pct = config["size"]
        wallet = self.state.live_portfolio_value
        return wallet * size_pct

    def can_enter(self, strategy: str) -> bool:
        """
        Returns True if this strategy can enter
        a new position right now.
        """
        if self.state.session_locked:
            # Only exception and fade allowed when locked
            if strategy not in ("exception", "fade"):
                return False
        if self.state.entries_halted:
            return False
        if self.state.new_entries_paused:
            return False

        strategies = get_active_strategies(
            self.state.profit_mode,
            self.state.loss_mode
        )
        config = strategies.get(strategy)
        return bool(config and config.get("active"))

    def get_utilization_pct(self) -> float:
        working = (
            self.state.live_portfolio_value
            - self.state.floor_value
        )
        if working <= 0:
            return 0.0
        deployed = self.state.open_positions_value
        return min(deployed / working * 100, 100.0)

    async def monitor_loop(self):
        """Runs every 10 seconds."""
        while True:
            await asyncio.sleep(10)
            await self.recalculate()

    async def reset_daily(self):
        """Called by midnight_scheduler."""
        self.state.daily_peak_gain = 0.0
        self.state.daily_gain_pct = 0.0
        self.state.realized_pnl_today = 0.0
        self.state.profit_mode = "NORMAL"
        self.state.loss_mode = "NORMAL"
        self.state.session_locked = False
        self.state.entries_halted = False
        self.state.new_entries_paused = False
        self.state.sizing_reduced = False
        self.state.exception_trades_today = 0
        self.state.fade_trades_today = 0
        # Re-anchor session start value
        self.state.session_start_value = (
            self.state.live_portfolio_value
        )
        self.state.floor_value = (
            self.state.session_start_value * FLOOR_PCT
        )
        logger.info("Daily reset complete")
