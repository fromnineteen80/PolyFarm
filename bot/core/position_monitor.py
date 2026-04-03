import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from core.order_manager import OpenPosition

logger = logging.getLogger("polyfarm.positions")

class PositionMonitor:

    def __init__(self, client, wallet,
                 order_manager, registry):
        self.client = client
        self.wallet = wallet
        self.om = order_manager
        self.registry = registry
        self._positions: dict[str, OpenPosition] = {}
        self._pending_fills: dict[str, asyncio.Event] = {}
        self._fill_prices: dict[str, float] = {}
        self._lock = asyncio.Lock()

    def has_position(self, slug: str) -> bool:
        return slug in self._positions

    async def get_position(
        self, slug: str
    ) -> Optional[OpenPosition]:
        async with self._lock:
            return self._positions.get(slug)

    def get_all_positions(self) -> dict:
        return dict(self._positions)

    def get_htr_count(self) -> int:
        return sum(
            1 for p in self._positions.values()
            if p.hold_to_resolution
        )

    async def add_position(self,
                            slug: str,
                            position: OpenPosition):
        async with self._lock:
            self._positions[slug] = position
        self.wallet.update_position_value(
            slug,
            position.entry_price,
            position.shares
        )

    async def remove_position(self, slug: str):
        async with self._lock:
            self._positions.pop(slug, None)
        self.wallet.remove_position(slug)

    async def update_position(self,
                               slug: str,
                               updates: dict):
        async with self._lock:
            pos = self._positions.get(slug)
            if pos:
                for k, v in updates.items():
                    if hasattr(pos, k):
                        setattr(pos, k, v)

    def register_pending_fill(self,
                               order_id: str,
                               event: asyncio.Event):
        self._pending_fills[order_id] = event

    def notify_fill(self,
                    order_id: str,
                    fill_price: float):
        self._fill_prices[order_id] = fill_price
        event = self._pending_fills.pop(
            order_id, None
        )
        if event:
            event.set()

    def get_fill_price(self,
                        order_id: str) -> Optional[float]:
        return self._fill_prices.pop(order_id, None)

    async def on_ws_position_update(self,
                                     slug: str,
                                     current_price: float,
                                     shares: float):
        """Called by private WebSocket on POSITION event."""
        self.wallet.update_position_value(
            slug, current_price, shares
        )

    async def on_ws_order_fill(self,
                                order_id: str,
                                slug: str,
                                fill_price: float,
                                intent: str):
        """
        Called by private WebSocket on ORDER fill.
        Handles both entry fills and exit fills.
        """
        # Entry fill
        self.notify_fill(order_id, fill_price)

        # Exit fill (GTC sell filled = reprice exit)
        pos = self._positions.get(slug)
        if pos and pos.sell_order_id == order_id:
            if "SELL" in intent.upper():
                await self.om.on_reprice_fill(
                    slug, fill_price, order_id
                )

    async def load_existing_positions(self):
        """
        Called at startup to resume monitoring
        of any positions open from before restart.
        Paper mode: loads from Supabase only.
        Live mode: loads from Polymarket portfolio API
        cross-referenced with Supabase trades.
        """
        from data.database import get_open_trades
        from config import PAPER_MODE
        try:
            open_trades = await get_open_trades(
                PAPER_MODE
            )
            if PAPER_MODE:
                # Paper: load directly from Supabase
                for trade in open_trades:
                    slug = trade["market_slug"]
                    if slug in self._positions:
                        continue
                    position = OpenPosition(
                        trade_id=trade["id"],
                        slug=slug,
                        sport=trade.get("sport", ""),
                        teams=trade.get("teams", ""),
                        band=trade.get("band", "A"),
                        strategy=trade.get(
                            "position_type",
                            "oracle_arb"
                        ),
                        position_type=trade.get(
                            "position_type", "normal"
                        ),
                        entry_price=float(
                            trade.get(
                                "entry_price", 0.5
                            )
                        ),
                        shares=int(
                            trade.get("shares", 0) or 0
                        ),
                        exit_target=float(
                            trade.get(
                                "entry_price", 0.5
                            )
                        ) + 0.05,
                        original_edge=float(
                            trade.get(
                                "raw_edge_at_entry",
                                0.05
                            )
                        ),
                        entry_time=(
                            datetime.fromisoformat(
                                trade["timestamp_entry"]
                                .replace("Z", "+00:00")
                            )
                        ),
                        sell_order_id=None,
                        paper_mode=True,
                    )
                    await self.add_position(
                        slug, position
                    )
                    logger.info(
                        f"Resumed paper position: "
                        f"{slug}"
                    )
            else:
                # Live: cross-reference real positions
                # with Supabase trades
                result = await (
                    self.client.portfolio.positions()
                )
                positions_map = result.get(
                    "positions", {}
                )
                for slug, pos in positions_map.items():
                    if slug in self._positions:
                        continue
                    shares = float(
                        pos.get("longShares", 0) or 0
                    )
                    if shares <= 0:
                        continue
                    trade = next(
                        (t for t in open_trades
                         if t["market_slug"] == slug),
                        None
                    )
                    if trade:
                        position = OpenPosition(
                            trade_id=trade["id"],
                            slug=slug,
                            sport=trade.get(
                                "sport", ""
                            ),
                            teams=trade.get(
                                "teams", ""
                            ),
                            band=trade.get(
                                "band", "A"
                            ),
                            strategy=trade.get(
                                "position_type",
                                "oracle_arb"
                            ),
                            position_type=trade.get(
                                "position_type",
                                "normal"
                            ),
                            entry_price=float(
                                trade.get(
                                    "entry_price", 0.5
                                )
                            ),
                            shares=int(shares),
                            exit_target=float(
                                trade.get(
                                    "entry_price", 0.5
                                )
                            ) + 0.05,
                            original_edge=float(
                                trade.get(
                                    "raw_edge_at_entry",
                                    0.05
                                )
                            ),
                            entry_time=(
                                datetime.fromisoformat(
                                    trade[
                                        "timestamp_entry"
                                    ].replace(
                                        "Z", "+00:00"
                                    )
                                )
                            ),
                            sell_order_id=None,
                            paper_mode=False,
                        )
                        await self.add_position(
                            slug, position
                        )
                        logger.info(
                            f"Resumed position: {slug}"
                        )

            logger.info(
                f"Loaded {len(self._positions)} "
                f"existing positions"
            )
        except Exception as e:
            logger.error(
                f"Load existing positions error: {e}"
            )

    async def monitor_loop(self):
        """Check all positions every 30 seconds."""
        while True:
            await asyncio.sleep(30)
            await self._check_all_positions()

    async def _check_all_positions(self):
        from config import PAPER_MODE
        positions = list(self._positions.values())
        for position in positions:
            try:
                if PAPER_MODE:
                    # Paper mode: use pipeline price,
                    # no real API calls
                    market = await self.registry.get(
                        position.slug
                    )
                    current_bid = (
                        market.yes_price
                        if market and market.yes_price > 0
                        else position.entry_price
                    )
                else:
                    from core.market_loader import parse_bbo
                    bbo = await self.client.markets.bbo(
                        position.slug
                    )
                    current_bid, _ask, _cur = parse_bbo(
                        bbo
                    )
                    if current_bid == 0:
                        current_bid = (
                            _cur if _cur > 0 else (
                                _ask if _ask > 0
                                else position.entry_price
                            )
                        )
                self.wallet.update_position_value(
                    position.slug,
                    current_bid,
                    position.shares
                )

                # Get live game state
                game_state = None
                market = await self.registry.get(
                    position.slug
                )
                if market and market.is_live:
                    game_state = self._compute_game_state(
                        sport=market.sport,
                        period_str=market.current_period,
                        elapsed_str=market.time_elapsed,
                        score=market.current_score,
                        is_finished=market.is_finished,
                    )

                await self.om.check_position_exits(
                    position, current_bid, game_state
                )

            except Exception as e:
                logger.error(
                    f"Position monitor error "
                    f"{position.slug}: {e}"
                )

    def _compute_game_state(
        self,
        sport: str,
        period_str: Optional[str],
        elapsed_str: Optional[str],
        score: Optional[str],
        is_finished: bool,
    ) -> dict:
        """Compute game state from real API fields.

        Returns dict with:
          time_remaining_seconds: int or None
          period: int or None (period/quarter number)
          inning: int or None (MLB only)
          game_minute: int or None (soccer elapsed)
          is_overtime: bool
          score: str or None
          is_finished: bool
        """
        result = {
            "time_remaining_seconds": None,
            "period": None,
            "inning": None,
            "game_minute": None,
            "is_overtime": False,
            "score": score,
            "is_finished": is_finished,
        }

        if not period_str:
            return result

        p = period_str.strip().upper()

        # Detect overtime / extra time
        if "OT" in p or "OVERTIME" in p \
           or "EXTRA" in p or p == "ET":
            result["is_overtime"] = True
            result["time_remaining_seconds"] = 0
            return result

        # Parse elapsed minutes:seconds
        elapsed_mins = 0.0
        if elapsed_str:
            try:
                parts = elapsed_str.strip().split(":")
                if len(parts) == 2:
                    elapsed_mins = (
                        int(parts[0])
                        + int(parts[1]) / 60.0
                    )
                elif len(parts) == 1:
                    elapsed_mins = float(parts[0])
            except (ValueError, IndexError):
                pass

        import re
        nums = re.findall(r'\d+', p)
        period_num = int(nums[0]) if nums else None

        sport_lower = (sport or "").lower()

        # ── NBA: 4Q x 12min ──────────────
        if sport_lower == "basketball_nba":
            if period_num is not None and p.startswith("Q"):
                result["period"] = period_num
                remaining_in_q = 12.0 - elapsed_mins
                remaining_qs = max(0, 4 - period_num)
                total = remaining_in_q + (
                    remaining_qs * 12
                )
                result["time_remaining_seconds"] = (
                    int(max(0, total * 60))
                )

        # ── CBB: 2H x 20min ──────────────
        elif sport_lower == "basketball_ncaab":
            if p.startswith("H") and period_num:
                result["period"] = period_num
                remaining_in_h = 20.0 - elapsed_mins
                remaining_hs = max(0, 2 - period_num)
                total = remaining_in_h + (
                    remaining_hs * 20
                )
                result["time_remaining_seconds"] = (
                    int(max(0, total * 60))
                )
            elif "END" in p:
                # "End H1" = halftime
                result["period"] = period_num
                remaining_hs = max(0, 2 - (
                    period_num or 0
                ))
                result["time_remaining_seconds"] = (
                    remaining_hs * 20 * 60
                )

        # ── NHL: 3P x 20min ──────────────
        elif sport_lower == "icehockey_nhl":
            if p.startswith("P") and period_num:
                result["period"] = period_num
                remaining_in_p = 20.0 - elapsed_mins
                remaining_ps = max(0, 3 - period_num)
                total = remaining_in_p + (
                    remaining_ps * 20
                )
                result["time_remaining_seconds"] = (
                    int(max(0, total * 60))
                )

        # ── MLB: 9 innings, no clock ─────
        elif sport_lower == "baseball_mlb":
            if period_num is not None:
                result["inning"] = period_num
                result["period"] = period_num
                # Approximate: each inning ~1/9
                # No time_remaining for baseball
                # but set a sentinel for progress
                # T = top, B = bottom
                half = 0.5 if p.startswith("B") else 0.0
                progress = (
                    (period_num - 1 + half) / 9.0
                )
                # No seconds-based time for MLB
                result["time_remaining_seconds"] = None

        # ── NFL/CFB: 4Q x 15min ──────────
        elif "americanfootball" in sport_lower:
            if p.startswith("Q") and period_num:
                result["period"] = period_num
                remaining_in_q = 15.0 - elapsed_mins
                remaining_qs = max(0, 4 - period_num)
                total = remaining_in_q + (
                    remaining_qs * 15
                )
                result["time_remaining_seconds"] = (
                    int(max(0, total * 60))
                )

        # ── Soccer: 90min total elapsed ───
        elif "soccer" in sport_lower:
            # Soccer elapsed is total match minutes
            if elapsed_str:
                try:
                    parts = elapsed_str.strip().split(":")
                    if len(parts) >= 1:
                        match_min = int(parts[0])
                    else:
                        match_min = 0
                    result["game_minute"] = match_min
                    remaining = max(0, 90 - match_min)
                    result["time_remaining_seconds"] = (
                        remaining * 60
                    )
                except (ValueError, IndexError):
                    pass
            # Also parse period for half info
            if p in ("1H", "H1"):
                result["period"] = 1
                if result["game_minute"] is None:
                    # First half, unknown minute
                    result["time_remaining_seconds"] = (
                        45 * 60
                    )
            elif p in ("2H", "H2"):
                result["period"] = 2
                if result["game_minute"] is None:
                    result["time_remaining_seconds"] = (
                        15 * 60
                    )

        return result
