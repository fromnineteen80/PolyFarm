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

class EdgeDetector:

    def __init__(self,
                 registry,
                 mapper,
                 wallet,
                 position_monitor):
        self.registry = registry
        self.mapper = mapper
        self.wallet = wallet
        self.position_monitor = position_monitor
        self.price_queue: asyncio.Queue = (
            asyncio.Queue()
        )
        self._paper_stats: dict = {
            "completed": 0,
            "win_rate": 0.0
        }

    def update_paper_stats(self,
                            completed: int,
                            win_rate: float):
        self._paper_stats = {
            "completed": completed,
            "win_rate": win_rate
        }

    async def detection_loop(self):
        """Consumes WebSocket price events."""
        while True:
            try:
                event = await asyncio.wait_for(
                    self.price_queue.get(),
                    timeout=1.0
                )
                await self.evaluate_signal(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(
                    f"Detection loop error: {e}"
                )

    async def evaluate_signal(self,
                               event: dict
                               ) -> Optional[EdgeSignal]:
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

        mapping = self.mapper.get_mapping(slug)
        if not mapping:
            return None
        if mapping["mapping_status"] == "UNCONFIRMED":
            return None

        # Skip if already in this market
        if self.position_monitor.has_position(slug):
            # Allow add only if fresh signal is
            # significantly stronger (handled separately)
            return None

        # ── SHARP PROBABILITY ───────────────────────
        sharp_prob = self.mapper.get_sharp_probability(
            slug
        )
        if sharp_prob is None:
            return None

        raw_edge = sharp_prob - poly_price

        # ── BAND CLASSIFICATION ─────────────────────
        market = await self.registry.get(slug)
        if not market:
            return None

        is_live = market.is_live
        live_adj = LIVE_GAME_EDGE_REDUCTION if is_live \
            else 0.0

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
        # Freshness
        import os
        event_id = mapping.get("odds_api_event_id")
        last_updated = (
            self.mapper.loader.odds_last_updated.get(
                event_id
            )
        )
        if not last_updated:
            return None
        age = (
            datetime.now(timezone.utc) - last_updated
        ).total_seconds()
        if age > 10:
            return None
        freshness = 1.0 if age < 3 else 0.75

        # Mapping quality
        mapping_conf = 1.0 if mapping[
            "mapping_status"
        ] == "CONFIRMED" else 0.85

        # Liquidity
        volume = market.volume
        if volume < 20000:
            return None
        liquidity = 1.0 if volume > 50000 else 0.90

        # Line stability (simplified — always 1.0
        # for now, can be enhanced with price history)
        stability = 1.0

        confidence = (
            freshness   * 0.35 +
            mapping_conf * 0.25 +
            liquidity   * 0.25 +
            stability   * 0.15
        )

        if confidence < CONFIDENCE_THRESHOLD:
            return None

        # ── SPORT CONCENTRATION ─────────────────────
        open_positions = (
            self.position_monitor.get_all_positions()
        )
        total = len(open_positions)
        if total > 0:
            sport_count = sum(
                1 for p in open_positions.values()
                if p.get("sport") == market.sport
            )
            if sport_count / total >= \
               MAX_SINGLE_SPORT_PCT:
                return None

        # ── PAPER MODE UNLOCK CHECK ─────────────────
        from config import PAPER_MODE
        if not PAPER_MODE:
            if self._paper_stats["completed"] < \
               PAPER_TRADES_REQUIRED:
                logger.warning(
                    f"Live mode blocked: "
                    f"{self._paper_stats['completed']}"
                    f"/{PAPER_TRADES_REQUIRED} "
                    f"paper trades"
                )
                return None

        # ── FEE-ADJUSTED NET EDGE ───────────────────
        position_usd = self.wallet.get_position_size_usd(
            strategy_key
        )
        if position_usd <= 0:
            return None

        shares = int(position_usd / poly_price)
        if shares < 1:
            return None

        entry_notional = shares * poly_price
        taker_fee = entry_notional * TAKER_FEE_RATE

        exit_target = poly_price + (
            raw_edge * REPRICE_EXIT_PCT
        )
        exit_notional = shares * (1 - exit_target)
        maker_rebate = exit_notional * MAKER_REBATE_RATE

        net_edge_usd = (
            (raw_edge * shares)
            - taker_fee
            + maker_rebate
        )
        net_edge_pct = net_edge_usd / position_usd

        if net_edge_pct < min_edge:
            return None

        return EdgeSignal(
            slug=slug,
            sport=market.sport,
            teams=f"{market.home_team} vs "
                  f"{market.away_team}",
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
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),
            strategy="oracle_arb",
        )
