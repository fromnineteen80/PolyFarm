# ORACLEFARMING STRATEGY V2

## IMPORTANT CONTEXT

This strategy REPLACES the strategy sections in CLAUDE.md. The pipeline, team registry, APIs, Supabase schema, systemd, Telegram infrastructure, WebSocket connections, and everything documented as "working" in STAGING_REPAIR.md stays exactly as-is. We are ONLY fixing what is broken and adjusting the trading strategy per this document.

The architecture diagram in CLAUDE.md remains accurate for the pipeline and data flow. The changes below affect the TRADING ENGINE — everything from edge detection through position management through exits.

---

## INFRASTRUCTURE

Behind the scenes, OracleFarming runs on a cloud-hosted production stack built for continuous market monitoring, execution, and oversight.

### DigitalOcean — Production Runtime

The cloud infrastructure layer where the live bot operates continuously on a Droplet (virtual machine). 4GB RAM, 25GB disk, Ubuntu 24.04. The bot runs as a systemd service (`oraclefarming.service`) that starts on boot, restarts on crash, and runs 24/7. DigitalOcean's API allows programmatic management and its monitoring provides real-time resource metrics. This is the machine and operating environment, not the strategy engine.

### Python Bot — Execution Core

The live engine that connects to Polymarket and odds sources, processes WebSocket and REST data, runs the registry and signal logic, applies risk rules, and places and manages trades. It owns real-time market state, trade lifecycle management, session rules, and all floor/ceiling logic. This is the actual trading system. Located at `bot/` in the repo.

### Three APIs — By Function

**Polymarket (market data + execution surface):** Gateway API (`gateway.polymarket.us`) for v2 event discovery, game state, scores. SDK (`api.polymarket.us`) for BBO pricing, order placement, balance, positions. WebSocket (`wss://api.polymarket.us/v1/ws/markets` and `/ws/private`) for real-time price ticks and order fills. One feeds market structure and execution.

**The Odds API (external sharp reference line):** Provides vig-removed consensus probabilities from DraftKings, FanDuel, BetMGM, Caesars, BetRivers, and others. Odds endpoint for live h2h/spreads/totals. Scores endpoint for final results. Participants endpoint for team name verification. One feeds external truth.

**DigitalOcean API (infrastructure control):** Supports deployment actions, operational visibility, and resource management. Manages the machine that runs the system.

### Team Registry — Normalization Layer

929 teams across 12 leagues. Every team has a canonical name, Polymarket ID, Odds API name, league, sport, color, abbreviation. Different APIs label teams differently — the registry creates one canonical internal ID so signals are never triggered off mismatched events. Lookup by `polymarket_id` first (unique, never ambiguous). This is not cosmetic. It is a core control layer that prevents false trades.

### Pipeline — Data Flow Engine

Steps 1-8 run every 60 seconds:
1. Discover leagues from Polymarket v2
2. Load teams from v2 events
3. Map to Odds API sport keys
4. Load odds (bookmaker consensus)
5. Match teams via registry (polymarket_id lookup)
6. Load games with ET times and buckets
7. Match games to Odds API events
8. Load scores from Odds API

Step 9 writes to Supabase for the dashboard. The pipeline also syncs MarketRegistry for the position monitor and subscribes matched slugs to the Markets WebSocket.

### Supabase — Data Store

Tables: `trades` (every entry/exit with P&L), `markets` (live game data for dashboard), `sharp_odds` (bookmaker consensus), `daily_snapshots` (end-of-day summaries), `investor_profiles` (capital and ownership), `bot_config` (session state, paper balance), `system_events` (logs).

### Next.js Dashboard — Operator Interface (10% complete)

Located at `dashboard/`. Deployed on Vercel. Current state: navbar skeleton works, Google OAuth login works, initial profile edit works (but can't access profile page after or edit it), loose attempt at home page tables with column uniformity. Team registry, scores, and actual API endpoints are NOT integrated. About 2% functionally complete. The dashboard should not trade. It should display system health, live positions, session P&L, qualifying signals, trade logs, and risk state, with limited operator controls (pause, resume, safe restart). That is the target state, not the current state.

### Telegram — Alert and Remote Command Layer

Sends batched 30-minute trade summaries. Receives commands (`status`, `positions`, `trades`, `target`, `stop`, `start`, `investors`, `help`). Uses Telegram Bot API with long-polling (`getUpdates`). Serves as lightweight operator channel for real-time alerts (ceiling hit, floor breach, bot paused, feed mismatch) and session oversight.

### Health API — Diagnostic Surface

REST endpoints on port 8080 (`bot/core/health.py`): `/health`, `/status`, `/positions`, `/decisions`, `/errors`, `/games`, `/pipeline`. Enables remote monitoring without SSH. Committed but not yet verified in production.

---

## WHAT ORACLEFARMING DOES

An automated probability execution system on Polymarket US. Identifies, filters, and executes trades based on measurable mispricing between Polymarket's order book and normalized, vig-removed consensus probabilities from regulated sportsbooks. Does not predict outcomes. Selectively participates only when a statistically valid and executable edge exists. Capital deployed with strict discipline to preserve edge through execution.

Prioritizes consistency over volume. Trades taken only when signal quality, persistence, and liquidity align. No trade is a valid outcome when conditions are not met.

---

## MARKET SELECTION

**Primary: Totals and Spreads.** Continuous pricing instruments shaped by sharper inputs. Tighter alignment across sportsbooks. More stable price movement. Smaller edges but higher execution reliability and realized win rate.

**Secondary: Moneyline/Winners.** More volatile, narrative-driven. Larger apparent edges but less stable. Used only when edge strength, persistence, and liquidity all exceed higher thresholds.

Totals are particularly stable because they depend on game dynamics rather than team narrative. This reduces noise and improves signal clarity.

---

## ENTRY CONDITIONS (ALL FOUR REQUIRED)

1. **True edge exists** after vig removal from bookmaker consensus
2. **Edge persists** — observed across at least 2 consecutive pipeline refreshes (2+ minutes)
3. **Sufficient liquidity** at intended entry price (bid/ask depth >= 3)
4. **Market behavior supports** the signal — stability or confirmation from price direction

If any condition fails, no trade. Sitting out is a valid outcome.

### Entry Filters

- Game must not exceed 75% completion (sport-specific — see Sport Timing below)
- Edge must be executable via limit order at a price that preserves the edge
- No re-entry on any game already traded this session
- Sport concentration cannot exceed 40% of open exposure
- Odds must be fresh (< 5 minutes since last Odds API update)

### Position Sizing (Tiered by Signal Quality)

- **High-confidence**: Strong persistent edge + deep liquidity → 4% of fund
- **Mid-tier**: Moderate edge + adequate liquidity → 2.5% of fund
- **Low-tier**: Marginal edge → 1.5% of fund or skip entirely

Falling price with widening gap → modest size increase (up to 1.15x). Rising price → reduce size (0.85x) or cancel entry.

---

## SPORT TIMING — REAL API DATA

The Polymarket v2 API returns these fields on every event:
- `period`: current game period (e.g. `H1`, `Q4`, `P2`, `T5`)
- `elapsed`: time elapsed in current period (e.g. `03:26`, `17:58`)
- `score`: current score (e.g. `23-31`, `2-0`)
- `live`: boolean
- `ended`: boolean

The bot MUST parse these correctly for every sport:

### NBA
- 4 quarters × 12 minutes = 48 minutes total
- Periods: `Q1`, `Q2`, `Q3`, `Q4`, `OT`
- `elapsed` counts up within the quarter
- Minutes remaining = (12 - elapsed_minutes) + (remaining_quarters × 12)
- Early game: Q1-Q2 (first 24 minutes). Dips are noise.
- Late game: Q4 last 5 minutes. Decisions matter.
- Entry cutoff: don't enter in Q4 or OT

### College Basketball (CBB)
- 2 halves × 20 minutes = 40 minutes total
- Periods: `H1`, `H2`, `End H1`, `End H2`
- `elapsed` counts up within the half
- Minutes remaining = (20 - elapsed_minutes) + (remaining_halves × 20)
- Early game: H1 (first 20 minutes). Dips are noise.
- Late game: H2 last 5 minutes.
- Entry cutoff: don't enter in H2 last 5 minutes or OT
- IMPORTANT: A score of 22-23 in H1 is NORMAL for college basketball. Do not treat as game-ending.

### NHL
- 3 periods × 20 minutes = 60 minutes total
- Periods: `P1`, `P2`, `P3`, `OT`
- `elapsed` counts up within the period
- Minutes remaining = (20 - elapsed_minutes) + (remaining_periods × 20)
- Early game: P1 (first 20 minutes). Dips are noise.
- Late game: P3 last 5 minutes.
- Entry cutoff: don't enter in P3 last 5 minutes or OT

### MLB
- 9 innings, no game clock
- Periods: `T1`/`B1` through `T9`/`B9` (Top/Bottom of inning)
- No `elapsed` field — progress measured by inning
- Game progress: inning / 9 (approximate)
- Early game: Innings 1-5. Dips are noise.
- Late game: Innings 8-9.
- Entry cutoff: don't enter in inning 8+
- A team down 1 run in inning 3 has plenty of game left

### NFL / College Football (CFB)
- 4 quarters × 15 minutes = 60 minutes total
- Periods: `Q1`, `Q2`, `Q3`, `Q4`, `OT`
- `elapsed` counts up within the quarter
- Minutes remaining = (15 - elapsed_minutes) + (remaining_quarters × 15)
- Early game: Q1-Q2 (first 30 minutes). Dips are noise.
- Late game: Q4 last 5 minutes.
- Entry cutoff: don't enter in Q4 or OT

### Soccer (EPL, MLS, La Liga, Bundesliga, Serie A, UCL)
- 2 halves × 45 minutes = 90 minutes total
- Periods: `1H`, `2H`, `ET` (extra time)
- `elapsed` is total match minutes (not per-half)
- Minutes remaining = 90 - elapsed_minutes
- Early game: first 60 minutes. Dips are noise.
- Late game: 80+ minutes.
- Entry cutoff: don't enter after 75 minutes
- A team down 1 goal at minute 30 has a full hour to equalize

### When Time Cannot Be Determined

If `period` or `elapsed` is None or unparseable, the bot MUST NOT trigger any time-based exit (pre_resolution, timeout). Default to HOLDING. Never assume the game is ending when you can't confirm it.

---

## TRADE STATE MODEL — FOUR STATES

Every trade moves through: **Entry → Advancement → Protection → Exit**

### State 1: Entry

Record at entry:
- `entry_price`: what we paid
- `fair_probability`: sharp consensus at time of entry
- `initial_edge`: fair_probability - entry_price
- `entry_time`: UTC timestamp
- `game_state`: period, elapsed, score at entry

Compute:
- `step_1_ceiling`: entry_price × 1.03 (3% gain)
- `step_2_ceiling`: entry_price × 1.06 (6% gain)
- `step_3_ceiling`: entry_price × 1.10 (10% gain — full exit)
- `soft_floor`: entry_price × 0.95 (5% loss — warning)
- `hard_floor`: entry_price × 0.85 (15% loss — exit if probability also broke)

### State 2: Advancement

Triggered when price reaches Step 1 ceiling (3% gain).

Actions:
- Raise floor to entry_price × 1.01 (lock in 1% gain minimum)
- Continue holding toward Step 2
- If price falls back to raised floor AND momentum stalls → exit with locked gain

If Step 2 ceiling reached (6% gain):
- Raise floor to entry_price × 1.03 (lock in 3% gain minimum)
- Continue holding toward Step 3

If Step 3 ceiling reached (10% gain):
- Exit fully. Remaining edge is minimal vs execution risk.

### State 3: Protection

Triggered when price drops toward floors.

**Soft floor hit (5% loss from entry):**
- Check sharp probability. If probability > entry_price → HOLD. This is noise.
- If probability dropped but still within 2% of entry → WARNING state. Monitor closely.
- If probability dropped below entry_price - 3% → escalate to hard floor check.

**Hard floor hit (15% loss from entry):**
- Check sharp probability.
- If probability STILL above entry_price → HOLD. Extreme noise but thesis intact.
- If probability broke below entry_price → EXIT IMMEDIATELY. Thesis is dead.

**Recovery from protection:**
- If price was at soft floor but probability stabilized, and price recovers above entry → reset to Advancement state. Pursue ceiling again.

### State 4: Exit

Triggers (first one wins):
1. **Step 3 ceiling hit**: Full exit at 10% gain.
2. **Raised floor hit after advancement**: Exit with locked gains (1% or 3% depending on how far we advanced).
3. **Hard floor + probability breakdown**: Exit at loss.
4. **Time expiry**: Edge hasn't materialized within the time window (see below). Edge compressed. Exit.
5. **Game over**: If winning → settle at $1.00. If losing → accept $0.00.

### Time Windows (Sport-Specific)

- **Pre-game entry**: Hold until game goes live. No timeout while waiting for kickoff.
- **NBA/CBB live**: Reevaluate after 20 minutes of hold time. If still in Entry state (no advancement), check if edge compressed. If edge gone, exit.
- **NHL live**: Reevaluate after 20 minutes.
- **MLB live**: Reevaluate after 3 innings of hold time.
- **NFL/CFB live**: Reevaluate after 15 minutes.
- **Soccer live**: Reevaluate after 20 minutes.

Reevaluation does NOT mean automatic exit. It means: check sharp probability. If edge still exists, keep holding. If edge compressed to < 0.5%, exit.

---

## GAME CONTEXT INTELLIGENCE

Every hold/exit decision uses REAL API data:

1. **Sharp odds vs entry price** — bookmakers still support us? This is the PRIMARY signal.
2. **Team record** — parse `record` field (e.g. "58-18"). Win rate > 65% = strong team, hold through dips. Win rate < 35% = weak, exit faster.
3. **Dominant team status** — from config.py DOMINANT_TEAMS dict. Comeback win rate, market overreaction tendency. OKC at 36% comeback rate = hold. Celtics at 35% = hold.
4. **Fade opponent** — from config.py FADE_TEAMS dict. If opponent is White Sox (101-223 combined record), they can't hold leads. Hold.
5. **Score in context of sport:**
   - NBA/CBB: down 15+ = hard to recover. Down 5 in Q1 = noise.
   - MLB: down 4+ runs = exit. Down 1 in inning 3 = hold.
   - NHL: down 3+ goals = exit. Down 1 in P1 = hold.
   - NFL/CFB: down 17+ (3 scores) = exit. Down 7 in Q1 = hold.
   - Soccer: down 2+ goals = exit. Down 1 before 60' = hold.
6. **Game progress** — early game dips are always noise. Late game dips are real.
7. **Late game reality** — winning late = hold to settlement ($1.00). No point selling at 92c with 2 minutes left. Losing late = no buyers anyway, accept settlement at $0.00.

Decision method: count hold reasons vs exit reasons. More reasons to hold = hold. BUT probability breakdown overrides everything — if sharp odds dropped below entry price, exit regardless of other signals.

---

## RISK ENGINE

Overrides all strategies:

- **+15% daily realized** → stop new trades. Let winners settle to $1.00. Reset midnight ET.
- **-5% realized** → reduce position sizes 50%
- **-10% realized** → pause entries. Resume if recovers to -5%.
- **-15% realized** → done for the day. Reset midnight ET.
- Loss tiers use **REALIZED P&L only** — unrealized mid-game dips are noise, not losses.
- **One entry per game per session** — no re-entry after any exit, win or lose.
- **Floor at 85% of session start** — absolute backstop. Stop for day, reset midnight.
- **Sport concentration cap** — no single sport > 40% of open exposure.

---

## DAILY CYCLE

- **Midnight ET**: `reset_daily()` — unlock session, reset all modes, re-anchor floor to current balance, clear exited games list, reset realized P&L to zero. Fresh start.
- **Morning Telegram**: "Good morning. New trading day. Opening balance: $X. Daily target (+15%): $Y. Floor (-15%): $Z. Ready to trade." Shows change from last night if balance shifted.
- **During day**: Selective trading when quality signals align across all sports and market types.
- **30-minute Telegram**: Batched summary — trades opened/closed, W/L record, P&L, balance, daily growth %, investor split.
- **Hit +15%**: "Daily target hit! No new trades. Open positions will close naturally."
- **Hit floor or -15%**: "Daily loss limit reached. No new trades until tomorrow. Resets at midnight ET."
- **Urgent alerts only**: Daily target hit, daily loss limit, floor breach. Sent immediately, not batched.

---

## TELEGRAM COMMANDS

| Command | Response |
|---------|----------|
| `status` | Balance, P&L, mode, investor split |
| `investors` | Each investor's capital, current value, growth |
| `positions` | Open positions with team names, entry, current price, game state |
| `trades` | Today's closed trades with team names, P&L, exit reason, hold time, score |
| `target` | Session start, current, daily target, floor |
| `stop` | Pause new entries. Open positions close naturally. |
| `start` | Resume trading (unless session locked). |
| `help` | Command list |

All messages use team registry canonical names. No slugs. No abbreviations. Human-readable exit reasons: "target hit", "locked in gains", "game ending", "held too long", "cut losses".

---

## FUND DETAILS

- Colin Maynard: $1,200 initial capital
- Hugo Sanchez: $1,200 initial capital
- Total fund: $2,400
- Paper mode: 0/300 trades toward live unlock (need 70%+ win rate)
- Paper balance tracked in Supabase `bot_config`, independent of real Polymarket wallet
- 50/50 split. Each investor's current value = total fund value / 2.

---

## DEPLOY WORKFLOW

```
staging branch → staging verification → PR to main → production deploy
```

No direct pushes to main. No "pull and restart." Code goes through staging first. Verified against live games before merge.

Production deploy script: `git pull origin main && systemctl restart oraclefarming`

Droplet: 137.184.159.0, root, systemd service `oraclefarming`, log at `/tmp/oraclefarming.log`
