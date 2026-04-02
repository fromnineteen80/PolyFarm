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
        """
        try:
            result = await (
                self.client.portfolio.positions()
            )
            positions_map = result.get("positions", {})
            for slug, pos in positions_map.items():
                if slug in self._positions:
                    continue
                shares = float(pos.get("longShares", 0) or 0)
                if shares <= 0:
                    continue
                # Try to find matching open trade
                from data.database import get_open_trades
                from config import PAPER_MODE
                open_trades = await get_open_trades(
                    PAPER_MODE
                )
                trade = next(
                    (t for t in open_trades
                     if t["market_slug"] == slug),
                    None
                )
                if trade:
                    position = OpenPosition(
                        trade_id=trade["id"],
                        slug=slug,
                        sport=trade.get("sport", ""),
                        teams=trade.get("teams", ""),
                        band=trade.get("band", "A"),
                        strategy=trade.get(
                            "position_type", "oracle_arb"
                        ),
                        position_type=trade.get(
                            "position_type", "normal"
                        ),
                        entry_price=float(
                            trade.get("entry_price", 0.5)
                        ),
                        shares=int(shares),
                        exit_target=float(
                            trade.get("entry_price", 0.5)
                        ) + 0.05,
                        original_edge=float(
                            trade.get(
                                "raw_edge_at_entry", 0.05
                            )
                        ),
                        entry_time=datetime.fromisoformat(
                            trade["timestamp_entry"]
                            .replace("Z", "+00:00")
                        ),
                        sell_order_id=None,
                        paper_mode=PAPER_MODE,
                    )
                    await self.add_position(slug, position)
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
        positions = list(self._positions.values())
        for position in positions:
            try:
                from core.market_loader import parse_bbo
                bbo = await self.client.markets.bbo(
                    position.slug
                )
                current_bid, _ask, _cur = parse_bbo(bbo)
                if current_bid == 0:
                    # Use current price or ask as fallback
                    current_bid = _cur if _cur > 0 else (
                        _ask if _ask > 0 else position.entry_price
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
                    game_state = {
                        "time_remaining_seconds": (
                            market.time_remaining_seconds
                        ),
                        "inning": self._parse_inning(
                            market.current_period
                        ),
                        "period": self._parse_period(
                            market.current_period
                        ),
                        "game_minute": (
                            self._parse_minute(
                                market.current_period
                            )
                        ),
                        "is_overtime": self._is_ot(
                            market.current_period
                        ),
                        "score": market.current_score,
                        "is_finished": market.is_finished,
                    }

                await self.om.check_position_exits(
                    position, current_bid, game_state
                )

            except Exception as e:
                logger.error(
                    f"Position monitor error "
                    f"{position.slug}: {e}"
                )

    def _parse_inning(self,
                       period: Optional[str]) -> int:
        if not period:
            return 0
        try:
            p = period.lower()
            if "inning" in p or "inn" in p:
                import re
                nums = re.findall(r'\d+', p)
                return int(nums[0]) if nums else 0
        except Exception:
            pass
        return 0

    def _parse_period(self,
                       period: Optional[str]) -> int:
        if not period:
            return 0
        try:
            import re
            nums = re.findall(r'\d+', period)
            return int(nums[0]) if nums else 0
        except Exception:
            return 0

    def _parse_minute(self,
                       period: Optional[str]) -> int:
        return self._parse_period(period)

    def _is_ot(self, period: Optional[str]) -> bool:
        if not period:
            return False
        p = period.lower()
        return "ot" in p or "overtime" in p or \
               "extra" in p
