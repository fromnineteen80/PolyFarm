#!/bin/bash
# OracleFarming Bot — Start
# Run from anywhere: bash /root/PolyFarm/bot/start.sh

BOT_DIR="/root/PolyFarm/bot"
LOG="/tmp/oraclefarming.log"

cd "$BOT_DIR" || exit 1

# Stop any existing bot
pkill -f "python3 main.py" 2>/dev/null && echo "Stopped existing bot" && sleep 2 || true

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "ERROR: Run setup.sh first"
    exit 1
fi
source venv/bin/activate

# Verify .env
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

# Start bot (truncate log so we don't mix old/new output)
echo "Starting OracleFarming bot..."
> "$LOG"
python3 main.py > "$LOG" 2>&1 &
echo "PID: $!"

# Wait for pipeline
echo "Waiting for pipeline startup..."
for i in $(seq 1 50); do
    if grep -aq "Pipeline startup complete" "$LOG" 2>/dev/null; then
        break
    fi
    sleep 1
done

echo ""
echo "=== Status ==="
grep -a -E "(Buying power|Step [0-9]|Pipeline|matched|WebSocket connected)" "$LOG" 2>/dev/null || echo "Still starting — run: tail -f $LOG"

ERRORS=$(grep -ac "ERROR" "$LOG" 2>/dev/null || echo "0")
if [ "$ERRORS" != "0" ]; then
    echo ""
    echo "=== $ERRORS Errors ==="
    grep -a "ERROR" "$LOG" 2>/dev/null | head -5
fi

echo ""
echo "  tail -f $LOG"
echo "  bash /root/PolyFarm/bot/stop.sh"
