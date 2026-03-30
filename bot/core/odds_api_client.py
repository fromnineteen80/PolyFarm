"""
The Odds API client for PolyFarm.
Fetches US bookmaker consensus odds and matches
them to Polymarket market slugs.
Provides fair probability and movement-adjusted
composite edge signal for edge detection.

Sharp reference: consensus from US books
(DraftKings, FanDuel, BetMGM, Caesars, etc.)
"""
import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Optional
import aiohttp

logger = logging.getLogger("polyfarm.odds_api")

BASE_URL = "https://api.the-odds-api.com"
POLL_INTERVAL = 180
MATCH_TIME_WINDOW = 7200
MIN_MATCH_CONFIDENCE = 0.7
MIN_BOOKS_FOR_CONSENSUS = 2

SPORT_KEYS_NON_SOCCER = [
    "basketball_nba",
    "americanfootball_nfl",
    "baseball_mlb",
    "icehockey_nhl",
]

SOCCER_KEY_SUBSTRINGS = [
    "mls", "epl", "bundesliga", "la_liga",
    "serie_a", "ligue_1", "champions_league",
    "europa_league",
]

PREFERRED_BOOKS = {
    "draftkings", "fanduel", "betmgm",
    "caesars", "betrivers", "betonlineag",
}

DIRECTION_THRESHOLD_MULTIPLIER = {
    "falling": 0.85, "stable": 1.00, "rising": 1.20,
}

DIRECTION_SIZE_MULTIPLIER = {
    "falling_strong": 1.15, "default": 1.00, "caution": 0.85,
}


def normalize_team(name: str) -> str:
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r"[^\w\s]", "", n)
    n = re.sub(r"\b(fc|sc|cf|afc|the)\s*$", "", n)
    n = re.sub(r"^the\s+", "", n)
    return n.strip()


def name_similarity(a: str, b: str) -> float:
    na, nb = normalize_team(a), normalize_team(b)
    if na == nb:
        return 1.0
    if not na or not nb:
        return 0.0
    ta, tb = set(na.split()), set(nb.split())
    if not ta or not tb:
        return 0.0
    intersection = ta & tb
    if not intersection:
        return 0.0
    union = ta | tb
    score = len(intersection) / len(union)
    shorter = ta if len(ta) <= len(tb) else tb
    longer = tb if len(ta) <= len(tb) else ta
    if shorter.issubset(longer) and len(shorter) >= 1:
        score = max(score, 0.85)
    return score


def american_to_implied(price: int) -> float:
    if price == 0:
        return 0.0
    if price > 0:
        return 100.0 / (price + 100.0)
    return abs(price) / (abs(price) + 100.0)


def calculate_fair_probs(outcomes, home_team, away_team):
    home_price = None
    away_price = None
    draw_price = None

    for o in outcomes:
        name = o.get("name", "")
        price = o.get("price", 0)
        if name == "Draw":
            draw_price = price
        elif normalize_team(name) == normalize_team(home_team):
            home_price = price
        elif normalize_team(name) == normalize_team(away_team):
            away_price = price
        else:
            if home_price is None and name != "Draw":
                home_price = price
            elif away_price is None and name != "Draw":
                away_price = price

    if home_price is None or away_price is None:
        return None, None, None

    home_imp = american_to_implied(home_price)
    away_imp = american_to_implied(away_price)

    if draw_price:
        draw_imp = american_to_implied(draw_price)
        total = home_imp + away_imp + draw_imp
        if total <= 0:
            return None, None, None
        return (round(home_imp / total, 4), round(away_imp / total, 4), round(draw_imp / total, 4))
    else:
        total = home_imp + away_imp
        if total <= 0:
            return None, None, None
        return (round(home_imp / total, 4), round(away_imp / total, 4), None)


def consensus_from_bookmakers(bookmakers, home_team, away_team):
    home_probs, away_probs, draw_probs = [], [], []
    books_used = []
    raw_bookmakers = []

    for bk in bookmakers:
        bk_key = bk.get("key", "")
        h2h = next((m for m in bk.get("markets", []) if m.get("key") == "h2h"), None)
        if not h2h:
            continue
        h, a, d = calculate_fair_probs(h2h.get("outcomes", []), home_team, away_team)
        if h is None:
            continue
        home_probs.append(h)
        away_probs.append(a)
        if d is not None:
            draw_probs.append(d)
        books_used.append(bk_key)
        raw_bookmakers.append(bk)

    if len(books_used) < MIN_BOOKS_FOR_CONSENSUS:
        return None, None, None, [], []

    sharp_available = [k for k in books_used if k in PREFERRED_BOOKS]
    if len(sharp_available) >= 2:
        hp, ap, dp, bs = [], [], [], []
        for bk in bookmakers:
            if bk.get("key") not in PREFERRED_BOOKS:
                continue
            h2h = next((m for m in bk.get("markets", []) if m.get("key") == "h2h"), None)
            if not h2h:
                continue
            h, a, d = calculate_fair_probs(h2h.get("outcomes", []), home_team, away_team)
            if h is None:
                continue
            hp.append(h); ap.append(a)
            if d is not None:
                dp.append(d)
            bs.append(bk.get("key"))
        if len(bs) >= 2:
            home_probs, away_probs, draw_probs, books_used = hp, ap, dp, bs

    avg_home = round(sum(home_probs) / len(home_probs), 4)
    avg_away = round(sum(away_probs) / len(away_probs), 4)
    avg_draw = round(sum(draw_probs) / len(draw_probs), 4) if draw_probs else None

    return avg_home, avg_away, avg_draw, books_used, raw_bookmakers


class OddsAPIClient:

    def __init__(self, api_key, db):
        self.api_key = api_key
        self.db = db
        self._soccer_keys = []
        self._sharp_odds = {}
        self._market_map = {}
        self._requests_remaining = 100000
        self._requests_used = 0
        self._last_poll = None
        self._polls_today = 0
        self._session = None

    async def _get(self, path, params=None):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        p = params or {}
        p["apiKey"] = self.api_key
        url = f"{BASE_URL}{path}"
        try:
            async with self._session.get(url, params=p, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                headers = dict(resp.headers)
                remaining = headers.get("x-requests-remaining")
                used = headers.get("x-requests-used")
                if remaining:
                    self._requests_remaining = int(remaining)
                if used:
                    self._requests_used = int(used)
                if resp.status == 200:
                    return await resp.json(), headers
                elif resp.status == 429:
                    logger.warning("Odds API rate limited. Waiting 5s.")
                    await asyncio.sleep(5)
                    return None, headers
                else:
                    logger.error(f"Odds API {path} returned {resp.status}")
                    return None, headers
        except asyncio.TimeoutError:
            logger.error(f"Odds API timeout: {path}")
            return None, {}
        except Exception as e:
            logger.error(f"Odds API error: {e}")
            return None, {}

    async def discover_soccer_keys(self):
        data, _ = await self._get("/v4/sports")
        if not data:
            self._soccer_keys = ["soccer_usa_mls"]
            return
        soccer_keys = []
        for sport in data:
            if not sport.get("active"):
                continue
            key = sport.get("key", "")
            group = sport.get("group", "")
            if group.lower() != "soccer":
                continue
            if any(sub in key for sub in SOCCER_KEY_SUBSTRINGS):
                soccer_keys.append(key)
        self._soccer_keys = soccer_keys
        logger.info(f"Active soccer keys: {soccer_keys}")

    async def startup(self, market_registry):
        logger.info("Odds API client starting up")
        await self.discover_soccer_keys()
        await asyncio.sleep(1)
        await self.fetch_all_odds()
        await asyncio.sleep(1)
        await self.match_markets(market_registry)
        logger.info("Odds API startup complete")

    def _all_sport_keys(self):
        return SPORT_KEYS_NON_SOCCER + self._soccer_keys

    async def fetch_all_odds(self):
        total_updated = 0
        for sport_key in self._all_sport_keys():
            await asyncio.sleep(0.5)
            total_updated += await self._fetch_sport_odds(sport_key)
        self._last_poll = datetime.now(timezone.utc)
        self._polls_today += 1
        logger.info(f"Odds API poll: {total_updated} events. Credits remaining: {self._requests_remaining}")
        try:
            await self.db.set_bot_config("odds_api_last_poll", self._last_poll.isoformat())
            await self.db.set_bot_config("odds_api_requests_remaining", str(self._requests_remaining))
            await self.db.set_bot_config("sharpapi_last_update", self._last_poll.isoformat())
        except Exception:
            pass

    async def _fetch_sport_odds(self, sport_key):
        data, _ = await self._get(f"/v4/sports/{sport_key}/odds", {"regions": "us", "markets": "h2h", "oddsFormat": "american"})
        if not data:
            return 0
        count = 0
        for event in data:
            try:
                await self._process_event(event)
                count += 1
            except Exception as e:
                logger.error(f"Event processing error: {e}")
        return count

    async def _process_event(self, event):
        event_id = event.get("id")
        if not event_id:
            return
        sport_key = event.get("sport_key", "")
        home_team = event.get("home_team", "")
        away_team = event.get("away_team", "")
        commence_time = event.get("commence_time", "")
        bookmakers = event.get("bookmakers", [])

        now = datetime.now(timezone.utc)
        try:
            ct = datetime.fromisoformat(commence_time.replace("Z", "+00:00"))
            status = "live" if ct <= now else "upcoming"
        except Exception:
            status = "upcoming"

        home_prob, away_prob, draw_prob, books_used, raw_books = consensus_from_bookmakers(bookmakers, home_team, away_team)
        if home_prob is None:
            return

        record = {
            "odds_api_event_id": event_id,
            "sport_key": sport_key,
            "home_team": home_team,
            "away_team": away_team,
            "commence_time": commence_time,
            "status": status,
            "consensus_home_prob": home_prob,
            "consensus_away_prob": away_prob,
            "consensus_draw_prob": draw_prob,
            "bookmakers_used": books_used,
            "bookmaker_count": len(books_used),
            "updated_at": now.isoformat(),
        }
        existing = self._sharp_odds.get(event_id)
        if existing and existing.get("polymarket_slug"):
            record["polymarket_slug"] = existing["polymarket_slug"]
        self._sharp_odds[event_id] = record
        try:
            await self.db.upsert_sharp_odds(record)
        except Exception as e:
            logger.debug(f"Sharp odds upsert error: {e}")

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
            best_event_id = None
            best_confidence = 0.0
            for event_id, odds in self._sharp_odds.items():
                odds_sport = odds.get("sport_key", "")
                if poly_sport not in odds_sport and not odds_sport.startswith(poly_sport[:4]):
                    continue
                if poly_start and odds.get("commence_time"):
                    try:
                        pt = datetime.fromisoformat(str(poly_start).replace("Z", "+00:00"))
                        ot = datetime.fromisoformat(odds["commence_time"].replace("Z", "+00:00"))
                        if abs((pt - ot).total_seconds()) > MATCH_TIME_WINDOW:
                            continue
                    except Exception:
                        pass
                h_sim = name_similarity(poly_home, odds.get("home_team", ""))
                a_sim = name_similarity(poly_away, odds.get("away_team", ""))
                conf_fwd = (h_sim + a_sim) / 2
                h_rev = name_similarity(poly_home, odds.get("away_team", ""))
                a_rev = name_similarity(poly_away, odds.get("home_team", ""))
                conf_rev = (h_rev + a_rev) / 2
                confidence = max(conf_fwd, conf_rev)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_event_id = event_id

            if best_confidence >= MIN_MATCH_CONFIDENCE and best_event_id:
                self._market_map[slug] = best_event_id
                matched += 1
                method = "exact" if best_confidence >= 0.99 else "fuzzy"
                odds = self._sharp_odds[best_event_id]
                try:
                    await self.db.upsert_market_mapping({
                        "polymarket_slug": slug,
                        "polymarket_event_id": getattr(market, "event_id", None),
                        "odds_api_event_id": best_event_id,
                        "sport_key": poly_sport,
                        "home_team_polymarket": poly_home,
                        "away_team_polymarket": poly_away,
                        "home_team_odds_api": odds.get("home_team"),
                        "away_team_odds_api": odds.get("away_team"),
                        "start_time": poly_start,
                        "match_confidence": best_confidence,
                        "match_method": method,
                        "matched_at": datetime.now(timezone.utc).isoformat(),
                        "is_active": True,
                    })
                    await self.db.update_sharp_odds_slug(best_event_id, slug)
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
        event_id = self._market_map.get(polymarket_slug)
        if not event_id:
            return None
        odds = self._sharp_odds.get(event_id)
        if not odds:
            return None
        if team_side == "home":
            return odds.get("consensus_home_prob")
        elif team_side == "away":
            return odds.get("consensus_away_prob")
        return None

    def get_consensus_data(self, polymarket_slug):
        event_id = self._market_map.get(polymarket_slug)
        if not event_id:
            return None
        return self._sharp_odds.get(event_id)

    def is_matched(self, slug):
        return slug in self._market_map

    def get_edge_signal(self, polymarket_slug, team_side, poly_yes_price, ws_markets, band_threshold):
        sharp_prob = self.get_fair_prob(polymarket_slug, team_side)
        if sharp_prob is None:
            return None
        static_edge = round(sharp_prob - poly_yes_price, 4)
        velocity, direction = ws_markets.calculate_velocity(polymarket_slug)
        net_pressure = ws_markets.get_net_buy_pressure(polymarket_slug)

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
        event_id = self._market_map.get(polymarket_slug, "")
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

    async def flush_price_history(self, ws_markets):
        for slug in list(ws_markets.get_subscribed_slugs()):
            try:
                history = ws_markets.get_price_history(slug)
                flow = ws_markets.get_trade_flow(slug)
                if not history:
                    continue
                velocity, direction = ws_markets.calculate_velocity(slug)
                pressure = ws_markets.get_net_buy_pressure(slug)
                current = history[-1]["price"] if history else 0.0
                oldest = history[0]["price"] if history else 0.0
                await self.db.upsert_price_history(
                    slug=slug, snapshots=history, trade_flow=[flow] if flow else [],
                    velocity=velocity, direction=direction, net_buy_pressure=pressure,
                    current_price=current, price_30m_ago=oldest,
                )
            except Exception as e:
                logger.error(f"Price history flush error for {slug}: {e}")

    async def poll_loop(self, market_registry_fn, ws_markets):
        last_price_flush = datetime.now(timezone.utc)
        while True:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                await self.fetch_all_odds()
                await self.match_markets(market_registry_fn())
                now = datetime.now(timezone.utc)
                if (now - last_price_flush).total_seconds() >= 300:
                    await self.flush_price_history(ws_markets)
                    last_price_flush = now
            except Exception as e:
                logger.error(f"Odds API poll error: {e}")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
