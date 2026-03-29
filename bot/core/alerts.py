import asyncio
import logging
import os
import aiohttp
from datetime import datetime, timezone

logger = logging.getLogger("polyfarm.alerts")

EXIT_EMOJI = {
    "reprice": "✅",
    "exception_reprice": "✅",
    "fade_reprice": "✅",
    "profit_lock": "🔒",
    "trailing_stop": "🛡️",
    "timeout": "⏱️",
    "resolution": "🏁",
    "pre_resolution": "🏁",
    "stop_loss": "🛑",
    "exception_stop_loss": "🛑",
    "fade_stop_loss": "🛑",
    "drain": "💧",
    "drain_LOCK_AND_DRAIN": "💧",
    "drain_SHUTDOWN": "💧",
    "emergency": "🚨",
    "emergency_DAILY_HALT": "🚨",
    "emergency_FLOOR_BREACH": "🚨",
    "fade_deficit_closed": "⚠️",
    "overnight_reeval": "🌙",
}


class AlertManager:

    def __init__(self):
        self._token = None
        self._chat_id = None
        self._enabled = False
        self._queue: asyncio.Queue = asyncio.Queue()
        self._session: aiohttp.ClientSession = None

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
        logger.info("Telegram alerts initialized")

    async def _sender_loop(self):
        while True:
            try:
                msg = await self._queue.get()
                await self._send(msg)
            except Exception as e:
                logger.debug(f"Alert sender error: {e}")

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
        try:
            self._queue.put_nowait(text)
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
        mode = "PAPER" if paper else "LIVE"
        band = getattr(signal, "band", "?")
        label = f"BAND {band}"
        if strategy == "exception":
            label = "EX"
        elif strategy == "fade":
            label = "FADE"

        profit_mode = "NORMAL"
        loss_mode = "NORMAL"
        wallet_val = 0.0
        floor_val = 0.0
        try:
            from core.wallet import WalletManager
            # signal may carry these via context
        except Exception:
            pass

        msg = (
            f"🟢 [{label}] {mode} ENTRY\n"
            f"Sport: {signal.sport} | "
            f"Type: {signal.market_type}\n"
            f"{signal.teams}\n"
            f"Entry: {fill_price:.4f} | "
            f"Sharp: {signal.sharp_prob:.4f} | "
            f"Edge: {signal.raw_edge:.4f}\n"
            f"Net edge: {signal.net_edge_pct:.2%}\n"
            f"Size: ${signal.position_usd:.2f} | "
            f"Shares: {signal.shares}\n"
            f"Exit target: {signal.exit_target:.4f} | "
            f"Confidence: {signal.confidence:.0%}"
        )
        self._enqueue(msg)

    async def send_exit(self, position, exit_price,
                         exit_type, net_pnl,
                         duration_seconds,
                         wallet_value):
        emoji = EXIT_EMOJI.get(exit_type, "📤")
        # Match partial keys
        if emoji == "📤":
            for k, v in EXIT_EMOJI.items():
                if k in exit_type:
                    emoji = v
                    break
        mode = "PAPER" if position.paper_mode else "LIVE"
        pnl_pct = (
            net_pnl / (
                position.entry_price * position.shares
            ) * 100 if position.shares > 0 else 0
        )
        duration = self._fmt_duration(duration_seconds)
        sign = "+" if net_pnl >= 0 else ""
        msg = (
            f"{emoji} {exit_type.upper()} {mode}\n"
            f"{position.teams}\n"
            f"Entry: {position.entry_price:.4f} → "
            f"Exit: {exit_price:.4f}\n"
            f"P&L: {sign}${net_pnl:.4f} "
            f"({sign}{pnl_pct:.1f}%) | "
            f"Hold: {duration}\n"
            f"Wallet: ${wallet_value:.2f}"
        )
        self._enqueue(msg)

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
            f"🚨 FLOOR BREACH — TRADING HALTED\n"
            f"All orders cancelled. "
            f"Exiting positions.\n"
            f"Portfolio: ${value:.2f} | "
            f"Floor: ${floor:.2f}\n"
            f"Manual restart required."
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
            f"🏆 SESSION LOCKED — {reason}\n"
            f"Up {gain_pct:.1%} today.\n"
            f"Exception and fade trades "
            f"still active.\n"
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
                                  paper_progress):
        mode = "PAPER" if paper_mode else "LIVE"
        msg = (
            f"🚀 POLYFARM SESSION START {mode}\n"
            f"Wallet: ${wallet:.2f} | "
            f"Floor: ${floor:.2f}\n"
            f"Working capital: ${capital:.2f}\n"
            f"Markets loaded: {market_count}\n"
            f"Paper unlock: {paper_progress}/50 trades"
        )
        self._enqueue(msg)

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
        msg = (
            f"📊 DAILY COMPLETE {date}\n"
            f"P&L: {sign}${pnl:.2f} "
            f"({sign}{pnl_pct:.1f}%)\n"
            f"Wallet: ${start:.2f} → ${end:.2f}\n"
            f"Peak today: +{peak:.1%}"
        )
        self._enqueue(msg)

    async def close(self):
        if self._session:
            await self._session.close()
