-- ═══════════════════════════════════════════════
-- 002_odds_api_and_movement.sql
-- Adds The Odds API consensus sharp odds,
-- price movement tracking, and enriched
-- trade/market columns.
-- Safe to run on a live database with
-- 001_initial_schema.sql already applied.
-- ═══════════════════════════════════════════════


-- ═══════════════════════════════════════════════
-- SECTION 1 — ALTER trades TABLE
-- ═══════════════════════════════════════════════

ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  home_team TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  away_team TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  team_id INTEGER;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  team_record TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  sharp_prob FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  poly_price_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  edge_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  price_velocity_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  price_direction_at_entry TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  net_buy_pressure_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  consensus_home_book TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  odds_api_event_id TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  tournament_name TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  game_start_time TIMESTAMPTZ;


-- ═══════════════════════════════════════════════
-- SECTION 2 — ALTER market_mappings TABLE
-- ═══════════════════════════════════════════════

-- market_mappings from 001 had: polymarket_slug,
-- odds_api_event_id, sport, teams, market_type,
-- line_value, mapping_status, mapping_confidence,
-- last_confirmed, failure_reason.
-- Add columns for The Odds API matching.

ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  polymarket_event_id TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  sport_key TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_team_polymarket TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_team_polymarket TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_team_odds_api TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_team_odds_api TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  start_time TIMESTAMPTZ;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  match_confidence FLOAT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  match_method TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  matched_at TIMESTAMPTZ;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  is_active BOOLEAN DEFAULT TRUE;


-- ═══════════════════════════════════════════════
-- SECTION 3 — ALTER sessions TABLE
-- ═══════════════════════════════════════════════

ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_loaded INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_matched INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_unmatched INTEGER DEFAULT 0;


-- ═══════════════════════════════════════════════
-- SECTION 4 — NEW TABLE: sharp_odds
-- ═══════════════════════════════════════════════

-- Stores US bookmaker consensus fair probabilities
-- from The Odds API. Updated every 3 minutes.
-- Dashboard reads this for the Mispricing page.

CREATE TABLE IF NOT EXISTS sharp_odds (
  id                    UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  odds_api_event_id     TEXT UNIQUE NOT NULL,
  polymarket_slug       TEXT,
  sport_key             TEXT,
  home_team             TEXT NOT NULL,
  away_team             TEXT NOT NULL,
  commence_time         TIMESTAMPTZ,
  status                TEXT,
  consensus_home_prob   FLOAT,
  consensus_away_prob   FLOAT,
  consensus_draw_prob   FLOAT,
  bookmakers_used       JSONB,
  bookmaker_count       INTEGER DEFAULT 0,
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE sharp_odds DISABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS idx_sharp_odds_slug
  ON sharp_odds(polymarket_slug)
  WHERE polymarket_slug IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_sharp_odds_sport
  ON sharp_odds(sport_key);

CREATE INDEX IF NOT EXISTS idx_sharp_odds_updated
  ON sharp_odds(updated_at);


-- ═══════════════════════════════════════════════
-- SECTION 5 — NEW TABLE: price_history
-- ═══════════════════════════════════════════════

-- Rolling price movement data per market.
-- Written every 5 minutes by the bot from
-- the ws_markets price history buffer.
-- Dashboard reads for movement indicators.

CREATE TABLE IF NOT EXISTS price_history (
  id                    UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  market_slug           TEXT UNIQUE NOT NULL,
  snapshots             JSONB,
  trade_flow            JSONB,
  price_velocity        FLOAT,
  price_direction       TEXT,
  net_buy_pressure      FLOAT,
  current_price         FLOAT,
  price_30m_ago         FLOAT,
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE price_history DISABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS idx_price_history_slug
  ON price_history(market_slug);

CREATE INDEX IF NOT EXISTS idx_price_history_updated
  ON price_history(updated_at);


-- ═══════════════════════════════════════════════
-- SECTION 6 — UPDATED_AT TRIGGER
-- ═══════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_sharp_odds_updated_at
  BEFORE UPDATE ON sharp_odds
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_price_history_updated_at
  BEFORE UPDATE ON price_history
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ═══════════════════════════════════════════════
-- SECTION 7 — SEED BOT_CONFIG KEYS
-- ═══════════════════════════════════════════════

INSERT INTO bot_config (key, value) VALUES
  ('odds_api_last_poll', NULL),
  ('odds_api_requests_used', '0'),
  ('odds_api_requests_remaining', '100000'),
  ('markets_loaded_count', '0'),
  ('markets_matched_count', '0'),
  ('markets_unmatched_count', '0'),
  ('ws_markets_subscribed_slugs', '[]'),
  ('ws_reconnect_count', '0')
ON CONFLICT (key) DO NOTHING;
