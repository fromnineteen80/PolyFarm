import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from config import (
    FAVORITES_FLOOR,
    BAND_A_MIN_PRICE, BAND_A_MIN_EDGE,
    BAND_B_MIN_PRICE, BAND_B_MIN_EDGE,
    BAND_C_MIN_PRICE, BAND_C_MIN_EDGE,
    LIVE_GAME_EDGE_REDUCTION,
    CONFIDENCE_THRESHOLD,
    MAX_SINGLE_SPORT_PCT,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
    REPRICE_EXIT_PCT,
    PAPER_TRADES_REQUIRED,
    PAPER_WIN_RATE_REQUIRED,
)
from core.pipeline import normalize_team

logger = logging.getLogger("polyfarm.edge")

@dataclass
class EdgeSignal:
    slug: str
    sport: str
    teams: str
    band: str
    poly_price: float
    sharp_prob: float
    raw_edge: float
    net_edge_pct: float
    confidence: float
    position_usd: float
    shares: int
    exit_target: float
    taker_fee: float
    maker_rebate: float
    is_live: bool
    market_type: str
    timestamp: str
    strategy: str = "oracle_arb"
    game_id: Optional[str] = None
    poly_price_at_entry: float = 0.0
    edge_at_entry: float = 0.0
    price_direction: str = "stable"
    price_velocity: float = 0.0
    net_buy_pressure: float = 1.0
    size_multiplier: float = 1.0
    composite_score: float = 0.0
    books_used: list = field(default_factory=list)
    odds_api_event_id: str = ""

class EdgeDetector:

    def __init__(self, registry, mapper, wallet, position_monitor):
        self.registry = registry
        self.mapper = mapper
        self.wallet = wallet
        self.position_monitor = position_monitor
        self.odds_api = None
        self.ws_markets = None
        self.order_manager = None
        self.price_queue: asyncio.Queue = asyncio.Queue()
        self._paper_stats: dict = {"completed": 0, "win_rate": 0.0}
        self._recently_exited: set = set()  # slugs we exited at a loss — don't re-enter

    def mark_exited(self, slug: str):
        """Called by order_manager when a trade closes at a loss.
        Prevents re-entering the same game."""
        self._recently_exited.add(slug)

    def update_paper_stats(self, completed, win_rate):
        self._paper_stats = {"completed": completed, "win_rate": win_rate}

    async def detection_loop(self):
        while True:
            try:
                event = await asyncio.wait_for(self.price_queue.get(), timeout=1.0)
                signal = await self.evaluate_signal(event)
                if signal and self.order_manager:
                    await self.order_manager.enter_position(signal)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Detection loop error: {e}")

    def _get_team_side(self, market) -> str:
        if not hasattr(market, "market_sides"):
            return "home"
        sides = getattr(market, "market_sides", None)
        if not sides:
            return "home"
        for side in sides:
            if isinstance(side, dict) and side.get("long"):
                team_name = side.get("team", {}).get("name", "")
                if team_name and market.home_team:
                    if normalize_team(team_name) == normalize_team(market.home_team):
                        return "home"
                    else:
                        return "away"
        return "home"

    async def evaluate_signal(self, event):
        slug = event.get("market_slug")
        yes_price = event.get("yes_price")
        if not slug or yes_price is None:
            return None

        poly_price = float(yes_price)

        if poly_price < FAVORITES_FLOOR:
            return None

        if not self.wallet.can_enter("band_a") and \
           not self.wallet.can_enter("band_b") and \
           not self.wallet.can_enter("band_c"):
            return None

        if not self.odds_api or not self.odds_api.is_matched(slug):
            return None

        if self.position_monitor.has_position(slug):
            return None

        # Don't re-enter a game we recently exited at a loss
        if slug in self._recently_exited:
            return None

        market = await self.registry.get(slug)
        if not market:
            return None

        # Only trade live games — pre-game prices don't move
        if not market.is_live:
            return None

        # Band classification (thresholds preserved exactly)
        is_live = market.is_live
        live_adj = LIVE_GAME_EDGE_REDUCTION if is_live else 0.0

        if poly_price >= BAND_A_MIN_PRICE:
            band = "A"
            band_threshold = BAND_A_MIN_EDGE - live_adj
            strategy_key = "band_a"
        elif poly_price >= BAND_B_MIN_PRICE:
            band = "B"
            band_threshold = BAND_B_MIN_EDGE - live_adj
            strategy_key = "band_b"
        elif poly_price >= BAND_C_MIN_PRICE:
            band = "C"
            band_threshold = BAND_C_MIN_EDGE - live_adj
            strategy_key = "band_c"
        else:
            return None

        if not self.wallet.can_enter(strategy_key):
            return None

        # Composite edge signal with price movement
        team_side = self._get_team_side(market)
        signal = self.odds_api.get_edge_signal(
            polymarket_slug=slug,
            team_side=team_side,
            poly_yes_price=poly_price,
            ws_markets=self.ws_markets,
            band_threshold=band_threshold,
        )

        if signal is None:
            return None

        if not signal["qualifies"]:
            return None

        sharp_prob = signal["sharp_prob"]
        static_edge = signal["static_edge"]
        size_multiplier = signal["size_multiplier"]
        composite_score = signal["composite_score"]
        direction = signal["direction"]
        raw_edge = static_edge

        # Confidence score
        consensus = self.odds_api.get_consensus_data(slug)
        freshness = 1.0
        if consensus and consensus.get("updated_at"):
            try:
                updated = datetime.fromisoformat(consensus["updated_at"].replace("Z", "+00:00"))
                age = (datetime.now(timezone.utc) - updated).total_seconds()
                if age > 300:
                    return None
                freshness = 1.0 if age < 60 else 0.85
            except Exception:
                pass

        mapping_conf = 1.0
        # Use bid/ask depth from WebSocket as liquidity proxy
        # v2 doesn't return volume; depth is a better real-time measure
        bid_depth = event.get("bid_depth", 0) or 0
        ask_depth = event.get("ask_depth", 0) or 0
        if bid_depth < 3 and ask_depth < 3:
            return None
        liquidity = 1.0 if (bid_depth >= 5 and ask_depth >= 5) else 0.90
        stability = 1.0

        confidence = (
            freshness * 0.35 +
            mapping_conf * 0.25 +
            liquidity * 0.25 +
            stability * 0.15
        )
        if confidence < CONFIDENCE_THRESHOLD:
            return None

        # Sport concentration
        open_positions = self.position_monitor.get_all_positions()
        total = len(open_positions)
        if total > 0:
            sport_count = sum(1 for p in open_positions.values() if getattr(p, "sport", None) == market.sport)
            if sport_count / total >= MAX_SINGLE_SPORT_PCT:
                return None

        # Paper mode unlock
        from config import PAPER_MODE
        if not PAPER_MODE:
            if self._paper_stats["completed"] < PAPER_TRADES_REQUIRED:
                logger.warning(f"Live mode blocked: {self._paper_stats['completed']}/{PAPER_TRADES_REQUIRED} paper trades")
                return None

        # Position sizing with size_multiplier
        base_position_usd = self.wallet.get_position_size_usd(strategy_key)
        if base_position_usd <= 0:
            return None
        position_usd = round(base_position_usd * size_multiplier, 2)

        shares = int(position_usd / poly_price)
        if shares < 1:
            return None

        # Fee-adjusted net edge
        entry_notional = shares * poly_price
        taker_fee = entry_notional * TAKER_FEE_RATE
        exit_target = poly_price + (raw_edge * REPRICE_EXIT_PCT)
        exit_notional = shares * (1 - exit_target)
        maker_rebate = exit_notional * MAKER_REBATE_RATE
        net_edge_usd = (raw_edge * shares) - taker_fee + maker_rebate
        net_edge_pct = net_edge_usd / position_usd

        if net_edge_pct < band_threshold:
            return None

        return EdgeSignal(
            slug=slug,
            sport=market.sport,
            teams=f"{market.home_team} vs {market.away_team}",
            band=band,
            poly_price=poly_price,
            sharp_prob=sharp_prob,
            raw_edge=raw_edge,
            net_edge_pct=net_edge_pct,
            confidence=confidence,
            position_usd=position_usd,
            shares=shares,
            exit_target=round(exit_target, 4),
            taker_fee=taker_fee,
            maker_rebate=maker_rebate,
            is_live=is_live,
            market_type=market.market_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            strategy="oracle_arb",
            poly_price_at_entry=poly_price,
            edge_at_entry=static_edge,
            price_direction=direction,
            price_velocity=signal["velocity"],
            net_buy_pressure=signal["net_buy_pressure"],
            size_multiplier=size_multiplier,
            composite_score=composite_score,
            books_used=signal["books_used"],
            odds_api_event_id=signal["event_id"],
        )
