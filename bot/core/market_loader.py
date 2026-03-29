"""
Market discovery and registry using the official
polymarket-us SDK. Loads active moneyline markets
for target sports, maintains a registry of
MarketInfo objects, and manages WebSocket subs.
"""
import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from config import logger as config_logger

logger = logging.getLogger("polyfarm.market_loader")

MIN_MARKET_VOLUME = 20000


def parse_bbo(bbo: dict) -> tuple:
    """
    Parse response from client.markets.bbo(slug).
    Returns (bid, ask, current_price) as floats.
    bestBid and bestAsk are OBJECTS with "value" key
    in the BBO endpoint (different from events.list).
    """
    try:
        md = bbo.get("marketData", {})
        bid = float(md.get("bestBid", {}).get("value", 0) or 0)
        ask = float(md.get("bestAsk", {}).get("value", 1) or 1)
        cur = float(md.get("currentPx", {}).get("value", bid) or bid)
        return bid, ask, cur
    except (TypeError, ValueError, KeyError):
        return 0.0, 1.0, 0.5


@dataclass
class MarketInfo:
    slug: str
    event_id: str = ""
    event_slug: str = ""
    sport: str = ""
    league: str = ""
    game_id: int = 0
    sportradar_game_id: str = ""
    home_team: str = ""
    away_team: str = ""
    home_team_id: int = 0
    away_team_id: int = 0
    home_record: str = ""
    away_record: str = ""
    home_ranking: str = ""
    away_ranking: str = ""
    home_conference: str = ""
    away_conference: str = ""
    yes_price: float = 0.5
    bid_price: float = 0.5
    volume: float = 0.0
    liquidity: float = 0.0
    is_live: bool = False
    is_finished: bool = False
    current_score: Optional[str] = None
    current_period: Optional[str] = None
    time_elapsed: Optional[str] = None
    game_start_time: str = ""
    main_spread_line: float = 0.0
    main_total_line: float = 0.0
    football_down: int = 0
    football_yard: int = 0
    possession_team_id: int = 0
    latest_update_title: str = ""
    latest_update_team: str = ""
    latest_update_clock: str = ""
    market_type: str = "moneyline"
    series_slug: str = ""
    time_remaining_seconds: Optional[int] = None


class MarketRegistry:
    """Thread-safe market data store."""

    def __init__(self):
        self._markets: dict[str, MarketInfo] = {}
        self._lock = asyncio.Lock()

    async def update(self, slug, info):
        async with self._lock:
            self._markets[slug] = info

    async def remove(self, slug):
        async with self._lock:
            self._markets.pop(slug, None)

    async def get(self, slug):
        async with self._lock:
            return self._markets.get(slug)

    async def all_slugs(self):
        async with self._lock:
            return list(self._markets.keys())

    async def all_markets(self):
        async with self._lock:
            return list(self._markets.values())

    async def count(self):
        async with self._lock:
            return len(self._markets)


class MarketLoader:

    def __init__(self, client, registry, ws_manager=None, min_volume=None):
        self.client = client
        self.registry = registry
        self.ws_manager = ws_manager
        self.min_volume = min_volume or MIN_MARKET_VOLUME

    async def load_all_markets(self):
        """Load all active sports moneyline markets."""
        try:
            new_slugs = []

            # Load scheduled games
            scheduled = await self._fetch_events(live=False)
            for slug in scheduled:
                new_slugs.append(slug)

            # Load live games
            live = await self._fetch_events(live=True)
            for slug in live:
                if slug not in new_slugs:
                    new_slugs.append(slug)

            # Subscribe WebSocket to all slugs
            if self.ws_manager and new_slugs:
                await self.ws_manager.subscribe_markets(new_slugs)

            count = await self.registry.count()
            logger.info(f"Market refresh: {count} active markets, {len(new_slugs)} slugs")

        except Exception as e:
            logger.error(f"Market load error: {e}")

    async def _fetch_events(self, live=False):
        """Fetch events from SDK and build registry."""
        slugs = []
        try:
            params = {
                "active": True,
                "live": live,
                "ended": False,
                "categories": "sports",
                "limit": 100,
            }
            result = await self.client.events.list(params)
            events = result.get("events", [])

            for event in events:
                event_id = event.get("id", "")
                event_slug = event.get("slug", "")
                is_live = event.get("live", False)
                is_ended = event.get("ended", False)
                series_slug = event.get("seriesSlug", "")
                game_id = event.get("gameId", 0)
                sportradar_id = event.get("sportradarGameId", "")
                start_time = event.get("startTime", "") or event.get("eventDate", "")

                if is_ended:
                    continue

                # Extract teams
                teams = event.get("teams", [])
                home = teams[0] if len(teams) > 0 else {}
                away = teams[1] if len(teams) > 1 else {}

                # Extract event state
                state = event.get("eventState", {}) or {}
                score = state.get("score") or event.get("score")
                period = state.get("period") or event.get("period")
                elapsed = state.get("elapsed") or event.get("elapsed")
                spread_line = state.get("mainSpreadLine", 0) or 0
                total_line = state.get("mainTotalLine", 0) or 0

                # Football state
                fb = state.get("footballState", {}) or {}
                fb_down = fb.get("down", 0) or 0
                fb_yard = fb.get("yard", 0) or 0
                fb_possession = fb.get("possessionProviderId", 0) or 0

                # Latest update
                meta = event.get("metadata", {}) or {}
                update = meta.get("latestGameUpdate", {}) or {}

                # Determine sport from series slug or team league
                sport = ""
                league = home.get("league", "") or away.get("league", "")
                if league:
                    sport_map = {
                        "nba": "basketball", "ncaab": "basketball",
                        "nfl": "football", "ncaaf": "football",
                        "mlb": "baseball", "nhl": "ice_hockey",
                        "mls": "soccer", "epl": "soccer",
                    }
                    sport = sport_map.get(league.lower(), league.lower())

                # Filter markets — moneyline only
                for market in event.get("markets", []):
                    mtype = market.get("sportsMarketTypeV2", "")
                    if mtype != "SPORTS_MARKET_TYPE_MONEYLINE":
                        continue
                    if not market.get("active"):
                        continue
                    if not market.get("acceptingOrders"):
                        continue

                    slug = market.get("slug")
                    if not slug:
                        continue

                    vol = float(market.get("volumeNum", 0) or 0)
                    if vol < self.min_volume:
                        continue

                    # In events.list(), bestBid/bestAsk are PLAIN NUMBERS
                    bid_price = float(market.get("bestBid", 0) or 0)
                    ask_price = float(market.get("bestAsk", 0) or 0)
                    liq = float(market.get("liquidityNum", 0) or 0)
                    mkt_start = market.get("gameStartTime", "") or start_time

                    info = MarketInfo(
                        slug=slug,
                        event_id=str(event_id),
                        event_slug=event_slug,
                        sport=sport,
                        league=league,
                        game_id=game_id,
                        sportradar_game_id=str(sportradar_id),
                        home_team=home.get("name", ""),
                        away_team=away.get("name", ""),
                        home_team_id=home.get("id", 0) or 0,
                        away_team_id=away.get("id", 0) or 0,
                        home_record=home.get("record", ""),
                        away_record=away.get("record", ""),
                        home_ranking=home.get("ranking", ""),
                        away_ranking=away.get("ranking", ""),
                        home_conference=home.get("conference", ""),
                        away_conference=away.get("conference", ""),
                        yes_price=ask_price,
                        bid_price=bid_price,
                        volume=vol,
                        liquidity=liq,
                        is_live=is_live,
                        is_finished=is_ended,
                        current_score=score,
                        current_period=period,
                        time_elapsed=elapsed,
                        game_start_time=mkt_start,
                        main_spread_line=float(spread_line or 0),
                        main_total_line=float(total_line or 0),
                        football_down=fb_down,
                        football_yard=fb_yard,
                        possession_team_id=int(fb_possession or 0),
                        latest_update_title=update.get("title", ""),
                        latest_update_team=update.get("team", ""),
                        latest_update_clock=update.get("clock", ""),
                        market_type="moneyline",
                        series_slug=series_slug,
                    )
                    await self.registry.update(slug, info)
                    slugs.append(slug)

        except Exception as e:
            logger.error(f"Event fetch error (live={live}): {e}")

        return slugs

    async def refresh_loop(self):
        """Refresh markets every 5 minutes."""
        while True:
            await asyncio.sleep(300)
            await self.load_all_markets()

    async def update_game_state(self, slug):
        """Update live game state for a market."""
        try:
            market = await self.registry.get(slug)
            if not market or not market.is_live:
                return
            event = await self.client.events.retrieve(market.event_id)
            if not event:
                return
            state = event.get("eventState", {}) or {}
            market.current_score = state.get("score") or event.get("score")
            market.current_period = state.get("period") or event.get("period")
            market.time_elapsed = state.get("elapsed") or event.get("elapsed")
            market.is_finished = event.get("ended", False)
            await self.registry.update(slug, market)
        except Exception as e:
            logger.debug(f"Game state update error {slug}: {e}")
