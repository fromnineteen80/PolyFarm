# PolyFarm Dashboard

Web dashboard for the PolyFarm automated sports prediction market bot. Reads from Supabase. Deployed on Vercel. The bot runs on DigitalOcean and writes all data.

## Google OAuth Setup

1. Go to console.cloud.google.com
2. Create new project: PolyFarm Dashboard
3. OAuth consent screen: External type
4. Add your Gmail as test user
5. Credentials → Create OAuth 2.0 Web Application
6. Add Authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google`
   - `https://your-vercel-url/api/auth/callback/google`
7. Copy Client ID and Client Secret to .env.local

## Vercel Deployment

1. Go to vercel.com → New Project
2. Import your polyfarm GitHub repository
3. Set Root Directory to `dashboard`
4. Add all environment variables from .env.local.example
5. Deploy
6. Update Google OAuth redirect URI with real Vercel URL
7. Auto-deploys on every push to main

## Environment Variables

| Variable | Description |
|----------|-------------|
| NEXT_PUBLIC_SUPABASE_URL | Supabase project URL |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Supabase anon/public key |
| NEXTAUTH_SECRET | Random secret for NextAuth |
| NEXTAUTH_URL | Your Vercel deployment URL |
| GOOGLE_CLIENT_ID | Google OAuth client ID |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret |
| GOOGLE_AUTHORIZED_EMAIL | Only this email can log in |

## Investor Ownership Unit Math

Unit-based ownership system:

- First deposit: investor gets 1000 units, total = 1000
- Subsequent deposits: new_units = (amount / wallet_value) x total_units
- Withdrawals: units_removed = (amount / wallet_value) x total_units
- Ownership % = investor_units / total_units x 100
- Investor value = ownership % / 100 x wallet_value

Example:
- A deposits $750. Units=1000, Total=1000, A=100%
- B deposits $750. B units=(750/750)x1000=1000. Total=2000. A=50%, B=50%
- Day 200, wallet=$15,000. A adds $1,000.
- new_units=(1000/15000)x2000=133.33
- A=1133.33/2133.33=53.1%. B=46.9%

## iPhone Home Screen (PWA)

Open in Safari → Share → Add to Home Screen. The dashboard is PWA-capable with dark status bar.

## Pages

| Page | Description |
|------|-------------|
| Overview | Portfolio value, open positions, recent trades |
| Projections | Growth vs 1%/1.5%/2% daily targets |
| Bands | Band A/B/C performance breakdown |
| Daily | Daily P&L results and charts |
| Range | Date range deep dive with comparison |
| Investors | Capital management and ownership tracking |
| History | Full trade history with filters and export |
| Performance | Analytics, Sharpe, drawdown, heatmaps |
| Sessions | Bot session history |
| Markets | Market mapping intelligence |
| Mispricing | Live mispricing monitor with fee calc |
| Teams | Dominant and fade team intelligence cards |
