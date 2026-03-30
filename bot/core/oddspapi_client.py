"""
OddsPapi client for PolyFarm.
Fetches Pinnacle sharp odds and matches
them to Polymarket market slugs.
Provides fair probability for edge detection.
"""
import asyncio
import logging
import re
import os
from datetime import datetime, timezone, timedelta
from typing import Optional
import aiohttp

logger = logging.getLogger("polyfarm.oddspapi")

BASE_URL = "https://api.oddspapi.io/v4"
POLL_INTERVAL = 180
SCORE_INTERVAL = 60
TOURNAMENT_REFRESH = 86400
MATCH_TIME_WINDOW = 7200
MIN_MATCH_CONFIDENCE = 0.7

TARGET_SPORTS = {
    "basketball": ["Basketball", "basketball"],
    "football": ["American Football", "americanfootball", "American football"],
    "baseball": ["Baseball", "baseball"],
    "ice_hockey": ["Ice Hockey", "Ice hockey", "icehockey"],
    "soccer": ["Soccer", "soccer", "Football"],
}

TARGET_TOURNAMENTS = {
    "basketball": ["nba", "ncaa", "college basketball"],
    "football": ["nfl", "ncaa football", "college football"],
    "baseball": ["mlb"],
    "ice_hockey": ["nhl"],
    "soccer": ["mls", "premier league", "laliga", "bundesliga", "serie a", "ligue 1", "champions league", "europa league"],
}


def normalize_team(name: str) -> str:
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r"[^\w\s]", "", n)
    n = re.sub(r"\b(fc|sc|cf|afc|rfc|bsc|fk|sk|ac)\s*$", "", n).strip()
    n = re.sub(r"^the\s+", "", n).strip()
    return n


def name_similarity(a: str, b: str) -> float:
    na = normalize_team(a)
    nb = normalize_team(b)
    if na == nb:
        return 1.0
    if not na or not nb:
        return 0.0
    tokens_a = set(na.split())
    tokens_b = set(nb.split())
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    if not intersection:
        return 0.0
    union = tokens_a | tokens_b
    jaccard = len(intersection) / len(union)
    # Boost if all tokens of the shorter set appear in the longer
    shorter = tokens_a if len(tokens_a) <= len(tokens_b) else tokens_b
    longer = tokens_b if len(tokens_a) <= len(tokens_b) else tokens_a
    if shorter.issubset(longer) and len(shorter) >= 1:
        jaccard = max(jaccard, 0.85)
    return jaccard


def decimal_to_fair_prob(home_decimal, away_decimal, draw_decimal=None):
    if home_decimal <= 1.0 or away_decimal <= 1.0:
        return 0.5, 0.5, None
    home_implied = 1.0 / home_decimal
    away_implied = 1.0 / away_decimal
    if draw_decimal and draw_decimal > 1.0:
        draw_implied = 1.0 / draw_decimal
        total = home_implied + away_implied + draw_implied
        if total <= 0:
            return 0.33, 0.33, 0.34
        return (round(home_implied / total, 4), round(away_implied / total, 4), round(draw_implied / total, 4))
    else:
        total = home_implied + away_implied
        if total <= 0:
            return 0.5, 0.5, None
        return (round(home_implied / total, 4), round(away_implied / total, 4), None)


class OddsPapiClient:

    def __init__(self, api_key, db):
        self.api_key = api_key
        self.db = db
        self._sport_ids = {}
        self._tournament_ids = []
        self._tournament_meta = {}
        self._participant_names = {}
        self._pinnacle_odds = {}
        self._market_map = {}
        self._last_poll = None
        self._polls_today = 0
        self._session = None

    async def _get(self, endpoint, params=None):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        p = params or {}
        p["apiKey"] = self.api_key
        url = f"{BASE_URL}{endpoint}"
        try:
            async with self._session.get(url, params=p, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:
                    logger.warning("OddsPapi rate limited. Waiting 2s.")
                    await asyncio.sleep(2)
                    return None
                else:
                    logger.error(f"OddsPapi {endpoint} returned {resp.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"OddsPapi timeout: {endpoint}")
            return None
        except Exception as e:
            logger.error(f"OddsPapi request error: {e}")
            return None

    async def discover_sports(self):
        data = await self._get("/sports", {"language": "en"})
        if not data:
            logger.error("Failed to fetch OddsPapi sports")
            return
        for sport in data:
            sport_id = sport.get("sportId")
            sport_name = sport.get("sportName", "")
            slug = sport.get("slug", "")
            for internal_name, aliases in TARGET_SPORTS.items():
                for alias in aliases:
                    if alias.lower() == sport_name.lower() or alias.lower() == slug.lower():
                        self._sport_ids[internal_name] = sport_id
                        break
        logger.info(f"OddsPapi sport IDs: {self._sport_ids}")
        await self.db.set_bot_config("oddspapi_sport_ids", str(self._sport_ids))

    async def discover_tournaments(self):
        target_ids = []
        meta = {}
        for sport_name, sport_id in self._sport_ids.items():
            await asyncio.sleep(1)
            data = await self._get("/tournaments", {"sportId": sport_id, "language": "en"})
            if not data:
                continue
            targets = TARGET_TOURNAMENTS.get(sport_name, [])
            for t in data:
                t_name = t.get("tournamentName", "").lower()
                t_slug = t.get("tournamentSlug", "").lower()
                t_id = t.get("tournamentId")
                is_target = any(target in t_name or target in t_slug for target in targets)
                if is_target:
                    target_ids.append(t_id)
                    meta[t_id] = {
                        "tournament_name": t.get("tournamentName"),
                        "tournament_slug": t.get("tournamentSlug"),
                        "sport": sport_name,
                        "sport_id": sport_id,
                        "category_name": t.get("categoryName"),
                    }
                    logger.info(f"Target tournament: {t.get('tournamentName')} (ID: {t_id})")
                try:
                    await self.db.upsert_tournament({
                        "tournament_id": t_id,
                        "tournament_slug": t.get("tournamentSlug"),
                        "tournament_name": t.get("tournamentName"),
                        "sport_id": sport_id,
                        "sport_name": sport_name,
                        "category_slug": t.get("categorySlug"),
                        "category_name": t.get("categoryName"),
                        "is_target": is_target,
                        "future_fixtures": t.get("futureFixtures", 0),
                        "upcoming_fixtures": t.get("upcomingFixtures", 0),
                        "live_fixtures": t.get("liveFixtures", 0),
                    })
                except Exception as e:
                    logger.debug(f"Tournament upsert error: {e}")
        self._tournament_ids = target_ids
        self._tournament_meta = meta
        logger.info(f"Target tournaments: {len(target_ids)}")
        await self.db.set_bot_config("oddspapi_tournament_ids", str(target_ids))

    async def build_participant_cache(self):
        for sport_name, sport_id in self._sport_ids.items():
            await asyncio.sleep(1)
            data = await self._get("/participants", {"sportId": sport_id, "language": "en"})
            if not data:
                continue
            for pid_str, name in data.items():
                try:
                    pid = int(pid_str)
                    self._participant_names[(sport_id, pid)] = name
                    await self.db.upsert_participant({
                        "sport_id": sport_id,
                        "participant_id": pid,
                        "participant_name": name,
                        "sport_name": sport_name,
                    })
                except (ValueError, Exception):
                    pass
        logger.info(f"Participant cache: {len(self._participant_names)} teams")

    def get_participant_name(self, sport_id, participant_id):
        return self._participant_names.get((sport_id, participant_id))

    async def fetch_pinnacle_odds(self):
        if not self._tournament_ids:
            logger.warning("No target tournament IDs — skipping odds fetch")
            return
        tournament_str = ",".join(str(t) for t in self._tournament_ids)
        data = await self._get("/odds-by-tournaments", {"bookmaker": "pinnacle", "tournamentIds": tournament_str})
        if not data:
            return
        updated = 0
        for fixture in data:
            try:
                await self._process_fixture(fixture)
                updated += 1
            except Exception as e:
                logger.error(f"Fixture processing error: {e}")
        self._last_poll = datetime.now(timezone.utc)
        self._polls_today += 1
        logger.info(f"OddsPapi poll complete: {updated} fixtures")
        try:
            await self.db.set_bot_config("oddspapi_last_poll", self._last_poll.isoformat())
            await self.db.set_bot_config("oddspapi_polls_today", str(self._polls_today))
            await self.db.set_bot_config("sharpapi_last_update", self._last_poll.isoformat())
        except Exception:
            pass

    async def _process_fixture(self, fixture):
        fixture_id = fixture.get("fixtureId")
        if not fixture_id:
            return
        sport_id = fixture.get("sportId")
        tournament_id = fixture.get("tournamentId")
        status_id = fixture.get("statusId", 0)
        start_time = fixture.get("startTime")
        p1_id = fixture.get("participant1Id")
        p2_id = fixture.get("participant2Id")
        if status_id in (2, 3):
            return
        home_team = self.get_participant_name(sport_id, p1_id) or f"participant_{p1_id}"
        away_team = self.get_participant_name(sport_id, p2_id) or f"participant_{p2_id}"
        t_meta = self._tournament_meta.get(tournament_id, {})
        sport_name = t_meta.get("sport", "unknown")
        tournament_name = t_meta.get("tournament_name", "")
        pinnacle = fixture.get("bookmakerOdds", {}).get("pinnacle", {})
        if not pinnacle.get("bookmakerIsActive"):
            return
        markets = pinnacle.get("markets", {})
        moneyline = markets.get("101", {})
        outcomes = moneyline.get("outcomes", {})
        home_decimal = None
        away_decimal = None
        draw_decimal = None
        home_limit = None
        away_limit = None
        home_changed_at = None
        away_changed_at = None
        pinnacle_bk_id = pinnacle.get("bookmakerFixtureId")
        for outcome_id, outcome in outcomes.items():
            player = outcome.get("players", {}).get("0", {})
            if not player.get("active"):
                continue
            side = player.get("bookmakerOutcomeId")
            price = player.get("price")
            limit = player.get("limit")
            changed = player.get("changedAt")
            if side == "home" and price:
                home_decimal = float(price)
                home_limit = limit
                home_changed_at = changed
            elif side == "away" and price:
                away_decimal = float(price)
                away_limit = limit
                away_changed_at = changed
            elif side == "draw" and price:
                draw_decimal = float(price)
        if not home_decimal or not away_decimal:
            return
        home_fair, away_fair, draw_fair = decimal_to_fair_prob(home_decimal, away_decimal, draw_decimal)
        self._pinnacle_odds[fixture_id] = {
            "oddspapi_fixture_id": fixture_id,
            "sport": sport_name,
            "sport_id": sport_id,
            "tournament_id": tournament_id,
            "tournament_name": tournament_name,
            "home_team": home_team,
            "away_team": away_team,
            "participant1_id": p1_id,
            "participant2_id": p2_id,
            "start_time": start_time,
            "status_id": status_id,
            "home_decimal": home_decimal,
            "away_decimal": away_decimal,
            "draw_decimal": draw_decimal,
            "home_fair_prob": home_fair,
            "away_fair_prob": away_fair,
            "draw_fair_prob": draw_fair,
            "pinnacle_active": True,
            "home_limit": home_limit,
            "away_limit": away_limit,
            "home_odds_changed_at": home_changed_at,
            "away_odds_changed_at": away_changed_at,
            "pinnacle_fixture_id": pinnacle_bk_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            await self.db.upsert_pinnacle_odds(self._pinnacle_odds[fixture_id])
        except Exception as e:
            logger.debug(f"Pinnacle odds upsert error: {e}")

    async def match_markets(self, market_registry):
        matched = 0
        unmatched = 0
        registry_items = {}
        if hasattr(market_registry, '_markets'):
            registry_items = dict(market_registry._markets)
        elif isinstance(market_registry, dict):
            registry_items = market_registry

        for slug, market in registry_items.items():
            if slug in self._market_map:
                continue
            poly_home = getattr(market, 'home_team', '') or ''
            poly_away = getattr(market, 'away_team', '') or ''
            poly_sport = getattr(market, 'sport', '') or ''
            poly_start = getattr(market, 'game_start_time', '') or ''
            if not poly_home or not poly_away:
                unmatched += 1
                continue
            best_match = None
            best_confidence = 0.0
            for fix_id, odds in self._pinnacle_odds.items():
                odds_sport = odds.get("sport", "")
                if odds_sport != poly_sport:
                    continue
                odds_home = odds.get("home_team", "")
                odds_away = odds.get("away_team", "")
                odds_start = odds.get("start_time")
                if poly_start and odds_start:
                    try:
                        pt = datetime.fromisoformat(poly_start.replace("Z", "+00:00"))
                        ot = datetime.fromisoformat(odds_start.replace("Z", "+00:00"))
                        if abs((pt - ot).total_seconds()) > MATCH_TIME_WINDOW:
                            continue
                    except Exception:
                        pass
                h_sim = name_similarity(poly_home, odds_home)
                a_sim = name_similarity(poly_away, odds_away)
                confidence_fwd = (h_sim + a_sim) / 2
                h_sim_rev = name_similarity(poly_home, odds_away)
                a_sim_rev = name_similarity(poly_away, odds_home)
                confidence_rev = (h_sim_rev + a_sim_rev) / 2
                confidence = max(confidence_fwd, confidence_rev)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = fix_id
            if best_confidence >= MIN_MATCH_CONFIDENCE and best_match:
                self._market_map[slug] = best_match
                matched += 1
                odds = self._pinnacle_odds[best_match]
                method = "exact" if best_confidence >= 0.99 else "fuzzy"
                try:
                    await self.db.upsert_fixture_mapping({
                        "polymarket_slug": slug,
                        "polymarket_event_id": getattr(market, "event_id", None),
                        "polymarket_event_slug": getattr(market, "event_slug", None),
                        "oddspapi_fixture_id": best_match,
                        "sport": poly_sport,
                        "home_team_polymarket": poly_home,
                        "away_team_polymarket": poly_away,
                        "home_team_oddspapi": odds.get("home_team"),
                        "away_team_oddspapi": odds.get("away_team"),
                        "start_time": poly_start,
                        "match_confidence": best_confidence,
                        "match_method": method,
                        "matched_at": datetime.now(timezone.utc).isoformat(),
                        "last_verified_at": datetime.now(timezone.utc).isoformat(),
                        "is_active": True,
                    })
                    await self.db.update_pinnacle_odds_slug(best_match, slug)
                except Exception as e:
                    logger.debug(f"Mapping upsert error: {e}")
            else:
                unmatched += 1
        logger.info(f"Market matching: {matched} matched, {unmatched} unmatched")
        try:
            await self.db.set_bot_config("markets_matched_count", str(matched))
            await self.db.set_bot_config("markets_unmatched_count", str(unmatched))
        except Exception:
            pass

    def get_fair_prob(self, polymarket_slug, team_side="home"):
        fixture_id = self._market_map.get(polymarket_slug)
        if not fixture_id:
            return None
        odds = self._pinnacle_odds.get(fixture_id)
        if not odds:
            return None
        if team_side == "home":
            return odds.get("home_fair_prob")
        elif team_side == "away":
            return odds.get("away_fair_prob")
        return None

    def get_both_fair_probs(self, polymarket_slug):
        fixture_id = self._market_map.get(polymarket_slug)
        if not fixture_id:
            return None
        odds = self._pinnacle_odds.get(fixture_id)
        if not odds:
            return None
        return {
            "home_fair_prob": odds.get("home_fair_prob"),
            "away_fair_prob": odds.get("away_fair_prob"),
            "draw_fair_prob": odds.get("draw_fair_prob"),
            "home_team": odds.get("home_team"),
            "away_team": odds.get("away_team"),
            "home_decimal": odds.get("home_decimal"),
            "away_decimal": odds.get("away_decimal"),
            "fixture_id": fixture_id,
            "updated_at": odds.get("updated_at"),
        }

    def is_matched(self, slug):
        return slug in self._market_map

    async def fetch_live_scores(self):
        live = [fid for fid, odds in self._pinnacle_odds.items() if odds.get("status_id") == 1]
        if not live:
            return
        for fix_id in live:
            await asyncio.sleep(1)
            data = await self._get("/scores", {"fixtureId": fix_id})
            if not data:
                continue
            scores = data.get("scores", {})
            if "0" in scores:
                total = scores["0"]
                score_str = f"{total['participant1Score']}-{total['participant2Score']}"
                if fix_id in self._pinnacle_odds:
                    self._pinnacle_odds[fix_id]["current_score"] = score_str

    async def startup(self, market_registry):
        logger.info("OddsPapi startup beginning")
        await self.discover_sports()
        await asyncio.sleep(1)
        await self.discover_tournaments()
        await asyncio.sleep(1)
        await self.build_participant_cache()
        await asyncio.sleep(1)
        await self.fetch_pinnacle_odds()
        await asyncio.sleep(1)
        await self.match_markets(market_registry)
        logger.info("OddsPapi startup complete")

    async def poll_loop(self, market_registry):
        while True:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                await self.fetch_pinnacle_odds()
                await self.match_markets(market_registry)
            except Exception as e:
                logger.error(f"OddsPapi poll error: {e}")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
