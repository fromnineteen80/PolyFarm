-- ═══════════════════════════════════════════════
-- 003_markets_table.sql
-- Creates the markets table that the bot writes
-- live market data to and the dashboard reads.
-- Also adds team color columns.
-- Safe to run on a live database with 001 and
-- 002 already applied.
-- ═══════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS markets (
  market_slug           TEXT UNIQUE NOT NULL PRIMARY KEY,
  event_id              TEXT,
  event_slug            TEXT,
  sport                 TEXT,
  league                TEXT,
  game_id               INTEGER,
  sportradar_game_id    TEXT,
  home_team             TEXT,
  away_team             TEXT,
  home_team_id          INTEGER,
  away_team_id          INTEGER,
  home_record           TEXT,
  away_record           TEXT,
  home_ranking          TEXT,
  away_ranking          TEXT,
  home_conference       TEXT,
  away_conference       TEXT,
  home_color            TEXT,
  away_color            TEXT,
  yes_price             FLOAT,
  bid_price             FLOAT,
  volume                FLOAT DEFAULT 0,
  liquidity             FLOAT DEFAULT 0,
  is_live               BOOLEAN DEFAULT FALSE,
  is_finished           BOOLEAN DEFAULT FALSE,
  game_status           TEXT,
  game_score            TEXT,
  game_period           TEXT,
  game_elapsed          TEXT,
  game_start_time       TIMESTAMPTZ,
  main_spread_line      FLOAT,
  main_total_line       FLOAT,
  market_type            TEXT DEFAULT 'moneyline',
  series_slug           TEXT,
  tournament_name       TEXT,
  current_sharp_prob    FLOAT,
  current_edge          FLOAT,
  current_price_velocity FLOAT,
  current_price_direction TEXT,
  current_net_buy_pressure FLOAT,
  odds_api_event_id     TEXT,
  match_confidence      FLOAT,
  last_sharp_update     TIMESTAMPTZ,
  last_movement_update  TIMESTAMPTZ,
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE markets DISABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS idx_markets_sport
  ON markets(sport);

CREATE INDEX IF NOT EXISTS idx_markets_live
  ON markets(is_live);

CREATE INDEX IF NOT EXISTS idx_markets_edge
  ON markets(current_edge);

CREATE INDEX IF NOT EXISTS idx_markets_updated
  ON markets(updated_at);

-- Auto-update timestamp
CREATE OR REPLACE TRIGGER update_markets_updated_at
  BEFORE UPDATE ON markets
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
