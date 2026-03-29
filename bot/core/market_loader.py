import asyncio
import logging
import requests
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from config import (
    ODDS_API_BASE,
    ODDS_SPORTS_CONFIGURED,
    ODDS_BOOKMAKERS, ODDS_MARKETS,
    ODDS_POLL_INTERVAL,
    logger as config_logger
)

logger = logging.getLogger("polyfarm.market_loader")

@dataclass
class MarketInfo:
    slug: str
    sport: str
    market_type: str
    home_team: str
    away_team: str
    start_time: str
    yes_price: float
    volume: float
    is_live: bool = False
    current_score: Optional[str] = None
    current_period: Optional[str] = None
    time_remaining_seconds: Optional[int] = None
    is_finished: bool = False

class MarketRegistry:
    """Thread-safe market data store."""

    def __init__(self):
        self._markets: dict[str, MarketInfo] = {}
        self._lock = asyncio.Lock()

    async def update(self, slug: str,
                     info: MarketInfo):
        async with self._lock:
            self._markets[slug] = info

    async def remove(self, slug: str):
        async with self._lock:
            self._markets.pop(slug, None)

    async def get(self, slug: str
                  ) -> Optional[MarketInfo]:
        async with self._lock:
            return self._markets.get(slug)

    async def all_slugs(self) -> list[str]:
        async with self._lock:
            return list(self._markets.keys())

    async def all_markets(self) -> list[MarketInfo]:
        async with self._lock:
            return list(self._markets.values())

    async def count(self) -> int:
        async with self._lock:
            return len(self._markets)

class MarketLoader:

    def __init__(self, client,
                 registry: MarketRegistry,
                 ws_manager=None):
        self.client = client
        self.registry = registry
        self.ws_manager = ws_manager
        self.odds_data: dict = {}
        self.odds_last_updated: dict = {}
        self.valid_sports: list = []

    async def validate_sport_keys(self) -> list:
        """
        Validates configured sport keys against
        actual Odds API available sports.
        Returns list of valid sport keys.
        """
        try:
            odds_key = __import__(
                "os"
            ).environ["ODDS_API_KEY"]
            resp = requests.get(
                f"{ODDS_API_BASE}/sports",
                params={"apiKey": odds_key},
                timeout=10
            )
            if resp.status_code != 200:
                logger.warning(
                    f"Odds API sports validation "
                    f"failed: {resp.status_code}"
                )
                return ODDS_SPORTS_CONFIGURED

            available = {
                s["key"] for s in resp.json()
            }
            valid = []
            for sport in ODDS_SPORTS_CONFIGURED:
                if sport in available:
                    valid.append(sport)
                elif sport == "soccer_usa_mls" and \
                     "soccer_mls" in available:
                    valid.append("soccer_mls")
                    logger.info(
                        "Using soccer_mls instead of "
                        "soccer_usa_mls"
                    )
                else:
                    logger.warning(
                        f"Invalid Odds API sport "
                        f"key: {sport}"
                    )

            logger.info(
                f"Validated {len(valid)} sport keys"
            )
            self.valid_sports = valid
            return valid

        except Exception as e:
            logger.error(
                f"Sport key validation error: {e}"
            )
            return ODDS_SPORTS_CONFIGURED

    async def refresh_markets(self):
        """
        Loads all active markets from Polymarket.
        Called on startup and every 5 minutes.
        """
        try:
            tasks = [
                self._load_sport(sport)
                for sport in self.valid_sports
            ]
            results = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            new_slugs = []
            for result in results:
                if isinstance(result, Exception):
                    logger.error(
                        f"Sport load error: {result}"
                    )
                    continue
                if result:
                    new_slugs.extend(result)

            # Subscribe WebSocket to new slugs
            if self.ws_manager and new_slugs:
                await self.ws_manager.subscribe_slugs(
                    new_slugs
                )

            count = await self.registry.count()
            logger.info(
                f"Market refresh: {count} active markets"
            )

        except Exception as e:
            logger.error(f"Market refresh error: {e}")

    async def _load_sport(self,
                           sport: str) -> list[str]:
        """
        Loads all markets for one sport.
        Inspect SDK for correct method name:
        python -c "from polymarket_us import
          AsyncPolymarketUS;
          help(AsyncPolymarketUS().sports)"
        """
        new_slugs = []
        try:
            # Try get_events_by_sport_slug first
            # Fall back to events.list if not available
            try:
                events = await (
                    self.client.sports
                    .get_events_by_sport_slug(sport)
                )
            except AttributeError:
                events = await self.client.events.list({
                    "active": True,
                    "limit": 100
                })
                events = events.get("events", [])

            for event in events:
                for market in event.get(
                    "markets", []
                ):
                    slug = market.get("slug")
                    if not slug:
                        continue
                    volume = float(
                        market.get("volume", 0) or 0
                    )
                    # Skip props below $10k volume
                    mtype = market.get(
                        "market_type", "moneyline"
                    )
                    if mtype == "prop" and \
                       volume < 10000:
                        continue

                    yes_price = float(
                        market.get("yes_price", 0.5)
                        or 0.5
                    )
                    info = MarketInfo(
                        slug=slug,
                        sport=sport,
                        market_type=mtype,
                        home_team=event.get(
                            "home_team", ""
                        ),
                        away_team=event.get(
                            "away_team", ""
                        ),
                        start_time=event.get(
                            "start_time", ""
                        ),
                        yes_price=yes_price,
                        volume=volume,
                        is_live=event.get(
                            "is_live", False
                        ),
                        current_score=event.get(
                            "score"
                        ),
                        current_period=event.get(
                            "period"
                        ),
                        time_remaining_seconds=event.get(
                            "time_remaining_seconds"
                        ),
                        is_finished=event.get(
                            "is_finished", False
                        ),
                    )
                    await self.registry.update(slug, info)
                    new_slugs.append(slug)

        except Exception as e:
            logger.error(
                f"Error loading sport {sport}: {e}"
            )

        return new_slugs

    async def poll_odds(self):
        """
        Polls The Odds API for all active sports.
        Runs every ODDS_POLL_INTERVAL seconds.
        """
        import os
        odds_key = os.environ.get("ODDS_API_KEY")
        if not odds_key:
            logger.error("ODDS_API_KEY not set")
            return

        for sport in self.valid_sports:
            try:
                resp = requests.get(
                    f"{ODDS_API_BASE}/sports/"
                    f"{sport}/odds",
                    params={
                        "apiKey": odds_key,
                        "regions": "us",
                        "markets": ODDS_MARKETS,
                        "bookmakers": ODDS_BOOKMAKERS,
                        "oddsFormat": "american",
                    },
                    timeout=10
                )
                if resp.status_code == 200:
                    events = resp.json()
                    for event in events:
                        eid = event.get("id")
                        self.odds_data[eid] = event
                        self.odds_last_updated[eid] = (
                            datetime.now(timezone.utc)
                        )
                elif resp.status_code == 429:
                    logger.warning(
                        "Odds API rate limit hit"
                    )
                    break
                else:
                    logger.warning(
                        f"Odds API {sport}: "
                        f"{resp.status_code}"
                    )
            except Exception as e:
                logger.error(
                    f"Odds poll error {sport}: {e}"
                )

    async def refresh_loop(self):
        """Refresh markets every 5 minutes."""
        await self.validate_sport_keys()
        await self.refresh_markets()
        while True:
            await asyncio.sleep(300)
            await self.refresh_markets()

    async def poll_loop(self):
        """Poll odds every ODDS_POLL_INTERVAL seconds."""
        while True:
            await self.poll_odds()
            await asyncio.sleep(ODDS_POLL_INTERVAL)

    async def update_game_state(self, slug: str):
        """Update live game state for a market."""
        try:
            market = await self.registry.get(slug)
            if not market or not market.is_live:
                return
            try:
                event = await (
                    self.client.events
                    .retrieve_by_slug(slug)
                )
            except AttributeError:
                return

            market.current_score = event.get("score")
            market.current_period = event.get("period")
            market.time_remaining_seconds = event.get(
                "time_remaining_seconds"
            )
            market.is_finished = event.get(
                "is_finished", False
            )
            await self.registry.update(slug, market)
        except Exception as e:
            logger.debug(
                f"Game state update error {slug}: {e}"
            )
