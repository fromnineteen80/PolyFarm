#!/bin/bash
# OracleFarming Bot — Update and restart
# Run from anywhere: bash /root/PolyFarm/bot/update.sh

cd /root/PolyFarm || exit 1

echo "Pulling latest code..."
git pull origin main || { echo "Pull failed — check network"; exit 1; }

cd bot
echo "Installing any new dependencies..."
source venv/bin/activate
pip install --quiet httpx python-dotenv supabase polymarket-us pynacl websockets aiohttp rich

echo "Restarting bot..."
bash start.sh
