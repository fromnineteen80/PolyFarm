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
    write_daily_snapshot,
    get_bot_config
)
from core.wallet import WalletManager
from core.market_loader import MarketLoader, MarketRegistry
from core.pipeline import Pipeline
from core.edge_detector import EdgeDetector
from core.order_manager import OrderManager
from core.position_monitor import PositionMonitor
from core.exception_monitor import ExceptionMonitor
from core.fade_monitor import FadeMonitor
from core.overnight_monitor import OvernightMonitor
from core.alerts import AlertManager
from core.ws_markets import MarketsWebSocket
from core.ws_private import PrivateWebSocket
from dashboard.terminal import TerminalDashboard


async def main():
    logger.info("PolyFarm starting...")
    logger.info(f"Paper mode: {PAPER_MODE}")

    # ── STEP 1: Validate environment ──────────────
    required_vars = [
        "POLYMARKET_KEY_ID",
        "POLYMARKET_SECRET_KEY",
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

    # ── STEP 3: Initialize Polymarket SDK client ──
    client = AsyncPolymarketUS(
        key_id=os.environ["POLYMARKET_KEY_ID"],
        secret_key=os.environ["POLYMARKET_SECRET_KEY"],
    )
    logger.info("Polymarket SDK client initialized")

    # ── STEP 4: Verify connectivity ───────────────
    try:
        result = await client.account.balances()
        balances = result.get("balances", [])
        if balances:
            bp = balances[0].get("buyingPower", 0)
            logger.info(f"Connected. Buying power: ${bp:.2f}")
        else:
            logger.warning("Balance check returned empty")
    except Exception as e:
        logger.critical(f"Cannot connect to Polymarket: {e}")
        raise SystemExit(1)

    # ── STEP 5: Initialize components ─────────────
    alerts = AlertManager()
    await alerts.initialize()

    registry = MarketRegistry()
    wallet = WalletManager(client, PAPER_MODE)
    alerts.wallet = wallet

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
        client, wallet, registry, None,
        order_manager, position_monitor
    )
    fade_monitor = FadeMonitor(
        client, wallet, registry, None,
        order_manager, position_monitor
    )
    overnight_monitor = OvernightMonitor(
        client, wallet, registry, None,
        order_manager, position_monitor
    )

    # ── STEP 6: Set up shared queues ──────────────
    price_queue = asyncio.Queue(maxsize=500)
    trade_queue = asyncio.Queue(maxsize=500)

    # ── STEP 7: Initialize WebSocket handlers ─────
    private_ws = PrivateWebSocket(
        client=client,
        position_monitor=position_monitor,
        wallet=wallet,
    )
    markets_ws = MarketsWebSocket(
        client=client,
        price_queue=price_queue,
        trade_queue=trade_queue,
    )

    # ── STEP 8: Initialize market loader ──────────
    market_loader = MarketLoader(
        client=client,
        registry=registry,
        ws_manager=markets_ws,
    )
    edge_detector = EdgeDetector(
        registry, None, wallet, position_monitor
    )
    edge_detector.order_manager = order_manager
    edge_detector.price_queue = price_queue

    terminal = TerminalDashboard(
        wallet, position_monitor,
        market_loader, registry
    )

    # ── STEP 9: Reconcile orphaned orders ─────────
    try:
        result = await client.orders.list()
        open_orders = result.get("orders", [])
        if open_orders:
            logger.warning(
                f"Found {len(open_orders)} orphaned orders. Cancelling."
            )
            await client.orders.cancel_all()
    except Exception as e:
        logger.error(f"Order reconciliation error: {e}")

    # ── STEP 10: Session initialization ───────────
    await wallet.session_init()
    await position_monitor.load_existing_positions()

    # ── STEP 11: Load markets ─────────────────────
    await market_loader.load_all_markets()

    # ── STEP 12: Initialize pipeline ─────────────
    import data.database as db

    pipeline = None
    odds_key = os.environ.get("ODDS_API_KEY")
    if odds_key:
        pipeline = Pipeline(odds_api_key=odds_key, db=db)
        pipeline.ws_markets = markets_ws
        pipeline.market_registry = registry
        await pipeline.run_startup()
        edge_detector.odds_api = pipeline
        edge_detector.ws_markets = markets_ws
        exception_monitor.mapper = pipeline
        fade_monitor.mapper = pipeline
        overnight_monitor.mapper = pipeline
        logger.info("Pipeline active — registry-based team matching")
    else:
        logger.warning("ODDS_API_KEY not set — running without sharp odds")

    # ── STEP 13: Send session start alert ─────────
    stats = await get_bot_config("paper_trades_completed")
    try:
        paper_progress = int(str(stats or 0).strip('"'))
    except (ValueError, TypeError):
        paper_progress = 0
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

    # ── STEP 13: Start terminal in thread ─────────
    terminal_thread = threading.Thread(
        target=terminal.run,
        daemon=True
    )
    terminal_thread.start()

    # ── STEP 14: Run all async tasks ──────────────
    tasks = [
        asyncio.create_task(private_ws.start(), name="ws_private"),
        asyncio.create_task(markets_ws.start(), name="ws_markets"),
        asyncio.create_task(edge_detector.detection_loop(), name="edge_detection"),
        asyncio.create_task(position_monitor.monitor_loop(), name="position_monitor"),
        asyncio.create_task(wallet.monitor_loop(), name="wallet_recalculate"),
        asyncio.create_task(exception_monitor.monitor_loop(), name="exception_monitor"),
        asyncio.create_task(fade_monitor.monitor_loop(), name="fade_monitor"),
        asyncio.create_task(overnight_monitor.monitor_loop(), name="overnight_monitor"),
        asyncio.create_task(midnight_scheduler(wallet, alerts, market_loader), name="midnight"),
        asyncio.create_task(pre_game_scanner(registry, pipeline, alerts), name="pre_game"),
        asyncio.create_task(game_complete_scanner(registry, position_monitor, alerts), name="game_complete"),
        asyncio.create_task(heartbeat_loop(), name="heartbeat"),
        asyncio.create_task(paper_milestone_checker(alerts), name="paper_milestones"),
    ]

    if pipeline:
        tasks.append(
            asyncio.create_task(pipeline.refresh_loop(), name="pipeline_refresh")
        )

    if PHASE2_ENABLED:
        from phase2.binance_feed import BinanceFeed
        from phase2.crypto_edge_detector import CryptoEdgeDetector
        from phase2.crypto_order_manager import CryptoOrderManager
        await set_bot_config("phase2_enabled", "true")
        existing = await get_bot_config("phase2_activation_date")
        if not existing:
            await set_bot_config(
                "phase2_activation_date",
                datetime.now(timezone.utc).date().isoformat()
            )
        binance = BinanceFeed()
        crypto_detector = CryptoEdgeDetector(
            registry, wallet, position_monitor, binance.price_queue
        )
        crypto_om = CryptoOrderManager(
            client, wallet, alerts, position_monitor
        )
        tasks.extend([
            asyncio.create_task(binance.stream_loop()),
            asyncio.create_task(crypto_detector.detection_loop()),
        ])

    # Handle shutdown signals
    shutdown_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    def handle_shutdown(sig):
        logger.info(f"Shutdown signal: {sig}")
        shutdown_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig, lambda s=sig: handle_shutdown(s)
        )

    try:
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_EXCEPTION
        )
        for task in done:
            if task.exception():
                raise task.exception()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await shutdown(wallet, alerts, order_manager)
        await private_ws.stop()
        await markets_ws.stop()
        if pipeline:
            await pipeline.close()


async def paper_milestone_checker(alerts):
    """Check paper trade count every 5 minutes.
    Fire analysis report at every 50-trade milestone."""
    from data.database import get_paper_trade_stats, get_today_closed_trades
    last_milestone = 0

    while True:
        await asyncio.sleep(300)
        try:
            stats = await get_paper_trade_stats()
            count = stats.get("count", 0)
            if count <= 0:
                continue

            # Check if we crossed a 50-trade milestone
            current_milestone = (count // 50) * 50
            if current_milestone <= last_milestone:
                continue
            if current_milestone == 0:
                continue

            last_milestone = current_milestone

            # Build analysis from all paper trades
            from data.database import db_execute
            from data.database import _supabase
            result = await db_execute(
                lambda: _supabase.table("trades")
                    .select("*")
                    .eq("paper_mode", True)
                    .not_.is_("timestamp_exit", "null")
                    .execute()
            )
            trades = result.data or []
            if not trades:
                continue

            total_pnl = sum(float(t.get("pnl", 0) or 0) for t in trades)
            wins = sum(1 for t in trades if float(t.get("pnl", 0) or 0) > 0)
            win_rate = wins / len(trades) if trades else 0

            # By sport
            by_sport = {}
            for t in trades:
                s = t.get("sport", "unknown") or "unknown"
                if s not in by_sport:
                    by_sport[s] = {"trades": 0, "wins": 0, "pnl": 0}
                by_sport[s]["trades"] += 1
                pnl = float(t.get("pnl", 0) or 0)
                by_sport[s]["pnl"] += pnl
                if pnl > 0:
                    by_sport[s]["wins"] += 1
            for s in by_sport:
                by_sport[s]["win_rate"] = by_sport[s]["wins"] / by_sport[s]["trades"] if by_sport[s]["trades"] > 0 else 0

            # By band
            by_band = {}
            for t in trades:
                b = t.get("band", "?") or "?"
                if b not in by_band:
                    by_band[b] = {"trades": 0, "wins": 0, "pnl": 0}
                by_band[b]["trades"] += 1
                pnl = float(t.get("pnl", 0) or 0)
                by_band[b]["pnl"] += pnl
                if pnl > 0:
                    by_band[b]["wins"] += 1
            for b in by_band:
                by_band[b]["win_rate"] = by_band[b]["wins"] / by_band[b]["trades"] if by_band[b]["trades"] > 0 else 0

            # By direction at entry
            by_direction = {}
            for t in trades:
                d = t.get("price_direction_at_entry", "unknown") or "unknown"
                if d not in by_direction:
                    by_direction[d] = {"trades": 0, "wins": 0}
                by_direction[d]["trades"] += 1
                if float(t.get("pnl", 0) or 0) > 0:
                    by_direction[d]["wins"] += 1
            for d in by_direction:
                by_direction[d]["win_rate"] = by_direction[d]["wins"] / by_direction[d]["trades"] if by_direction[d]["trades"] > 0 else 0

            # By edge bin
            by_edge_bin = {"2-4c": {"trades": 0, "wins": 0}, "4-6c": {"trades": 0, "wins": 0}, "6-8c": {"trades": 0, "wins": 0}, "8-10c": {"trades": 0, "wins": 0}, "10c+": {"trades": 0, "wins": 0}}
            for t in trades:
                edge = float(t.get("edge_at_entry", 0) or t.get("raw_edge_at_entry", 0) or 0)
                ec = edge * 100
                if ec >= 10:
                    b = "10c+"
                elif ec >= 8:
                    b = "8-10c"
                elif ec >= 6:
                    b = "6-8c"
                elif ec >= 4:
                    b = "4-6c"
                else:
                    b = "2-4c"
                by_edge_bin[b]["trades"] += 1
                if float(t.get("pnl", 0) or 0) > 0:
                    by_edge_bin[b]["wins"] += 1
            for b in by_edge_bin:
                by_edge_bin[b]["win_rate"] = by_edge_bin[b]["wins"] / by_edge_bin[b]["trades"] if by_edge_bin[b]["trades"] > 0 else 0

            # Hold times
            winner_holds = [int(t.get("hold_duration_seconds", 0) or 0) / 60 for t in trades if float(t.get("pnl", 0) or 0) > 0]
            loser_holds = [int(t.get("hold_duration_seconds", 0) or 0) / 60 for t in trades if float(t.get("pnl", 0) or 0) <= 0]
            avg_hold_winners = sum(winner_holds) / len(winner_holds) if winner_holds else 0
            avg_hold_losers = sum(loser_holds) / len(loser_holds) if loser_holds else 0

            # Generate recommendations
            recommendations = []
            for s, data in by_sport.items():
                if data["trades"] >= 5 and data["win_rate"] < 0.60:
                    recommendations.append(f"{s}: {data['win_rate']:.0%} win rate is below 60%. Consider reducing position size or adding filters.")
            for b, data in by_band.items():
                if data["trades"] >= 5 and data["win_rate"] < 0.60:
                    recommendations.append(f"Band {b}: {data['win_rate']:.0%} win rate. Edge threshold may need increasing.")
            for d, data in by_direction.items():
                if d == "rising" and data["trades"] >= 3 and data["win_rate"] < 0.50:
                    recommendations.append(f"Rising price entries have {data['win_rate']:.0%} WR. Direction modifier may need tightening.")
            if avg_hold_losers > 0 and avg_hold_losers > avg_hold_winners * 2:
                recommendations.append(f"Losers held {avg_hold_losers:.0f}m vs winners {avg_hold_winners:.0f}m. Consider tighter timeout.")
            if not recommendations:
                recommendations.append("No specific issues detected. Continue accumulating data.")

            go_live_ready = count >= 300 and win_rate >= 0.70

            analysis = {
                "win_rate": win_rate,
                "total_pnl": total_pnl,
                "avg_pnl": total_pnl / len(trades) if trades else 0,
                "by_sport": by_sport,
                "by_band": by_band,
                "by_direction": by_direction,
                "by_edge_bin": by_edge_bin,
                "avg_hold_winners": avg_hold_winners,
                "avg_hold_losers": avg_hold_losers,
                "recommendations": recommendations,
                "go_live_ready": go_live_ready,
            }

            await alerts.send_paper_milestone(current_milestone, analysis)
            logger.info(f"Paper milestone report sent: {current_milestone} trades, {win_rate:.0%} WR")

        except Exception as e:
            logger.error(f"Paper milestone checker error: {e}")


async def heartbeat_loop():
    """Write heartbeat timestamp every 60 seconds."""
    while True:
        try:
            await set_bot_config(
                "last_heartbeat",
                datetime.now(timezone.utc).isoformat()
            )
        except Exception:
            pass
        await asyncio.sleep(60)


async def pre_game_scanner(registry, mapper, alerts):
    """Scan for upcoming games 90 min before start."""
    from config import (
        DOMINANT_TEAMS, FADE_TEAMS,
        BAND_A_MIN_PRICE, BAND_A_MIN_EDGE,
        BAND_B_MIN_PRICE, BAND_B_MIN_EDGE,
        BAND_C_MIN_PRICE, BAND_C_MIN_EDGE,
        FAVORITES_FLOOR,
    )
    alerted_slugs = set()

    while True:
        try:
            now = datetime.now(timezone.utc)
            window_start = now + timedelta(minutes=30)
            window_end = now + timedelta(minutes=90)
            markets = await registry.all_markets()

            for market in markets:
                if market.slug in alerted_slugs:
                    continue
                if market.is_live or market.is_finished:
                    continue
                try:
                    start = datetime.fromisoformat(
                        market.game_start_time.replace("Z", "+00:00")
                    )
                    if not (window_start <= start <= window_end):
                        continue
                except Exception:
                    continue

                signals = {}
                sharp = mapper.get_fair_prob(market.slug, "home") if mapper else None
                if sharp and market.yes_price >= FAVORITES_FLOOR:
                    gap = sharp - market.yes_price
                    band = None
                    if market.yes_price >= BAND_A_MIN_PRICE and gap >= BAND_A_MIN_EDGE:
                        band = "A"
                    elif market.yes_price >= BAND_B_MIN_PRICE and gap >= BAND_B_MIN_EDGE:
                        band = "B"
                    elif market.yes_price >= BAND_C_MIN_PRICE and gap >= BAND_C_MIN_EDGE:
                        band = "C"
                    if band:
                        signals["oracle_arb"] = {
                            "poly_price": market.yes_price,
                            "sharp_prob": sharp,
                            "gap": gap,
                            "band": band,
                            "line_movement": None,
                        }

                home_l = market.home_team.lower()
                away_l = market.away_team.lower()
                for tn, tc in DOMINANT_TEAMS.items():
                    if tn.lower() in home_l or tn.lower() in away_l:
                        signals["dominant"] = {"team": tn}
                        break
                for tn, tc in FADE_TEAMS.items():
                    if tn.lower() in home_l or tn.lower() in away_l:
                        signals["fade"] = {"team": tn}
                        break

                if signals:
                    await alerts.send_pre_game_intel(market, signals)
                    alerted_slugs.add(market.slug)

        except Exception as e:
            logger.error(f"Pre-game scanner error: {e}")

        await asyncio.sleep(60)


async def game_complete_scanner(registry, position_monitor, alerts):
    """Check for finished games and fire summary."""
    from data.database import get_closed_trades_by_game
    alerted_games = set()

    while True:
        try:
            markets = await registry.all_markets()
            for market in markets:
                if not market.is_finished:
                    continue
                if market.slug in alerted_games:
                    continue
                trades = await get_closed_trades_by_game(market.slug)
                if trades:
                    await alerts.send_game_summary(
                        game_slug=market.slug,
                        trades=trades,
                        final_score=market.current_score,
                        teams=f"{market.home_team} vs {market.away_team}",
                        sport=market.sport,
                    )
                alerted_games.add(market.slug)
        except Exception as e:
            logger.error(f"Game complete scanner error: {e}")
        await asyncio.sleep(30)


async def midnight_scheduler(wallet, alerts, market_loader):
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
    while True:
        now = datetime.now(ET)
        # Reset at 11:59 PM Eastern
        target = now.replace(hour=23, minute=59, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        seconds_until = (target - now).total_seconds()
        await asyncio.sleep(seconds_until)
        await write_end_of_day(wallet, alerts)
        await wallet.reset_daily()
        logger.info("Daily reset complete — ready for tomorrow")
        await asyncio.sleep(70)


async def write_end_of_day(wallet, alerts):
    from datetime import date
    from data.database import get_today_closed_trades, get_paper_trade_stats
    today = date.today().isoformat()
    wallet_value = wallet.state.live_portfolio_value

    first_date = await get_bot_config("first_live_trade_date")
    first_value = await get_bot_config("first_live_wallet_value")
    proj_1pct = None
    proj_15pct = None
    proj_2pct = None
    if first_date and first_value:
        try:
            start = datetime.fromisoformat(first_date)
            start_val = float(first_value)
            days = (datetime.now() - start).days
            proj_1pct = start_val * (1.01 ** days)
            proj_15pct = start_val * (1.015 ** days)
            proj_2pct = start_val * (1.02 ** days)
        except Exception:
            pass

    await write_daily_snapshot({
        "date": today,
        "wallet_value": wallet_value,
        "floor_value": wallet.state.floor_value,
        "session_pnl": wallet_value - wallet.state.session_start_value,
        "cumulative_pnl": wallet_value - float(
            await get_bot_config("first_live_wallet_value") or wallet_value
        ),
        "cumulative_pnl_pct": 0,
        "trades_today": 0,
        "win_rate_today": 0,
        "projected_1pct": proj_1pct,
        "projected_15pct": proj_15pct,
        "projected_2pct": proj_2pct,
        "paper_mode": PAPER_MODE,
    })

    closed = await get_today_closed_trades(today, PAPER_MODE)
    strats = {}
    for name in ("oracle_arb", "exception", "fade", "overnight"):
        st = [t for t in closed if t.get("position_type") == name or (name == "oracle_arb" and t.get("position_type") in ("normal", "oracle_arb"))]
        wins = sum(1 for t in st if float(t.get("pnl", 0) or 0) > 0)
        total_pnl = sum(float(t.get("pnl", 0) or 0) for t in st)
        strats[name] = {"trades": len(st), "win_rate": wins / len(st) * 100 if st else 0, "pnl": total_pnl}

    sports = {}
    for t in closed:
        sport = t.get("sport", "unknown")
        if sport not in sports:
            sports[sport] = {"trades": 0, "pnl": 0}
        sports[sport]["trades"] += 1
        sports[sport]["pnl"] += float(t.get("pnl", 0) or 0)

    total_fees = sum(float(t.get("taker_fee_paid", 0) or 0) for t in closed)
    total_rebates = sum(float(t.get("maker_rebate_earned", 0) or 0) for t in closed)

    alltime = None
    if first_date and first_value:
        try:
            alltime = {
                "original_capital": float(first_value),
                "current_value": wallet_value,
                "days_running": max((datetime.now() - datetime.fromisoformat(first_date)).days, 1),
            }
        except Exception:
            pass

    paper_progress = None
    if PAPER_MODE:
        ps = await get_paper_trade_stats()
        paper_progress = {
            "completed": ps["count"],
            "win_rate": ps["win_rate"],
            "trades_per_day": max(len([t for t in closed if t.get("paper_mode")]), 1),
        }

    await alerts.send_daily_report({
        "date": today,
        "wallet_start": wallet.state.session_start_value,
        "wallet_end": wallet_value,
        "pnl": wallet_value - wallet.state.session_start_value,
        "peak_gain": wallet.state.daily_peak_gain,
        "strategies": strats,
        "sports": sports,
        "total_fees": total_fees,
        "total_rebates": total_rebates,
        "alltime": alltime,
        "paper_progress": paper_progress,
    })


async def shutdown(wallet, alerts, order_manager):
    logger.info("Shutting down PolyFarm...")
    try:
        if not PAPER_MODE:
            await order_manager.drain_all_positions("SHUTDOWN")
        await alerts.send_daily_report({
            "date": datetime.now().date().isoformat(),
            "wallet_start": wallet.state.session_start_value,
            "wallet_end": wallet.state.live_portfolio_value,
            "pnl": wallet.state.live_portfolio_value - wallet.state.session_start_value,
            "peak_gain": wallet.state.daily_peak_gain,
        })
        await alerts.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
    logger.info("PolyFarm shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
