#!/bin/bash
set -e

echo "=== PolyFarm Server Setup ==="

apt update && apt upgrade -y
apt install -y python3.11 python3.11-pip \
    python3.11-venv git curl

cd /opt
git clone https://github.com/USERNAME/polyfarm.git
cd polyfarm/bot

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
mkdir -p /var/log/polyfarm

cp deploy/polyfarm.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable polyfarm

echo ""
echo "============================================"
echo "NEXT STEPS:"
echo "1. Run SQL migration in Supabase SQL editor"
echo "2. Edit /opt/polyfarm/bot/.env with all keys"
echo "3. systemctl start polyfarm"
echo "4. systemctl status polyfarm"
echo "5. tail -f /var/log/polyfarm/bot.log"
echo "============================================"
