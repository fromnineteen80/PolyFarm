"""
PolyFarm Pipeline — the complete data flow from
API discovery to trade execution.

This module is the single entry point for all
market data operations. It owns the pipeline:

Step 1: Discover leagues (Polymarket v2/sports)
Step 2: Load teams (Polymarket v2/leagues/{slug}/events)
Step 3: Discover Odds API sport keys (Odds API v4/sports)
Step 4: Load odds + Odds API team names (Odds API v4/sports/{key}/odds)
Step 5: Match teams across APIs
Step 6: Load games from Polymarket
Step 7: Match games using team bridge
Step 8: Calculate edge
Step 9: Write to Supabase
Step 10: Trade (via edge detector)
Step 11: Report (via alerts)
"""
import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Optional
import httpx
import aiohttp

logger = logging.getLogger("polyfarm.pipeline")

POLYMARKET_GATEWAY = "https://gateway.polymarket.us"
ODDS_API_BASE = "https://api.the-odds-api.com"

# Sports we trade — must match Polymarket v2/sports sport names
TARGET_SPORTS = {"Basketball", "Football", "Ice Hockey", "Baseball", "Soccer"}


def normalize_team(name: str) -> str:
    """Normalize team name for comparison."""
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r"[^\w\s]", "", n)
    n = re.sub(r"\b(fc|sc|cf|afc|the)\s*$", "", n)
    n = re.sub(r"^the\s+", "", n)
    return n.strip()


def build_full_name(team: dict) -> str:
    """Build canonical team name from Polymarket team data.
    Handles: safeName=name (duplicates), trailing abbreviations,
    containment (one name inside the other)."""
    safe = (team.get("safeName", "") or "").strip()
    short = (team.get("name", "") or "").strip()
    if not short:
        return safe
    if not safe:
        return short
    if safe.lower() == short.lower():
        return short
    # Strip single trailing letter (e.g. "Los Angeles L")
    safe_clean = re.sub(r'\s+[A-Z]$', '', safe).strip()
    if short.lower() in safe_clean.lower():
        return safe_clean
    if safe_clean.lower() in short.lower():
        return short
    if safe_clean:
        return f"{safe_clean} {short}"
    return short


class Pipeline:
    """The complete PolyFarm data pipeline."""

    def __init__(self, odds_api_key: str, db):
        self.odds_api_key = odds_api_key
        self.db = db

        # Step 1 output: operational leagues
        # [{slug: "nba", name: "NBA", sport: "Basketball"}, ...]
        self.leagues: list = []

        # Step 2 output: team registry
        # {team_id: {name, full_name, safeName, league, color, record}}
        self.teams: dict = {}
        # {normalized_full_name: team_id}
        self.team_name_to_id: dict = {}

        # Step 3 output: Odds API sport keys mapped to our leagues
        # {polymarket_league_slug: odds_api_sport_key}
        self.league_to_odds_key: dict = {}

        # Step 4 output: Odds API events with consensus probabilities
        # {odds_api_event_id: {home_team, away_team, consensus_home_prob, ...}}
        self.odds_events: dict = {}

        # Step 5 output: team name bridge
        # {normalized_polymarket_name: normalized_odds_api_name}
        self.team_bridge: dict = {}

        # Step 6+7 output: matched games
        # {polymarket_slug: {odds_event_id, reversed, ...}}
        self.matched_games: dict = {}

        # Internal
        self._http: Optional[httpx.AsyncClient] = None
        self._aiohttp: Optional[aiohttp.ClientSession] = None

    async def _get_poly(self, path: str, params: dict = None):
        """GET from Polymarket public gateway."""
        if self._http is None or self._http.is_closed:
            self._http = httpx.AsyncClient(timeout=15)
        r = await self._http.get(f"{POLYMARKET_GATEWAY}{path}", params=params)
        if r.status_code == 200:
            return r.json()
        logger.error(f"Polymarket {path} returned {r.status_code}")
        return None

    async def _get_odds(self, path: str, params: dict = None):
        """GET from The Odds API."""
        if self._aiohttp is None or self._aiohttp.closed:
            self._aiohttp = aiohttp.ClientSession()
        p = params or {}
        p["apiKey"] = self.odds_api_key
        try:
            async with self._aiohttp.get(
                f"{ODDS_API_BASE}{path}", params=p,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                logger.error(f"Odds API {path} returned {resp.status}")
                return None
        except Exception as e:
            logger.error(f"Odds API error: {e}")
            return None

    # ─────────────────────────────────────────
    # STEP 1: Discover leagues
    # ─────────────────────────────────────────

    async def step1_discover_leagues(self):
        """Call Polymarket v2/sports. Extract operational
        leagues for our target sports."""
        data = await self._get_poly("/v2/sports")
        if not data:
            logger.error("Step 1 FAILED: cannot reach Polymarket v2/sports")
            return False

        self.leagues = []
        sports_list = data.get("sports", [])
        for sport in sports_list:
            sport_name = sport.get("name", "")
            if sport_name not in TARGET_SPORTS:
                continue
            for league in sport.get("leagues", []):
                if not league.get("isOperational"):
                    continue
                self.leagues.append({
                    "slug": league["slug"],
                    "name": league.get("name", league["slug"]),
                    "sport": sport_name,
                    "image": league.get("image", ""),
                })

        league_slugs = [l["slug"] for l in self.leagues]
        logger.info(f"Step 1 complete: {len(self.leagues)} operational leagues: {league_slugs}")
        return True

    # ─────────────────────────────────────────
    # STEP 2: Load teams
    # ─────────────────────────────────────────

    async def step2_load_teams(self):
        """For each league, load events and extract
        every team into the registry."""
        self.teams = {}
        self.team_name_to_id = {}

        for league in self.leagues:
            slug = league["slug"]
            data = await self._get_poly(
                f"/v2/leagues/{slug}/events",
                {"limit": 100}
            )
            if not data:
                continue

            events = data.get("events", [])
            for event in events:
                for team in event.get("teams", []):
                    tid = team.get("id")
                    if not tid or tid in self.teams:
                        continue

                    full_name = build_full_name(team)
                    short_name = (team.get("name", "") or "").strip()

                    self.teams[tid] = {
                        "name": short_name,
                        "full_name": full_name,
                        "safeName": (team.get("safeName", "") or "").strip(),
                        "league": team.get("league", ""),
                        "color": team.get("colorPrimary", ""),
                        "record": team.get("record", ""),
                        "abbreviation": team.get("abbreviation", ""),
                    }

                    # Index by both full and short name
                    norm_full = normalize_team(full_name)
                    norm_short = normalize_team(short_name)
                    if norm_full:
                        self.team_name_to_id[norm_full] = tid
                    if norm_short and norm_short != norm_full:
                        self.team_name_to_id[norm_short] = tid

        logger.info(f"Step 2 complete: {len(self.teams)} teams from {len(self.leagues)} leagues")
        return True

    # ─────────────────────────────────────────
    # STEP 3: Discover Odds API sport keys
    # ─────────────────────────────────────────

    async def step3_discover_odds_keys(self):
        """Call Odds API /v4/sports. Map our Polymarket
        league slugs to Odds API sport keys."""
        data = await self._get_odds("/v4/sports")
        if not data:
            logger.error("Step 3 FAILED: cannot reach Odds API /v4/sports")
            return False

        # Build lookup of active Odds API keys by group
        odds_by_group = {}
        for sport in data:
            if not sport.get("active"):
                continue
            key = sport["key"]
            group = sport.get("group", "").lower()
            title = sport.get("title", "").lower()
            if group not in odds_by_group:
                odds_by_group[group] = []
            odds_by_group[group].append({
                "key": key,
                "title": title,
            })

        # Map each Polymarket league to an Odds API key
        # This mapping is based on known correspondences
        LEAGUE_MAP = {
            "nba": "basketball_nba",
            "cbb": "basketball_ncaab",
            "nfl": "americanfootball_nfl",
            "cfb": "americanfootball_ncaaf",
            "mlb": "baseball_mlb",
            "nhl": "icehockey_nhl",
            "mls": "soccer_usa_mls",
            "epl": "soccer_epl",
            "ucl": "soccer_uefa_champs_league",
            "lal": "soccer_spain_la_liga",
            "bun": "soccer_germany_bundesliga",
            "sea": "soccer_italy_serie_a",
        }

        self.league_to_odds_key = {}
        active_odds_keys = {s["key"] for group in odds_by_group.values() for s in group}

        for league in self.leagues:
            slug = league["slug"]
            odds_key = LEAGUE_MAP.get(slug)
            if odds_key and odds_key in active_odds_keys:
                self.league_to_odds_key[slug] = odds_key

        mapped = list(self.league_to_odds_key.items())
        logger.info(f"Step 3 complete: {len(mapped)} leagues mapped to Odds API keys: {mapped}")
        return True

    async def close(self):
        if self._http and not self._http.is_closed:
            await self._http.aclose()
        if self._aiohttp and not self._aiohttp.closed:
            await self._aiohttp.close()
