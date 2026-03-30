import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass
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
    oddspapi_fixture_id: str = ""
    pinnacle_home_decimal: float = 0.0
    pinnacle_away_decimal: float = 0.0

class EdgeDetector:

    def __init__(self, registry, mapper, wallet, position_monitor):
        self.registry = registry
        self.mapper = mapper  # kept for backward compat, may be None
        self.wallet = wallet
        self.position_monitor = position_monitor
        self.oddspapi = None  # set by main.py after init
        self.price_queue: asyncio.Queue = asyncio.Queue()
        self._paper_stats: dict = {"completed": 0, "win_rate": 0.0}

    def update_paper_stats(self, completed: int, win_rate: float):
        self._paper_stats = {"completed": completed, "win_rate": win_rate}

    async def detection_loop(self):
        """Consumes WebSocket price events."""
        while True:
            try:
                event = await asyncio.wait_for(
                    self.price_queue.get(), timeout=1.0
                )
                await self.evaluate_signal(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Detection loop error: {e}")

    def _get_team_side(self, market) -> str:
        """
        Determine if the YES (long) side of this
        market represents the home or away team.
        Compares market_sides data if available,
        otherwise defaults to home.
        """
        if not hasattr(market, "market_sides"):
            return "home"
        sides = getattr(market, "market_sides", None)
        if not sides:
            return "home"
        for side in sides:
            if isinstance(side, dict) and side.get("long"):
                team_name = side.get("team", {}).get("name", "")
                if team_name and market.home_team:
                    from core.oddspapi_client import normalize_team
                    if normalize_team(team_name) == normalize_team(market.home_team):
                        return "home"
                    else:
                        return "away"
        return "home"

    async def evaluate_signal(self, event: dict) -> Optional[EdgeSignal]:
        slug = event.get("market_slug")
        yes_price = event.get("yes_price")
        if not slug or yes_price is None:
            return None

        poly_price = float(yes_price)

        # ── GUARDS ──────────────────────────────────
        if poly_price < FAVORITES_FLOOR:
            return None

        if not self.wallet.can_enter("band_a") and \
           not self.wallet.can_enter("band_b") and \
           not self.wallet.can_enter("band_c"):
            return None

        # Check OddsPapi match
        if not self.oddspapi or not self.oddspapi.is_matched(slug):
            return None

        # Skip if already in this market
        if self.position_monitor.has_position(slug):
            return None

        # ── SHARP PROBABILITY ───────────────────────
        market = await self.registry.get(slug)
        if not market:
            return None

        team_side = self._get_team_side(market)
        sharp_prob = self.oddspapi.get_fair_prob(slug, team_side)
        if sharp_prob is None:
            return None

        raw_edge = sharp_prob - poly_price

        # ── BAND CLASSIFICATION ─────────────────────
        is_live = market.is_live
        live_adj = LIVE_GAME_EDGE_REDUCTION if is_live else 0.0

        if poly_price >= BAND_A_MIN_PRICE:
            band = "A"
            min_edge = BAND_A_MIN_EDGE - live_adj
            strategy_key = "band_a"
        elif poly_price >= BAND_B_MIN_PRICE:
            band = "B"
            min_edge = BAND_B_MIN_EDGE - live_adj
            strategy_key = "band_b"
        elif poly_price >= BAND_C_MIN_PRICE:
            band = "C"
            min_edge = BAND_C_MIN_EDGE - live_adj
            strategy_key = "band_c"
        else:
            return None

        if raw_edge < min_edge:
            return None

        if not self.wallet.can_enter(strategy_key):
            return None

        # ── CONFIDENCE SCORE ────────────────────────
        probs = self.oddspapi.get_both_fair_probs(slug)
        freshness = 1.0  # OddsPapi polls every 3min
        if probs and probs.get("updated_at"):
            try:
                updated = datetime.fromisoformat(
                    probs["updated_at"].replace("Z", "+00:00")
                )
                age = (datetime.now(timezone.utc) - updated).total_seconds()
                if age > 300:  # stale if over 5 min
                    return None
                freshness = 1.0 if age < 60 else 0.85
            except Exception:
                pass

        # Mapping quality
        mapping_conf = 1.0  # OddsPapi matches are verified

        # Liquidity
        volume = market.volume
        if volume < 20000:
            return None
        liquidity = 1.0 if volume > 50000 else 0.90

        stability = 1.0

        confidence = (
            freshness * 0.35 +
            mapping_conf * 0.25 +
            liquidity * 0.25 +
            stability * 0.15
        )

        if confidence < CONFIDENCE_THRESHOLD:
            return None

        # ── SPORT CONCENTRATION ─────────────────────
        open_positions = self.position_monitor.get_all_positions()
        total = len(open_positions)
        if total > 0:
            sport_count = sum(
                1 for p in open_positions.values()
                if p.get("sport") == market.sport
            )
            if sport_count / total >= MAX_SINGLE_SPORT_PCT:
                return None

        # ── PAPER MODE UNLOCK CHECK ─────────────────
        from config import PAPER_MODE
        if not PAPER_MODE:
            if self._paper_stats["completed"] < PAPER_TRADES_REQUIRED:
                logger.warning(
                    f"Live mode blocked: "
                    f"{self._paper_stats['completed']}"
                    f"/{PAPER_TRADES_REQUIRED} paper trades"
                )
                return None

        # ── FEE-ADJUSTED NET EDGE ───────────────────
        position_usd = self.wallet.get_position_size_usd(strategy_key)
        if position_usd <= 0:
            return None

        shares = int(position_usd / poly_price)
        if shares < 1:
            return None

        entry_notional = shares * poly_price
        taker_fee = entry_notional * TAKER_FEE_RATE

        exit_target = poly_price + (raw_edge * REPRICE_EXIT_PCT)
        exit_notional = shares * (1 - exit_target)
        maker_rebate = exit_notional * MAKER_REBATE_RATE

        net_edge_usd = (raw_edge * shares) - taker_fee + maker_rebate
        net_edge_pct = net_edge_usd / position_usd

        if net_edge_pct < min_edge:
            return None

        # Build enriched signal
        fixture_id = ""
        pinnacle_home = 0.0
        pinnacle_away = 0.0
        if probs:
            fixture_id = probs.get("fixture_id", "")
            pinnacle_home = probs.get("home_decimal", 0) or 0
            pinnacle_away = probs.get("away_decimal", 0) or 0

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
            edge_at_entry=raw_edge,
            oddspapi_fixture_id=fixture_id,
            pinnacle_home_decimal=pinnacle_home,
            pinnacle_away_decimal=pinnacle_away,
        )
