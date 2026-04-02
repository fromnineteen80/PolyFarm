import asyncio
import logging
import os
import aiohttp
from datetime import datetime, timezone

logger = logging.getLogger("polyfarm.alerts")

# Human-readable exit reason labels
EXIT_LABEL = {
    "reprice": "sold at target",
    "exception_reprice": "sold at target",
    "fade_reprice": "sold at target",
    "profit_lock": "target hit",
    "trailing_stop": "locked in gains",
    "timeout": "held too long",
    "resolution": "game over",
    "pre_resolution": "game ending",
    "stop_loss": "cut losses",
    "exception_stop_loss": "cut losses",
    "fade_stop_loss": "cut losses",
    "drain": "closing out",
    "drain_LOCK_AND_DRAIN": "closing out",
    "drain_SHUTDOWN": "shutting down",
    "emergency": "emergency exit",
    "emergency_DAILY_HALT": "daily limit hit",
    "emergency_FLOOR_BREACH": "floor breached",
    "fade_deficit_closed": "fade recovered",
    "overnight_reeval": "overnight review",
}

def _exit_label(exit_type: str) -> str:
    label = EXIT_LABEL.get(exit_type)
    if label:
        return label
    for k, v in EXIT_LABEL.items():
        if k in exit_type:
            return v
    return exit_type


class AlertManager:

    BATCH_INTERVAL = 1800  # 30 minutes

    def __init__(self):
        self._token = None
        self._chat_id = None
        self._enabled = False
        self._queue: asyncio.Queue = asyncio.Queue()
        self._session: aiohttp.ClientSession = None
        self._trade_batch: list = []  # batched trade alerts
        self._urgent_queue: asyncio.Queue = asyncio.Queue()  # sent immediately
        self.wallet = None  # set by main.py for balance reads

    async def initialize(self):
        self._token = os.environ.get(
            "TELEGRAM_BOT_TOKEN"
        )
        self._chat_id = os.environ.get(
            "TELEGRAM_CHAT_ID"
        )
        if not self._token or not self._chat_id:
            logger.warning(
                "Telegram credentials missing — "
                "alerts disabled"
            )
            return
        self._session = aiohttp.ClientSession()
        self._enabled = True
        asyncio.create_task(self._sender_loop())
        asyncio.create_task(self._batch_loop())
        logger.info("Telegram alerts initialized")

    async def _sender_loop(self):
        """Send urgent messages immediately."""
        while True:
            try:
                msg = await self._urgent_queue.get()
                await self._send(msg)
                await asyncio.sleep(2)
            except Exception as e:
                logger.debug(f"Alert sender error: {e}")

    async def _batch_loop(self):
        """Send trade summary every 30 minutes."""
        while True:
            await asyncio.sleep(self.BATCH_INTERVAL)
            if not self._trade_batch:
                continue
            batch = self._trade_batch.copy()
            self._trade_batch.clear()

            entries = [b for b in batch if b["type"] == "entry"]
            exits = [b for b in batch if b["type"] == "exit"]

            total_pnl = sum(b.get("pnl", 0) for b in exits)
            wins = sum(1 for b in exits if b.get("pnl", 0) > 0)
            losses = len(exits) - wins

            # Get wallet state directly
            wallet_val = None
            start_val = None
            if self.wallet:
                wallet_val = self.wallet.state.live_portfolio_value
                start_val = self.wallet.state.session_start_value

            lines = ["-- 30-Minute Summary --", ""]

            # Trade activity
            if entries:
                lines.append(f"Opened: {len(entries)} new trades")
            if exits:
                sign = "+" if total_pnl >= 0 else ""
                lines.append(
                    f"Closed: {len(exits)} trades "
                    f"({wins} won, {losses} lost)"
                )
                lines.append(f"Period P&L: {sign}${total_pnl:.2f}")

            # Individual results
            if exits:
                lines.append("")
                for b in exits[-5:]:
                    sign = "+" if b.get("pnl", 0) >= 0 else ""
                    lines.append(
                        f"  {b.get('teams', '?')}: "
                        f"{sign}${b.get('pnl', 0):.2f} "
                        f"({_exit_label(b.get('exit_type', '?'))})"
                    )
                if len(exits) > 5:
                    lines.append(f"  ... and {len(exits) - 5} more")

            # Portfolio summary
            lines.append("")
            if wallet_val:
                lines.append(f"Balance: ${wallet_val:.2f}")
            if wallet_val and start_val and start_val > 0:
                growth = ((wallet_val - start_val) / start_val) * 100
                sign = "+" if growth >= 0 else ""
                lines.append(f"Today: {sign}{growth:.1f}%")

            msg = "\n".join(lines)
            await self._send(msg)

    async def _send(self, text: str):
        if not self._enabled:
            return
        url = (
            f"https://api.telegram.org/"
            f"bot{self._token}/sendMessage"
        )
        payload = {
            "chat_id": self._chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
        for attempt in range(2):
            try:
                async with self._session.post(
                    url, json=payload, timeout=10
                ) as resp:
                    if resp.status == 200:
                        try:
                            from data.database import (
                                set_bot_config
                            )
                            await set_bot_config(
                                "telegram_last_alert",
                                datetime.now(
                                    timezone.utc
                                ).isoformat()
                            )
                        except Exception:
                            pass
                        return
                    logger.debug(
                        f"Telegram {resp.status}"
                    )
            except Exception as e:
                if attempt == 0:
                    await asyncio.sleep(1)
                else:
                    logger.debug(
                        f"Telegram retry failed: {e}"
                    )

    def _enqueue(self, text: str):
        """Send urgent messages immediately."""
        try:
            self._urgent_queue.put_nowait(text)
        except asyncio.QueueFull:
            logger.debug("Alert queue full")

    def _fmt_duration(self, seconds: int) -> str:
        if seconds < 60:
            return f"{seconds}s"
        m = seconds // 60
        s = seconds % 60
        if m < 60:
            return f"{m}m {s}s"
        h = m // 60
        m = m % 60
        return f"{h}h {m}m"

    async def send_entry(self, signal, fill_price,
                          strategy, paper):
        self._trade_batch.append({
            "type": "entry",
            "teams": signal.teams,
            "sport": signal.sport,
            "band": getattr(signal, "band", "?"),
            "price": fill_price,
            "edge": signal.raw_edge,
            "strategy": strategy,
        })

    async def send_exit(self, position, exit_price,
                         exit_type, net_pnl,
                         duration_seconds,
                         wallet_value):
        self._trade_batch.append({
            "type": "exit",
            "teams": position.teams,
            "exit_type": exit_type,
            "pnl": net_pnl,
            "duration": duration_seconds,
            "wallet": wallet_value,
        })

    async def send_stop_loss(self, position,
                              current_gain, strategy):
        msg = (
            f"🛑 {strategy.upper()} STOP LOSS HIT\n"
            f"{position.teams}\n"
            f"Position down {current_gain:.1%} — "
            f"exiting immediately.\n"
            f"Wallet protected."
        )
        self._enqueue(msg)

    async def send_fade_broken(self, position):
        msg = (
            f"⚠️ FADE THESIS BROKEN — GAME TIED\n"
            f"{position.teams}\n"
            f"Fade team equalized score. "
            f"Exiting position."
        )
        self._enqueue(msg)

    async def send_floor_warning(self, value,
                                  floor, gap_pct):
        gap = value - floor
        msg = (
            f"⚠️ FLOOR WARNING — "
            f"{gap_pct:.0%} PROXIMITY\n"
            f"Portfolio: ${value:.2f} | "
            f"Floor: ${floor:.2f}\n"
            f"Gap: ${gap:.2f} ({gap_pct:.1%})"
        )
        self._enqueue(msg)

    async def send_floor_critical(self, value,
                                   floor, gap_pct):
        gap = value - floor
        msg = (
            f"🔴 CRITICAL FLOOR WARNING — "
            f"5% PROXIMITY\n"
            f"Portfolio: ${value:.2f} | "
            f"Floor: ${floor:.2f}\n"
            f"Gap: ${gap:.2f} ({gap_pct:.1%})"
        )
        self._enqueue(msg)

    async def send_floor_breach(self, value, floor):
        msg = (
            f"Daily loss limit reached.\n"
            f"No new trades until tomorrow.\n"
            f"Open positions will close naturally.\n"
            f"Balance: ${value:.2f}\n"
            f"Resets at midnight ET."
        )
        self._enqueue(msg)

    async def send_harvest_mode(self, gain_pct,
                                 wallet_value):
        msg = (
            f"📈 HARVEST MODE — Up {gain_pct:.1%}\n"
            f"Sizing reduced 25%. Still farming.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_protection_mode(self, gain_pct,
                                    wallet_value):
        msg = (
            f"🛡️ PROTECTION MODE — Up {gain_pct:.1%}\n"
            f"Band A only. Sizing reduced 50%.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_session_locked(self, reason,
                                   gain_pct,
                                   wallet_value):
        msg = (
            f"Daily target hit! Up {gain_pct:.1%} today.\n"
            f"No new trades. Open positions "
            f"will close naturally.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_daily_reduce(self, pnl_pct,
                                 wallet_value):
        msg = (
            f"⚠️ DAILY LOSS -10% — SIZING REDUCED\n"
            f"Session P&L: {pnl_pct:.1%}\n"
            f"Exception/fade suspended.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_daily_pause(self, pnl_pct,
                                wallet_value):
        msg = (
            f"⚠️ DAILY LOSS -15% — ENTRIES PAUSED\n"
            f"No new entries. Managing existing "
            f"positions.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_daily_halt(self, pnl_pct,
                               wallet_value):
        msg = (
            f"🚨 DAILY LOSS HALT — -20%\n"
            f"Emergency exit all positions.\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

    async def send_session_start(self, wallet, floor,
                                  capital, market_count,
                                  paper_mode,
                                  paper_progress,
                                  paper_win_rate=0.0):
        if paper_mode:
            wr = paper_win_rate * 100 if paper_win_rate else 0
            needs = max(0, 300 - paper_progress)
            status = "ready to go live" if paper_progress >= 300 and wr >= 70 else f"{needs} trades to go"
            msg = (
                f"Bot started. Paper mode.\n\n"
                f"Balance: ${wallet:.2f}\n"
                f"Paper progress: {paper_progress}/300 trades "
                f"({wr:.0f}% win rate)\n"
                f"{status}"
            )
        else:
            msg = (
                f"Bot started. Live mode.\n\n"
                f"Balance: ${wallet:.2f}\n"
                f"Daily target: ${wallet * 1.15:.2f}\n"
                f"Floor: ${floor:.2f}"
            )
        self._enqueue(msg)

    # ─────────────────────────────────────────────
    # 1. PRE-GAME INTELLIGENCE ALERT
    # ─────────────────────────────────────────────

    async def send_pre_game_intel(self, game, signals):
        """
        Fires ~90 min before game start when any
        qualifying signal or team matchup is found.
        game: MarketInfo from registry
        signals: dict with keys: oracle_arb, dominant,
                 fade — each None or signal data
        """
        sport_emoji = {
            "basketball_nba": "🏀",
            "basketball_ncaab": "🏀",
            "icehockey_nhl": "🏒",
            "baseball_mlb": "⚾",
            "americanfootball_nfl": "🏈",
            "americanfootball_ncaaf": "🏈",
            "soccer_epl": "⚽",
            "soccer_usa_mls": "⚽",
            "soccer_mls": "⚽",
            "soccer_uefa_champs_league": "⚽",
            "tennis_atp": "🎾",
            "tennis_wta": "🎾",
            "mma_mixed_martial_arts": "🥊",
            "golf_pga_tour": "⛳",
        }
        emoji = sport_emoji.get(game.sport, "🎯")

        lines = [
            f"{emoji} PRE-GAME INTEL",
            f"{game.home_team} vs {game.away_team}",
            f"Sport: {game.sport} | "
            f"Start: {game.game_start_time}",
            f"Price: {game.yes_price:.2f}",
            "",
        ]

        arb = signals.get("oracle_arb")
        if arb:
            lines.append("📐 ORACLE ARB SETUP")
            lines.append(
                f"  Poly: {arb['poly_price']:.4f} | "
                f"Sharp: {arb['sharp_prob']:.4f}"
            )
            lines.append(
                f"  Gap: {arb['gap']:.4f} | "
                f"Band: {arb['band']}"
            )
            if arb.get("line_movement"):
                lines.append(
                    f"  Sharp moved: "
                    f"{arb['line_movement']}"
                )
            lines.append("")

        dom = signals.get("dominant")
        if dom:
            from config import DOMINANT_TEAMS
            team_cfg = DOMINANT_TEAMS.get(
                dom["team"], {}
            )
            lines.append(
                f"⭐ DOMINANT TEAM: {dom['team']}"
            )
            lines.append(
                f"  Comeback rate: "
                f"{team_cfg.get('comeback_win_rate_when_trailing', 0):.0%}"
            )
            lines.append(
                f"  Overreaction: "
                f"{team_cfg.get('market_overreaction_tendency', 'unknown')}"
            )
            deficit = team_cfg.get(
                "deficit_range", (0, 0)
            )
            lines.append(
                f"  Exception triggers at "
                f"{deficit[0]}-{deficit[1]} deficit"
            )
            notes = team_cfg.get("notes", "")
            if notes:
                lines.append(f"  Why: {notes}")
            lines.append("")

        fade = signals.get("fade")
        if fade:
            from config import FADE_TEAMS, FADE_MIN_GAP
            fade_cfg = FADE_TEAMS.get(
                fade["team"], {}
            )
            conf = fade_cfg.get("confidence", "medium")
            min_gap = FADE_MIN_GAP.get(conf, 0.10)
            lines.append(
                f"🚫 FADE TARGET: {fade['team']}"
            )
            lines.append(
                f"  Confidence: {conf} | "
                f"Min gap: {min_gap:.2f}"
            )
            reason = fade_cfg.get("reason", "")
            if reason:
                lines.append(f"  Why: {reason}")
            lines.append("")

        self._enqueue("\n".join(lines))

    # ─────────────────────────────────────────────
    # 2. GAME COMPLETE SUMMARY ALERT
    # ─────────────────────────────────────────────

    async def send_game_summary(self, game_slug,
                                 trades, final_score=None,
                                 teams=None, sport=None):
        """
        Fires when all positions for a game close
        or game is_finished=True.
        trades: list of closed trade dicts for this game
        """
        if not trades:
            return

        sport_emoji = {
            "basketball_nba": "🏀",
            "icehockey_nhl": "🏒",
            "baseball_mlb": "⚾",
            "americanfootball_nfl": "🏈",
            "soccer_epl": "⚽",
        }
        emoji = sport_emoji.get(sport or "", "🏁")

        lines = [f"{emoji} GAME COMPLETE"]
        if teams:
            lines.append(teams)
        if final_score:
            lines.append(f"Final: {final_score}")
        lines.append("")

        total_pnl = 0.0
        wins = 0
        for t in trades:
            pnl = float(t.get("pnl", 0) or 0)
            total_pnl += pnl
            if pnl > 0:
                wins += 1
            entry = float(
                t.get("entry_price", 0) or 0
            )
            exit_p = float(
                t.get("exit_price", 0) or 0
            )
            etype = t.get("exit_type", "?")
            sign = "+" if pnl >= 0 else ""
            lines.append(
                f"  {entry:.4f} → {exit_p:.4f} "
                f"({etype}) {sign}${pnl:.4f}"
            )

        lines.append("")
        count = len(trades)
        wr = wins / count * 100 if count > 0 else 0
        sign = "+" if total_pnl >= 0 else ""
        lines.append(
            f"Trades: {count} | Won: {wins} | "
            f"Rate: {wr:.0f}%"
        )
        lines.append(
            f"Game P&L: {sign}${total_pnl:.4f}"
        )

        self._enqueue("\n".join(lines))

    # ─────────────────────────────────────────────
    # 3. ENHANCED END OF DAY REPORT
    # ─────────────────────────────────────────────

    async def send_daily_report(self, stats: dict):
        date = stats.get("date", "")
        pnl = stats.get("pnl", 0)
        peak = stats.get("peak_gain", 0)
        start = stats.get("wallet_start", 0)
        end = stats.get("wallet_end", 0)
        pnl_pct = (
            pnl / start * 100 if start > 0 else 0
        )
        sign = "+" if pnl >= 0 else ""

        lines = [
            f"📊 DAILY COMPLETE {date}",
            f"P&L: {sign}${pnl:.2f} "
            f"({sign}{pnl_pct:.1f}%)",
            f"Wallet: ${start:.2f} → ${end:.2f}",
            f"Peak today: +{peak:.1%}",
            "",
        ]

        # Strategy breakdown
        strats = stats.get("strategies")
        if strats:
            lines.append("BY STRATEGY:")
            for name, s in strats.items():
                trades = s.get("trades", 0)
                if trades == 0:
                    continue
                wr = s.get("win_rate", 0)
                s_pnl = s.get("pnl", 0)
                s_sign = "+" if s_pnl >= 0 else ""
                lines.append(
                    f"  {name}: {trades} trades | "
                    f"{wr:.0f}% WR | "
                    f"{s_sign}${s_pnl:.2f}"
                )
            lines.append("")

        # Sport breakdown
        sports = stats.get("sports")
        if sports:
            lines.append("BY SPORT:")
            sorted_sports = sorted(
                sports.items(),
                key=lambda x: x[1].get("pnl", 0),
                reverse=True
            )
            for sport, s in sorted_sports:
                trades = s.get("trades", 0)
                if trades == 0:
                    continue
                s_pnl = s.get("pnl", 0)
                s_sign = "+" if s_pnl >= 0 else ""
                lines.append(
                    f"  {sport}: {trades} trades | "
                    f"{s_sign}${s_pnl:.2f}"
                )
            lines.append("")

        # Fee summary
        fees = stats.get("total_fees", 0)
        rebates = stats.get("total_rebates", 0)
        if fees or rebates:
            net_cost = fees - rebates
            lines.append("FEES:")
            lines.append(
                f"  Taker fees: ${fees:.4f}"
            )
            lines.append(
                f"  Maker rebates: ${rebates:.4f}"
            )
            lines.append(
                f"  Net cost: ${net_cost:.4f}"
            )
            lines.append("")

        # All-time summary
        alltime = stats.get("alltime")
        if alltime:
            orig = alltime.get("original_capital", 0)
            current = alltime.get("current_value", 0)
            at_gain = current - orig
            at_pct = (
                at_gain / orig * 100
                if orig > 0 else 0
            )
            days = alltime.get("days_running", 0)
            avg_daily = (
                at_pct / days if days > 0 else 0
            )
            at_sign = "+" if at_gain >= 0 else ""
            lines.append("ALL-TIME:")
            lines.append(
                f"  Start: ${orig:.2f} → "
                f"Now: ${current:.2f}"
            )
            lines.append(
                f"  Gain: {at_sign}${at_gain:.2f} "
                f"({at_sign}{at_pct:.1f}%)"
            )
            lines.append(
                f"  Days: {days} | "
                f"Avg daily: {avg_daily:.2f}%"
            )
            if avg_daily > 0 and current > 0:
                proj_30 = current * (
                    (1 + avg_daily / 100) ** 30
                )
                lines.append(
                    f"  30-day projection: "
                    f"${proj_30:.2f}"
                )
            lines.append("")

        # Paper mode progress
        paper = stats.get("paper_progress")
        if paper:
            completed = paper.get("completed", 0)
            wr = paper.get("win_rate", 0)
            lines.append("PAPER PROGRESS:")
            lines.append(
                f"  {completed}/300 trades"
            )
            lines.append(
                f"  Win rate: {wr:.0%} "
                f"(need 70%)"
            )
            if completed > 0:
                days_est = max(
                    1,
                    int(
                        (300 - completed)
                        / max(
                            paper.get(
                                "trades_per_day", 1
                            ), 1
                        )
                    )
                )
                lines.append(
                    f"  Est. days to unlock: "
                    f"~{days_est}"
                )
            lines.append("")

        self._enqueue("\n".join(lines))

    # ─────────────────────────────────────────────
    # PAPER TRADING MILESTONE ANALYSIS
    # ─────────────────────────────────────────────

    async def send_paper_milestone(self, milestone, analysis):
        """
        Sent every 50 paper trades with full
        performance breakdown and recommendations.
        """
        a = analysis
        lines = [
            f"PAPER MILESTONE: {milestone} TRADES",
            "",
            f"Win Rate: {a.get('win_rate', 0):.0%} (need 70%)",
            f"Total P&L: {'+'if a.get('total_pnl',0)>=0 else ''}{a.get('total_pnl',0):.2f}",
            f"Avg P&L per trade: {'+'if a.get('avg_pnl',0)>=0 else ''}{a.get('avg_pnl',0):.4f}",
            "",
            "BY SPORT:",
        ]
        for sport, data in sorted(
            a.get("by_sport", {}).items(),
            key=lambda x: x[1].get("pnl", 0),
            reverse=True
        ):
            wr = data.get("win_rate", 0)
            pnl = data.get("pnl", 0)
            count = data.get("trades", 0)
            flag = " [WEAK]" if wr < 0.60 and count >= 5 else ""
            lines.append(
                f"  {sport}: {count} trades | "
                f"{wr:.0%} WR | "
                f"{'+'if pnl>=0 else ''}{pnl:.2f}{flag}"
            )

        lines.append("")
        lines.append("BY BAND:")
        for band, data in sorted(
            a.get("by_band", {}).items()
        ):
            wr = data.get("win_rate", 0)
            pnl = data.get("pnl", 0)
            count = data.get("trades", 0)
            lines.append(
                f"  Band {band}: {count} trades | "
                f"{wr:.0%} WR | "
                f"{'+'if pnl>=0 else ''}{pnl:.2f}"
            )

        lines.append("")
        lines.append("BY ENTRY DIRECTION:")
        for direction, data in a.get(
            "by_direction", {}
        ).items():
            wr = data.get("win_rate", 0)
            count = data.get("trades", 0)
            lines.append(
                f"  {direction}: {count} trades | "
                f"{wr:.0%} WR"
            )

        lines.append("")
        lines.append("BY EDGE SIZE:")
        for edge_bin, data in a.get(
            "by_edge_bin", {}
        ).items():
            wr = data.get("win_rate", 0)
            count = data.get("trades", 0)
            lines.append(
                f"  {edge_bin}: {count} trades | "
                f"{wr:.0%} WR"
            )

        lines.append("")
        lines.append("TIMING:")
        lines.append(
            f"  Avg hold (winners): "
            f"{a.get('avg_hold_winners', 0):.0f}m"
        )
        lines.append(
            f"  Avg hold (losers): "
            f"{a.get('avg_hold_losers', 0):.0f}m"
        )

        # Recommendations
        recs = a.get("recommendations", [])
        if recs:
            lines.append("")
            lines.append("RECOMMENDATIONS:")
            for r in recs:
                lines.append(f"  - {r}")

        # Go-live readiness
        lines.append("")
        ready = a.get("go_live_ready", False)
        if ready:
            lines.append(
                "STATUS: READY for live mode "
                "(300+ trades, 70%+ WR)"
            )
        else:
            remaining = max(0, 300 - milestone)
            lines.append(
                f"STATUS: {remaining} trades remaining "
                f"to unlock evaluation"
            )

        self._enqueue("\n".join(lines))

    async def close(self):
        if self._session:
            await self._session.close()
