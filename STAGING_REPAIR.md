# STAGING REPAIR PLAN

## READ THIS FIRST

This branch exists to fix the OracleFarming trading bot. The bot's pipeline (team matching, odds loading, game discovery) works. Everything after that — trading, monitoring, exiting, reporting — is broken. Do NOT deploy to production (main branch) until every issue is verified fixed on staging.

## WHAT THIS PROJECT IS

An automated sports prediction market trading bot on Polymarket US. It:
1. Compares real-time Polymarket CLOB prices against US bookmaker consensus (The Odds API)
2. Finds misprices and enters trades
3. Monitors positions using game state, sharp odds, team analysis
4. Exits when the edge is captured or the game situation changes
5. Tracks paper balance at $2,400 ($1,200 x 2 investors)
6. Reports via Telegram every 30 minutes
7. Runs 24/7 on a DigitalOcean droplet via systemd

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

## WHAT WORKS

- **Team registry** (bot/core/team_registry.py): 929 teams across 12 leagues. Exact matches. Verified.
- **Pipeline steps 1-8** (bot/core/pipeline.py): Discovers leagues, loads teams, matches to Odds API, loads odds, loads scores. All against real APIs.
- **Polymarket SDK**: Authenticated. Balance reads, BBO reads, order placement all work.
- **WebSocket connections**: Both Markets and Private connect on the droplet.
- **Supabase**: Schema exists, reads/writes work.
- **Telegram**: Can send and receive messages.
- **Systemd**: Bot runs as oraclefarming.service.
- **Health API** (bot/core/health.py): REST endpoints on port 8080 for diagnostics. Committed but not tested in production.

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

Read CLAUDE.md in the repo root for the full architecture. Key points:

- **Entry**: Find misprice between Polymarket CLOB price and bookmaker consensus. Enter when edge > threshold (Band A: 2c at 50c+, Band B: 1.5c at 30-50c, Band C: 1c at 15-30c).
- **Hold**: As long as sharp odds > entry price, hold. A 73% team down 10 in Q2 still wins 73% of the time.
- **Exit**: When sharp odds drop below entry price, OR game ends, OR profit target hit.
- **Late game**: Winning late = hold to settlement ($1.00). Losing late = no buyers anyway.
- **Daily target**: +15% = stop trading for the day. Let winners settle.
- **Daily loss**: -5% reduce size, -10% pause (resume at -5%), -15% done for the day. Uses REALIZED P&L only.
- **Never re-enter** a game we already traded.

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
