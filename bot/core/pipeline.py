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
from datetime import datetime, timezone, date, time
from typing import Optional
from zoneinfo import ZoneInfo
import httpx
from core.team_registry import lookup_by_polymarket_id

logger = logging.getLogger("polyfarm.pipeline")

POLYMARKET_GATEWAY = "https://gateway.polymarket.us"
ODDS_API_BASE = "https://api.the-odds-api.com"

# Sports we trade — must match Polymarket v2/sports sport names
TARGET_SPORTS = {"Basketball", "Football", "Ice Hockey", "Baseball", "Soccer"}

# Eastern timezone (handles EST/EDT automatically)
ET = ZoneInfo("America/New_York")


def utc_to_et(utc_str: str) -> Optional[datetime]:
    """Convert a UTC ISO string (with Z suffix) to Eastern datetime."""
    if not utc_str:
        return None
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(ET)
    except Exception:
        return None


def format_et(dt: Optional[datetime]) -> Optional[str]:
    """Format an Eastern datetime as ISO string."""
    if not dt:
        return None
    return dt.isoformat()


def game_bucket(game_start_utc: str, is_live: bool, is_ended: bool) -> str:
    """Determine game bucket based on Eastern time.
    - live: game is in progress
    - today: game starts between 12:01 AM and 11:59 PM ET today
    - upcoming: game starts after today
    """
    if is_ended:
        return "historical"
    if is_live:
        return "live"
    et_dt = utc_to_et(game_start_utc)
    if not et_dt:
        return "upcoming"
    now_et = datetime.now(ET)
    today_start = datetime.combine(now_et.date(), time(0, 1), tzinfo=ET)
    today_end = datetime.combine(now_et.date(), time(23, 59), tzinfo=ET)
    if today_start <= et_dt <= today_end:
        return "today"
    return "upcoming"



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
        self.ws_markets = None  # Set by main.py for slug subscription
        self.market_registry = None  # Set by main.py for MarketInfo updates

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

        # Step 6 output: games
        # {polymarket_slug: {home_team, away_team, yes_price, ...}}
        self.games: dict = {}

        # Step 7 output: matched games
        # {polymarket_slug: {odds_event_id, reversed, ...}}
        self.matched_games: dict = {}

        # Step 8 output: scores
        # {odds_api_event_id: {home_score, away_score, completed, ...}}
        self.scores: dict = {}

        # Internal
        self._http: Optional[httpx.AsyncClient] = None

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
        if self._http is None or self._http.is_closed:
            self._http = httpx.AsyncClient(timeout=15)
        p = params or {}
        p["apiKey"] = self.odds_api_key
        try:
            r = await self._http.get(f"{ODDS_API_BASE}{path}", params=p)
            if r.status_code == 200:
                return r.json()
            logger.error(f"Odds API {path} returned {r.status_code}")
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
                    "updated_at": datetime.now(timezone.utc).isoformat(),
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
        and Odds API team names using the team registry.

        For each Polymarket team from step 2, look up by
        polymarket_id in the registry. The registry entry
        contains the exact odds_api_name. No fuzzy matching."""
        self.team_bridge = {}
        matched = 0
        unmatched = []

        for tid, team in self.teams.items():
            poly_league = team["league"]
            odds_key = self.league_to_odds_key.get(poly_league)
            if not odds_key:
                continue

            # Registry lookup by Polymarket team ID
            entry = lookup_by_polymarket_id(tid)
            if not entry:
                unmatched.append(f"{team['full_name']} (id={tid}, league={poly_league})")
                continue

            odds_name = entry.get("odds_api_name", "")
            if not odds_name:
                unmatched.append(f"{team['full_name']} (id={tid}, league={poly_league}, no odds_api_name)")
                continue

            # Bridge: normalized Polymarket name -> normalized Odds API name
            norm_full = normalize_team(team["full_name"])
            norm_short = normalize_team(team["name"])
            norm_odds = normalize_team(odds_name)

            if norm_full:
                self.team_bridge[norm_full] = norm_odds
            if norm_short and norm_short != norm_full:
                self.team_bridge[norm_short] = norm_odds
            matched += 1

        if unmatched:
            for name in unmatched:
                logger.warning(f"Step 5 UNMATCHED: {name}")

        logger.info(
            f"Step 5 complete: {matched}/{len(self.teams)} active teams matched via registry "
            f"(registry has 929 total), {len(unmatched)} unmatched"
        )
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
                    "game_start_time_et": format_et(utc_to_et(
                        chosen_market.get("gameStartTime", "") or event.get("startTime", "")
                    )),
                    "game_bucket": game_bucket(
                        chosen_market.get("gameStartTime", "") or event.get("startTime", ""),
                        event.get("live", False),
                        event.get("ended", False),
                    ),
                    "series_slug": event.get("seriesSlug", ""),
                    "market_type": chosen_market.get("marketType", ""),
                    "market_sides": sides,
                    "outcome_prices": chosen_market.get("outcomePrices", []),
                    "outcomes": chosen_market.get("outcomes", []),
                    "ep3_status": chosen_market.get("ep3Status", ""),
                    "market_closed": chosen_market.get("closed", False),
                }
                seen_events.add(eid)

        logger.info(f"Step 6 complete: {len(self.games)} games (1 per event) from {len(self.leagues)} leagues")
        return True

    # ─────────────────────────────────────────
    # STEP 7: Match games
    # ─────────────────────────────────────────

    async def step7_match_games(self):
        """Match Polymarket games to Odds API events
        using the team bridge from Step 5.

        Three outcomes per game:
        - matched: both teams found in Odds API event, edge can be calculated
        - waiting_for_odds: no Odds API event exists yet (normal for future games)
        - unmatched: Odds API has events for this league but we couldn't
          connect this game (broken — team bridge or time mismatch)
        """
        self.matched_games = {}
        matched = 0
        waiting_for_odds = 0
        unmatched = []

        # Build set of odds events by sport key for quick lookup
        odds_by_sport = {}
        for eid, ev in self.odds_events.items():
            key = ev["sport_key"]
            if key not in odds_by_sport:
                odds_by_sport[key] = []
            odds_by_sport[key].append((eid, ev))

        for slug, game in self.games.items():
            poly_league = game["league"]
            odds_key = self.league_to_odds_key.get(poly_league)
            if not odds_key:
                waiting_for_odds += 1
                continue

            sport_events = odds_by_sport.get(odds_key, [])
            if not sport_events:
                waiting_for_odds += 1
                continue

            norm_home = normalize_team(game["home_team"])
            norm_away = normalize_team(game["away_team"])

            # Resolve through team bridge
            bridge_home = self.team_bridge.get(norm_home, norm_home)
            bridge_away = self.team_bridge.get(norm_away, norm_away)

            poly_start = game.get("game_start_time", "")

            best_event_id = None
            best_reversed = False

            for eid, odds_event in sport_events:
                odds_home = normalize_team(odds_event["home_team"])
                odds_away = normalize_team(odds_event["away_team"])
                odds_start = odds_event.get("commence_time", "")

                # Time proximity check
                if poly_start and odds_start:
                    try:
                        pt = datetime.fromisoformat(str(poly_start).replace("Z", "+00:00"))
                        ot = datetime.fromisoformat(odds_start.replace("Z", "+00:00"))
                        if abs((pt - ot).total_seconds()) > 10800:
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
                # Odds exist for this league but we couldn't match this game.
                # Check if the game time is beyond what the Odds API covers
                # (bookmakers typically only post odds 1-2 days out)
                has_nearby_odds = False
                for eid, odds_event in sport_events:
                    odds_start = odds_event.get("commence_time", "")
                    if poly_start and odds_start:
                        try:
                            pt = datetime.fromisoformat(str(poly_start).replace("Z", "+00:00"))
                            ot = datetime.fromisoformat(odds_start.replace("Z", "+00:00"))
                            if abs((pt - ot).total_seconds()) <= 10800:
                                has_nearby_odds = True
                                break
                        except Exception:
                            pass

                if has_nearby_odds:
                    # Odds API has events around this time but we couldn't match — broken
                    unmatched.append(
                        f"{game['home_team']} vs {game['away_team']} ({poly_league}, {slug})")
                else:
                    # No odds near this game time — just not posted yet
                    waiting_for_odds += 1

        if unmatched:
            for name in unmatched:
                logger.warning(f"Step 7 UNMATCHED: {name}")

        logger.info(
            f"Step 7 complete: {matched}/{len(self.games)} games matched with odds, "
            f"{waiting_for_odds} future games waiting for bookmaker lines, "
            f"{len(unmatched)} broken (should be 0)")
        return True

    # ─────────────────────────────────────────
    # STEP 8: Load scores from Odds API
    # ─────────────────────────────────────────

    async def step8_load_scores(self):
        """Fetch live and completed scores from the
        Odds API /scores endpoint for all matched sport
        keys. Updates game data with scores and
        completed status."""
        self.scores = {}  # {odds_api_event_id: {home_score, away_score, completed}}
        odds_keys_to_poll = set(self.league_to_odds_key.values())

        for key in odds_keys_to_poll:
            await asyncio.sleep(0.5)  # rate limit
            data = await self._get_odds(
                f"/v4/sports/{key}/scores",
                {"daysFrom": 3}
            )
            if not data or not isinstance(data, list):
                continue

            for event in data:
                eid = event.get("id")
                if not eid:
                    continue
                scores = event.get("scores")
                if not scores:
                    continue

                home_team = event.get("home_team", "")
                away_team = event.get("away_team", "")
                home_score = None
                away_score = None
                for s in scores:
                    if s.get("name") == home_team:
                        home_score = s.get("score")
                    elif s.get("name") == away_team:
                        away_score = s.get("score")

                self.scores[eid] = {
                    "sport_key": key,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": home_score,
                    "away_score": away_score,
                    "completed": event.get("completed", False),
                    "last_update": event.get("last_update", ""),
                }

        # Also index scores by normalized team names for matching
        # completed games whose event IDs rotated off the odds endpoint
        scores_by_teams = {}  # {(sport_key, norm_home, norm_away): score_data}
        for eid, sd in self.scores.items():
            sport_key = sd.get("sport_key", "")
            nh = normalize_team(sd["home_team"])
            na = normalize_team(sd["away_team"])
            scores_by_teams[(sport_key, nh, na)] = sd
            scores_by_teams[(sport_key, na, nh)] = {
                "home_team": sd["away_team"],
                "away_team": sd["home_team"],
                "home_score": sd["away_score"],
                "away_score": sd["home_score"],
                "completed": sd["completed"],
                "last_update": sd["last_update"],
            }

        # Update matched games with scores
        updated = 0
        for slug, match in self.matched_games.items():
            game = self.games.get(slug)
            if not game:
                continue

            # Try direct event ID match first
            score_data = self.scores.get(match["event_id"])

            # Fall back to team name match within the sport
            if not score_data:
                odds_key = self.league_to_odds_key.get(game["league"], "")
                bridge_home = self.team_bridge.get(
                    normalize_team(game["home_team"]),
                    normalize_team(game["home_team"]))
                bridge_away = self.team_bridge.get(
                    normalize_team(game["away_team"]),
                    normalize_team(game["away_team"]))
                score_data = scores_by_teams.get((odds_key, bridge_home, bridge_away))

            if not score_data:
                continue

            # Respect orientation — if reversed, swap home/away scores
            if match["reversed"]:
                game["odds_api_home_score"] = score_data["away_score"]
                game["odds_api_away_score"] = score_data["home_score"]
            else:
                game["odds_api_home_score"] = score_data["home_score"]
                game["odds_api_away_score"] = score_data["away_score"]
            game["odds_api_completed"] = score_data["completed"]
            game["odds_api_score_update"] = score_data["last_update"]
            updated += 1

        logger.info(f"Step 8 complete: {len(self.scores)} scores fetched, {updated} matched games updated")
        return True

    # ─────────────────────────────────────────
    # Edge calculation
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
    # COMPATIBILITY: methods for edge_detector
    # and monitors (same interface as OddsAPIClient)
    # ─────────────────────────────────────────

    def is_matched(self, slug: str) -> bool:
        return slug in self.matched_games

    def get_fair_prob(self, polymarket_slug, team_side="home"):
        match = self.matched_games.get(polymarket_slug)
        if not match:
            return None
        odds = self.odds_events.get(match["event_id"])
        if not odds:
            return None
        reversed_orientation = match["reversed"]
        if reversed_orientation:
            if team_side == "home":
                return odds.get("consensus_away_prob")
            else:
                return odds.get("consensus_home_prob")
        else:
            if team_side == "home":
                return odds.get("consensus_home_prob")
            else:
                return odds.get("consensus_away_prob")

    def get_consensus_data(self, polymarket_slug):
        match = self.matched_games.get(polymarket_slug)
        if not match:
            return None
        odds = self.odds_events.get(match["event_id"])
        if not odds:
            return None
        result = dict(odds)
        result["reversed"] = match["reversed"]
        return result

    def get_edge_signal(self, polymarket_slug, team_side, poly_yes_price, ws_markets, band_threshold):
        sharp_prob = self.get_fair_prob(polymarket_slug, team_side)
        if sharp_prob is None:
            return None
        static_edge = round(sharp_prob - poly_yes_price, 4)
        velocity, direction = ws_markets.calculate_velocity(polymarket_slug)
        net_pressure = ws_markets.get_net_buy_pressure(polymarket_slug)

        DIRECTION_THRESHOLD_MULTIPLIER = {
            "falling": 0.85, "stable": 1.00, "rising": 1.20,
        }
        DIRECTION_SIZE_MULTIPLIER = {
            "falling_strong": 1.15, "default": 1.00, "caution": 0.85,
        }

        multiplier = DIRECTION_THRESHOLD_MULTIPLIER.get(direction, 1.0)
        required_edge = round(band_threshold * multiplier, 4)

        if direction == "falling" and net_pressure < 0.8:
            size_mult = DIRECTION_SIZE_MULTIPLIER["falling_strong"]
        elif direction == "rising" or net_pressure > 1.5:
            size_mult = DIRECTION_SIZE_MULTIPLIER["caution"]
        else:
            size_mult = DIRECTION_SIZE_MULTIPLIER["default"]

        base_score = min(static_edge / 0.10, 1.0) * 60
        direction_score = {"falling": 30, "stable": 15, "rising": 0}.get(direction, 15)
        pressure_score = 10 if net_pressure < 0.7 else 5 if net_pressure <= 1.3 else 0
        composite_score = round(base_score + direction_score + pressure_score, 1)

        consensus = self.get_consensus_data(polymarket_slug)
        match_data = self.matched_games.get(polymarket_slug, {})
        event_id = match_data.get("event_id", "")
        books_used = consensus.get("bookmakers_used", []) if consensus else []

        return {
            "sharp_prob": sharp_prob,
            "static_edge": static_edge,
            "direction": direction,
            "velocity": velocity,
            "net_buy_pressure": net_pressure,
            "required_edge": required_edge,
            "size_multiplier": size_mult,
            "composite_score": composite_score,
            "qualifies": static_edge >= required_edge,
            "books_used": books_used,
            "event_id": event_id,
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
                    "game_status": game.get("game_bucket", "upcoming"),
                    "game_score": game["game_score"] or None,
                    "game_period": game["game_period"] or None,
                    "game_elapsed": game["game_elapsed"] or None,
                    "game_start_time": game["game_start_time"] or None,
                    "game_start_time_et": game.get("game_start_time_et"),
                    "game_bucket": game.get("game_bucket", "upcoming"),
                    "market_type": game["market_type"],
                    "series_slug": game["series_slug"],
                }

                # Add outcome/settlement data
                if game.get("outcome_prices"):
                    data["outcome_prices"] = game["outcome_prices"]
                    data["outcomes"] = game.get("outcomes", [])
                    data["ep3_status"] = game.get("ep3_status", "")
                    data["market_closed"] = game.get("market_closed", False)

                # Add Odds API scores if available
                if game.get("odds_api_home_score") is not None:
                    data["odds_api_home_score"] = game["odds_api_home_score"]
                    data["odds_api_away_score"] = game.get("odds_api_away_score")
                    data["odds_api_completed"] = game.get("odds_api_completed", False)
                    data["odds_api_score_update"] = game.get("odds_api_score_update")

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
        await self.step8_load_scores()
        await self.step9_write_to_supabase()
        await self._subscribe_matched_slugs()
        await self._sync_market_registry()

        logger.info("Pipeline startup complete")
        return True

    async def run_refresh(self):
        """Refresh pipeline — reload games, odds, and scores."""
        await self.step4_load_odds()
        await self.step6_load_games()
        await self.step7_match_games()
        await self.step8_load_scores()
        await self.step9_write_to_supabase()
        await self._subscribe_matched_slugs()
        await self._sync_market_registry()

    async def _subscribe_matched_slugs(self):
        """Push all matched game slugs to the Markets WebSocket
        so they get real-time price streams for edge detection."""
        if not self.ws_markets:
            return
        matched_slugs = list(self.matched_games.keys())
        if matched_slugs:
            await self.ws_markets.subscribe_markets(matched_slugs)
            logger.info(f"Subscribed {len(matched_slugs)} matched slugs to Markets WebSocket")

    async def _sync_market_registry(self):
        """Sync pipeline game data to MarketRegistry so position_monitor,
        edge_detector, terminal, and scanners have current game state."""
        if not self.market_registry:
            return
        from core.market_loader import MarketInfo
        for slug, game in self.games.items():
            info = MarketInfo(
                slug=slug,
                event_id=game.get("event_id", ""),
                event_slug=game.get("event_slug", ""),
                sport=game.get("sport", ""),
                league=game.get("league", ""),
                home_team=game.get("home_team", ""),
                away_team=game.get("away_team", ""),
                home_team_id=game.get("home_team_id", 0),
                away_team_id=game.get("away_team_id", 0),
                home_record=game.get("home_record", ""),
                away_record=game.get("away_record", ""),
                home_color=game.get("home_color", ""),
                away_color=game.get("away_color", ""),
                yes_price=game.get("yes_price", 0.5),
                is_live=game.get("is_live", False),
                is_finished=game.get("is_finished", False),
                current_score=game.get("game_score") or None,
                current_period=game.get("game_period") or None,
                time_elapsed=game.get("game_elapsed") or None,
                game_start_time=game.get("game_start_time", ""),
                market_type=game.get("market_type", "moneyline"),
                series_slug=game.get("series_slug", ""),
                market_sides=game.get("market_sides"),
            )
            await self.market_registry.update(slug, info)

    async def refresh_loop(self):
        """Run refresh every 60 seconds."""
        while True:
            await asyncio.sleep(60)
            try:
                await self.run_refresh()
            except Exception as e:
                logger.error(f"Pipeline refresh error: {e}")

    async def close(self):
        if self._http and not self._http.is_closed:
            await self._http.aclose()
