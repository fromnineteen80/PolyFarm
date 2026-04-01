#!/bin/bash
# OracleFarming Bot — Start
# Run from anywhere: bash /root/PolyFarm/bot/start.sh

set -e

BOT_DIR="/root/PolyFarm/bot"
LOG="/tmp/oraclefarming.log"

cd "$BOT_DIR"

# Pull latest code
echo "Pulling latest code..."
cd /root/PolyFarm && git pull origin main
cd "$BOT_DIR"

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
echo "Starting OracleFarming bot..."
echo "Log: $LOG"
python3 main.py > "$LOG" 2>&1 &
BOT_PID=$!
echo "Bot PID: $BOT_PID"

# Wait for pipeline startup
echo "Waiting for pipeline..."
sleep 40

# Show status
echo ""
echo "=== Pipeline Status ==="
grep -a -E "(Step [0-9]|Pipeline|matched|WebSocket connected|Buying power)" "$LOG" 2>/dev/null || echo "No output yet — check: tail -f $LOG"
echo ""
echo "=== Errors ==="
grep -a -c "ERROR" "$LOG" 2>/dev/null | xargs -I{} echo "{} errors found"
grep -a "ERROR" "$LOG" 2>/dev/null | head -5
echo ""
echo "=== Commands ==="
echo "  tail -f $LOG"
echo "  bash $BOT_DIR/stop.sh"
echo "  bash $BOT_DIR/start.sh"
