# TEST ENVIRONMENTS

## READ BUILD_SECURITY_MANAGER.md FIRST

All test environments must follow BSM rules. No fuzzy matching. Real API data only. Team registry canonical names. Explain changes in plain English before editing.

## CRITICAL WARNING

These test environments must match STRATEGY_V2.md exactly. If the strategy changes, the tests must change. If a test produces results that contradict the strategy, STOP and report it.

---

## PURPOSE

Three test environments exist in `bot/tests/`. Their job is to verify the trading engine works correctly against real live games BEFORE any code touches the production droplet. Every test uses real API data from Polymarket and The Odds API. No mocks. No fakes.

---

## TEST 1: test_oracle_arb.py

**What it tests:** The pipeline and edge detection logic. Can we find real misprices on real games?

**What it must verify:**
- Pipeline steps 1-8 complete without errors
- Team matching uses registry polymarket_id lookup (not fuzzy)
- Edge calculation is correct: sharp_prob minus poly_price
- Edge persistence: observed across 2+ pipeline refreshes before qualifying
- Band classification matches STRATEGY_V2.md thresholds
- Entry filters work: game progress < 75%, fresh odds, liquidity check
- Qualifying games are real and currently on Polymarket
- Position sizing matches the tiered system in STRATEGY_V2.md

**What it must NOT do:**
- Simulate wins/losses by comparing sharp_prob > entry_price (that's cheating)
- Skip the entry conditions
- Use default values when API data is unavailable

**How to run:** `cd bot && PYTHONPATH=. python3 tests/test_oracle_arb.py`

**What output looks like:** List of qualifying games with full reasoning for each entry/skip decision. Edge, sharp prob, poly price, band, game state, team names from registry.

**Current status:** EXISTS but does not test entry persistence, game progress filtering, or real position sizing. Needs rebuild to match STRATEGY_V2.md.

---

## TEST 2: test_clob_intel.py

**What it tests:** CLOB intelligence — detecting crowd panic and overreaction on the Polymarket order book.

**What it must verify:**
- Fetches real BBO data from Polymarket SDK for live games
- Compares BBO price against sharp consensus from Odds API
- Detects panic situations: price dropped significantly but sharp odds stable
- Uses team registry for all team identification
- Uses game context: dominant team status, team record, score, game progress
- Recommends entry with proper position sizing per STRATEGY_V2.md
- Risk assessment: what could go wrong, what sport-specific factors apply

**What it must NOT do:**
- Assume a price drop is always panic (could be legitimate movement)
- Ignore game progress (a price drop in Q4 is different from Q1)
- Skip the persistence check

**How to run:** `cd bot && PYTHONPATH=. python3 tests/test_clob_intel.py`

**What output looks like:** Live games scanned with BBO data. For each game: current price vs sharp, gap percentage, whether panic is detected, team analysis, recommended action or skip with reasoning.

**Current status:** EXISTS but does not use the four-state trade model, does not check edge persistence, and simulates profit incorrectly. Needs rebuild to match STRATEGY_V2.md.

---

## TEST 3: test_full_engine.py

**What it tests:** The COMPLETE trading lifecycle. This is the most important test. It runs the same code path the real bot runs.

**What it must verify:**
- Game state parser correctly reads period, elapsed, score for EVERY sport
- Minutes remaining calculated correctly (not defaulted to 0 or None)
- Entry decisions match all four conditions in STRATEGY_V2.md
- Four-state trade model works: Entry → Advancement → Protection → Exit
- Stepped ceilings trigger at correct thresholds (3%, 6%, 10%)
- Floors are anchored to PROBABILITY not just price
- Soft floor (5% loss) checks sharp probability before deciding
- Hard floor (15% loss) exits only when probability ALSO broke
- Recovery logic: dip then probability stabilizes → back to advancement
- Time reevaluation: checks both hold time AND game time remaining
- Pre-game entry holds until game goes live (no timeout before kickoff)
- Late game: winning positions hold to settlement, losing with no probability = exit
- One entry per game per session (no re-entry)
- Paper balance tracked independently from real Polymarket wallet
- Every decision logged with full reasoning in plain English
- Telegram message simulation matches what investors would see
- Team names from registry canonical names everywhere

**What it must NOT do:**
- Run once and stop (must simulate the 30-second monitoring cycle)
- Use entry price as exit price (must use real BBO at exit time)
- Default time_remaining to 0 when unparseable (must hold instead)
- Skip the probability check on any exit decision
- Allow re-entry on a game already traded

**How to run:** `cd bot && PYTHONPATH=. python3 tests/test_full_engine.py`

**What output looks like:** A running log of a simulated trading session against real live games. Shows every entry with reasoning, every 30-second check with hold/exit reasoning, every exit with P&L. Ends with session summary and simulated Telegram message including investor split.

**Current status:** EXISTS but does not persist positions across cycles, does not simulate the monitoring loop, does not implement the four-state model, and uses simplified win/loss logic. Needs complete rebuild to match STRATEGY_V2.md.

---

## HOW TESTS RELATE TO EACH OTHER

```
test_oracle_arb.py     → Can we FIND edges? (Pipeline + detection)
test_clob_intel.py     → Can we SPOT panic? (CLOB + context analysis)
test_full_engine.py    → Can we TRADE profitably? (Complete lifecycle)
```

test_oracle_arb and test_clob_intel feed into test_full_engine. If the edge detection is wrong, trades will be wrong. If CLOB analysis is wrong, panic entries will be wrong. test_full_engine is the integration test that proves the whole system works.

---

## VERIFICATION BEFORE PRODUCTION

Before ANY code merges to main:

1. Run test_oracle_arb against real live games → all qualifying edges are real
2. Run test_clob_intel against real live games → panic detection is accurate
3. Run test_full_engine for a full evening of games → every decision is correct
4. Show output to user → user confirms decisions make sense
5. Only then create PR from staging to main

If any test produces a decision that contradicts STRATEGY_V2.md, the code is wrong, not the strategy. Fix the code.
