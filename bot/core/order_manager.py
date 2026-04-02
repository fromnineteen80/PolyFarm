import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
from config import (
    PAPER_MODE,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
    REPRICE_EXIT_PCT,
    PROFIT_LOCK_BAND_A, PROFIT_LOCK_BAND_B,
    PROFIT_LOCK_BAND_C, PROFIT_LOCK_OVERNIGHT,
    TRAILING_STOP_ACTIVATE, TRAILING_STOP_FLOOR,
    TRAILING_STOP_FLOOR_PROTECTION,
    REPRICE_TIMEOUT_MINUTES,
    EXCEPTION_REPRICE_PCT, EXCEPTION_PROFIT_LOCK,
    EXCEPTION_TRAILING_ACTIVATE,
    EXCEPTION_TRAILING_FLOOR,
    EXCEPTION_STOP_LOSS, EXCEPTION_TIMEOUT_MINUTES,
    FADE_REPRICE_PCT, FADE_PROFIT_LOCK,
    FADE_TRAILING_ACTIVATE, FADE_TRAILING_FLOOR,
    FADE_STOP_LOSS, FADE_TIMEOUT_MINUTES,
)
from data.database import (
    insert_trade, update_trade, log_incentive,
    set_bot_config, get_bot_config,
    log_system_event
)

logger = logging.getLogger("polyfarm.orders")

@dataclass
class OpenPosition:
    trade_id: int
    slug: str
    sport: str
    teams: str
    band: str
    strategy: str       # oracle_arb|exception|fade
    position_type: str  # normal|overnight|add|
                        # exception|fade
    entry_price: float
    shares: int
    exit_target: float
    original_edge: float
    entry_time: datetime
    sell_order_id: Optional[str]
    peak_gain: float = 0.0
    hold_to_resolution: bool = False
    fade_team: Optional[str] = None
    game_id: Optional[str] = None
    paper_mode: bool = True

class OrderManager:

    def __init__(self, client, wallet, alerts,
                 position_monitor):
        self.client = client
        self.wallet = wallet
        self.alerts = alerts
        self.pm = position_monitor
        self.pipeline = None  # set by main.py for sharp odds check

    # ─────────────────────────────────────────────
    # ENTRY
    # ─────────────────────────────────────────────

    async def enter_position(self,
                              signal,
                              strategy: str = "oracle_arb",
                              position_type: str = "normal",
                              fade_team: str = None):
        """
        Execute entry for any strategy.
        signal: EdgeSignal or similar dataclass
        """
        if PAPER_MODE:
            await self._paper_entry(
                signal, strategy,
                position_type, fade_team
            )
        else:
            await self._live_entry(
                signal, strategy,
                position_type, fade_team
            )

    async def _paper_entry(self, signal, strategy,
                            position_type, fade_team):
        try:
            from core.market_loader import parse_bbo
            bbo = await self.client.markets.bbo(
                signal.slug
            )
            bid, ask, cur = parse_bbo(bbo)
            if bid == 0:
                bid = signal.poly_price
            if ask == 0:
                ask = signal.poly_price
            mid = (bid + ask) / 2
            fill_price = mid

            trade_data = self._build_trade_record(
                signal, fill_price, strategy,
                position_type, fade_team,
                paper_mode=True
            )
            result = await insert_trade(trade_data)
            trade_id = result.get("id", 0)

            position = OpenPosition(
                trade_id=trade_id,
                slug=signal.slug,
                sport=signal.sport,
                teams=signal.teams,
                band=signal.band,
                strategy=strategy,
                position_type=position_type,
                entry_price=fill_price,
                shares=signal.shares,
                exit_target=signal.exit_target,
                original_edge=signal.raw_edge,
                entry_time=datetime.now(timezone.utc),
                sell_order_id=None,
                fade_team=fade_team,
                game_id=getattr(
                    signal, "game_id", None
                ),
                paper_mode=True,
            )
            await self.pm.add_position(
                signal.slug, position
            )

            # Update paper stats
            stats = await self._get_paper_stats()
            await set_bot_config(
                "paper_trades_completed",
                str(stats["count"])
            )
            await set_bot_config(
                "paper_win_rate",
                str(stats["win_rate"])
            )

            await self.alerts.send_entry(
                signal, fill_price, strategy,
                paper=True
            )
            logger.info(
                f"[PAPER] Entry {signal.slug} "
                f"at {fill_price:.4f}"
            )

        except Exception as e:
            logger.error(f"Paper entry error: {e}")

    async def _live_entry(self, signal, strategy,
                           position_type, fade_team):
        try:
            # Preview first
            try:
                await self.client.orders.preview_order({
                    "marketSlug": signal.slug,
                    "intent": "ORDER_INTENT_BUY_LONG",
                    "type": "ORDER_TYPE_LIMIT",
                    "price": {
                        "value": str(
                            round(signal.poly_price, 4)
                        ),
                        "currency": "USD"
                    },
                    "quantity": signal.shares,
                    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL"
                })
            except Exception as e:
                logger.warning(
                    f"Order preview failed: {e}. "
                    f"Proceeding with entry."
                )

            # Place entry order
            order = await self.client.orders.create({
                "marketSlug": signal.slug,
                "intent": "ORDER_INTENT_BUY_LONG",
                "type": "ORDER_TYPE_LIMIT",
                "price": {
                    "value": str(
                        round(signal.poly_price, 4)
                    ),
                    "currency": "USD"
                },
                "quantity": signal.shares,
                "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL"
            })
            order_id = order.get("id")

            # Wait for fill via private WS event
            # fill_event set by position_monitor
            # when WS ORDER fill received
            fill_event = asyncio.Event()
            self.pm.register_pending_fill(
                order_id, fill_event
            )
            try:
                await asyncio.wait_for(
                    fill_event.wait(), timeout=30
                )
            except asyncio.TimeoutError:
                await self._cancel_order(order_id)
                logger.info(
                    f"Entry timeout: {signal.slug}"
                )
                return

            fill_price = self.pm.get_fill_price(
                order_id
            ) or signal.poly_price

            # Place GTC sell at exit target
            reprice_pct = self._get_reprice_pct(strategy)
            exit_target = fill_price + (
                signal.raw_edge * reprice_pct
            )
            sell = await self.client.orders.create({
                "marketSlug": signal.slug,
                "intent": "ORDER_INTENT_SELL_LONG",
                "type": "ORDER_TYPE_LIMIT",
                "price": {
                    "value": str(round(exit_target, 4)),
                    "currency": "USD"
                },
                "quantity": signal.shares,
                "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL"
            })
            sell_order_id = sell.get("id")

            trade_data = self._build_trade_record(
                signal, fill_price, strategy,
                position_type, fade_team,
                paper_mode=False
            )
            result = await insert_trade(trade_data)
            trade_id = result.get("id", 0)

            position = OpenPosition(
                trade_id=trade_id,
                slug=signal.slug,
                sport=signal.sport,
                teams=signal.teams,
                band=signal.band,
                strategy=strategy,
                position_type=position_type,
                entry_price=fill_price,
                shares=signal.shares,
                exit_target=round(exit_target, 4),
                original_edge=signal.raw_edge,
                entry_time=datetime.now(timezone.utc),
                sell_order_id=sell_order_id,
                fade_team=fade_team,
                game_id=getattr(
                    signal, "game_id", None
                ),
                paper_mode=False,
            )
            await self.pm.add_position(
                signal.slug, position
            )

            # Log incentive rewards
            await log_incentive({
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "order_id": sell_order_id,
                "market_slug": signal.slug,
                "order_type": "entry_taker",
                "fee_or_rebate": -signal.taker_fee,
                "incentive_type": "volume",
                "paper_mode": False,
            })
            await log_incentive({
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "order_id": sell_order_id,
                "market_slug": signal.slug,
                "order_type": "exit_maker_resting",
                "fee_or_rebate": 0,
                "incentive_type": "liquidity",
                "paper_mode": False,
            })

            # Record first live trade
            first = await get_bot_config(
                "first_live_trade_date"
            )
            if not first:
                await set_bot_config(
                    "first_live_trade_date",
                    datetime.now(
                        timezone.utc
                    ).date().isoformat()
                )
                await set_bot_config(
                    "first_live_wallet_value",
                    str(
                        self.wallet.state
                        .live_portfolio_value
                    )
                )
                await set_bot_config(
                    "current_mode", "live"
                )

            await self.alerts.send_entry(
                signal, fill_price, strategy,
                paper=False
            )
            logger.info(
                f"[LIVE] Entry {signal.slug} "
                f"at {fill_price:.4f}"
            )

        except Exception as e:
            logger.error(f"Live entry error: {e}")
            await log_system_event(
                "entry_error",
                str(e),
                {"slug": signal.slug}
            )

    def _get_reprice_pct(self, strategy: str) -> float:
        if strategy == "exception":
            return EXCEPTION_REPRICE_PCT
        if strategy == "fade":
            return FADE_REPRICE_PCT
        return REPRICE_EXIT_PCT

    def _get_profit_lock_threshold(
        self,
        band: str,
        strategy: str,
        profit_mode: str
    ) -> float:
        if strategy == "exception":
            return EXCEPTION_PROFIT_LOCK
        if strategy == "fade":
            return FADE_PROFIT_LOCK
        # Oracle arb — apply mode multiplier
        base = {
            "A": PROFIT_LOCK_BAND_A,
            "B": PROFIT_LOCK_BAND_B,
            "C": PROFIT_LOCK_BAND_C,
            "overnight": PROFIT_LOCK_OVERNIGHT,
        }.get(band, PROFIT_LOCK_BAND_C)

        if profit_mode == "PROTECTION":
            return base * 0.50
        return base

    def _get_trailing_activate(
        self,
        strategy: str
    ) -> float:
        if strategy == "exception":
            return EXCEPTION_TRAILING_ACTIVATE
        if strategy == "fade":
            return FADE_TRAILING_ACTIVATE
        return TRAILING_STOP_ACTIVATE

    def _get_trailing_floor(
        self,
        strategy: str,
        profit_mode: str
    ) -> float:
        if strategy in ("exception", "fade"):
            return EXCEPTION_TRAILING_FLOOR
        if profit_mode == "PROTECTION":
            return TRAILING_STOP_FLOOR_PROTECTION
        return TRAILING_STOP_FLOOR

    def _get_stop_loss(self,
                        strategy: str
                        ) -> Optional[float]:
        if strategy == "exception":
            return EXCEPTION_STOP_LOSS
        if strategy == "fade":
            return FADE_STOP_LOSS
        return None  # No stop loss on oracle arb

    def _get_timeout_minutes(self,
                              strategy: str) -> int:
        if strategy == "exception":
            return EXCEPTION_TIMEOUT_MINUTES
        if strategy == "fade":
            return FADE_TIMEOUT_MINUTES
        return REPRICE_TIMEOUT_MINUTES

    # ─────────────────────────────────────────────
    # EXIT TRIGGERS
    # ─────────────────────────────────────────────

    async def check_position_exits(
        self,
        position: OpenPosition,
        current_bid: float,
        game_state: Optional[dict] = None
    ):
        """
        Runs every 30 seconds per position.
        Checks all exit triggers in priority order.
        First trigger to fire wins.
        """
        slug = position.slug
        strategy = position.strategy
        profit_mode = self.wallet.state.profit_mode

        # Current gain percentage
        current_gain = (
            (current_bid - position.entry_price)
            / position.entry_price
        )

        # Update peak gain
        if current_gain > position.peak_gain:
            position.peak_gain = current_gain
            await self.pm.update_position(
                slug, {"peak_gain": current_gain}
            )

        # ── TRIGGER 1: Reprice Target ────────────
        # Handled by WS private ORDER fill event
        # position_monitor calls on_reprice_fill()
        # when GTC sell order fills automatically.
        # Nothing to check here — it fires passively.

        # ── TRIGGER 2: Profit Lock ───────────────
        lock_threshold = self._get_profit_lock_threshold(
            position.band, strategy, profit_mode
        )
        if current_gain >= lock_threshold:
            await self._ioc_exit(
                position, current_bid,
                "profit_lock"
            )
            return

        # ── TRIGGER 3: Trailing Stop ─────────────
        trail_activate = self._get_trailing_activate(
            strategy
        )
        trail_floor_pct = self._get_trailing_floor(
            strategy, profit_mode
        )
        if position.peak_gain >= trail_activate:
            trailing_floor = (
                position.peak_gain * trail_floor_pct
            )
            if current_gain < trailing_floor:
                await self._ioc_exit(
                    position, current_bid,
                    "trailing_stop"
                )
                return

        # ── TRIGGER 4: Smart Stop Loss ───────────
        # Hold as long as sharp odds > our entry price.
        # We're betting on the outcome, not the journey.
        # A 73% team down 10 points in Q2 still wins 73%
        # of the time. Only exit when bookmakers say
        # the team is less likely to win than what we paid.
        stop_loss = self._get_stop_loss(strategy)
        if stop_loss is not None:
            if current_gain <= stop_loss:
                sharp_still_supports = False
                if self.pipeline and self.pipeline.is_matched(slug):
                    sharp_prob = self.pipeline.get_fair_prob(slug, "home")
                    if sharp_prob and sharp_prob > position.entry_price:
                        # Bookmakers still say this team wins
                        # more often than what we paid. Hold.
                        sharp_still_supports = True
                if not sharp_still_supports:
                    await self._ioc_exit(
                        position, current_bid,
                        f"{strategy}_stop_loss"
                    )
                    await self.alerts.send_stop_loss(
                        position, current_gain, strategy
                    )
                    return

        # ── TRIGGER 4B: Fade Deficit Closed ──────
        if strategy == "fade" and game_state:
            # Fade team has equalized — exit
            score = game_state.get("score", "")
            if self._is_game_tied(score):
                await self._ioc_exit(
                    position, current_bid,
                    "fade_deficit_closed"
                )
                await self.alerts.send_fade_broken(
                    position
                )
                return

        # ── TRIGGER 5: Timeout ───────────────────
        if not position.hold_to_resolution:
            timeout_min = self._get_timeout_minutes(
                strategy
            )
            elapsed = (
                datetime.now(timezone.utc)
                - position.entry_time
            ).total_seconds() / 60

            if elapsed >= timeout_min:
                await self._handle_timeout(
                    position, current_bid,
                    game_state
                )
                return

        # ── TRIGGER 6: Pre-Resolution ────────────
        if game_state and not position.hold_to_resolution:
            if strategy != "exception":
                # Exception trades never hold to res
                await self._check_pre_resolution(
                    position, current_bid, game_state
                )

    async def _handle_timeout(
        self,
        position: OpenPosition,
        current_bid: float,
        game_state: Optional[dict]
    ):
        """
        Timeout exit. Re-evaluate edge first.
        If edge still meaningful: modify GTC target.
        Otherwise: IOC exit.
        """
        # Attempt edge recalculation
        # Simplified: check if still above 2% of original
        try:
            from core.market_loader import parse_bbo
            bbo = await self.client.markets.bbo(
                position.slug
            )
            bid_v, current_ask, cur_v = parse_bbo(bbo)
            if current_ask == 0:
                current_ask = current_bid
            # Rough current edge estimate
            current_edge = (
                current_ask - position.entry_price
            )
            original_edge = position.original_edge

            if current_edge > original_edge * 0.02 and \
               position.sell_order_id:
                # Still has some edge — modify target
                new_target = current_ask + (
                    current_edge * self._get_reprice_pct(
                        position.strategy
                    )
                )
                await self._modify_order(
                    position.sell_order_id,
                    round(new_target, 4)
                )
                # Reset timeout by updating entry_time
                position.entry_time = (
                    datetime.now(timezone.utc)
                )
                await self.pm.update_position(
                    position.slug,
                    {"entry_time": position.entry_time}
                )
                return

        except Exception as e:
            logger.debug(f"Timeout edge check: {e}")

        await self._ioc_exit(
            position, current_bid, "timeout"
        )

    async def _check_pre_resolution(
        self,
        position: OpenPosition,
        current_bid: float,
        game_state: dict
    ):
        """
        Apply sport-specific hold logic near game end.
        If hold conditions not met: IOC exit.
        """
        sport = position.sport
        time_rem = game_state.get(
            "time_remaining_seconds", 9999
        )
        inning = game_state.get("inning", 0)
        period = game_state.get("period", 0)
        minute = game_state.get("game_minute", 0)
        is_overtime = game_state.get(
            "is_overtime", False
        )

        should_hold = False

        # Hold if we're on the winning side late in the game.
        # current_bid > 0.55 means our team is favored to win.
        # Only exit if current_bid < 0.40 (we're clearly losing).

        if sport in ("basketball_nba",
                     "basketball_ncaab"):
            # 4th quarter, last 2 minutes
            if time_rem <= 120 and \
               current_bid > 0.55:
                should_hold = True

        elif sport in ("americanfootball_nfl",
                       "americanfootball_ncaaf"):
            # 4th quarter, last 4 minutes
            if time_rem <= 240 and \
               current_bid > 0.55:
                should_hold = True

        elif sport == "baseball_mlb":
            # 8th inning or later
            if inning >= 8 and current_bid > 0.55:
                should_hold = True

        elif sport == "icehockey_nhl":
            # 3rd period, last 5 minutes
            if time_rem <= 300 and \
               not is_overtime and \
               current_bid > 0.55:
                should_hold = True

        elif sport in ("soccer_epl", "soccer_usa_mls",
                       "soccer_mls",
                       "soccer_uefa_champs_league",
                       "soccer_spain_la_liga",
                       "soccer_germany_bundesliga",
                       "soccer_italy_serie_a"):
            # 80th minute or later
            if minute >= 80 and current_bid > 0.55:
                should_hold = True

        if should_hold:
            # We're winning late in the game — hold to settlement
            position.hold_to_resolution = True
            if position.sell_order_id:
                await self._cancel_order(
                    position.sell_order_id
                )
            await self.pm.update_position(
                position.slug,
                {"hold_to_resolution": True}
            )
            return

        # We're losing late in the game — exit
        await self._ioc_exit(
            position, current_bid, "pre_resolution"
        )

    async def _ioc_exit(self,
                         position: OpenPosition,
                         current_bid: float,
                         exit_type: str):
        """Execute immediate IOC exit."""
        if PAPER_MODE:
            await self._paper_exit(
                position, current_bid, exit_type
            )
            return

        try:
            # Cancel pending GTC sell if exists
            if position.sell_order_id:
                await self._cancel_order(
                    position.sell_order_id
                )

            # Close position via IOC
            # Use close_position_order if available
            # Fall back to SELL_LONG IOC if not
            try:
                await self.client.orders\
                    .close_position_order({
                        "marketSlug": position.slug,
                        "type": "ORDER_TYPE_LIMIT",
                        "tif": "TIME_IN_FORCE_IOC",
                        "price": {
                            "value": str(
                                round(current_bid, 4)
                            ),
                            "currency": "USD"
                        }
                    })
            except AttributeError:
                await self.client.orders.create({
                    "marketSlug": position.slug,
                    "intent": "ORDER_INTENT_SELL_LONG",
                    "type": "ORDER_TYPE_LIMIT",
                    "tif": "TIME_IN_FORCE_IOC",
                    "price": {
                        "value": str(
                            round(current_bid, 4)
                        ),
                        "currency": "USD"
                    },
                    "quantity": position.shares,
                })

            await self._record_exit(
                position, current_bid, exit_type
            )

        except Exception as e:
            logger.error(
                f"IOC exit error {position.slug}: {e}"
            )

    async def _paper_exit(self,
                           position: OpenPosition,
                           exit_price: float,
                           exit_type: str):
        """Simulate exit in paper mode."""
        await self._record_exit(
            position, exit_price, exit_type
        )

    async def _record_exit(self,
                            position: OpenPosition,
                            exit_price: float,
                            exit_type: str):
        """Record exit to database and send alert."""
        gross_pnl = (
            (exit_price - position.entry_price)
            * position.shares
        )
        # Calculate fees
        taker_fee = 0.0
        maker_rebate = 0.0
        if exit_type in (
            "reprice", "exception_reprice",
            "fade_reprice"
        ):
            # Maker rebate on GTC fill
            notional = position.shares * (
                1 - exit_price
            )
            maker_rebate = notional * MAKER_REBATE_RATE
        else:
            # Taker fee on IOC exit
            notional = position.shares * (
                1 - exit_price
            )
            taker_fee = notional * TAKER_FEE_RATE

        net_pnl = gross_pnl - taker_fee + maker_rebate
        duration = int((
            datetime.now(timezone.utc)
            - position.entry_time
        ).total_seconds())

        exit_utc = datetime.now(timezone.utc)
        await update_trade(position.trade_id, {
            "timestamp_exit": exit_utc.isoformat(),
            "timestamp_exit_et": exit_utc.astimezone(ET).isoformat(),
            "trade_bucket": "historical",
            "exit_price": exit_price,
            "exit_type": exit_type,
            "pnl": net_pnl,
            "pnl_pct": net_pnl / (
                position.entry_price * position.shares
            ) if position.shares > 0 else 0,
            "wallet_at_exit": (
                self.wallet.state.live_portfolio_value
            ),
            "hold_duration_seconds": duration,
            "maker_rebate_earned": maker_rebate,
            "taker_fee_paid": taker_fee,
        })

        self.wallet.remove_position(position.slug, net_pnl)
        await self.pm.remove_position(position.slug)

        await self.alerts.send_exit(
            position, exit_price, exit_type,
            net_pnl, duration,
            self.wallet.state.live_portfolio_value
        )
        logger.info(
            f"Exit {position.slug} via {exit_type} "
            f"at {exit_price:.4f} "
            f"P&L: {net_pnl:+.4f}"
        )

    async def on_reprice_fill(self,
                               slug: str,
                               fill_price: float,
                               order_id: str):
        """
        Called by position_monitor when a GTC sell
        order fills (Trigger 1 — passive reprice).
        """
        position = await self.pm.get_position(slug)
        if not position:
            return
        strategy = position.strategy
        exit_type = f"{strategy}_reprice" \
            if strategy != "oracle_arb" \
            else "reprice"
        await self._record_exit(
            position, fill_price, exit_type
        )
        # Log fill incentive
        if not PAPER_MODE:
            notional = position.shares * (
                1 - fill_price
            )
            rebate = notional * MAKER_REBATE_RATE
            await log_incentive({
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "order_id": order_id,
                "market_slug": slug,
                "order_type": "exit_maker_filled",
                "fee_or_rebate": rebate,
                "incentive_type": "fill",
                "paper_mode": False,
            })

    async def drain_all_positions(self, reason: str):
        """
        LOCK AND DRAIN — called when session locks.
        Places limit sell at bid+0.01 for each position.
        Falls back to IOC after 3 minutes.
        """
        positions = list(
            self.pm.get_all_positions().values()
        )
        logger.info(
            f"Drain all positions: {reason} "
            f"({len(positions)} positions)"
        )
        for position in positions:
            try:
                from core.market_loader import parse_bbo
                bbo = await self.client.markets.bbo(
                    position.slug
                )
                bid, _ask, _cur = parse_bbo(bbo)
                if bid == 0:
                    bid = position.entry_price
                drain_price = round(bid + 0.01, 4)

                if position.sell_order_id:
                    await self._modify_order(
                        position.sell_order_id,
                        drain_price
                    )
                else:
                    if not PAPER_MODE:
                        await self.client.orders.create({
                            "marketSlug": position.slug,
                            "intent":
                                "ORDER_INTENT_SELL_LONG",
                            "type": "ORDER_TYPE_LIMIT",
                            "price": {
                                "value": str(
                                    drain_price
                                ),
                                "currency": "USD"
                            },
                            "quantity": position.shares,
                            "tif":
                                "TIME_IN_FORCE_GOOD_TILL_CANCEL"
                        })
            except Exception as e:
                logger.error(
                    f"Drain error {position.slug}: {e}"
                )

        # Wait 3 minutes then IOC anything remaining
        await asyncio.sleep(180)
        remaining = list(
            self.pm.get_all_positions().values()
        )
        for position in remaining:
            try:
                from core.market_loader import parse_bbo
                bbo = await self.client.markets.bbo(
                    position.slug
                )
                bid, _ask, _cur = parse_bbo(bbo)
                if bid == 0:
                    bid = position.entry_price
                await self._ioc_exit(
                    position, bid, f"drain_{reason}"
                )
            except Exception as e:
                logger.error(
                    f"Force drain error "
                    f"{position.slug}: {e}"
                )

    async def emergency_exit_all(self, reason: str):
        """
        Emergency IOC exit all positions immediately.
        Used for DAILY HALT and FLOOR BREACH.
        """
        if not PAPER_MODE:
            try:
                await self.client.orders.cancel_all()
            except Exception as e:
                logger.error(
                    f"Cancel all orders error: {e}"
                )

        positions = list(
            self.pm.get_all_positions().values()
        )
        # Sort by lowest value first
        positions.sort(
            key=lambda p: (
                self.wallet._position_values.get(
                    p.slug, {}
                ).get("value", 9999)
            )
        )
        for position in positions:
            try:
                bid = (
                    self.wallet._position_values.get(
                        position.slug, {}
                    ).get(
                        "current_bid",
                        position.entry_price
                    )
                )
                await self._ioc_exit(
                    position, bid,
                    f"emergency_{reason}"
                )
            except Exception as e:
                logger.error(
                    f"Emergency exit error "
                    f"{position.slug}: {e}"
                )

    async def _modify_order(self,
                             order_id: str,
                             new_price: float):
        if PAPER_MODE:
            return
        try:
            await self.client.orders.modify_order(
                order_id,
                {"price": {
                    "value": str(new_price),
                    "currency": "USD"
                }}
            )
        except AttributeError:
            # modify_order may not exist in SDK
            # Cancel and replace
            await self._cancel_order(order_id)

    async def _cancel_order(self, order_id: str):
        if PAPER_MODE:
            return
        try:
            await self.client.orders.cancel_order(
                order_id
            )
        except Exception as e:
            logger.debug(f"Cancel order error: {e}")

    def _build_trade_record(self,
                             signal,
                             fill_price: float,
                             strategy: str,
                             position_type: str,
                             fade_team: Optional[str],
                             paper_mode: bool) -> dict:
        now_utc = datetime.now(timezone.utc)
        return {
            "timestamp_entry": now_utc.isoformat(),
            "timestamp_entry_et": now_utc.astimezone(ET).isoformat(),
            "trade_bucket": "live",
            "market_slug": signal.slug,
            "sport": signal.sport,
            "teams": signal.teams,
            "market_type": signal.market_type,
            "band": signal.band,
            "position_type": position_type,
            "entry_price": fill_price,
            "sharp_prob_at_entry": signal.sharp_prob,
            "raw_edge_at_entry": signal.raw_edge,
            "net_edge_at_entry": signal.net_edge_pct,
            "confidence_score": signal.confidence,
            "position_size_usd": signal.position_usd,
            "shares": signal.shares,
            "taker_fee_paid": signal.taker_fee,
            "paper_mode": paper_mode,
            "phase": "phase1",
            "is_live_game": signal.is_live,
            "profit_mode_at_entry": (
                self.wallet.state.profit_mode
            ),
            "loss_mode_at_entry": (
                self.wallet.state.loss_mode
            ),
            "fade_team": fade_team,
            "game_id": getattr(signal, "game_id", None),
            "price_direction_at_entry": getattr(signal, "price_direction", "stable"),
            "price_velocity_at_entry": getattr(signal, "price_velocity", 0.0),
            "net_buy_pressure_at_entry": getattr(signal, "net_buy_pressure", 1.0),
            "odds_api_event_id": getattr(signal, "odds_api_event_id", ""),
        }

    def _is_game_tied(self, score: str) -> bool:
        """Parse score string to detect tie."""
        if not score:
            return False
        try:
            parts = str(score).split("-")
            if len(parts) == 2:
                return parts[0].strip() == \
                       parts[1].strip()
        except Exception:
            pass
        return False

    async def _get_paper_stats(self) -> dict:
        from data.database import get_paper_trade_stats
        return await get_paper_trade_stats()
