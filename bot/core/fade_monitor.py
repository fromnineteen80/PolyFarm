import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from config import (
    FADE_TEAMS, FADE_MIN_GAP,
    FADE_MAX_POSITION_PCT,
    FADE_MAX_TRADES_PER_SESSION,
    FADE_MIN_VOLUME, FADE_MAX_BID_ASK_SPREAD,
    FADE_REPRICE_PCT,
    FAVORITES_FLOOR,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
)

logger = logging.getLogger("polyfarm.fade")

@dataclass
class FadeSignal:
    slug: str
    sport: str
    teams: str
    fade_team: str
    opponent: str
    poly_price: float
    sharp_prob: float
    oracle_gap: float
    position_usd: float
    shares: int
    exit_target: float
    taker_fee: float
    maker_rebate: float
    game_state: dict
    timestamp: str
    strategy: str = "fade"
    band: str = "FADE"
    raw_edge: float = 0.0
    net_edge_pct: float = 0.0
    confidence: float = 0.85
    is_live: bool = True
    market_type: str = "moneyline"

class FadeMonitor:

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

    def _budget_remaining(self) -> bool:
        return (
            self.wallet.state.fade_trades_today
            < FADE_MAX_TRADES_PER_SESSION
        )

    def _get_fade_team(self, market) -> tuple | None:
        """
        Returns (fade_team_name, config, opponent_name)
        if a trailing team in this market is a fade team.
        None otherwise.
        """
        for team_name, config in FADE_TEAMS.items():
            if config["sport"] != market.sport:
                continue
            home = market.home_team.lower()
            away = market.away_team.lower()
            t = team_name.lower()
            if t in home or t in away:
                # Determine if this team is trailing
                score = market.current_score or ""
                is_trailing = self._is_trailing(
                    team_name, market, score
                )
                if is_trailing:
                    # Opponent is the leading team
                    if t in home:
                        opponent = market.away_team
                    else:
                        opponent = market.home_team
                    return team_name, config, opponent
        return None

    def _is_trailing(self,
                      team_name: str,
                      market,
                      score: str) -> bool:
        """Check if team is currently trailing."""
        try:
            if not score:
                return False
            parts = str(score).split("-")
            if len(parts) != 2:
                return False
            home_s = int(parts[0].strip())
            away_s = int(parts[1].strip())
            t = team_name.lower()
            home = market.home_team.lower()
            if t in home:
                return home_s < away_s
            else:
                return away_s < home_s
        except Exception:
            return False

    def _deficit_in_range(self,
                           config: dict,
                           market,
                           score: str) -> bool:
        """Check deficit is in fade range."""
        try:
            parts = str(score).split("-")
            if len(parts) != 2:
                return False
            scores = sorted([
                int(parts[0].strip()),
                int(parts[1].strip())
            ])
            deficit = scores[1] - scores[0]
            min_d = config["deficit_range"][0]
            max_d = config["deficit_range"][1]
            return min_d <= deficit <= max_d
        except Exception:
            return False

    def _game_window_valid(self,
                            config: dict,
                            market,
                            game_state: dict) -> bool:
        """Check game is in valid fade window."""
        sport = market.sport
        time_rem = game_state.get(
            "time_remaining_seconds", 0
        )

        if sport == "baseball_mlb":
            innings = config.get(
                "game_window_innings", (5, 9)
            )
            inning = game_state.get("inning", 0)
            return innings[0] <= inning <= innings[1]

        elif sport in ("basketball_nba",
                       "basketball_ncaab"):
            quarters = config.get(
                "game_window", {}
            ).get("quarters", [3, 4])
            q = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", 360)
            return q in quarters and \
                   time_rem >= min_s

        elif sport == "icehockey_nhl":
            periods = config.get(
                "game_window", {}
            ).get("periods", [2, 3])
            p = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", 480)
            return p in periods and time_rem >= min_s

        elif sport in ("americanfootball_nfl",
                       "americanfootball_ncaaf"):
            quarters = config.get(
                "game_window", {}
            ).get("quarters", [3, 4])
            q = game_state.get("period", 0)
            min_s = config.get(
                "game_window", {}
            ).get("min_seconds_remaining", 480)
            return q in quarters and time_rem >= min_s

        elif "soccer" in sport:
            r = config.get(
                "game_window", {}
            ).get("minute_range", (50, 85))
            minute = game_state.get("game_minute", 0)
            return r[0] <= minute <= r[1]

        return False

    async def check_fade_opportunities(self):
        """Check all live markets for fade signals."""
        if not self._budget_remaining():
            return
        if not self.wallet.can_enter("fade"):
            return

        markets = await self.registry.all_markets()
        for market in markets:
            if not market.is_live:
                continue
            if market.is_finished:
                continue
            if not market.current_score:
                continue

            result = self._get_fade_team(market)
            if not result:
                continue
            fade_team, config, opponent = result

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
            }

            if not self._deficit_in_range(
                config, market,
                market.current_score
            ):
                continue

            if not self._game_window_valid(
                config, market, game_state
            ):
                continue

            # We bet on the OPPONENT (leading team)
            # YES price on opponent
            # For moneyline: if fade team is away,
            # opponent is home — their YES price
            # Note: Polymarket YES = home team wins
            # Adjust based on which side is opponent
            poly_price = market.yes_price
            if opponent.lower() in \
               market.away_team.lower():
                # Opponent is away team
                # Away = NO = 1 - YES price
                poly_price = 1 - market.yes_price

            if poly_price < FAVORITES_FLOOR:
                continue

            # Get oracle gap on opponent side
            sharp_prob = self.mapper.get_sharp_probability(
                market.slug
            )
            if not sharp_prob:
                continue
            # Adjust for opponent side
            if opponent.lower() in \
               market.away_team.lower():
                sharp_prob = 1 - sharp_prob

            oracle_gap = sharp_prob - poly_price

            # Min gap by confidence tier
            min_gap = FADE_MIN_GAP.get(
                config.get("confidence", "medium"),
                0.10
            )
            if oracle_gap < min_gap:
                continue

            if market.volume < FADE_MIN_VOLUME:
                continue

            try:
                bbo = await self.client.markets.bbo(
                    market.slug
                )
                bid = float(
                    bbo.get("bid", {}).get("price", 0)
                )
                ask = float(
                    bbo.get("ask", {}).get("price", 1)
                )
                spread = ask - bid
                if spread > FADE_MAX_BID_ASK_SPREAD:
                    continue
            except Exception:
                continue

            if self.pm.has_position(market.slug):
                continue

            position_usd = (
                self.wallet.get_position_size_usd(
                    "fade"
                )
            )
            if position_usd <= 0:
                continue

            shares = int(position_usd / poly_price)
            if shares < 1:
                continue

            exit_target = poly_price + (
                oracle_gap * FADE_REPRICE_PCT
            )
            entry_notional = shares * poly_price
            taker_fee = entry_notional * TAKER_FEE_RATE
            exit_notional = shares * (1 - exit_target)
            maker_rebate = (
                exit_notional * MAKER_REBATE_RATE
            )

            signal = FadeSignal(
                slug=market.slug,
                sport=market.sport,
                teams=f"{market.home_team} vs "
                      f"{market.away_team}",
                fade_team=fade_team,
                opponent=opponent,
                poly_price=poly_price,
                sharp_prob=sharp_prob,
                oracle_gap=oracle_gap,
                position_usd=position_usd,
                shares=shares,
                exit_target=round(exit_target, 4),
                taker_fee=taker_fee,
                maker_rebate=maker_rebate,
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
                strategy="fade",
                position_type="fade",
                fade_team=fade_team,
            )
            self.wallet.state.fade_trades_today += 1
            logger.info(
                f"Fade trade: {fade_team} trailing "
                f"backing {opponent} in {market.slug}"
            )

    async def monitor_loop(self):
        """Run every 30 seconds."""
        while True:
            await asyncio.sleep(30)
            try:
                await self.check_fade_opportunities()
            except Exception as e:
                logger.error(
                    f"Fade monitor error: {e}"
                )
