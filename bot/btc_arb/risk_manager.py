"""
Risk Manager — position sizing and daily loss limits.

Rules:
  - 0.5% of bankroll per trade
  - 2% daily loss cap (hard stop)
  - Max 5 concurrent positions
  - Track all P&L in real time
"""
import logging
import time
from dataclasses import dataclass, field
from typing import Optional

from btc_arb.config import (
    RISK_PER_TRADE,
    DAILY_LOSS_CAP,
    MAX_CONCURRENT_POSITIONS,
    MAX_POSITION_USD,
    MIN_POSITION_USD,
    PAPER_MODE,
    PAPER_SEED_BALANCE,
    TAKER_FEE,
)

logger = logging.getLogger("btc_arb.risk")


@dataclass
class Position:
    """An open BTC arb position."""
    position_id: str
    slug: str
    side: str  # "YES" or "NO"
    entry_price: float
    shares: float
    cost_usd: float
    entry_time_ms: int
    peak_value: float = 0.0
    current_value: float = 0.0
    paper: bool = True

    @property
    def pnl_usd(self) -> float:
        return self.current_value - self.cost_usd

    @property
    def pnl_pct(self) -> float:
        if self.cost_usd == 0:
            return 0.0
        return self.pnl_usd / self.cost_usd

    @property
    def hold_time_s(self) -> float:
        return (int(time.time() * 1000) - self.entry_time_ms) / 1000


@dataclass
class DailyStats:
    """Daily P&L tracking."""
    date: str  # YYYY-MM-DD
    trades_opened: int = 0
    trades_closed: int = 0
    wins: int = 0
    losses: int = 0
    realized_pnl: float = 0.0
    fees_paid: float = 0.0
    peak_pnl: float = 0.0
    worst_pnl: float = 0.0

    @property
    def win_rate(self) -> float:
        total = self.wins + self.losses
        if total == 0:
            return 0.0
        return self.wins / total


class RiskManager:
    """Enforces risk limits and tracks positions."""

    def __init__(self, balance: Optional[float] = None):
        self.balance = balance or PAPER_SEED_BALANCE
        self.session_start_balance = self.balance
        self.positions: dict[str, Position] = {}
        self.daily = DailyStats(
            date=time.strftime("%Y-%m-%d")
        )
        self._position_counter = 0
        self._halted = False

    @property
    def daily_pnl_pct(self) -> float:
        if self.session_start_balance == 0:
            return 0.0
        return self.daily.realized_pnl / self.session_start_balance

    @property
    def is_halted(self) -> bool:
        return self._halted

    def can_open(self) -> tuple[bool, str]:
        """Check if a new position can be opened."""
        # Daily loss cap
        if self.daily_pnl_pct <= -DAILY_LOSS_CAP:
            self._halted = True
            return False, (
                f"Daily loss cap hit: "
                f"{self.daily_pnl_pct:.2%} <= -{DAILY_LOSS_CAP:.1%}"
            )

        # Max concurrent positions
        if len(self.positions) >= MAX_CONCURRENT_POSITIONS:
            return False, (
                f"Max positions: {len(self.positions)}"
                f"/{MAX_CONCURRENT_POSITIONS}"
            )

        # Minimum balance
        position_size = self.balance * RISK_PER_TRADE
        if position_size < MIN_POSITION_USD:
            return False, (
                f"Position too small: ${position_size:.2f}"
            )

        return True, "OK"

    def calculate_size(self, entry_price: float) -> tuple[float, int]:
        """
        Calculate position size based on risk limits.
        Returns (cost_usd, shares).
        """
        # 0.5% of current balance
        raw_size = self.balance * RISK_PER_TRADE

        # Clamp to limits
        size = max(MIN_POSITION_USD, min(MAX_POSITION_USD, raw_size))

        # Calculate shares (each share costs entry_price)
        if entry_price <= 0:
            return 0.0, 0
        shares = int(size / entry_price)
        actual_cost = shares * entry_price

        return actual_cost, shares

    def open_position(
        self,
        slug: str,
        side: str,
        entry_price: float,
        shares: int,
        cost_usd: float,
    ) -> Optional[Position]:
        """Record a new position."""
        can, reason = self.can_open()
        if not can:
            logger.warning(f"Cannot open: {reason}")
            return None

        self._position_counter += 1
        pid = f"btc_{self._position_counter}_{int(time.time())}"

        pos = Position(
            position_id=pid,
            slug=slug,
            side=side,
            entry_price=entry_price,
            shares=shares,
            cost_usd=cost_usd,
            entry_time_ms=int(time.time() * 1000),
            current_value=cost_usd,
            peak_value=cost_usd,
            paper=PAPER_MODE,
        )
        self.positions[pid] = pos
        self.balance -= cost_usd
        self.daily.trades_opened += 1

        logger.info(
            f"Opened {pid}: {side} {slug} "
            f"@ {entry_price:.4f} x{shares} "
            f"= ${cost_usd:.2f}"
        )
        return pos

    def close_position(
        self, position_id: str, exit_price: float
    ) -> Optional[float]:
        """
        Close a position and record P&L.
        Returns realized P&L in USD.
        """
        pos = self.positions.get(position_id)
        if not pos:
            logger.warning(f"Position not found: {position_id}")
            return None

        # Calculate exit value
        exit_value = pos.shares * exit_price
        fee = exit_value * TAKER_FEE
        net_exit = exit_value - fee

        pnl = net_exit - pos.cost_usd

        # Update balance
        self.balance += net_exit

        # Update daily stats
        self.daily.trades_closed += 1
        self.daily.realized_pnl += pnl
        self.daily.fees_paid += fee
        if pnl > 0:
            self.daily.wins += 1
        else:
            self.daily.losses += 1
        self.daily.peak_pnl = max(
            self.daily.peak_pnl, self.daily.realized_pnl
        )
        self.daily.worst_pnl = min(
            self.daily.worst_pnl, self.daily.realized_pnl
        )

        logger.info(
            f"Closed {position_id}: "
            f"exit={exit_price:.4f} "
            f"pnl=${pnl:+.2f} "
            f"hold={pos.hold_time_s:.1f}s"
        )

        del self.positions[position_id]
        return pnl

    def update_position_value(
        self, position_id: str, current_price: float
    ):
        """Update mark-to-market value of a position."""
        pos = self.positions.get(position_id)
        if not pos:
            return
        pos.current_value = pos.shares * current_price
        pos.peak_value = max(pos.peak_value, pos.current_value)

    def reset_daily(self):
        """Reset daily stats at midnight."""
        logger.info(
            f"Daily reset. Final stats: "
            f"trades={self.daily.trades_closed}, "
            f"W/L={self.daily.wins}/{self.daily.losses}, "
            f"pnl=${self.daily.realized_pnl:+.2f}"
        )
        self.daily = DailyStats(
            date=time.strftime("%Y-%m-%d")
        )
        self.session_start_balance = self.balance
        self._halted = False

    def status(self) -> dict:
        """Current risk manager status."""
        return {
            "balance": round(self.balance, 2),
            "open_positions": len(self.positions),
            "daily_pnl": round(self.daily.realized_pnl, 2),
            "daily_pnl_pct": f"{self.daily_pnl_pct:.2%}",
            "trades_today": self.daily.trades_closed,
            "win_rate": f"{self.daily.win_rate:.0%}",
            "halted": self._halted,
        }
