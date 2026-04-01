#!/bin/bash
# OracleFarming Bot Setup — DigitalOcean Droplet
# Run once: bash /root/PolyFarm/bot/setup.sh

set -e

BOT_DIR="/root/PolyFarm/bot"
cd "$BOT_DIR"

echo "=== OracleFarming Setup ==="

# Virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet \
    httpx \
    python-dotenv \
    supabase \
    polymarket-us \
    pynacl \
    websockets \
    aiohttp \
    rich

echo "Verifying imports..."
python3 -c "
from polymarket_us import AsyncPolymarketUS
from supabase import create_client
from core.pipeline import Pipeline
from core.team_registry import lookup_by_polymarket_id
import aiohttp
import rich
print('All imports OK')
"

# Check .env
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found."
    echo "Copy .env.example to .env and fill in your credentials."
    exit 1
fi

echo ""
echo "=== Setup complete ==="
echo "Start: bash $BOT_DIR/start.sh"
echo "Stop:  bash $BOT_DIR/stop.sh"
