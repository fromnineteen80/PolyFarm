# PolyFarm — Automated Sports Prediction Market Bot

## What It Does

PolyFarm runs three complementary trading strategies
simultaneously on Polymarket US Sports:

1. Oracle Arb (Bands A/B/C) — exploits pricing lag
   between sharp sportsbooks and Polymarket
2. Exception Trades — bets on dominant teams when
   session is in protected profit mode
3. Fade Trades — bets against structurally weak teams
   when market overprices their comeback probability

## Prerequisites

- DigitalOcean account
- GitHub account (private repo)
- Polymarket US account with API access
- The Odds API account (Developer tier minimum)
- Telegram account
- Supabase account

## API Key Setup

1. Polymarket: polymarket.us/developer
2. Odds API: the-odds-api.com
3. Telegram: @BotFather on Telegram
4. Supabase: supabase.com → new project

## Database Setup

After creating your Supabase project:
1. Go to SQL Editor in Supabase dashboard
2. Paste and run: data/migrations/001_initial_schema.sql
3. All tables and RLS settings applied automatically

## Server Deployment

1. Create $6/month Ubuntu 22.04 DigitalOcean Droplet
2. SSH: ssh root@YOUR_SERVER_IP
3. git clone your private GitHub repo
4. cd polyfarm && bash bot/deploy/setup.sh
5. Edit /opt/polyfarm/bot/.env with all API keys
6. Run SQL migration in Supabase
7. systemctl start polyfarm
8. Verify Telegram alert arrives on your phone

## Paper Trading

Default state is paper mode. Bot simulates all trades
without using real capital. 50 paper trades with 70%+
win rate required before live mode unlocks.

## Going Live

Set PAPER_MODE=false in .env
Restart: systemctl restart polyfarm
Bot verifies unlock requirements before first live order.

## Phase 2 Activation

When crypto markets open on Polymarket US:
Set PHASE2_CRYPTO_ENABLED=true in .env
Restart service.
See phase2/README.md for gRPC proto file setup.

## Monitoring

Watch Telegram for every trade alert.
Check logs: tail -f /var/log/polyfarm/bot.log
Restart: systemctl restart polyfarm
Status: systemctl status polyfarm
