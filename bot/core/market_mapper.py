import asyncio
import logging
from datetime import datetime, timezone, timedelta
from thefuzz import fuzz
from typing import Optional, Tuple
from config import logger as config_logger
from data.database import upsert_market_mapping

logger = logging.getLogger("polyfarm.mapper")

SPORT_KEY_MAP = {
    "basketball_nba":        "NBA",
    "icehockey_nhl":         "NHL",
    "baseball_mlb":          "MLB",
    "basketball_ncaab":      "NCAAB",
    "americanfootball_ncaaf":"NCAAF",
    "americanfootball_nfl":  "NFL",
    "soccer_epl":            "EPL",
    "soccer_usa_mls":        "MLS",
    "soccer_mls":            "MLS",
    "soccer_uefa_champs_league": "UCL",
    "tennis_atp":            "ATP",
    "tennis_wta":            "WTA",
    "mma_mixed_martial_arts":"MMA",
    "golf_pga_tour":         "PGA",
}

class MarketMapper:

    def __init__(self, registry, market_loader):
        self.registry = registry
        self.loader = market_loader
        self._mapping_cache: dict = {}

    def _american_to_prob(self,
                          odds: float) -> float:
        """Convert American odds to implied probability.
        Does NOT include vig removal."""
        if odds < 0:
            return abs(odds) / (abs(odds) + 100)
        return 100 / (odds + 100)

    def _remove_vig(self,
                    yes_prob: float,
                    no_prob: float) -> Tuple[float, float]:
        """Normalize both sides to sum to 1.0."""
        total = yes_prob + no_prob
        if total == 0:
            return 0.5, 0.5
        return yes_prob / total, no_prob / total

    def _fuzzy_match_teams(self,
                            poly_home: str,
                            poly_away: str,
                            odds_home: str,
                            odds_away: str
                            ) -> Tuple[float, bool]:
        """
        Returns (best_score, is_home_away_match).
        Tries both orderings of home/away.
        """
        # Standard order
        score1 = (
            fuzz.ratio(
                poly_home.lower(), odds_home.lower()
            ) +
            fuzz.ratio(
                poly_away.lower(), odds_away.lower()
            )
        ) / 2

        # Reversed order (away teams sometimes flipped)
        score2 = (
            fuzz.ratio(
                poly_home.lower(), odds_away.lower()
            ) +
            fuzz.ratio(
                poly_away.lower(), odds_home.lower()
            )
        ) / 2

        return max(score1, score2), score1 >= score2

    def _times_within_window(self,
                              poly_time: str,
                              odds_time: str,
                              hours: int = 2) -> bool:
        """Returns True if times are within X hours."""
        try:
            if not poly_time or not odds_time:
                return True
            pt = datetime.fromisoformat(
                poly_time.replace("Z", "+00:00")
            )
            ot = datetime.fromisoformat(
                odds_time.replace("Z", "+00:00")
            )
            diff = abs((pt - ot).total_seconds())
            return diff <= hours * 3600
        except Exception:
            return True

    async def map_all_markets(self):
        """
        Attempt mapping for all markets in registry.
        Called after every market refresh.
        """
        markets = await self.registry.all_markets()
        for market in markets:
            await self.attempt_mapping(market.slug)

    async def attempt_mapping(self,
                               slug: str
                               ) -> Optional[dict]:
        """
        Attempt to map a Polymarket slug to Odds API.
        Returns mapping dict or None.
        """
        market = await self.registry.get(slug)
        if not market:
            return None

        sport = market.sport
        odds_events = [
            e for eid, e in
            self.loader.odds_data.items()
            if e.get("sport_key") == sport
        ]

        best_score = 0
        best_event = None

        for event in odds_events:
            odds_home = event.get("home_team", "")
            odds_away = event.get("away_team", "")
            odds_time = event.get(
                "commence_time", ""
            )

            if not self._times_within_window(
                market.start_time, odds_time
            ):
                continue

            score, _ = self._fuzzy_match_teams(
                market.home_team,
                market.away_team,
                odds_home,
                odds_away
            )

            if score > best_score:
                best_score = score
                best_event = event

        if not best_event:
            status = "UNCONFIRMED"
        elif best_score >= 95:
            status = "CONFIRMED"
        elif best_score >= 85:
            status = "FUZZY"
        else:
            status = "UNCONFIRMED"

        mapping = {
            "polymarket_slug": slug,
            "odds_api_event_id": best_event.get(
                "id"
            ) if best_event else None,
            "sport": sport,
            "teams": f"{market.home_team} vs "
                     f"{market.away_team}",
            "market_type": market.market_type,
            "mapping_status": status,
            "mapping_confidence": best_score / 100,
            "last_confirmed": (
                datetime.now(timezone.utc).isoformat()
                if status != "UNCONFIRMED" else None
            ),
            "failure_reason": (
                f"Best score: {best_score:.1f}%"
                if status == "UNCONFIRMED" else None
            ),
        }

        self._mapping_cache[slug] = mapping
        await upsert_market_mapping(mapping)
        return mapping

    def get_mapping(self, slug: str) -> Optional[dict]:
        return self._mapping_cache.get(slug)

    def get_sharp_probability(self,
                               slug: str,
                               max_age_seconds: int = 10
                               ) -> Optional[float]:
        """
        Returns sharp-book implied probability for
        the market's YES outcome.
        Returns None if data is stale or unavailable.
        """
        mapping = self._mapping_cache.get(slug)
        if not mapping:
            return None
        if mapping["mapping_status"] == "UNCONFIRMED":
            return None

        event_id = mapping.get("odds_api_event_id")
        if not event_id:
            return None

        last_updated = self.loader.odds_last_updated.get(
            event_id
        )
        if not last_updated:
            return None

        age = (
            datetime.now(timezone.utc) - last_updated
        ).total_seconds()
        if age > max_age_seconds:
            return None

        event = self.loader.odds_data.get(event_id)
        if not event:
            return None

        # Try Pinnacle first, fall back to DraftKings
        bookmaker_priority = [
            "pinnacle", "draftkings",
            "fanduel", "betmgm"
        ]
        # Use cached market_type from mapping
        mtype_map = {
            "moneyline": "h2h",
            "spread":    "spreads",
            "totals":    "totals",
        }
        odds_market = mtype_map.get(
            mapping.get("market_type", "moneyline"),
            "h2h"
        )

        for bookmaker_key in bookmaker_priority:
            for bm in event.get("bookmakers", []):
                if bm["key"] != bookmaker_key:
                    continue
                for mkt in bm.get("markets", []):
                    if mkt["key"] != odds_market:
                        continue
                    outcomes = mkt.get("outcomes", [])
                    if len(outcomes) < 2:
                        continue

                    # Match outcome to home/away
                    # YES = home team wins for moneyline
                    home_outcome = None
                    away_outcome = None
                    for o in outcomes:
                        if fuzz.ratio(
                            o["name"].lower(),
                            event.get(
                                "home_team", ""
                            ).lower()
                        ) > 80:
                            home_outcome = o
                        else:
                            away_outcome = o

                    if not home_outcome:
                        continue

                    yes_odds = home_outcome["price"]
                    no_odds = (
                        away_outcome["price"]
                        if away_outcome else -yes_odds
                    )

                    yes_prob = self._american_to_prob(
                        yes_odds
                    )
                    no_prob = self._american_to_prob(
                        no_odds
                    )
                    yes_clean, _ = self._remove_vig(
                        yes_prob, no_prob
                    )
                    return yes_clean

        return None
