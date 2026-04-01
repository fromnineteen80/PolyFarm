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

# Known name differences between Polymarket and Odds API
# {normalized_polymarket_name: normalized_odds_api_name}
TEAM_ALIASES = {
    "fc bayern munchen": "bayern munich",
    "fc internazionale milano": "inter milan",
    "sporting cp": "sporting lisbon",
    "borussia monchengladbach": "borussia monchengladbach",  # accent handled by normalize
    "bv borussia 09 dortmund": "borussia dortmund",
    "sv werder bremen": "werder bremen",
    "tsg 1899 hoffenheim": "tsg hoffenheim",
    "1 fc heidenheim 1846": "1 fc heidenheim",
    "1 fsv mainz 05": "fsv mainz 05",
    "1 fc union berlin": "union berlin",
    "fc st pauli 1910": "fc st pauli",
    "bayer 04 leverkusen": "bayer leverkusen",
}


def normalize_team(name: str) -> str:
    """Normalize team name for comparison.
    Strips accents, punctuation, common suffixes."""
    if not name:
        return ""
    import unicodedata
    # Remove accents
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower().strip()
    n = re.sub(r"[^\w\s]", "", n)
    n = re.sub(r"\b(fc|sc|cf|afc|the)\s*$", "", n)
    n = re.sub(r"^the\s+", "", n)
    return n.strip()


def build_full_name(team: dict) -> str:
    """Build canonical team name from Polymarket team data.
    Handles all known duplication patterns:
    - safeName == name (exact duplicate)
    - safeName contains name or vice versa
    - safeName is alternate spelling (UConn vs Connecticut)
    - Accent differences (Montreal vs Montréal)
    """
    safe = (team.get("safeName", "") or "").strip()
    short = (team.get("name", "") or "").strip()
    if not short:
        return safe
    if not safe:
        return short

    # Normalize both for comparison
    norm_safe = normalize_team(safe)
    norm_short = normalize_team(short)

    # Exact match after normalization
    if norm_safe == norm_short:
        return short

    # Strip single trailing letter abbreviation (e.g. "Los Angeles L")
    safe_clean = re.sub(r'\s+[A-Z]$', '', safe).strip()
    norm_safe_clean = normalize_team(safe_clean)

    # One contains the other
    if norm_short in norm_safe_clean:
        return safe_clean
    if norm_safe_clean in norm_short:
        return short

    # Check word overlap — if they share the mascot (last word), use shorter name
    safe_words = set(norm_safe_clean.split())
    short_words = set(norm_short.split())
    if safe_words and short_words:
        overlap = safe_words & short_words
        # If they share any words, they're the same team
        if overlap:
            return short if len(short) <= len(safe_clean) else safe_clean

    # No overlap — genuinely different city + mascot
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

    # ─────────────────────────────────────────
    # STEP 4: Load odds from The Odds API
    # ─────────────────────────────────────────

    async def step4_load_odds(self):
        """For each mapped sport key, fetch consensus
        odds and build the odds events store."""
        self.odds_events = {}
        odds_keys_to_poll = set(self.league_to_odds_key.values())

        for key in odds_keys_to_poll:
            await asyncio.sleep(0.5)  # rate limit
            data = await self._get_odds(
                f"/v4/sports/{key}/odds",
                {"regions": "us", "markets": "h2h", "oddsFormat": "american"}
            )
            if not data or not isinstance(data, list):
                continue

            for event in data:
                eid = event.get("id")
                if not eid:
                    continue
                home = event.get("home_team", "")
                away = event.get("away_team", "")
                commence = event.get("commence_time", "")
                bookmakers = event.get("bookmakers", [])

                # Calculate consensus fair probability
                home_prob, away_prob, draw_prob, books = self._consensus(bookmakers, home, away)
                if home_prob is None:
                    continue

                self.odds_events[eid] = {
                    "event_id": eid,
                    "sport_key": key,
                    "home_team": home,
                    "away_team": away,
                    "commence_time": commence,
                    "consensus_home_prob": home_prob,
                    "consensus_away_prob": away_prob,
                    "consensus_draw_prob": draw_prob,
                    "bookmakers_used": books,
                    "bookmaker_count": len(books),
                }

        logger.info(f"Step 4 complete: {len(self.odds_events)} events with odds from {len(odds_keys_to_poll)} sport keys")
        return True

    def _american_to_implied(self, price: int) -> float:
        if price == 0:
            return 0.0
        if price > 0:
            return 100.0 / (price + 100.0)
        return abs(price) / (abs(price) + 100.0)

    def _consensus(self, bookmakers, home_team, away_team):
        """Calculate vig-removed consensus from bookmakers."""
        PREFERRED = {"draftkings", "fanduel", "betmgm", "caesars", "betrivers", "betonlineag"}
        home_probs, away_probs, draw_probs = [], [], []
        books_used = []
        norm_home = normalize_team(home_team)
        norm_away = normalize_team(away_team)

        for bk in bookmakers:
            h2h = next((m for m in bk.get("markets", []) if m.get("key") == "h2h"), None)
            if not h2h:
                continue
            outcomes = h2h.get("outcomes", [])
            home_price, away_price, draw_price = None, None, None
            for o in outcomes:
                name = o.get("name", "")
                price = o.get("price", 0)
                if name == "Draw":
                    draw_price = price
                elif normalize_team(name) == norm_home:
                    home_price = price
                elif normalize_team(name) == norm_away:
                    away_price = price
                else:
                    if home_price is None and name != "Draw":
                        home_price = price
                    elif away_price is None and name != "Draw":
                        away_price = price
            if home_price is None or away_price is None:
                continue
            home_imp = self._american_to_implied(home_price)
            away_imp = self._american_to_implied(away_price)
            if draw_price:
                draw_imp = self._american_to_implied(draw_price)
                total = home_imp + away_imp + draw_imp
            else:
                draw_imp = 0
                total = home_imp + away_imp
            if total <= 0:
                continue
            home_probs.append(round(home_imp / total, 4))
            away_probs.append(round(away_imp / total, 4))
            if draw_price:
                draw_probs.append(round(draw_imp / total, 4))
            books_used.append(bk.get("key", ""))

        if len(books_used) < 2:
            return None, None, None, []

        # Prefer sharp books if 2+ available
        sharp = [i for i, k in enumerate(books_used) if k in PREFERRED]
        if len(sharp) >= 2:
            home_probs = [home_probs[i] for i in sharp]
            away_probs = [away_probs[i] for i in sharp]
            draw_probs = [draw_probs[i] for i in sharp] if draw_probs else []
            books_used = [books_used[i] for i in sharp]

        avg_home = round(sum(home_probs) / len(home_probs), 4)
        avg_away = round(sum(away_probs) / len(away_probs), 4)
        avg_draw = round(sum(draw_probs) / len(draw_probs), 4) if draw_probs else None

        return avg_home, avg_away, avg_draw, books_used

    # ─────────────────────────────────────────
    # STEP 5: Match teams across APIs
    # ─────────────────────────────────────────

    async def step5_match_teams(self):
        """Build a bridge between Polymarket team names
        and Odds API team names. Both sources use
        standard team names from the same leagues,
        so exact match after normalization works."""
        self.team_bridge = {}

        # Collect all Odds API team names by sport key
        odds_teams = {}  # {sport_key: set of normalized names}
        for event in self.odds_events.values():
            key = event["sport_key"]
            if key not in odds_teams:
                odds_teams[key] = set()
            odds_teams[key].add(normalize_team(event["home_team"]))
            odds_teams[key].add(normalize_team(event["away_team"]))

        # For each Polymarket team, find the matching Odds API name
        matched = 0
        for tid, team in self.teams.items():
            poly_league = team["league"]
            odds_key = self.league_to_odds_key.get(poly_league)
            if not odds_key:
                continue

            odds_names = odds_teams.get(odds_key, set())
            norm_full = normalize_team(team["full_name"])
            norm_short = normalize_team(team["name"])

            # Try exact match on full name
            if norm_full in odds_names:
                self.team_bridge[norm_full] = norm_full
                matched += 1
                continue

            # Try exact match on short name
            if norm_short in odds_names:
                self.team_bridge[norm_full] = norm_short
                self.team_bridge[norm_short] = norm_short
                matched += 1
                continue

            # Try partial match — if all words of one appear in the other
            found_partial = False
            for odds_name in odds_names:
                poly_words = set(norm_full.split())
                odds_words = set(odds_name.split())
                if poly_words and odds_words:
                    if poly_words.issubset(odds_words) or odds_words.issubset(poly_words):
                        self.team_bridge[norm_full] = odds_name
                        self.team_bridge[norm_short] = odds_name
                        matched += 1
                        found_partial = True
                        break
            if found_partial:
                continue

            # Try mascot-only match — for leagues like NHL where
            # Polymarket uses abbreviations (FLA Panthers → Panthers)
            # Match if the mascot (last word) is unique within this sport
            mascot_full = norm_full.split()[-1] if norm_full else ""
            mascot_short = norm_short.split()[-1] if norm_short else ""
            mascot = mascot_short or mascot_full
            if mascot:
                mascot_matches = [n for n in odds_names if n.split()[-1] == mascot]
                if len(mascot_matches) == 1:
                    self.team_bridge[norm_full] = mascot_matches[0]
                    self.team_bridge[norm_short] = mascot_matches[0]
                    matched += 1

        logger.info(f"Step 5 complete: {matched} teams matched across APIs out of {len(self.teams)}")
        return True

    # ─────────────────────────────────────────
    # STEP 6: Load games from Polymarket
    # ─────────────────────────────────────────

    async def step6_load_games(self):
        """Load one game per event from each league.
        For moneyline: one market per event.
        For drawable_outcome (soccer): take the first
        market side where long=true as the YES price.
        Dedup by event ID — never load the same game twice."""
        self.games = {}
        seen_events = set()  # dedup by event ID

        for league in self.leagues:
            lslug = league["slug"]
            data = await self._get_poly(
                f"/v2/leagues/{lslug}/events",
                {"limit": 100}
            )
            if not data:
                continue

            for event in data.get("events", []):
                eid = str(event.get("id", ""))
                if not eid or eid in seen_events:
                    continue
                if event.get("ended"):
                    continue

                teams = event.get("teams", [])
                home_t = teams[0] if teams else {}
                away_t = teams[1] if len(teams) > 1 else {}

                # Find the first qualifying market for this event
                chosen_market = None
                for market in event.get("markets", []):
                    mtype = market.get("marketType", "")
                    stype = market.get("sportsMarketTypeV2", "")
                    if mtype not in ("moneyline", "drawable_outcome") and "MONEYLINE" not in stype and "DRAWABLE" not in stype:
                        continue
                    if not market.get("active"):
                        continue
                    if not market.get("slug"):
                        continue
                    chosen_market = market
                    break  # Take first qualifying market only

                if not chosen_market:
                    continue

                mslug = chosen_market["slug"]
                sides = chosen_market.get("marketSides", [])
                yes_price = 0.5
                for side in sides:
                    if side.get("long"):
                        try:
                            yes_price = float(side.get("price", "0.5"))
                        except (ValueError, TypeError):
                            pass
                        break

                home_name = build_full_name(home_t)
                away_name = build_full_name(away_t)

                self.games[mslug] = {
                    "slug": mslug,
                    "event_id": eid,
                    "event_slug": event.get("slug", ""),
                    "league": lslug,
                    "sport": league["sport"],
                    "home_team": home_name,
                    "away_team": away_name,
                    "home_team_id": home_t.get("id", 0),
                    "away_team_id": away_t.get("id", 0),
                    "home_color": home_t.get("colorPrimary", ""),
                    "away_color": away_t.get("colorPrimary", ""),
                    "home_record": home_t.get("record", ""),
                    "away_record": away_t.get("record", ""),
                    "yes_price": yes_price,
                    "is_live": event.get("live", False),
                    "is_finished": event.get("ended", False),
                    "game_score": event.get("score", "") or "",
                    "game_period": event.get("period", "") or "",
                    "game_elapsed": event.get("elapsed", "") or "",
                    "game_start_time": chosen_market.get("gameStartTime", "") or event.get("startTime", ""),
                    "series_slug": event.get("seriesSlug", ""),
                    "market_type": chosen_market.get("marketType", ""),
                    "market_sides": sides,
                }
                seen_events.add(eid)

        logger.info(f"Step 6 complete: {len(self.games)} games (1 per event) from {len(self.leagues)} leagues")
        return True

    # ─────────────────────────────────────────
    # STEP 7: Match games
    # ─────────────────────────────────────────

    async def step7_match_games(self):
        """Match Polymarket games to Odds API events
        using the team bridge from Step 5."""
        self.matched_games = {}
        matched = 0
        unmatched = 0

        for slug, game in self.games.items():
            poly_league = game["league"]
            odds_key = self.league_to_odds_key.get(poly_league)
            if not odds_key:
                unmatched += 1
                continue

            norm_home = normalize_team(game["home_team"])
            norm_away = normalize_team(game["away_team"])

            # Resolve through team bridge
            bridge_home = self.team_bridge.get(norm_home, norm_home)
            bridge_away = self.team_bridge.get(norm_away, norm_away)

            poly_start = game.get("game_start_time", "")

            best_event_id = None
            best_reversed = False

            for eid, odds_event in self.odds_events.items():
                if odds_event["sport_key"] != odds_key:
                    continue

                odds_home = normalize_team(odds_event["home_team"])
                odds_away = normalize_team(odds_event["away_team"])
                odds_start = odds_event.get("commence_time", "")

                # Time proximity check
                if poly_start and odds_start:
                    try:
                        pt = datetime.fromisoformat(str(poly_start).replace("Z", "+00:00"))
                        ot = datetime.fromisoformat(odds_start.replace("Z", "+00:00"))
                        if abs((pt - ot).total_seconds()) > 7200:
                            continue
                    except Exception:
                        pass

                # Exact match — standard orientation
                if bridge_home == odds_home and bridge_away == odds_away:
                    best_event_id = eid
                    best_reversed = False
                    break

                # Exact match — reversed
                if bridge_home == odds_away and bridge_away == odds_home:
                    best_event_id = eid
                    best_reversed = True
                    break

                # Partial — one team matches
                if bridge_home == odds_home or bridge_home == odds_away:
                    best_event_id = eid
                    best_reversed = bridge_home == odds_away
                elif bridge_away == odds_home or bridge_away == odds_away:
                    best_event_id = eid
                    best_reversed = bridge_away == odds_home

            if best_event_id:
                self.matched_games[slug] = {
                    "event_id": best_event_id,
                    "reversed": best_reversed,
                }
                matched += 1
            else:
                unmatched += 1

        logger.info(f"Step 7 complete: {matched} matched, {unmatched} unmatched")
        return True

    # ─────────────────────────────────────────
    # STEP 8: Calculate edge
    # ─────────────────────────────────────────

    def get_edge(self, slug: str) -> Optional[dict]:
        """Get the edge for a matched game."""
        match = self.matched_games.get(slug)
        if not match:
            return None
        odds = self.odds_events.get(match["event_id"])
        if not odds:
            return None
        game = self.games.get(slug)
        if not game:
            return None

        # Get the correct probability based on orientation
        if match["reversed"]:
            sharp_prob = odds["consensus_away_prob"]
        else:
            sharp_prob = odds["consensus_home_prob"]

        edge = round(sharp_prob - game["yes_price"], 4)

        return {
            "sharp_prob": sharp_prob,
            "poly_price": game["yes_price"],
            "edge": edge,
            "books_used": odds["bookmakers_used"],
            "reversed": match["reversed"],
            "odds_event_id": match["event_id"],
        }

    # ─────────────────────────────────────────
    # STEP 9: Write to Supabase
    # ─────────────────────────────────────────

    async def step9_write_to_supabase(self):
        """Write all game data to Supabase markets table."""
        from data.database import upsert_market, upsert_sharp_odds

        # Write sharp odds
        for eid, odds in self.odds_events.items():
            try:
                await upsert_sharp_odds({
                    "odds_api_event_id": eid,
                    "sport_key": odds["sport_key"],
                    "home_team": odds["home_team"],
                    "away_team": odds["away_team"],
                    "commence_time": odds.get("commence_time"),
                    "consensus_home_prob": odds["consensus_home_prob"],
                    "consensus_away_prob": odds["consensus_away_prob"],
                    "consensus_draw_prob": odds.get("consensus_draw_prob"),
                    "bookmakers_used": odds["bookmakers_used"],
                    "bookmaker_count": odds["bookmaker_count"],
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                })
            except Exception as e:
                logger.debug(f"Sharp odds write error: {e}")

        # Write markets (games + edge data)
        # First clean stale markets
        current_slugs = list(self.games.keys())
        try:
            from data.database import db_execute, _supabase
            if current_slugs:
                await db_execute(
                    lambda: _supabase.table("markets")
                        .delete()
                        .not_.in_("market_slug", current_slugs)
                        .execute()
                )
        except Exception:
            pass

        for slug, game in self.games.items():
            try:
                data = {
                    "market_slug": slug,
                    "event_id": game["event_id"],
                    "event_slug": game["event_slug"],
                    "sport": game["sport"],
                    "league": game["league"],
                    "home_team": game["home_team"],
                    "away_team": game["away_team"],
                    "home_team_id": game["home_team_id"],
                    "away_team_id": game["away_team_id"],
                    "home_color": game["home_color"],
                    "away_color": game["away_color"],
                    "home_record": game["home_record"],
                    "away_record": game["away_record"],
                    "yes_price": game["yes_price"],
                    "is_live": game["is_live"],
                    "is_finished": game["is_finished"],
                    "game_status": "live" if game["is_live"] else "finished" if game["is_finished"] else "upcoming",
                    "game_score": game["game_score"] or None,
                    "game_period": game["game_period"] or None,
                    "game_elapsed": game["game_elapsed"] or None,
                    "game_start_time": game["game_start_time"] or None,
                    "market_type": game["market_type"],
                    "series_slug": game["series_slug"],
                }

                # Add edge data if matched
                edge_data = self.get_edge(slug)
                if edge_data:
                    data["current_sharp_prob"] = edge_data["sharp_prob"]
                    data["current_edge"] = edge_data["edge"]
                    data["odds_api_event_id"] = edge_data["odds_event_id"]
                    data["match_confidence"] = 1.0

                await upsert_market(data)
            except Exception as e:
                logger.error(f"Market write error {slug}: {e}")

        logger.info(f"Step 9 complete: wrote {len(self.games)} markets to Supabase")
        return True

    # ─────────────────────────────────────────
    # RUN FULL PIPELINE
    # ─────────────────────────────────────────

    async def run_startup(self):
        """Run the full pipeline at startup."""
        logger.info("Pipeline starting...")

        if not await self.step1_discover_leagues():
            return False
        if not await self.step2_load_teams():
            return False
        if not await self.step3_discover_odds_keys():
            return False
        await asyncio.sleep(1)
        if not await self.step4_load_odds():
            return False
        if not await self.step5_match_teams():
            return False
        if not await self.step6_load_games():
            return False
        if not await self.step7_match_games():
            return False
        await self.step9_write_to_supabase()

        logger.info("Pipeline startup complete")
        return True

    async def run_refresh(self):
        """Refresh pipeline — reload games and odds."""
        await self.step4_load_odds()
        await self.step6_load_games()
        await self.step7_match_games()
        await self.step9_write_to_supabase()

    async def refresh_loop(self):
        """Run refresh every 3 minutes."""
        while True:
            await asyncio.sleep(180)
            try:
                await self.run_refresh()
            except Exception as e:
                logger.error(f"Pipeline refresh error: {e}")

    async def close(self):
        if self._http and not self._http.is_closed:
            await self._http.aclose()
        if self._aiohttp and not self._aiohttp.closed:
            await self._aiohttp.close()
