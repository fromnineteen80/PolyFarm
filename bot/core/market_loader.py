"""
Market discovery and registry using Polymarket US
v2 league endpoints for current events and the
SDK for BBO/order operations.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
import httpx
from config import logger as config_logger

logger = logging.getLogger("polyfarm.market_loader")

MIN_MARKET_VOLUME = 0  # v2 doesn't return volume; allow all

GATEWAY_URL = "https://gateway.polymarket.us"

# Leagues to poll via v2 endpoint
TARGET_LEAGUES = [
    "nba", "nfl", "mlb", "nhl",
    "ncaab", "ncaaf",
]

# Sport key mapping from league to our internal format
LEAGUE_TO_SPORT = {
    "nba": "basketball_nba",
    "ncaab": "basketball_ncaab",
    "nfl": "americanfootball_nfl",
    "ncaaf": "americanfootball_ncaaf",
    "mlb": "baseball_mlb",
    "nhl": "icehockey_nhl",
}


def parse_bbo(bbo: dict) -> tuple:
    """
    Parse response from client.markets.bbo(slug).
    bestBid and bestAsk are OBJECTS with "value" key.
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
    market_sides: list = None
    home_color: str = ""
    away_color: str = ""


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
        self._http = None

    async def _get_http(self):
        if self._http is None or self._http.is_closed:
            self._http = httpx.AsyncClient(timeout=15)
        return self._http

    async def load_all_markets(self):
        """Load current moneyline markets from v2 league endpoints."""
        try:
            new_slugs = []
            for league in TARGET_LEAGUES:
                slugs = await self._fetch_league(league)
                for s in slugs:
                    if s not in new_slugs:
                        new_slugs.append(s)

            # Also try v2 sports for soccer
            for sport_slug in ["soccer"]:
                slugs = await self._fetch_sport_v2(sport_slug)
                for s in slugs:
                    if s not in new_slugs:
                        new_slugs.append(s)

            if self.ws_manager and new_slugs:
                await self.ws_manager.subscribe_markets(new_slugs)

            count = await self.registry.count()
            logger.info(f"Market refresh: {count} active markets, {len(new_slugs)} slugs")

        except Exception as e:
            logger.error(f"Market load error: {e}")

    async def _fetch_league(self, league: str) -> list:
        """Fetch events from v2 /leagues/{league}/events endpoint."""
        slugs = []
        try:
            http = await self._get_http()
            r = await http.get(f"{GATEWAY_URL}/v2/leagues/{league}/events")
            if r.status_code != 200:
                logger.warning(f"v2 leagues/{league} returned {r.status_code}")
                return slugs

            data = r.json()
            events = data.get("events", [])
            sport = LEAGUE_TO_SPORT.get(league, league)

            for event in events:
                event_slugs = await self._process_event(event, sport, league)
                slugs.extend(event_slugs)

        except Exception as e:
            logger.error(f"League fetch error {league}: {e}")
        return slugs

    async def _fetch_sport_v2(self, sport_slug: str) -> list:
        """Fetch events from v2 /sports/{sport}/events endpoint."""
        slugs = []
        try:
            http = await self._get_http()
            r = await http.get(f"{GATEWAY_URL}/v2/sports/{sport_slug}/events")
            if r.status_code != 200:
                return slugs

            data = r.json()
            events = data.get("events", [])
            league_hint = data.get("league", sport_slug)

            for event in events:
                # Determine sport from event league if available
                event_league = ""
                teams = event.get("teams", [])
                if teams:
                    event_league = teams[0].get("league", "")
                sport_key = LEAGUE_TO_SPORT.get(event_league, f"soccer_{sport_slug}")
                event_slugs = await self._process_event(event, sport_key, event_league or sport_slug)
                slugs.extend(event_slugs)

        except Exception as e:
            logger.error(f"Sport v2 fetch error {sport_slug}: {e}")
        return slugs

    async def _process_event(self, event: dict, sport: str, league: str) -> list:
        """Process one event and extract moneyline markets."""
        slugs = []

        event_id = str(event.get("id", ""))
        event_slug = event.get("slug", "")
        is_live = event.get("live", False)
        is_ended = event.get("ended", False)
        series_slug = event.get("seriesSlug", "")
        game_id = event.get("gameId", 0) or 0
        sportradar_id = event.get("sportradarGameId", "") or ""
        start_time = event.get("startTime", "") or ""
        score = event.get("score", "") or ""
        period = event.get("period", "") or ""
        elapsed = event.get("elapsed", "") or ""

        if is_ended:
            return slugs

        # Extract teams
        teams = event.get("teams", [])
        home = teams[0] if len(teams) > 0 else {}
        away = teams[1] if len(teams) > 1 else {}

        def full_team_name(t):
            safe = t.get("safeName", "")
            short = t.get("name", "")
            if safe and short:
                return f"{safe} {short}"
            return short or safe or ""

        for market in event.get("markets", []):
            mtype = market.get("marketType", "")
            stype = market.get("sportsMarketTypeV2", "")
            if mtype != "moneyline" and "MONEYLINE" not in stype:
                continue
            if not market.get("active"):
                continue

            slug = market.get("slug")
            if not slug:
                continue

            # Get price from marketSides
            market_sides = market.get("marketSides", [])
            yes_price = 0.5
            for side in market_sides:
                if side.get("long"):
                    price_str = side.get("price", "0.5")
                    try:
                        yes_price = float(price_str)
                    except (ValueError, TypeError):
                        yes_price = 0.5
                    break

            mkt_start = market.get("gameStartTime", "") or start_time

            info = MarketInfo(
                slug=slug,
                event_id=event_id,
                event_slug=event_slug,
                sport=sport,
                league=league,
                game_id=game_id,
                sportradar_game_id=str(sportradar_id),
                home_team=full_team_name(home),
                away_team=full_team_name(away),
                home_color=home.get("colorPrimary", ""),
                away_color=away.get("colorPrimary", ""),
                home_team_id=home.get("id", 0) or 0,
                away_team_id=away.get("id", 0) or 0,
                home_record=home.get("record", ""),
                away_record=away.get("record", ""),
                home_ranking=home.get("ranking", ""),
                away_ranking=away.get("ranking", ""),
                home_conference=home.get("conference", ""),
                away_conference=away.get("conference", ""),
                yes_price=yes_price,
                bid_price=0.0,
                volume=0.0,
                liquidity=0.0,
                is_live=is_live,
                is_finished=is_ended,
                current_score=score if score else None,
                current_period=period if period else None,
                time_elapsed=elapsed if elapsed else None,
                game_start_time=mkt_start,
                market_type="moneyline",
                series_slug=series_slug,
                market_sides=market_sides,
            )
            await self.registry.update(slug, info)
            slugs.append(slug)

        return slugs

    async def refresh_loop(self):
        """Refresh markets every 5 minutes."""
        while True:
            await asyncio.sleep(300)
            await self.load_all_markets()

    async def flush_to_supabase(self, odds_api=None, ws_markets=None):
        """Write all markets to Supabase so dashboard can read them."""
        from data.database import upsert_market
        markets = await self.registry.all_markets()
        for m in markets:
            try:
                data = {
                    "market_slug": m.slug,
                    "event_id": m.event_id,
                    "event_slug": m.event_slug,
                    "sport": m.sport,
                    "league": m.league,
                    "game_id": m.game_id,
                    "sportradar_game_id": m.sportradar_game_id,
                    "home_team": m.home_team,
                    "away_team": m.away_team,
                    "home_team_id": m.home_team_id,
                    "away_team_id": m.away_team_id,
                    "home_record": m.home_record,
                    "away_record": m.away_record,
                    "home_ranking": m.home_ranking,
                    "away_ranking": m.away_ranking,
                    "home_conference": m.home_conference,
                    "away_conference": m.away_conference,
                    "home_color": m.home_color,
                    "away_color": m.away_color,
                    "yes_price": m.yes_price,
                    "bid_price": m.bid_price,
                    "volume": m.volume,
                    "liquidity": m.liquidity,
                    "is_live": m.is_live,
                    "is_finished": m.is_finished,
                    "game_status": "live" if m.is_live else "finished" if m.is_finished else "upcoming",
                    "game_score": m.current_score,
                    "game_period": m.current_period,
                    "game_elapsed": m.time_elapsed,
                    "game_start_time": m.game_start_time or None,
                    "main_spread_line": m.main_spread_line,
                    "main_total_line": m.main_total_line,
                    "market_type": m.market_type,
                    "series_slug": m.series_slug,
                }
                if odds_api and odds_api.is_matched(m.slug):
                    consensus = odds_api.get_consensus_data(m.slug)
                    if consensus:
                        sharp = odds_api.get_fair_prob(m.slug, "home")
                        data["current_sharp_prob"] = sharp
                        data["current_edge"] = round(sharp - m.yes_price, 4) if sharp else None
                        data["odds_api_event_id"] = consensus.get("odds_api_event_id", "")
                        data["match_confidence"] = 1.0
                        data["last_sharp_update"] = consensus.get("updated_at")

                if ws_markets:
                    velocity, direction = ws_markets.calculate_velocity(m.slug)
                    pressure = ws_markets.get_net_buy_pressure(m.slug)
                    data["current_price_velocity"] = velocity
                    data["current_price_direction"] = direction
                    data["current_net_buy_pressure"] = pressure
                    data["last_movement_update"] = datetime.now(timezone.utc).isoformat()

                await upsert_market(data)
            except Exception as e:
                logger.error(f"Market flush error {m.slug}: {e}")
        logger.info(f"Flushed {len(markets)} markets to Supabase")

    async def flush_loop(self, odds_api=None, ws_markets=None):
        """Flush markets to Supabase every 60 seconds."""
        logger.info("Market flush loop started")
        while True:
            await asyncio.sleep(60)
            try:
                await self.flush_to_supabase(odds_api, ws_markets)
            except Exception as e:
                logger.error(f"Market flush loop error: {e}")

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
