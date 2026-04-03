#!/bin/bash
# Build Security Manager — Pre-Commit Hook
# Runs before every commit. Blocks violations.

ERRORS=0

# Rule: Never push to main directly
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
    echo "BSM BLOCKED: Cannot commit directly to main. Use staging branch."
    ERRORS=$((ERRORS + 1))
fi

# Rule: No fuzzy matching in Python code
if git diff --cached --name-only -- '*.py' | xargs grep -l "fuzz\|partial_match\|ratio\|difflib" 2>/dev/null; then
    echo "BSM BLOCKED: Fuzzy matching detected in Python files."
    ERRORS=$((ERRORS + 1))
fi

# Rule: Paper mode must not call balance/positions API
PAPER_API=$(git diff --cached -- '*.py' | grep -c "client.account.balances\|client.portfolio.positions" || true)
PAPER_GUARD=$(git diff --cached -- '*.py' | grep -c "PAPER_MODE\|paper_mode" || true)
if [ "$PAPER_API" -gt 0 ] && [ "$PAPER_GUARD" -eq 0 ]; then
    echo "BSM WARNING: Polymarket API call added without paper mode check."
fi

# Rule: Team names must use registry
if git diff --cached -- '*.py' | grep -E "replace\(.*aec-.*\)|\.replace\(.*-2026" | grep -v "test_" > /dev/null 2>&1; then
    echo "BSM WARNING: Slug string manipulation detected. Use team registry canonical names."
fi

# Rule: No unbounded data structures
if git diff --cached -- '*.py' | grep -E "\.append\(|\.update\(" | grep -v "pruning\|cleanup\|clear\|pop\|remove\|bounded\|window\|limit" > /dev/null 2>&1; then
    echo "BSM NOTE: Data structure growth detected. Verify it is bounded."
fi

# Rule: Don't break what works — team registry is locked
if git diff --cached --name-only | grep "team_registry.py" > /dev/null 2>&1; then
    echo "BSM BLOCKED: team_registry.py is VERIFIED and LOCKED. Do not modify."
    ERRORS=$((ERRORS + 1))
fi

# Rule: Pipeline steps 1-8 work — changes need justification
if git diff --cached -- 'bot/core/pipeline.py' | grep -E "step[1-8]_|_get_poly|_get_odds|_consensus" > /dev/null 2>&1; then
    echo "BSM WARNING: Pipeline steps 1-8 are VERIFIED working. Modifying core pipeline functions. Ensure this is justified and tested."
fi

# Rule: Check for strategy alignment
if git diff --cached -- 'bot/core/edge_detector.py' | grep -v "^[-+].*#" | grep -E "return None|continue" > /dev/null 2>&1; then
    echo "BSM NOTE: Edge detector exit point changed. Verify against STRATEGY_V2.md entry conditions."
fi

# Rule: Check for Supabase write frequency
if git diff --cached -- '*.py' | grep -E "await.*upsert|await.*insert|await.*set_bot_config" | grep -v "only when\|if.*changed\|if.*!=\|change detection" > /dev/null 2>&1; then
    echo "BSM NOTE: Supabase write detected. Verify it only writes when data changes."
fi

# Rule: Check for memory growth
if git diff --cached -- '*.py' | grep -E "\[.*\]\.append\(|dict\(\)" | grep -v "bounded\|window\|limit\|prune\|clear\|max" > /dev/null 2>&1; then
    echo "BSM NOTE: New data structure detected. Verify it has a cleanup/pruning mechanism."
fi

# Rule: Check for tight polling loops that cause lag
if git diff --cached -- '*.py' | grep -E "sleep\((0\.|1\b|2\b|3\b)" | grep -v "test_\|#" > /dev/null 2>&1; then
    echo "BSM WARNING: Short sleep interval detected (<4s). May cause CPU/memory stress on 4GB droplet."
fi

# Rule: Check for writing every cycle (storage/memory stress)
if git diff --cached -- '*.py' | grep -E "while True.*await.*write\|while True.*await.*insert\|while True.*await.*upsert" > /dev/null 2>&1; then
    echo "BSM WARNING: Write inside loop detected. Verify change detection prevents writing every cycle."
fi

# Rule: Check for large file reads/writes that could block the event loop
if git diff --cached -- '*.py' | grep -E "open\(.*\.log\|\.read\(\)" | grep -v "test_" > /dev/null 2>&1; then
    echo "BSM NOTE: File I/O detected. Verify it doesn't block the async event loop."
fi

# Rule: Check for aiohttp sessions that may not be closed
if git diff --cached -- '*.py' | grep "aiohttp.ClientSession()" | grep -v "async with\|close\|cleanup" > /dev/null 2>&1; then
    echo "BSM WARNING: aiohttp session created. Verify it gets closed on shutdown to prevent memory leaks."
fi

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "Commit blocked by Build Security Manager. Fix violations above."
    exit 1
fi

exit 0
