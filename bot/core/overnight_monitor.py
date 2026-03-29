import asyncio
import logging
from datetime import datetime, timezone, timedelta
from config import (
    OVERNIGHT_MIN_EDGE,
    OVERNIGHT_MIN_VOLUME,
    OVERNIGHT_MAX_POOL_PCT,
    OVERNIGHT_REEVAL_HOUR,
    OVERNIGHT_EXIT_EDGE_THRESHOLD,
    FAVORITES_FLOOR,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
    REPRICE_EXIT_PCT,
)

logger = logging.getLogger("polyfarm.overnight")

class OvernightMonitor:

    def __init__(self, client, wallet,
                 registry, mapper,
                 order_manager,
                 position_monitor):
        self.client = client
        self.wallet = wallet
        self.registry = registry
        self.mapper = mapper
        self.om = order_manager
        self.pm = position_monitor
        self._overnight_slugs: set = set()

    def _overnight_pool_available(self) -> float:
        """Returns remaining overnight pool capacity."""
        total_wallet = (
            self.wallet.state.live_portfolio_value
        )
        max_pool = total_wallet * OVERNIGHT_MAX_POOL_PCT
        overnight_deployed = sum(
            self.wallet._position_values.get(
                slug, {}
            ).get("value", 0)
            for slug in self._overnight_slugs
        )
        return max(0, max_pool - overnight_deployed)

    async def scan_overnight_opportunities(self):
        """
        Scan next-day markets at midnight and 6am.
        Only runs in NORMAL mode — not during
        protected profit sessions.
        """
        if not self.wallet.can_enter("overnight"):
            return
        if self.wallet.state.profit_mode != "NORMAL":
            return

        markets = await self.registry.all_markets()
        pool_remaining = self._overnight_pool_available()
        if pool_remaining <= 0:
            return

        now = datetime.now(timezone.utc)
        tomorrow_start = now + timedelta(hours=1)
        tomorrow_end = now + timedelta(hours=36)

        for market in markets:
            if market.is_live:
                continue
            try:
                start = datetime.fromisoformat(
                    market.start_time.replace(
                        "Z", "+00:00"
                    )
                )
                if not (tomorrow_start
                        <= start
                        <= tomorrow_end):
                    continue
            except Exception:
                continue

            if market.yes_price < FAVORITES_FLOOR:
                continue
            if market.volume < OVERNIGHT_MIN_VOLUME:
                continue

            mapping = self.mapper.get_mapping(
                market.slug
            )
            if not mapping or \
               mapping["mapping_status"] == \
               "UNCONFIRMED":
                continue

            sharp_prob = (
                self.mapper.get_sharp_probability(
                    market.slug, max_age_seconds=60
                )
            )
            if not sharp_prob:
                continue

            edge = sharp_prob - market.yes_price
            if edge < OVERNIGHT_MIN_EDGE:
                continue

            # Size from overnight pool
            position_usd = min(
                pool_remaining,
                self.wallet.state.live_portfolio_value
                * 0.03
            )
            shares = int(
                position_usd / market.yes_price
            )
            if shares < 1:
                continue

            from core.edge_detector import EdgeSignal
            signal = EdgeSignal(
                slug=market.slug,
                sport=market.sport,
                teams=f"{market.home_team} vs "
                      f"{market.away_team}",
                band="A" if market.yes_price >= 0.70
                     else "B",
                poly_price=market.yes_price,
                sharp_prob=sharp_prob,
                raw_edge=edge,
                net_edge_pct=edge,
                confidence=0.87,
                position_usd=position_usd,
                shares=shares,
                exit_target=market.yes_price + (
                    edge * REPRICE_EXIT_PCT
                ),
                taker_fee=(
                    shares * market.yes_price
                    * TAKER_FEE_RATE
                ),
                maker_rebate=0,
                is_live=False,
                market_type=market.market_type,
                timestamp=datetime.now(
                    timezone.utc
                ).isoformat(),
                strategy="oracle_arb",
            )

            await self.om.enter_position(
                signal,
                strategy="oracle_arb",
                position_type="overnight",
            )
            self._overnight_slugs.add(market.slug)
            pool_remaining -= position_usd
            logger.info(
                f"Overnight entry: {market.slug} "
                f"edge={edge:.3f}"
            )
            if pool_remaining <= 0:
                break

    async def reeval_overnight_positions(self):
        """
        Re-evaluate overnight positions at 6am.
        Exit if edge has compressed below threshold.
        """
        overnight_positions = [
            p for p in
            self.pm.get_all_positions().values()
            if p.position_type == "overnight"
        ]

        for position in overnight_positions:
            sharp_prob = (
                self.mapper.get_sharp_probability(
                    position.slug, max_age_seconds=120
                )
            )
            if not sharp_prob:
                continue
            current_edge = (
                sharp_prob - position.entry_price
            )
            if current_edge < \
               OVERNIGHT_EXIT_EDGE_THRESHOLD:
                try:
                    from core.market_loader import parse_bbo
                    bbo = await self.client.markets.bbo(
                        position.slug
                    )
                    bid, _ask, _cur = parse_bbo(bbo)
                    if bid == 0:
                        bid = position.entry_price
                    await self.om._ioc_exit(
                        position, bid,
                        "overnight_reeval"
                    )
                    self._overnight_slugs.discard(
                        position.slug
                    )
                    logger.info(
                        f"Overnight exit (edge compressed):"
                        f" {position.slug}"
                    )
                except Exception as e:
                    logger.error(
                        f"Overnight reeval error: {e}"
                    )

    async def monitor_loop(self):
        """
        Scan at midnight and 6am.
        Re-evaluate at 6am.
        """
        while True:
            now = datetime.now(timezone.utc)
            hour = now.hour

            if hour == 0:  # Midnight
                await self.scan_overnight_opportunities()
                await asyncio.sleep(3700)
            elif hour == OVERNIGHT_REEVAL_HOUR:  # 6am
                await self.reeval_overnight_positions()
                await self.scan_overnight_opportunities()
                await asyncio.sleep(3700)
            else:
                await asyncio.sleep(60)
