#!/bin/bash
# OracleFarming Bot Setup — DigitalOcean Droplet
# Run once: bash setup.sh
# Start bot: bash start.sh

set -e

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
    websockets

echo "Verifying dependencies..."
python3 -c "
from polymarket_us import AsyncPolymarketUS
from supabase import create_client
from core.pipeline import Pipeline
from core.team_registry import lookup_by_polymarket_id
print('All imports OK')
"

# Check .env
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found."
    echo "Create bot/.env with your credentials before starting."
    exit 1
fi

echo ""
echo "=== Setup complete ==="
echo "Start the bot: cd bot && bash start.sh"
