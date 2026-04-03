import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from config import (
    DOMINANT_TEAMS,
    EXCEPTION_MIN_ORACLE_GAP,
    EXCEPTION_MIN_VOLUME,
    EXCEPTION_MAX_TRADES_PER_SESSION,
    EXCEPTION_MAX_POSITION_PCT,
    EXCEPTION_MAX_BID_ASK_SPREAD,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
    EXCEPTION_REPRICE_PCT,
    EXCEPTION_PROFIT_LOCK,
    EXCEPTION_TRAILING_ACTIVATE,
    EXCEPTION_STOP_LOSS,
    EXCEPTION_TIMEOUT_MINUTES,
    FAVORITES_FLOOR,
)

logger = logging.getLogger("polyfarm.exception")

@dataclass
class ExceptionSignal:
    slug: str
    sport: str
    teams: str
    dominant_team: str
    poly_price: float
    sharp_prob: float
    oracle_gap: float
    position_usd: float
    shares: int
    exit_target: float
    taker_fee: float
    maker_rebate: float
    trigger_reason: str
    game_state: dict
    timestamp: str
    strategy: str = "exception"
    band: str = "EX"
    raw_edge: float = 0.0
    net_edge_pct: float = 0.0
    confidence: float = 0.90
    is_live: bool = True
    market_type: str = "moneyline"
    game_id: Optional[str] = None

class ExceptionMonitor:

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

    def _is_exception_mode(self) -> bool:
        """Exception only runs above NORMAL mode."""
        return self.wallet.state.profit_mode in (
            "HARVEST", "PROTECTION",
            "LOCKED", "PORTFOLIO_TRAIL"
        )

    def _budget_remaining(self) -> bool:
        return (
            self.wallet.state.exception_trades_today
            < EXCEPTION_MAX_TRADES_PER_SESSION
        )

    def _get_dominant_team(
        self, market
    ) -> Optional[tuple]:
        """
        Returns (team_name, config_dict) if either
        team in this market is a dominant team.
        None if neither qualifies.
        """
        for team_name, config in DOMINANT_TEAMS.items():
            if config["sport"] != market.sport:
                continue
            home = market.home_team.lower()
            away = market.away_team.lower()
            t = team_name.lower()
            if t in home or t in away:
                return team_name, config
        return None

    def _is_deficit_in_range(self,
                              team_name: str,
                              game_state: dict,
                              config: dict) -> bool:
        """Check if trailing deficit is in valid range."""
        score = game_state.get("score", "")
        if not score:
            return False
        try:
            parts = str(score).split("-")
            if len(parts) != 2:
                return False
            home_score = int(parts[0].strip())
            away_score = int(parts[1].strip())
            deficit = home_score - away_score
            # Determine which side the dominant team is
            # and whether they are trailing
            if deficit < 0:
                trailing_by = abs(deficit)
            elif deficit > 0:
                trailing_by = deficit
            else:
                return False  # Tied — no exception

            min_d, max_d = config["deficit_range"]
            return min_d <= trailing_by <= max_d
        except Exception:
            return False

    def _is_game_window_valid(self,
                               market,
                               game_state: dict,
                               config: dict) -> bool:
        """Check if game is in valid time window."""
        sport = market.sport
        time_rem = game_state.get(
            "time_remaining_seconds", 0
        )
        min_seconds = 480

        if sport in ("basketball_nba",
                     "basketball_ncaab"):
            quarters = config.get(
                "game_window", {}
            ).get("quarters", [3, 4])
            q = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", min_seconds)
            return q in quarters and \
                   time_rem >= min_s

        elif sport == "baseball_mlb":
            innings = config.get(
                "game_window_innings", (6, 8)
            )
            inning = game_state.get("inning", 0)
            return innings[0] <= inning <= innings[1]

        elif sport == "icehockey_nhl":
            periods = config.get(
                "game_window", {}
            ).get("periods", [2, 3])
            p = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", min_seconds)
            return p in periods and time_rem >= min_s

        elif sport in ("americanfootball_nfl",
                       "americanfootball_ncaaf"):
            quarters = config.get(
                "game_window", {}
            ).get("quarters", [3, 4])
            q = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", min_seconds)
            return q in quarters and time_rem >= min_s

        elif "soccer" in sport:
            r = config.get(
                "game_window", {}
            ).get("minute_range", (55, 80))
            minute = game_state.get("game_minute", 0)
            return r[0] <= minute <= r[1]

        elif sport in ("basketball_ncaab",):
            halves = config.get(
                "game_window", {}
            ).get("halves", [2])
            h = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", min_seconds)
            return h in halves and time_rem >= min_s

        return False

    async def check_exception_opportunities(self):
        """
        Check all live markets for exception signals.
        Called every 30 seconds by monitor_loop.
        """
        if not self._is_exception_mode():
            return
        if not self._budget_remaining():
            return
        if not self.wallet.can_enter("exception"):
            return

        markets = await self.registry.all_markets()
        for market in markets:
            if not market.is_live:
                continue
            if market.is_finished:
                continue

            # Check if dominant team is in this market
            result = self._get_dominant_team(market)
            if not result:
                continue
            team_name, team_config = result

            game_state = {
                "score": market.current_score,
                "period": self.pm._parse_period(
                    market.current_period
                ),
                "inning": self.pm._parse_inning(
                    market.current_period
                ),
                "game_minute": self.pm._parse_minute(
                    market.current_period
                ),
                "time_remaining_seconds": (
                    market.time_remaining_seconds or 0
                ),
                "is_overtime": self.pm._is_ot(
                    market.current_period
                ),
            }

            # Check deficit range
            if not self._is_deficit_in_range(
                team_name, game_state, team_config
            ):
                continue

            # Check game window
            if not self._is_game_window_valid(
                market, game_state, team_config
            ):
                continue

            # Get oracle gap
            if not self.mapper or not hasattr(self.mapper, 'get_fair_prob'):
                continue
            sharp_prob = self.mapper.get_fair_prob(
                market.slug, "home"
            )
            if not sharp_prob:
                continue

            poly_price = market.yes_price
            oracle_gap = sharp_prob - poly_price

            if oracle_gap < EXCEPTION_MIN_ORACLE_GAP:
                continue

            if poly_price < FAVORITES_FLOOR:
                continue

            # volume not available from v2 — skip volume gate

            try:
                from config import PAPER_MODE
                if PAPER_MODE:
                    bid = poly_price
                    ask = poly_price
                else:
                    from core.market_loader import (
                        parse_bbo
                    )
                    bbo = await self.client.markets.bbo(
                        market.slug
                    )
                    bid, ask, _cur = parse_bbo(bbo)
                spread = ask - bid
                if spread > EXCEPTION_MAX_BID_ASK_SPREAD:
                    continue
            except Exception:
                continue

            # Don't double-enter same market
            if self.pm.has_position(market.slug):
                continue

            # Build signal and fire
            position_usd = (
                self.wallet.state.live_portfolio_value
                * EXCEPTION_MAX_POSITION_PCT
            )
            shares = int(position_usd / poly_price)
            if shares < 1:
                continue

            exit_target = poly_price + (
                oracle_gap * EXCEPTION_REPRICE_PCT
            )
            entry_notional = shares * poly_price
            taker_fee = entry_notional * TAKER_FEE_RATE
            exit_notional = shares * (1 - exit_target)
            maker_rebate = (
                exit_notional * MAKER_REBATE_RATE
            )

            trigger_reason = (
                f"{team_name} trailing "
                f"in {market.sport}. "
                f"Oracle gap: {oracle_gap:.2f}"
            )

            signal = ExceptionSignal(
                slug=market.slug,
                sport=market.sport,
                teams=f"{market.home_team} vs "
                      f"{market.away_team}",
                dominant_team=team_name,
                poly_price=poly_price,
                sharp_prob=sharp_prob,
                oracle_gap=oracle_gap,
                position_usd=position_usd,
                shares=shares,
                exit_target=round(exit_target, 4),
                taker_fee=taker_fee,
                maker_rebate=maker_rebate,
                trigger_reason=trigger_reason,
                game_state=game_state,
                timestamp=datetime.now(
                    timezone.utc
                ).isoformat(),
                raw_edge=oracle_gap,
                net_edge_pct=(oracle_gap * shares
                               - taker_fee
                               + maker_rebate)
                              / position_usd,
            )

            await self.om.enter_position(
                signal,
                strategy="exception",
                position_type="exception",
            )
            self.wallet.state.exception_trades_today += 1
            logger.info(
                f"Exception trade fired: "
                f"{team_name} in {market.slug}"
            )

    async def monitor_loop(self):
        """Run every 30 seconds."""
        while True:
            await asyncio.sleep(30)
            try:
                await self.check_exception_opportunities()
            except Exception as e:
                logger.error(
                    f"Exception monitor error: {e}"
                )
