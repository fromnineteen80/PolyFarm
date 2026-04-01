**TASK: Complete OracleFarming Bot — Registry, Pipeline, Main Integration**

**Branch:** `main` (commit and push everything to main)

---

## WHAT IS ORACLEFARMING

An automated sports prediction market trading bot that:
1. Monitors moneyline markets on **Polymarket US** across NBA, NHL, MLB, CBB, CFB, NFL, EPL, MLS, La Liga, Bundesliga, Serie A, UCL
2. Compares Polymarket crowd prices against US bookmaker consensus from **The Odds API** (DraftKings, FanDuel, BetMGM, Bovada, BetRivers, Fanatics, MyBookie)
3. Calculates edge (sharp fair probability minus Polymarket price)
4. Executes paper trades when edge exceeds band thresholds
5. Paper mode: $700 total seed ($350 per investor), 300 minimum trades at 70%+ win rate before going live
6. Runs on DigitalOcean server 24/7, Next.js dashboard deployed on Vercel

---

## THREE APIs WE USE

### 1. Polymarket Public API (no auth needed)
- Base URL: `https://gateway.polymarket.us`
- v1 teams (master roster): `GET /v1/sports/teams?filters.league={slug}&limit=100&offset=0`
  - Returns ALL teams for a league regardless of season. Paginate until all fetched.
  - Used ONLY to build team_registry.py. Not referenced in bot code at runtime.
  - Returns: id, name, safeName, abbreviation, colorPrimary (plus player props — filter by colorPrimary to get teams only)
  - team.id is stable and identical across v1 and v2
- v2 league events: `GET /v2/leagues/{slug}/events?limit=100`
- v2 sports: `GET /v2/sports`
- v2 returns: events with teams array (id, name, safeName, abbreviation, colorPrimary), markets array (slug, marketType, marketSides with prices), live scores, game state
- v2 is used at runtime for market discovery and live game state. Join on team.id to look up team_registry entries.
- League slugs: `nba`, `nhl`, `mlb`, `nfl`, `mls`, `epl`, `lal` (La Liga), `bun` (Bundesliga), `sea` (Serie A), `ucl`, `cbb`, `cfb`

### 2. Polymarket Auth API (via SDK)
- Package: `polymarket-us` Python SDK v0.1.2
- Init: `from polymarket_us import Client; client = Client()`
- Uses env vars: `POLY_API_KEY`, `POLY_SECRET`, `POLY_PASSPHRASE`
- SDK methods: `client.markets.bbo(slug)`, `client.orders.create()`, `client.orders.cancel_all()`, `client.ws.markets()`, `client.ws.private()`
- BBO response: `marketData.bestBid.value`, `marketData.bestAsk.value`, `marketData.currentPx.value`
- Private WS uses `buyingPower` (camelCase, not snake_case)

### 3. The Odds API
- Base URL: `https://api.the-odds-api.com/v4`
- API key: `fbd86b881d7b58c956f0d45a25b16219`
- Participants (master roster): `GET /v4/sports/{key}/participants?apiKey={KEY}`
  - Returns ALL teams for a sport with exact `full_name` spellings. Used ONLY to build team_registry.py.
- Odds: `GET /v4/sports/{key}/odds/?apiKey={KEY}&regions=us&markets=h2h&oddsFormat=american`
- Sports list: `GET /v4/sports/?apiKey={KEY}`
- Returns: events with `home_team`, `away_team` (strings, no numeric IDs), bookmakers array with American odds
- Sport keys: `basketball_nba`, `icehockey_nhl`, `baseball_mlb`, `soccer_usa_mls`, `soccer_epl`, `soccer_spain_la_liga`, `soccer_germany_bundesliga`, `soccer_italy_serie_a`, `soccer_uefa_champs_league`, `basketball_ncaab`, `americanfootball_ncaaf`, `americanfootball_nfl`

---

## INFRASTRUCTURE

### DigitalOcean Server
- The bot runs on a DigitalOcean droplet
- Bot directory: `/home/user/PolyFarm/bot/`
- Start bot: `cd /home/user/PolyFarm/bot && python3 main.py`
- Env vars are on the server (not in repo — no .env file in the repo)
- You can run curl commands, python scripts, and test directly on this machine
- You can verify API responses by curling the endpoints directly

### Supabase Database
- Tables: markets, trades, positions, signals, investor_profiles, sharp_odds, price_history
- `bot/data/migrations/001_initial_schema.sql` — 11 base tables
- `bot/data/migrations/002_odds_api_and_movement.sql` — sharp_odds, price_history, trade enrichment
- `bot/data/migrations/003_markets_table.sql` — markets table for dashboard reads
- `dashboard/supabase-migration.sql` — investor_profiles table
- The bot writes to Supabase via `bot/data/database.py` using `upsert_market()`

### Dashboard (Vercel)
- Next.js app in `dashboard/` directory
- DO NOT MODIFY any dashboard files in this task
- Uses Raleway font from Google Fonts, light theme (#faf9f7 background)
- Google Material Symbols for icons (no emojis ever)

---

## LEAGUE SLUG TO SPORT KEY MAPPING

```
Polymarket slug → Our sport key → Odds API key
nba → basketball_nba → basketball_nba
nhl → icehockey_nhl → icehockey_nhl
mlb → baseball_mlb → baseball_mlb
cbb → basketball_ncaab → basketball_ncaab
cfb → americanfootball_ncaaf → americanfootball_ncaaf
nfl → americanfootball_nfl → americanfootball_nfl
epl → soccer_epl → soccer_epl
mls → soccer_usa_mls → soccer_usa_mls
lal → soccer_spain_la_liga → soccer_spain_la_liga
bun → soccer_germany_bundesliga → soccer_germany_bundesliga
sea → soccer_italy_serie_a → soccer_italy_serie_a
ucl → soccer_uefa_champs_league → soccer_uefa_champs_league
```

---

## WHAT EXISTS AND ITS STATUS

### `bot/core/team_registry.py` — COMPLETE
929 teams across 12 leagues: NBA (30), NHL (32), MLB (30), NFL (32), MLS (30), EPL (20), La Liga (20), Bundesliga (18), Serie A (20), UCL (60), CBB (365), CFB (272). All Polymarket fields sourced from v1/sports/teams endpoint. All Odds API names sourced from v4/sports/{key}/participants endpoint. Zero fuzzy matching. Zero assumptions.

**Lookup functions are league-scoped** and index by:
- `polymarket_id` first (primary, unique, never ambiguous)
- `(league, normalized_name)` fallback for both Polymarket and Odds API names

**The team registry is a PERMANENT ROSTER — every team that exists in every league, regardless of whether they have a game today or ever. Do NOT limit the registry to teams with current events. If a team exists in the league, it goes in the registry.**

**How to get API-specific data for each team:**
- Polymarket: use v1 teams endpoint (`GET /v1/sports/teams?filters.league={slug}&limit=100&offset=0`)
- Odds API: use v4 participants endpoint (`GET /v4/sports/{key}/participants?apiKey={KEY}`)
- v1 is used ONLY for building the registry. It is NOT referenced in bot code at runtime. Make this clear in the md file. 
  When processing v2 events and trading and in game state, look up
  team_registry[team_id] to get full static
  team data (logos, colors, conference, etc).
  Override record and ranking from v2 since
  those update live during the season.

**Lookup functions must be league-scoped** to prevent cross-league collisions:
- "Kings" = Sacramento Kings (NBA) vs Los Angeles Kings (NHL)
- "Rangers" = New York Rangers (NHL) vs Texas Rangers (MLB)
- Lookup by `polymarket_id` first (unique, never ambiguous), fall back to name within league

---

### `bot/core/pipeline.py` — NEEDS STEP 5 UPDATED
782 lines. Steps 1-9 implemented. This is the NEW pipeline that replaces the old `market_loader.py` + `odds_api_client.py`.

**Steps:**
1. `step1_discover_leagues()` — fetch league slugs from Polymarket v2
2. `step2_load_teams()` — load team data from Polymarket per league
3. `step3_discover_odds_keys()` — map leagues to Odds API sport keys
4. `step4_load_odds()` — fetch odds from The Odds API for each sport key
5. `step5_match_teams()` — **CURRENTLY USES FUZZY MATCHING. MUST BE REWRITTEN to use team_registry lookups by polymarket_id first, then name fallback within league scope**
6. `step6_load_games()` — load game events from Polymarket
7. `step7_match_games()` — match Polymarket games to Odds API events
8. `step8_calculate_edge()` — compute edge = sharp fair prob - polymarket price
9. `step9_write_to_supabase()` — write matched data to Supabase for dashboard

**Other pipeline details:**
- Has `TEAM_ALIASES` dict (old approach, should be replaced by registry)
- Has `normalize_team()` function used by registry index building
- Has `build_full_name()` for Polymarket name dedup
- `TARGET_SPORTS = {"Basketball", "Football", "Ice Hockey", "Baseball", "Soccer"}`
- Uses `seen_events` set to dedup games (one market per event)
- `run_startup()` runs steps 1-9 sequentially
- `run_refresh()` re-runs for ongoing updates
- `refresh_loop()` calls refresh every 5 minutes

---

### `bot/main.py` — NEEDS REWIRING
Currently starts the bot using OLD components:
- `MarketLoader` from `market_loader.py` (OLD)
- `OddsAPIClient` from `odds_api_client.py` (OLD)

**Must be rewired to use `pipeline.py` instead.** The pipeline's `run_startup()` replaces the old market loading + odds loading + matching flow. The pipeline's `refresh_loop()` replaces the old `market_loader.refresh_loop()`.

Current main.py startup flow:
1. SDK client init → verify connectivity
2. Init components (market loader, odds api, edge detector, ws, wallet)
3. Reconcile orders → session init
4. Load markets → init Odds API → send alert
5. Start background tasks (heartbeat, pre_game_scanner, game_complete_scanner, paper_milestone_checker, midnight_scheduler)

New flow should replace steps 2-4 with pipeline init.

---

### `bot/core/market_loader.py` — OLD, BEING REPLACED BY PIPELINE
Still has `flush_to_supabase()` and `flush_loop()` which write to the markets Supabase table for the dashboard. This functionality needs to move into pipeline step 9 or remain as a utility.

### `bot/core/odds_api_client.py` — OLD, BEING REPLACED BY PIPELINE
Has `OddsAPIClient` with team matching, edge signals, `_market_map` for orientation tracking ({event_id, reversed} for knowing if YES = home or away). Being replaced by pipeline steps 4-5-8.

### `bot/core/edge_detector.py` — DO NOT MODIFY
Uses `self.odds_api.get_edge_signal()` for composite evaluation. Band thresholds:
- Prime (A): 8%+ edge at 70c+
- Standard (B): 5-8% at 60-70c
- Value (C): 3-5% at 55-60c
Direction modifiers adjust entry requirements. Size multiplier: falling+strong_sell=1.15x, rising+heavy_buy=0.85x.

### `bot/core/ws_markets.py` — DO NOT MODIFY
SDK WebSocket (`client.ws.markets()`) with MARKET_DATA_LITE subscription. Price history buffer (30-min rolling window). Trade flow tracking. `calculate_velocity()`, `get_net_buy_pressure()`. Batches subscriptions in groups of 10.

### `bot/core/ws_private.py` — DO NOT MODIFY
SDK WebSocket (`client.ws.private()`) for order fills, positions, balance. Uses `buyingPower` (camelCase).

### `bot/core/wallet.py` — DO NOT MODIFY
WalletManager with profit/loss tiers. Paper mode: $700 total, $350 per investor. Floor at 80% of session start.

---

## EDGE CALCULATION LOGIC
- American odds → vig-removed fair probability conversion
- Composite edge signal: static edge + price direction + buy pressure
- `edge = sharp_fair_prob - polymarket_yes_price`
- Direction modifiers adjust entry thresholds

## SOCCER SPECIAL HANDLING
- Soccer uses `drawable_outcome` market type (3 outcomes: home/away/draw) vs `moneyline` (2 outcomes)
- Must handle draw markets correctly
- Dedup: one game per event ID (soccer was triple-counting before fix)

## KNOWN PAST BUGS (ALREADY FIXED, DO NOT REINTRODUCE)
- Team name duplications ("Oklahoma Sooners Oklahoma Sooners") — fixed in `build_full_name()`
- "Los Angeles L Lakers" — fixed by stripping single trailing letter from safeName
- Team orientation bug (Charlotte showing -80.7c edge) — fixed by tracking {event_id, reversed} in `_market_map`
- Soccer triple-counting — fixed by deduping one game per event ID
- NHL abbreviation names ("FLA Panthers") — added mascot-only matching fallback
- `cancel_all_open_orders()` → correct SDK method is `cancel_all()`
- `buying_power` → correct SDK field is `buyingPower` (camelCase)
- BBO parsing → use `marketData.bestBid.value` not `bbo["bid"]["price"]`

---

## STEP-BY-STEP EXECUTION ORDER

**Step 1:** COMPLETE. Rewrote `team_registry.py` with approved structure for NBA (30), NHL (32), MLB (30), NFL (32), MLS (30), EPL (20), La Liga (20), Bundesliga (18), Serie A (20), UCL (60). All Polymarket fields from v1, all Odds API names from v4 participants.

**Step 2:** COMPLETE. Added all D1 college teams: CBB (365) and CFB (272). Total registry: 929 teams.

**Step 3:** Update `pipeline.py` Step 5 (`step5_match_teams()`) to use registry lookups by `polymarket_id` first, name fallback within league scope. Remove old `TEAM_ALIASES` dict. Commit and push to main.

**Step 4:** Wire `pipeline.py` into `main.py` replacing `market_loader.py` + `odds_api_client.py`. Commit and push to main.

**Step 5:** Run pipeline and verify zero unmatched teams across all leagues. Fix any mismatches. Commit and push to main.

---

## CRITICAL RULES
- Do NOT use fuzzy matching anywhere. Registry is the single source of truth.
- Do NOT modify: dashboard files, edge_detector.py, ws_markets.py, ws_private.py, wallet.py, CSS, or any frontend files
- Do NOT add emojis anywhere
- Do NOT use the old `market_loader.py` or `odds_api_client.py` patterns
- Do NOT make assumptions about team names — verify against the actual APIs by curling them
- Do NOT use monospace fonts, system font stacks — dashboard uses Raleway from Google Fonts
- Do NOT use inline CSS. All styling must be done in global CSS.
- Do NOT reference Polymarket v1 endpoints in bot code. v1 was used ONLY to build team_registry.py. The bot uses v2 at runtime.
- Commit and push to `main` after each step
- We are NOT doing WCBB (women's college basketball)
- The project name is **OracleFarming** (not PolyFarm)
- The user hates vibing, lazy workarounds, and making things up. Use the APIs. Verify everything.
- The team registry is a PERMANENT ROSTER of every team in every league. Do NOT limit it to teams with current events or upcoming games.
- You MUST deploy different agents to get all the teams and build the registry properly with no mistakes.
- When building the registry, use known full league rosters as the primary source. Use the APIs to get API-specific identifiers (Polymarket IDs, Odds API name spellings), NOT to determine which teams exist.
