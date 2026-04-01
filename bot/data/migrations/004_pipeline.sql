-- ═══════════════════════════════════════════════
-- 004_pipeline.sql
-- All schema changes for the new pipeline.
-- Covers: ET time handling, game buckets, Odds API
-- scores on markets, and ET timestamps + trade
-- buckets on trades.
-- Safe to run on a live database with 001-003
-- already applied.
-- ═══════════════════════════════════════════════

-- ─── MARKETS TABLE ───────────────────────────

-- Eastern time for game start (converted from UTC)
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS game_start_time_et TEXT;

-- Game bucket: live, today, upcoming, historical
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS game_bucket TEXT DEFAULT 'upcoming';

CREATE INDEX IF NOT EXISTS idx_markets_game_bucket
  ON markets(game_bucket);

CREATE INDEX IF NOT EXISTS idx_markets_game_start_time_et
  ON markets(game_start_time_et);

-- Polymarket outcome/settlement data
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS outcome_prices JSONB;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS outcomes JSONB;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS ep3_status TEXT;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS market_closed BOOLEAN DEFAULT FALSE;

-- Odds API scores (from /v4/sports/{key}/scores endpoint)
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS odds_api_home_score TEXT;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS odds_api_away_score TEXT;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS odds_api_completed BOOLEAN DEFAULT FALSE;

ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS odds_api_score_update TIMESTAMPTZ;

-- ─── TRADES TABLE ────────────────────────────

-- Eastern time for trade entry
ALTER TABLE trades
  ADD COLUMN IF NOT EXISTS timestamp_entry_et TEXT;

-- Eastern time for trade exit
ALTER TABLE trades
  ADD COLUMN IF NOT EXISTS timestamp_exit_et TEXT;

-- Trade bucket: live (open), historical (closed)
ALTER TABLE trades
  ADD COLUMN IF NOT EXISTS trade_bucket TEXT DEFAULT 'live';

CREATE INDEX IF NOT EXISTS idx_trades_trade_bucket
  ON trades(trade_bucket);

CREATE INDEX IF NOT EXISTS idx_trades_entry_et
  ON trades(timestamp_entry_et);
