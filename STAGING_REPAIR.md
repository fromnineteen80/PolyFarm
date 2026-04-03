# STAGING REPAIR PLAN

## READ THESE FILES IN ORDER

1. **BUILD_SECURITY_MANAGER.md** — governs all development. Read first. Has authority over all agents.
2. **STRATEGY_V2.md** — the trading strategy, infrastructure, and what to build.
3. **This file (STAGING_REPAIR.md)** — what is broken and needs fixing.
4. **CLAUDE.md** — implementation details (SDK methods, past bugs, soccer handling).

This branch exists to fix the OracleFarming trading bot. This file documents what is broken and needs fixing.

Do NOT deploy to production (main branch) until every issue is verified fixed on staging. Follow the Build Security Manager protocol in STRATEGY_V2.md.

## THE PIPELINE — WHAT WORKS AND WHAT IS BROKEN

```
PIPELINE (Steps 1-8) ── ALL WORKING ── verified against real APIs

  Step 1: Discover Leagues ── Polymarket v2/sports ──── 11 leagues         ✓ WORKS
  Step 2: Load Teams ──────── Polymarket v2/events ──── ~210 active teams  ✓ WORKS
  Step 3: Map Odds Keys ───── Odds API /v4/sports ───── 10 mapped          ✓ WORKS
  Step 4: Load Odds ───────── Odds API /v4/odds ─────── bookmaker consensus ✓ WORKS
  Step 5: Match Teams ─────── Team Registry (929) ───── polymarket_id lookup ✓ WORKS
  Step 6: Load Games ──────── Polymarket v2 events ──── ET times, buckets   ✓ WORKS (moneyline only)
  Step 7: Match Games ─────── Team bridge ────────────── matched/waiting     ✓ WORKS (labeling bug)
  Step 8: Load Scores ─────── Odds API /v4/scores ───── live + final        ✓ WORKS

  Step 9: Write Supabase ──── markets table ──────────── change detection   ✓ WORKS

TEAM REGISTRY ── 929 teams, 12 leagues, zero fuzzy matching              ✓ WORKS
WEBSOCKET ────── Markets + Private connect on droplet                     ✓ WORKS
SUPABASE ─────── Schema exists, reads/writes work                        ✓ WORKS
TELEGRAM ─────── Can send/receive (but has bugs — see below)             ⚠ PARTIAL

TRADING ENGINE (everything after the pipeline) ── BROKEN

  Edge Detection ──── finds misprices but no persistence check           ✗ BROKEN
  Game State Parser ── does not correctly parse period/elapsed/score      ✗ BROKEN
  Entry Logic ──────── enters games almost over, no game progress check  ✗ BROKEN
  Position Tracking ── registers after DB write, allows re-entry         ✗ BROKEN
  Exit Logic ───────── pre_resolution fires incorrectly, no four-state   ✗ NOT BUILT
  Paper Mode ───────── calls real Polymarket API, overwrites balance     ✗ BROKEN
  Daily Cycle ──────── midnight reset has bugs, morning message crashes  ✗ BROKEN
  Telegram Display ─── shows slugs, internal jargon, wrong balance      ✗ BROKEN
```

The pipeline (Steps 1-8) and team registry are solid. The trading engine — everything that takes a detected edge and turns it into a profitable trade — needs to be rebuilt per STRATEGY_V2.md.

## WHAT THIS PROJECT IS

An automated probability execution system on Polymarket US. Full description in STRATEGY_V2.md. Key points:
- Compares Polymarket CLOB prices against bookmaker consensus (The Odds API)
- Trades when mispricing is measurable, persistent, and executable
- Four-state trade lifecycle: Entry → Advancement → Protection → Exit
- Floors and ceilings anchored to probability, not price
- Paper mode at $2,400 ($1,200 x 2 investors)
- Reports via Telegram every 30 minutes
- Runs 24/7 on DigitalOcean via systemd

## CREDENTIALS (for .env on droplet — not in repo)

```
POLYMARKET_KEY_ID=d9864daf-4b48-4dfb-9234-eba9bd6a173c
POLYMARKET_SECRET_KEY=NxAcYppljqMM0NkPBTXYDkylLnyv4fh6nAtK1gQ7JdzMcqY1/j2GERggEvQf5lhDGHih3BvNdD7/fnnuhVtLNQ==
POLY_API_KEY=019d4979-e375-788d-8848-e6b26b720481
POLY_SECRET=R7NMcywjniJKDaReDhjZBiLpWwKU-vE6RxcWqczIv84=
POLY_PASSPHRASE=f5e942a32f946916d4a5d70dc79080d6bd1014fb15a603d22e665c1bc7ccbb6d
ODDS_API_KEY=fbd86b881d7b58c956f0d45a25b16219
SUPABASE_URL=https://bxsbotougofoltjkqkqq.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4c2JvdG91Z29mb2x0amtxa3FxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3NTM5MjIsImV4cCI6MjA5MDMyOTkyMn0.RdZsFKqg65hUlutrajbBdW3eDtguB_2GbIGdVzqcC24
TELEGRAM_BOT_TOKEN=8655659008:AAGuhmzKCqT5Fu36dZSKzX1-KnIvUR3-Zmg
TELEGRAM_CHAT_ID=8671258330
PAPER_MODE=true
PAPER_SEED_BALANCE=2400
```

## TEAM REGISTRY — THE FOUNDATION

File: `bot/core/team_registry.py` — 17,826 lines. THIS WORKS. DO NOT TOUCH.

929 teams across 12 leagues: NBA (30), NHL (32), MLB (30), NFL (32), MLS (30), EPL (20), La Liga (20), Bundesliga (18), Serie A (20), UCL (60), CBB (365), CFB (272).

Every team has:
- `canonical`: "Boston Celtics" — the ONE correct name used everywhere
- `polymarket_id`: 17 — unique, primary lookup key
- `odds_api_name`: "Boston Celtics" — exact spelling from The Odds API
- `league`: "nba"
- `sport`: "basketball_nba"
- `color`: "#009941"
- `polymarket_names`: ["Celtics", "Boston Celtics", "Boston", "BOS"]

Lookup functions:
- `lookup_by_polymarket_id(poly_id)` — PRIMARY. Used by pipeline step 5.
- `lookup_by_polymarket_name(name, league)` — fallback, league-scoped
- `lookup_by_odds_api_name(name, league)` — for Odds API side

**RULE: Every component that displays or writes a team name MUST resolve it through the registry to the canonical name. No slugs. No abbreviations. No raw API names. Telegram messages, trade records, position displays, Supabase writes — all use canonical names from the registry.**

The registry is the normalization layer that prevents false trades. Different APIs label teams differently. The registry creates one canonical ID so signals are never triggered off mismatched events. NO FUZZY MATCHING ANYWHERE.

## WHAT WORKS

See pipeline visual above. Summary: Steps 1-8 verified. Team registry verified. WebSocket connects. Supabase reads/writes. Polymarket SDK authenticated. Systemd service running. Health API committed but untested.

### League Slug to Sport Key Mapping (verified)
```
Polymarket slug → Odds API key
nba → basketball_nba
nhl → icehockey_nhl
mlb → baseball_mlb
cbb → basketball_ncaab
cfb → americanfootball_ncaaf
nfl → americanfootball_nfl
epl → soccer_epl
mls → soccer_usa_mls
lal → soccer_spain_la_liga
bun → soccer_germany_bundesliga
sea → soccer_italy_serie_a
ucl → soccer_uefa_champs_league
```

### Polymarket API (verified, used at runtime)
- v2 league events: `GET /v2/leagues/{slug}/events?limit=100`
- v2 sports: `GET /v2/sports`
- v2 returns: events with teams array (id, name, safeName, abbreviation, colorPrimary), markets array (slug, marketType, marketSides with prices), live scores, game state (period, elapsed, score, live, ended)
- v1 was used ONLY to build team_registry.py. NOT referenced at runtime.
- team.id is stable and identical across v1 and v2 — this is the polymarket_id in the registry.

### Odds API (verified)
- Odds: `GET /v4/sports/{key}/odds/?apiKey={KEY}&regions=us&markets=h2h&oddsFormat=american`
- Scores: `GET /v4/sports/{key}/scores/?apiKey={KEY}&daysFrom=3`
- Sports list: `GET /v4/sports/?apiKey={KEY}`
- Returns: events with home_team, away_team (strings matched through registry), bookmakers array with American odds

## CRITICAL WARNING

NOT ALL PROBLEMS IDENTIFIED HERE ARE THE FULL SET OF PROBLEMS AFFLICTING THIS BOT OR OUR INFRASTRUCTURE. YOU MUST BE VIGILANT FOR OTHER PROBLEMS THAT WERE MISSED OR NEW PROBLEMS THAT ARISE DURING DEVELOPMENT. The 20 issues below are only the ones identified so far. If something doesn't match STRATEGY_V2.md, doesn't work against real API data, or breaks in ways not listed here — it is a new issue. STOP, report it to the user in plain English, add it to this file, and get approval before proceeding.

## 20 THINGS THAT ARE BROKEN

### Trading Engine
1. **Game state parser doesn't work.** The APIs return `period: H1`, `elapsed: 03:26`, `score: 23-31` but the bot defaults `time_remaining_seconds` to 0 or None. Every exit decision based on game progress makes the wrong call. The bot exited a first-half CBB game after 24 seconds thinking it was over.

2. **Pre-resolution fires incorrectly.** When `time_remaining` is None or 0, the code thinks the game is ending and dumps the position. This caused the bot to exit Stanford vs WVU (H1, 3 minutes in) after 24 seconds.

3. **Bot enters the same game multiple times.** Position is registered AFTER the Supabase write. If the write fails, `has_position()` returns False and the bot re-enters. LAL vs OKC was entered 5 times.

4. **Timeout fires during live games.** 60-minute timeout doesn't know the game is in progress. An NBA game lasts 2.5 hours. The timeout exits mid-game for no reason.

5. **Bot enters games that are almost over.** No check on game progress at entry time. Entered a game that was 92% complete.

6. **No don't-exit-before-game-starts rule.** If we enter pre-game and the game hasn't started, the bot should hold. Instead timeouts and pre-resolution fire on pre-game positions.

### Paper Mode
7. **Paper mode calls Polymarket API for balance.** Paper should be fully simulated. It was calling `client.account.balances()` and `client.portfolio.positions()` which crash when Polymarket returns 503. Fixed in latest code but needs verification.

8. **Paper balance overwrites with real balance.** The `recalculate()` function reads the real Polymarket balance ($322) and overwrites the paper balance ($2,400) every 10 seconds. Fixed in latest code but needs verification.

9. **Daily report uses real balance.** `write_end_of_day` reads `wallet.state.live_portfolio_value` which was the real balance instead of paper.

### Telegram
10. **Telegram commands stopped working.** The command listener's long-poll was blocking the shared aiohttp session. Separated into its own session but needs verification.

11. **Messages show slugs instead of team names.** `nba-lal-okc-04-02` instead of "Los Angeles Lakers vs Oklahoma City Thunder". The team registry has canonical names for all 929 teams but they're not used in Telegram display.

12. **Maker rebates shown in daily report.** Internal trading metrics shouldn't be in investor-facing messages.

13. **"Manual restart required" on floor breach.** Should say "Resets at midnight ET" and behave like daily target (stop for day, auto-reset).

### Pipeline/Matching
14. **Future games labeled as "broken."** Games on April 4-9 show as "112 broken (should be 0)" because the team-name matching finds the same team playing on a different date and flags it as broken instead of "waiting for bookmaker lines."

15. **Sport-specific logic is hardcoded guesswork.** CBB uses H1/H2 not Q1-Q4. Soccer uses elapsed minutes. MLB uses inning notation. The parser was written to look right, not to work with real API data.

### Data/Supabase
16. **Supabase investor fund data incomplete.** Daily snapshots used real balance. Paper trades counter was broken. Cumulative P&L wasn't calculated.

17. **Team registry not used universally.** Pipeline uses it for matching but Telegram, trade records, and position display use whatever name the pipeline passes through. Should resolve to canonical names everywhere.

### Daily Cycle
18. **Midnight reset has bugs.** Morning Telegram uses `await` on a sync function (`_enqueue`). Session start value gets overwritten after restore. Loss tiers were using unrealized P&L instead of realized only.

19. **Session lock blocks all strategies.** When daily target hit, `entries_halted = True` blocks everything including exception/fade which the config says should remain active. Fixed to block all entries on lock.

20. **No feedback loop.** Bot makes a trade, exits, moves on. Doesn't evaluate whether past decisions were correct. Same mistakes repeat daily.

## THE STRATEGY

Read STRATEGY_V2.md — that is the complete strategy. Do NOT use the old strategy in CLAUDE.md. Key points:

- Four-state trade model: Entry → Advancement → Protection → Exit
- Floors and ceilings anchored to PROBABILITY, not price
- Edge must persist across 2+ pipeline refreshes before entry
- All four entry conditions must be met (edge, persistence, liquidity, market behavior)
- Sport-specific game timing parsed from real API data (period, elapsed, score)
- When time can't be determined, HOLD — never assume game is ending
- Primary markets: totals and spreads (requires pipeline step 6 update). Secondary: moneylines.
- Daily target +15%, loss tiers at -5%/-10%/-15% using REALIZED P&L only
- Never re-enter a game already traded
- Build Security Manager protocol enforced at all times

## INVESTOR DETAILS

- Colin Maynard: $1,200 initial capital
- Hugo Sanchez: $1,200 initial capital
- Total fund: $2,400
- Paper mode: 0/300 trades toward live unlock (need 70%+ win rate)

## DROPLET

- IP: 137.184.159.0
- User: root
- 4GB RAM, 25GB disk
- systemd service: oraclefarming
- Bot directory: /root/PolyFarm/bot/
- Log: /tmp/oraclefarming.log
- Deploy: `git pull origin main && systemctl restart oraclefarming`

## HOW TO FIX THIS

1. Build a real trading engine test that runs the ACTUAL trading code path against REAL live games
2. The test must use real API data — period, elapsed, score — not defaults
3. The test must simulate the 30-second position monitoring cycle
4. The test must track positions across time, not run once and stop
5. Every entry and exit decision must show full reasoning
6. Fix every issue against staging branch
7. Verify against a full evening of live games on staging
8. Only merge to main after user reviews and approves
9. Never push to main without staging verification

## DEPLOY WORKFLOW

```
staging branch → staging verification → PR to main → production deploy
```

No direct pushes to main. No "pull and restart." Code goes through staging first.
