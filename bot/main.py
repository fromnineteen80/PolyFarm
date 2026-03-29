import asyncio
import logging
import os
import signal
import threading
from datetime import datetime, timezone, timedelta
from polymarket_us import AsyncPolymarketUS
from config import PAPER_MODE, PHASE2_ENABLED, logger
from data.database import (
    init_database, seed_bot_config,
    log_system_event, set_bot_config,
    write_daily_snapshot, write_daily_stats,
    get_bot_config
)
from core.wallet import WalletManager
from core.market_loader import MarketLoader, MarketRegistry
from core.market_mapper import MarketMapper
from core.edge_detector import EdgeDetector
from core.order_manager import OrderManager
from core.position_monitor import PositionMonitor
from core.exception_monitor import ExceptionMonitor
from core.fade_monitor import FadeMonitor
from core.overnight_monitor import OvernightMonitor
from core.alerts import AlertManager
from core.ws_markets import WSMarkets
from core.ws_private import WSPrivate
from dashboard.terminal import TerminalDashboard


async def main():
    logger.info("PolyFarm starting...")
    logger.info(f"Paper mode: {PAPER_MODE}")

    # ── STEP 1: Validate environment ──────────────
    required_vars = [
        "POLYMARKET_KEY_ID",
        "POLYMARKET_SECRET_KEY",
        "ODDS_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "SUPABASE_URL",
        "SUPABASE_KEY",
    ]
    missing = [v for v in required_vars
               if not os.environ.get(v)]
    if missing:
        logger.critical(
            f"Missing required env vars: {missing}"
        )
        raise SystemExit(1)

    # ── STEP 2: Initialize database ───────────────
    init_database()
    await seed_bot_config()

    # ── STEP 3: Initialize Polymarket client ──────
    async with AsyncPolymarketUS(
        key_id=os.environ["POLYMARKET_KEY_ID"],
        secret_key=os.environ["POLYMARKET_SECRET_KEY"],
    ) as client:

        # ── STEP 4: Initialize components ─────────
        alerts = AlertManager()
        await alerts.initialize()

        registry = MarketRegistry()
        wallet = WalletManager(client, PAPER_MODE)
        market_loader = MarketLoader(client, registry)
        mapper = MarketMapper(registry, market_loader)

        position_monitor = PositionMonitor(
            client, wallet, None, registry
        )
        order_manager = OrderManager(
            client, wallet, alerts, position_monitor
        )
        position_monitor.om = order_manager

        wallet.set_alerts(alerts)
        wallet.set_order_manager(order_manager)

        exception_monitor = ExceptionMonitor(
            client, wallet, registry, mapper,
            order_manager, position_monitor
        )
        fade_monitor = FadeMonitor(
            client, wallet, registry, mapper,
            order_manager, position_monitor
        )
        overnight_monitor = OvernightMonitor(
            client, wallet, registry, mapper,
            order_manager, position_monitor
        )

        ws_markets = WSMarkets(
            registry, market_loader
        )
        market_loader.ws_manager = ws_markets

        ws_private = WSPrivate(
            position_monitor, wallet
        )

        edge_detector = EdgeDetector(
            registry, mapper, wallet, position_monitor
        )
        ws_markets.set_edge_detector(edge_detector)

        terminal = TerminalDashboard(
            wallet, position_monitor,
            market_loader, registry
        )

        # ── STEP 5: Session initialization ────────
        await wallet.session_init()
        await position_monitor.load_existing_positions()

        # ── STEP 6: Cancel orphaned orders ────────
        if not PAPER_MODE:
            try:
                await client.orders\
                    .cancel_all_open_orders()
                logger.info("Cancelled orphaned orders")
            except Exception as e:
                logger.warning(
                    f"Cancel orphaned orders: {e}"
                )

        # ── STEP 7: Send session start alert ──────
        stats = await get_bot_config(
            "paper_trades_completed"
        )
        paper_progress = int(stats or 0)
        await alerts.send_session_start(
            wallet=wallet.state.live_portfolio_value,
            floor=wallet.state.floor_value,
            capital=(
                wallet.state.live_portfolio_value
                - wallet.state.floor_value
            ),
            market_count=await registry.count(),
            paper_mode=PAPER_MODE,
            paper_progress=paper_progress,
        )

        # ── STEP 8: Start terminal in thread ──────
        terminal_thread = threading.Thread(
            target=terminal.run,
            daemon=True
        )
        terminal_thread.start()

        # ── STEP 9: Run all async tasks ───────────
        tasks = [
            market_loader.refresh_loop(),
            market_loader.poll_loop(),
            ws_markets.connect_and_listen(),
            ws_private.connect_and_listen(),
            position_monitor.monitor_loop(),
            edge_detector.detection_loop(),
            wallet.monitor_loop(),
            exception_monitor.monitor_loop(),
            fade_monitor.monitor_loop(),
            overnight_monitor.monitor_loop(),
            midnight_scheduler(
                wallet, alerts, market_loader
            ),
        ]

        if PHASE2_ENABLED:
            from phase2.binance_feed import BinanceFeed
            from phase2.crypto_edge_detector import (
                CryptoEdgeDetector
            )
            from phase2.crypto_order_manager import (
                CryptoOrderManager
            )
            await set_bot_config(
                "phase2_enabled", "true"
            )
            existing = await get_bot_config(
                "phase2_activation_date"
            )
            if not existing:
                await set_bot_config(
                    "phase2_activation_date",
                    datetime.now(
                        timezone.utc
                    ).date().isoformat()
                )
            binance = BinanceFeed()
            crypto_detector = CryptoEdgeDetector(
                registry, wallet, position_monitor,
                binance.price_queue
            )
            crypto_om = CryptoOrderManager(
                client, wallet, alerts,
                position_monitor
            )
            tasks.extend([
                binance.stream_loop(),
                crypto_detector.detection_loop(),
            ])

        # Handle shutdown signals
        shutdown_event = asyncio.Event()
        loop = asyncio.get_event_loop()

        def handle_shutdown(sig):
            logger.info(f"Shutdown signal: {sig}")
            shutdown_event.set()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: handle_shutdown(s)
            )

        try:
            done, pending = await asyncio.wait(
                [asyncio.create_task(t)
                 for t in tasks],
                return_when=asyncio.FIRST_EXCEPTION
            )
            for task in done:
                if task.exception():
                    raise task.exception()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            await shutdown(
                wallet, alerts, order_manager
            )


async def midnight_scheduler(wallet, alerts,
                              market_loader):
    """Pure async midnight scheduler."""
    while True:
        now = datetime.now()
        target = now.replace(
            hour=23, minute=59, second=0,
            microsecond=0
        )
        if now >= target:
            target += timedelta(days=1)
        seconds_until = (target - now).total_seconds()
        await asyncio.sleep(seconds_until)
        await write_end_of_day(wallet, alerts)
        await wallet.reset_daily()
        await asyncio.sleep(70)  # Avoid double-fire


async def write_end_of_day(wallet, alerts):
    """Write daily snapshot and stats at midnight."""
    from datetime import date
    today = date.today().isoformat()
    wallet_value = wallet.state.live_portfolio_value

    # Calculate projection values
    first_date = await get_bot_config(
        "first_live_trade_date"
    )
    first_value = await get_bot_config(
        "first_live_wallet_value"
    )
    proj_1pct = None
    proj_15pct = None
    proj_2pct = None
    if first_date and first_value:
        try:
            start = datetime.fromisoformat(first_date)
            start_val = float(first_value)
            days = (
                datetime.now() - start
            ).days
            proj_1pct = start_val * (1.01 ** days)
            proj_15pct = start_val * (1.015 ** days)
            proj_2pct = start_val * (1.02 ** days)
        except Exception:
            pass

    await write_daily_snapshot({
        "date": today,
        "wallet_value": wallet_value,
        "floor_value": wallet.state.floor_value,
        "session_pnl": (
            wallet_value
            - wallet.state.session_start_value
        ),
        "cumulative_pnl": (
            wallet_value
            - float(
                await get_bot_config(
                    "first_live_wallet_value"
                ) or wallet_value
            )
        ),
        "cumulative_pnl_pct": 0,
        "trades_today": 0,
        "win_rate_today": 0,
        "projected_1pct": proj_1pct,
        "projected_15pct": proj_15pct,
        "projected_2pct": proj_2pct,
        "paper_mode": PAPER_MODE,
    })

    # Send daily report
    await alerts.send_daily_report({
        "date": today,
        "wallet_start": wallet.state.session_start_value,
        "wallet_end": wallet_value,
        "pnl": (
            wallet_value
            - wallet.state.session_start_value
        ),
        "peak_gain": wallet.state.daily_peak_gain,
    })


async def shutdown(wallet, alerts, order_manager):
    """Clean shutdown sequence."""
    logger.info("Shutting down PolyFarm...")
    try:
        if not PAPER_MODE:
            await order_manager.drain_all_positions(
                "SHUTDOWN"
            )
        await alerts.send_daily_report({
            "date": datetime.now().date().isoformat(),
            "wallet_start": (
                wallet.state.session_start_value
            ),
            "wallet_end": (
                wallet.state.live_portfolio_value
            ),
            "pnl": (
                wallet.state.live_portfolio_value
                - wallet.state.session_start_value
            ),
            "peak_gain": wallet.state.daily_peak_gain,
        })
        await alerts.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
    logger.info("PolyFarm shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
