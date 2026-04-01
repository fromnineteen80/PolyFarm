#!/bin/bash
# OracleFarming Bot — Start
# Usage: bash start.sh

set -e

cd "$(dirname "$0")"

# Stop any existing bot
pkill -f "python3 main.py" 2>/dev/null && echo "Stopped existing bot" && sleep 2 || true

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Run setup.sh first"
    exit 1
fi
source venv/bin/activate

# Verify .env
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

# Start bot with logging
LOG="/tmp/oraclefarming.log"
echo "Starting OracleFarming bot..."
echo "Log: $LOG"
python3 main.py > "$LOG" 2>&1 &
BOT_PID=$!
echo "Bot PID: $BOT_PID"

# Wait for pipeline startup
echo "Waiting for pipeline..."
sleep 25

# Show status
echo ""
echo "=== Pipeline Status ==="
grep -E "(Step [0-9]|Pipeline|matched|WebSocket connected|WS error|Buying power|ERROR|CRITICAL)" "$LOG" 2>/dev/null || echo "No output yet"
echo ""
echo "=== Commands ==="
echo "  tail -f $LOG              # Watch live log"
echo "  bash stop.sh              # Stop the bot"
echo "  grep ERROR $LOG           # Check errors"
