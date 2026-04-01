-- ═══════════════════════════════════════════════
-- 004_pipeline_et_and_buckets.sql
-- Adds Eastern time and game bucket columns to
-- the markets table. Pipeline converts all UTC
-- times to America/New_York and assigns each game
-- a bucket (live, today, upcoming, historical).
-- Safe to run on a live database with 001-003
-- already applied.
-- ═══════════════════════════════════════════════

-- Eastern time for game start (converted from UTC)
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS game_start_time_et TEXT;

-- Game bucket: live, today, upcoming, historical
ALTER TABLE markets
  ADD COLUMN IF NOT EXISTS game_bucket TEXT DEFAULT 'upcoming';

-- Index on game_bucket for dashboard filtering
CREATE INDEX IF NOT EXISTS idx_markets_game_bucket
  ON markets(game_bucket);

-- Index on game_start_time_et for date-range queries
CREATE INDEX IF NOT EXISTS idx_markets_game_start_time_et
  ON markets(game_start_time_et);
