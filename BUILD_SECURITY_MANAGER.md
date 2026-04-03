# BUILD SECURITY MANAGER

## AUTHORITY

This protocol governs all development on OracleFarming. It has authority over all agents, all code changes, and all deployments. No agent may override, bypass, or reinterpret these rules. If an agent encounters a conflict between this protocol and any other instruction, this protocol wins. Report the conflict to the user.

## PERSISTENCE

This file must be read at the start of every session. Every agent working on this project must acknowledge it before writing any code. Context from this file carries across sessions — if a previous session identified issues, they remain issues until explicitly resolved and marked verified.

## CONNECTION MANAGEMENT

Large file writes crash the connection. Rules:
- Never write a file longer than 100 lines in a single Write call
- Break large changes into multiple small edits
- Commit after each logical change, not in bulk
- Keep talking to the user between operations — silence means the connection may be dying
- If writing a new file, write it in sections using append, not one massive write

## PLAN OF THE DAY

At the start of each build segment, produce a Plan of the Day:

1. **What will be built** — specific deliverable, not vague description
2. **Which files will be touched** — exact file paths
3. **Which endpoints are involved** — Polymarket, Odds API, Supabase
4. **Which registry components are involved** — lookups, canonical names
5. **Which infrastructure is affected** — droplet, memory, Supabase writes, Telegram
6. **How it will be verified** — specific test, not "run it and see"
7. **What could go wrong** — identify risks before coding

The user must approve the Plan before any code is written.

## BUILD RULES

### Never
- Use fuzzy matching. Endpoints and team registry only.
- Google anything. Use the APIs we have.
- Assume data formats. Read real API responses first.
- Default to zero or None when data is unavailable. Hold state instead.
- Push to main. Everything goes to staging first.
- Write code without testing it against real API data.
- Tell the user something works when it hasn't been verified.
- Make silent changes. Every change is documented.
- Rewrite files when a targeted edit will do.
- Skip the team registry for any team name display or matching.

### Always
- Read the actual API response before writing parsing code.
- Use team registry canonical names for all display and storage.
- Check that paper mode never calls Polymarket balance or positions APIs.
- Check that Supabase writes only happen when data changes.
- Check that memory structures are bounded (no unbounded growth).
- Check that Telegram messages use human language, not internal jargon.
- Verify game state parser returns correct minutes_remaining for the sport.
- Anchor all exit decisions to probability first, price second.
- Follow the four-state trade model: Entry → Advancement → Protection → Exit.
- Use limit orders, not market orders.
- Track realized P&L separately from unrealized position value.

## VERIFICATION CHECKLIST

After each build segment, check:

- [ ] Does the strategy require this? (Reference STRATEGY_V2.md section)
- [ ] Is it feasible for infrastructure? (No trading lag, memory tax, or disk fill)
- [ ] Does it use real API data, not defaults or assumptions?
- [ ] Does it resolve team names through the registry?
- [ ] Does it work in paper mode without calling Polymarket balance/positions?
- [ ] Does it write to Supabase only when necessary?
- [ ] Does it handle API failures gracefully (503, timeout, empty response)?
- [ ] Does it parse game state correctly for the sport? (period, elapsed, score)
- [ ] Does it follow the four-state trade model?
- [ ] Is the Telegram output human-readable with canonical team names?
- [ ] Will it survive a bot restart? (State persisted in Supabase)
- [ ] Does it stay within the 4GB memory and 25GB disk constraints?

If ALL checks pass: mark **VERIFIED**.
If ANY check fails: mark **BLOCKED** and explain why to the user.

## CONTEXT THAT MUST PERSIST

### Source of Truth Files
- `STRATEGY_V2.md` — the trading strategy. All code must align to this.
- `STAGING_REPAIR.md` — known broken things. Add new issues as found.
- `BUILD_SECURITY_MANAGER.md` — this file. Governs all development.
- `CLAUDE.md` — original architecture. Pipeline sections still accurate. Strategy sections superseded by STRATEGY_V2.md.

### What Works (do not break)
- Team registry: 929 teams, 12 leagues, verified. File: `bot/core/team_registry.py`
- Pipeline steps 1-8: verified against real APIs. File: `bot/core/pipeline.py`
- Polymarket SDK: authenticated, BBO/balance/orders work
- WebSocket: both channels connect on droplet
- Supabase: schema exists, reads/writes work
- Systemd: oraclefarming.service runs 24/7

### What Is Broken (must fix — see STAGING_REPAIR.md for full list)
- Trading engine: edge detection through exit logic
- Game state parser: doesn't parse period/elapsed/score
- Paper mode: calls real Polymarket API
- Telegram: shows slugs, crashes, wrong balance
- Daily cycle: midnight reset bugs
- Position tracking: re-entry bug
- Exit logic: fires incorrectly, not probability-anchored

### Key Decisions Already Made
- Totals and spreads are primary markets (moneyline secondary)
- Pipeline needs Step 6 update to discover totals/spreads
- Four-state trade model with stepped ceilings and probability-anchored floors
- Edge must persist 2+ pipeline refreshes before entry
- Loss tiers use realized P&L only
- Paper seed: $2,400 ($1,200 x 2 investors)
- Daily target: +15%. Daily loss limit: -15%.
- One entry per game per session
- 30-minute batched Telegram summaries
- Staging branch for all development. PR to main only after verification.

### Investors
- Colin Maynard: $1,200
- Hugo Sanchez: $1,200

### Droplet
- IP: 137.184.159.0
- 4GB RAM, 25GB disk
- Bot: /root/PolyFarm/bot/
- Service: oraclefarming
- Log: /tmp/oraclefarming.log

## ESCALATION

If at any point the Build Security Manager detects:
- Fuzzy matching being introduced
- Team names not resolved through registry
- Paper mode calling real Polymarket APIs
- Exit logic not anchored to probability
- Unbounded memory growth
- Supabase writes on every cycle regardless of changes
- Code pushed to main without staging verification
- Strategy drift from STRATEGY_V2.md

STOP IMMEDIATELY. Do not continue building. Report to the user with:
- What was detected
- Which rule was violated
- What the correct approach is

The user decides how to proceed. No agent overrides this.
