import time
import logging
from datetime import datetime, timezone
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live

logger = logging.getLogger("polyfarm.terminal")

STRATEGY_COLORS = {
    "oracle_arb": "green",
    "exception": "yellow",
    "fade": "dark_orange",
    "overnight": "blue",
}


class TerminalDashboard:

    def __init__(self, wallet, position_monitor,
                 market_loader, registry):
        self.wallet = wallet
        self.pm = position_monitor
        self.loader = market_loader
        self.registry = registry
        self._start_time = datetime.now(timezone.utc)
        self._session_num = 1
        self._recent_trades: list = []

    def add_recent_trade(self, trade: dict):
        self._recent_trades.insert(0, trade)
        self._recent_trades = (
            self._recent_trades[:20]
        )

    def _uptime(self) -> str:
        delta = datetime.now(timezone.utc) - \
                self._start_time
        hours = int(delta.total_seconds() // 3600)
        mins = int(
            (delta.total_seconds() % 3600) // 60
        )
        return f"{hours}h {mins}m"

    def _header(self) -> Panel:
        mode = "PAPER" if self.wallet.paper_mode \
            else "LIVE"
        phase = "2" if hasattr(self.wallet, '_phase2') \
            else "1"
        now = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
        text = Text()
        text.append("POLYFARM", style="bold cyan")
        text.append(f" | Phase {phase} | ")
        text.append(
            f"[{mode}]",
            style="bold green" if mode == "PAPER"
            else "bold red"
        )
        text.append(
            f"\n{now} | Uptime: {self._uptime()} | "
            f"Session #{self._session_num}"
        )
        return Panel(text, title="PolyFarm")

    def _wallet_panel(self) -> Panel:
        s = self.wallet.state
        gap = s.live_portfolio_value - s.floor_value
        working = gap
        deployed = s.open_positions_value
        pnl = (
            s.live_portfolio_value
            - s.session_start_value
        )
        pnl_pct = (
            s.daily_gain_pct * 100
        )

        table = Table(show_header=False, expand=True)
        table.add_column("Key", style="dim")
        table.add_column("Value", justify="right")
        table.add_row(
            "Total",
            f"${s.live_portfolio_value:.2f}"
        )
        table.add_row(
            "Floor",
            f"${s.floor_value:.2f}"
        )
        table.add_row("Gap", f"${gap:.2f}")
        table.add_row(
            "Working", f"${working:.2f}"
        )
        table.add_row(
            "Deployed", f"${deployed:.2f}"
        )
        table.add_row(
            "Cash", f"${s.cash_balance:.2f}"
        )
        sign = "+" if pnl >= 0 else ""
        table.add_row(
            "Session P&L",
            f"{sign}${pnl:.2f} ({sign}{pnl_pct:.1f}%)"
        )
        table.add_row(
            "Profit Mode", s.profit_mode
        )
        table.add_row(
            "Loss Mode", s.loss_mode
        )
        table.add_row(
            "Peak Today",
            f"+{s.daily_peak_gain:.1%}"
        )
        table.add_row("Lock at", "+17%")
        return Panel(table, title="Wallet")

    def _activity_panel(self) -> Panel:
        positions = self.pm.get_all_positions()
        htr = self.pm.get_htr_count()
        s = self.wallet.state

        table = Table(show_header=False, expand=True)
        table.add_column("Key", style="dim")
        table.add_column("Value", justify="right")
        table.add_row(
            "Open Positions", str(len(positions))
        )
        table.add_row("HTR Count", str(htr))
        table.add_row(
            "Exception Budget",
            f"{s.exception_trades_today}/2"
        )
        table.add_row(
            "Fade Budget",
            f"{s.fade_trades_today}/3"
        )

        sports = {}
        for p in positions.values():
            sports[p.sport] = (
                sports.get(p.sport, 0) + 1
            )
        for sport, count in sorted(
            sports.items()
        ):
            table.add_row(f"  {sport}", str(count))

        return Panel(table, title="Activity")

    def _positions_table(self) -> Panel:
        table = Table(expand=True)
        table.add_column("Market", max_width=25)
        table.add_column("Sport", max_width=8)
        table.add_column("Strategy", max_width=10)
        table.add_column("Band", max_width=4)
        table.add_column("Entry", justify="right")
        table.add_column("Now", justify="right")
        table.add_column("Gain%", justify="right")
        table.add_column("Target", justify="right")
        table.add_column("Time", max_width=8)

        positions = self.pm.get_all_positions()
        for slug, pos in positions.items():
            color = STRATEGY_COLORS.get(
                pos.strategy, "white"
            )
            now_val = self.wallet._position_values.get(
                slug, {}
            ).get("current_bid", pos.entry_price)
            gain = (
                (now_val - pos.entry_price)
                / pos.entry_price * 100
                if pos.entry_price > 0 else 0
            )
            elapsed = (
                datetime.now(timezone.utc)
                - pos.entry_time
            ).total_seconds()
            mins = int(elapsed // 60)
            gain_style = (
                "green" if gain >= 0 else "red"
            )
            short_slug = slug[:24]
            table.add_row(
                Text(short_slug, style=color),
                pos.sport[:8],
                pos.strategy,
                pos.band,
                f"{pos.entry_price:.4f}",
                f"{now_val:.4f}",
                Text(
                    f"{gain:+.1f}%",
                    style=gain_style
                ),
                f"{pos.exit_target:.4f}",
                f"{mins}m",
            )

        return Panel(
            table, title="Open Positions"
        )

    def _system_panel(self) -> Panel:
        table = Table(show_header=False, expand=True)
        table.add_column("System", style="dim")
        table.add_column("Status", justify="right")
        table.add_row("WS Markets", "●")
        table.add_row("WS Private", "●")
        table.add_row("Odds API", "●")
        table.add_row("Supabase", "●")
        table.add_row("Telegram", "●")
        table.add_row("Phase 2", "OFF")
        return Panel(table, title="System")

    def _build_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="body"),
            Layout(name="footer", size=8),
        )
        layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=2),
        )
        layout["left"].split_column(
            Layout(name="wallet"),
            Layout(name="activity"),
        )
        layout["right"].split_column(
            Layout(name="positions"),
        )
        layout["header"].update(self._header())
        layout["wallet"].update(self._wallet_panel())
        layout["activity"].update(
            self._activity_panel()
        )
        layout["positions"].update(
            self._positions_table()
        )
        layout["footer"].update(self._system_panel())
        return layout

    def run(self):
        """Run in daemon thread."""
        console = Console()
        try:
            with Live(
                self._build_layout(),
                console=console,
                refresh_per_second=0.5,
                screen=True,
            ) as live:
                while True:
                    time.sleep(2)
                    live.update(self._build_layout())
        except Exception as e:
            logger.debug(
                f"Terminal dashboard stopped: {e}"
            )
