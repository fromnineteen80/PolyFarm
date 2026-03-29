-- ═══════════════════════════════════════════════
-- 002_sdk_and_oddspapi.sql
-- Adds richer Polymarket data, Pinnacle sharp
-- odds from OddsPapi, and market-to-fixture
-- matching. Safe to run on a live database
-- with 001_initial_schema.sql already applied.
-- ═══════════════════════════════════════════════


-- ═══════════════════════════════════════════════
-- SECTION 1 — ALTER EXISTING TABLES
-- ═══════════════════════════════════════════════

-- trades: add SDK and OddsPapi enrichment columns
-- (sharp_prob_at_entry already exists as DECIMAL
-- from 001 — adding float version for new usage)
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  home_team TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  away_team TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  team_id INTEGER;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  team_record TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  oddspapi_fixture_id TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  sharp_prob FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  poly_price_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  edge_at_entry FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  pinnacle_home_decimal FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  pinnacle_away_decimal FLOAT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  tournament_name TEXT;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS
  game_start_time TIMESTAMPTZ;

-- market_mappings: add SDK and OddsPapi columns
-- to the existing table from 001
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_team TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_team TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_team_id INTEGER;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_team_id INTEGER;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_record TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_record TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_ranking TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_ranking TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  home_conference TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  away_conference TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  sportradar_game_id TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  polymarket_event_id TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  polymarket_event_slug TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  game_status TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  game_score TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  game_period TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  game_elapsed TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  current_sharp_prob FLOAT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  current_edge FLOAT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  oddspapi_fixture_id TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  series_slug TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  tournament_name TEXT;
ALTER TABLE market_mappings ADD COLUMN IF NOT EXISTS
  last_sharp_update TIMESTAMPTZ;
-- Columns that already exist from 001 and are
-- NOT re-added: polymarket_slug, odds_api_event_id,
-- sport, teams, market_type, line_value,
-- mapping_status, mapping_confidence,
-- last_confirmed, failure_reason

-- sessions: add market loading stats
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_loaded INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_matched INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  markets_unmatched INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS
  oddspapi_polls INTEGER DEFAULT 0;


-- ═══════════════════════════════════════════════
-- SECTION 2 — NEW TABLE: pinnacle_odds
-- ═══════════════════════════════════════════════

-- Stores the latest Pinnacle moneyline odds
-- for every fixture OddsPapi returns.
-- Updated every 3 minutes by the bot.
-- Dashboard reads this for the Mispricing page.

CREATE TABLE IF NOT EXISTS pinnacle_odds (
  id                    UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  oddspapi_fixture_id   TEXT UNIQUE NOT NULL,

  polymarket_slug       TEXT,

  sport                 TEXT NOT NULL,
  sport_id              INTEGER NOT NULL,
  tournament_id         INTEGER NOT NULL,
  tournament_name       TEXT NOT NULL,

  home_team             TEXT NOT NULL,
  away_team             TEXT NOT NULL,
  participant1_id       INTEGER NOT NULL,
  participant2_id       INTEGER NOT NULL,

  start_time            TIMESTAMPTZ NOT NULL,
  status_id             INTEGER NOT NULL DEFAULT 0,

  home_decimal          FLOAT,
  away_decimal          FLOAT,
  draw_decimal          FLOAT,

  home_fair_prob        FLOAT,
  away_fair_prob        FLOAT,
  draw_fair_prob        FLOAT,

  pinnacle_active       BOOLEAN DEFAULT TRUE,

  home_limit            INTEGER,
  away_limit            INTEGER,

  home_odds_changed_at  TIMESTAMPTZ,
  away_odds_changed_at  TIMESTAMPTZ,

  pinnacle_fixture_id   TEXT,

  created_at            TIMESTAMPTZ DEFAULT NOW(),
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pinnacle_odds_slug
  ON pinnacle_odds(polymarket_slug)
  WHERE polymarket_slug IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_pinnacle_odds_sport
  ON pinnacle_odds(sport);

CREATE INDEX IF NOT EXISTS idx_pinnacle_odds_status
  ON pinnacle_odds(status_id);

CREATE INDEX IF NOT EXISTS idx_pinnacle_odds_start
  ON pinnacle_odds(start_time);

CREATE INDEX IF NOT EXISTS idx_pinnacle_odds_updated
  ON pinnacle_odds(updated_at);


-- ═══════════════════════════════════════════════
-- SECTION 3 — NEW TABLE: oddspapi_fixture_mappings
-- ═══════════════════════════════════════════════

-- Links Polymarket market slugs to OddsPapi
-- fixture IDs. Built at startup and updated
-- as new markets appear.
-- Note: the existing market_mappings table from
-- 001 is preserved. This table stores the
-- OddsPapi-specific matching data separately.

CREATE TABLE IF NOT EXISTS oddspapi_fixture_mappings (
  id                    UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  polymarket_slug       TEXT UNIQUE NOT NULL,
  polymarket_event_id   TEXT,
  polymarket_event_slug TEXT,

  oddspapi_fixture_id   TEXT,

  sport                 TEXT NOT NULL,

  home_team_polymarket  TEXT,
  away_team_polymarket  TEXT,
  home_team_oddspapi    TEXT,
  away_team_oddspapi    TEXT,

  start_time            TIMESTAMPTZ,

  match_confidence      FLOAT DEFAULT 0,
  match_method          TEXT,

  matched_at            TIMESTAMPTZ,
  last_verified_at      TIMESTAMPTZ,

  is_active             BOOLEAN DEFAULT TRUE,

  created_at            TIMESTAMPTZ DEFAULT NOW(),
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fixture_mappings_fixture
  ON oddspapi_fixture_mappings(oddspapi_fixture_id)
  WHERE oddspapi_fixture_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_fixture_mappings_sport
  ON oddspapi_fixture_mappings(sport);

CREATE INDEX IF NOT EXISTS idx_fixture_mappings_active
  ON oddspapi_fixture_mappings(is_active);

CREATE INDEX IF NOT EXISTS idx_fixture_mappings_confidence
  ON oddspapi_fixture_mappings(match_confidence);


-- ═══════════════════════════════════════════════
-- SECTION 4 — NEW TABLE: oddspapi_participants
-- ═══════════════════════════════════════════════

-- Caches OddsPapi participant ID to name
-- mapping per sport. Populated once at startup
-- per sport and refreshed daily.

CREATE TABLE IF NOT EXISTS oddspapi_participants (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  sport_id        INTEGER NOT NULL,
  participant_id  INTEGER NOT NULL,
  participant_name TEXT NOT NULL,
  sport_name      TEXT NOT NULL,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(sport_id, participant_id)
);

CREATE INDEX IF NOT EXISTS idx_participants_sport
  ON oddspapi_participants(sport_id);

CREATE INDEX IF NOT EXISTS idx_participants_name
  ON oddspapi_participants(participant_name);


-- ═══════════════════════════════════════════════
-- SECTION 5 — NEW TABLE: oddspapi_tournaments
-- ═══════════════════════════════════════════════

-- Caches active tournament IDs the bot polls.
-- Populated at startup, refreshed daily.

CREATE TABLE IF NOT EXISTS oddspapi_tournaments (
  id                UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  tournament_id     INTEGER UNIQUE NOT NULL,
  tournament_slug   TEXT NOT NULL,
  tournament_name   TEXT NOT NULL,
  sport_id          INTEGER NOT NULL,
  sport_name        TEXT NOT NULL,
  category_slug     TEXT,
  category_name     TEXT,
  is_active         BOOLEAN DEFAULT TRUE,
  is_target         BOOLEAN DEFAULT FALSE,
  future_fixtures   INTEGER DEFAULT 0,
  upcoming_fixtures INTEGER DEFAULT 0,
  live_fixtures     INTEGER DEFAULT 0,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tournaments_sport
  ON oddspapi_tournaments(sport_id);

CREATE INDEX IF NOT EXISTS idx_tournaments_target
  ON oddspapi_tournaments(is_target)
  WHERE is_target = TRUE;


-- ═══════════════════════════════════════════════
-- SECTION 6 — ROW LEVEL SECURITY
-- ═══════════════════════════════════════════════

-- Note: 001 used DISABLE ROW LEVEL SECURITY on
-- all tables. New tables use ENABLE with policies
-- so dashboard (anon key) can read and bot
-- (service_role key) can read + write.

ALTER TABLE pinnacle_odds ENABLE ROW LEVEL SECURITY;
ALTER TABLE oddspapi_fixture_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE oddspapi_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE oddspapi_tournaments ENABLE ROW LEVEL SECURITY;

-- Anon (dashboard) can read everything
CREATE POLICY "anon_read_pinnacle_odds"
  ON pinnacle_odds FOR SELECT
  TO anon USING (true);

CREATE POLICY "anon_read_fixture_mappings"
  ON oddspapi_fixture_mappings FOR SELECT
  TO anon USING (true);

CREATE POLICY "anon_read_participants"
  ON oddspapi_participants FOR SELECT
  TO anon USING (true);

CREATE POLICY "anon_read_tournaments"
  ON oddspapi_tournaments FOR SELECT
  TO anon USING (true);

-- Service role (bot) can do everything
CREATE POLICY "service_all_pinnacle_odds"
  ON pinnacle_odds FOR ALL
  TO service_role USING (true);

CREATE POLICY "service_all_fixture_mappings"
  ON oddspapi_fixture_mappings FOR ALL
  TO service_role USING (true);

CREATE POLICY "service_all_participants"
  ON oddspapi_participants FOR ALL
  TO service_role USING (true);

CREATE POLICY "service_all_tournaments"
  ON oddspapi_tournaments FOR ALL
  TO service_role USING (true);


-- ═══════════════════════════════════════════════
-- SECTION 7 — UPDATED_AT TRIGGERS
-- ═══════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_pinnacle_odds_updated_at
  BEFORE UPDATE ON pinnacle_odds
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_fixture_mappings_updated_at
  BEFORE UPDATE ON oddspapi_fixture_mappings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_participants_updated_at
  BEFORE UPDATE ON oddspapi_participants
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_tournaments_updated_at
  BEFORE UPDATE ON oddspapi_tournaments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ═══════════════════════════════════════════════
-- SECTION 8 — SEED BOT_CONFIG KEYS
-- ═══════════════════════════════════════════════

INSERT INTO bot_config (key, value) VALUES
  ('oddspapi_sport_ids', '{}'),
  ('oddspapi_tournament_ids', '[]'),
  ('oddspapi_last_poll', NULL),
  ('oddspapi_polls_today', '0'),
  ('markets_loaded_count', '0'),
  ('markets_matched_count', '0'),
  ('markets_unmatched_count', '0'),
  ('ws_markets_subscribed_slugs', '[]'),
  ('ws_reconnect_count', '0')
ON CONFLICT (key) DO NOTHING;


-- ═══════════════════════════════════════════════
-- VERIFICATION QUERIES
-- Run these after applying to confirm success.
-- ═══════════════════════════════════════════════

-- SELECT column_name FROM information_schema.columns
-- WHERE table_name = 'trades'
-- AND column_name IN (
--   'home_team', 'away_team', 'team_id',
--   'sharp_prob', 'poly_price_at_entry',
--   'edge_at_entry', 'oddspapi_fixture_id'
-- );
-- Should return 7 rows

-- SELECT column_name FROM information_schema.columns
-- WHERE table_name = 'market_mappings'
-- AND column_name IN (
--   'home_team', 'away_team', 'current_sharp_prob',
--   'current_edge', 'oddspapi_fixture_id',
--   'game_score', 'game_period'
-- );
-- Should return 7 rows

-- SELECT table_name FROM information_schema.tables
-- WHERE table_schema = 'public'
-- AND table_name IN (
--   'pinnacle_odds',
--   'oddspapi_fixture_mappings',
--   'oddspapi_participants',
--   'oddspapi_tournaments'
-- );
-- Should return 4 rows

-- SELECT COUNT(*) FROM bot_config
-- WHERE key IN (
--   'oddspapi_sport_ids',
--   'oddspapi_tournament_ids',
--   'oddspapi_last_poll',
--   'ws_markets_subscribed_slugs'
-- );
-- Should return 4
