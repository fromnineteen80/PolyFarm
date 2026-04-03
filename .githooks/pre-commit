#!/bin/bash
# Build Security Manager — Pre-Commit Hook
# Catches problems and explains them in plain English.

ERRORS=0
WARNINGS=""

# Rule: Never push to main directly
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
    echo ""
    echo "PROBLEM: You're trying to save changes directly to the live production code."
    echo "WHY IT MATTERS: Untested changes on production can break the trading bot."
    echo "SOLUTION: Switch to the staging branch first. Test there. Then merge to main."
    echo ""
    ERRORS=$((ERRORS + 1))
fi

# Rule: No fuzzy matching implementations
if git diff --cached -- '*.py' | grep -E "from fuzzywuzzy|from difflib|from rapidfuzz|partial_ratio|token_sort_ratio|SequenceMatcher|get_close_matches" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code is using a fuzzy matching library to guess team names."
    echo "WHY IT MATTERS: Fuzzy matching causes false trades. We had this problem before."
    echo "SOLUTION: Use the team registry exact lookups. lookup_by_polymarket_id() or lookup_by_polymarket_name(). Never guess."
    echo ""
    ERRORS=$((ERRORS + 1))
fi

# Rule: Team registry is locked
if git diff --cached --name-only | grep "team_registry.py" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Someone is trying to modify the team registry."
    echo "WHY IT MATTERS: The registry has 929 verified teams. Changing it risks breaking all team matching."
    echo "SOLUTION: The registry is locked. If a team needs updating, discuss with the user first."
    echo ""
    ERRORS=$((ERRORS + 1))
fi

# Rule: Paper mode must not call real balance/positions API
PAPER_API=$(git diff --cached -- '*.py' | grep -c "client.account.balances\|client.portfolio.positions" || true)
PAPER_GUARD=$(git diff --cached -- '*.py' | grep -c "PAPER_MODE\|paper_mode" || true)
if [ "$PAPER_API" -gt 0 ] && [ "$PAPER_GUARD" -eq 0 ]; then
    echo ""
    echo "PROBLEM: Code calls the real Polymarket wallet but doesn't check if we're in paper mode."
    echo "WHY IT MATTERS: In paper mode, calling the real wallet overwrites our $2,400 simulated balance with the real $322. This crashed the bot before."
    echo "SOLUTION: Wrap the API call in an 'if not PAPER_MODE' check, or use the paper balance from Supabase instead."
    echo ""
    WARNINGS="${WARNINGS}paper_api "
fi

# Rule: Team names must use registry
if git diff --cached -- '*.py' | grep -E "replace\(.*aec-.*\)|\.replace\(.*-2026" | grep -v "test_" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code is chopping up market slugs to display team names."
    echo "WHY IT MATTERS: Slugs like 'nba-lal-okc-04-02' are not human readable. Investors see gibberish."
    echo "SOLUTION: Look up the canonical team name from the registry. Every team has a proper name like 'Los Angeles Lakers'."
    echo ""
    WARNINGS="${WARNINGS}slugs "
fi

# Rule: Pipeline steps 1-8 are working
if git diff --cached -- 'bot/core/pipeline.py' | grep -E "step[1-8]_|_get_poly|_get_odds|_consensus" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code modifies pipeline steps 1-8 which are currently working."
    echo "WHY IT MATTERS: These steps discover games, load odds, and match teams. They're verified. Breaking them stops all trading."
    echo "SOLUTION: Only modify if absolutely necessary. Test against real API data. Confirm with user."
    echo ""
    WARNINGS="${WARNINGS}pipeline "
fi

# Rule: Check for tight polling loops
if git diff --cached -- '*.py' | grep -E "sleep\((0\.|1\b|2\b|3\b)" | grep -v "test_\|#" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code has a very short wait time (under 4 seconds) in a loop."
    echo "WHY IT MATTERS: On our 4GB server, rapid loops eat CPU and memory. This crashed the bot before with alert spam."
    echo "SOLUTION: Use longer intervals. Wallet checks every 30s. Heartbeat every 300s. Only WebSocket needs fast response."
    echo ""
    WARNINGS="${WARNINGS}polling "
fi

# Rule: Check for unclosed sessions
if git diff --cached -- '*.py' | grep "aiohttp.ClientSession()" | grep -v "async with\|close\|cleanup" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code creates a network connection that may never get closed."
    echo "WHY IT MATTERS: Unclosed connections leak memory. Over hours of running, this kills the bot."
    echo "SOLUTION: Either use 'async with' to auto-close, or ensure there's a cleanup function that closes it."
    echo ""
    WARNINGS="${WARNINGS}sessions "
fi

# Rule: Supabase write frequency
if git diff --cached -- '*.py' | grep -E "await.*upsert|await.*insert|await.*set_bot_config" | grep -v "only when\|if.*changed\|if.*!=\|change detection" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: Code writes to the database but may not check if the data actually changed."
    echo "WHY IT MATTERS: Writing the same data every 10 seconds wastes database capacity and slows the bot."
    echo "SOLUTION: Only write when data changes. Compare against the last written value before writing."
    echo ""
    WARNINGS="${WARNINGS}writes "
fi

# Rule: Edge detector changes
if git diff --cached -- 'bot/core/edge_detector.py' | grep -v "^[-+].*#" | grep -E "return None|continue" > /dev/null 2>&1; then
    echo ""
    echo "PROBLEM: The edge detector's entry logic was changed."
    echo "WHY IT MATTERS: Entry conditions must match STRATEGY_V2.md exactly. Wrong conditions mean bad trades."
    echo "SOLUTION: Check STRATEGY_V2.md entry conditions section. All four conditions must be met."
    echo ""
    WARNINGS="${WARNINGS}edge "
fi

if [ $ERRORS -gt 0 ]; then
    echo "============================================"
    echo "COMMIT BLOCKED by Build Security Manager."
    echo "Fix the problems above before proceeding."
    echo "============================================"
    exit 1
fi

if [ -n "$WARNINGS" ]; then
    echo "============================================"
    echo "BSM WARNINGS — review the notes above."
    echo "Commit allowed but verify these are intentional."
    echo "============================================"
fi

exit 0
