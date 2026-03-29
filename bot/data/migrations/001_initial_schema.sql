-- trades: every entry and exit across all strategies
CREATE TABLE IF NOT EXISTS trades (
    id BIGSERIAL PRIMARY KEY,
    timestamp_entry TIMESTAMPTZ NOT NULL,
    timestamp_exit TIMESTAMPTZ,
    session_id BIGINT,
    market_slug TEXT NOT NULL,
    sport TEXT,
    teams TEXT,
    market_type TEXT,
    band TEXT,
    position_type TEXT DEFAULT 'normal',
    entry_price DECIMAL(10,4),
    exit_price DECIMAL(10,4),
    sharp_prob_at_entry DECIMAL(10,4),
    raw_edge_at_entry DECIMAL(10,4),
    net_edge_at_entry DECIMAL(10,4),
    confidence_score DECIMAL(10,4),
    position_size_usd DECIMAL(10,2),
    shares INTEGER,
    taker_fee_paid DECIMAL(10,4),
    maker_rebate_earned DECIMAL(10,4),
    exit_type TEXT,
    pnl DECIMAL(10,4),
    pnl_pct DECIMAL(10,4),
    wallet_at_entry DECIMAL(10,2),
    wallet_at_exit DECIMAL(10,2),
    hold_duration_seconds INTEGER,
    hold_to_resolution BOOLEAN DEFAULT FALSE,
    resolution_outcome TEXT,
    paper_mode BOOLEAN NOT NULL DEFAULT TRUE,
    phase TEXT DEFAULT 'phase1',
    is_live_game BOOLEAN DEFAULT FALSE,
    game_state_at_entry JSONB,
    profit_mode_at_entry TEXT,
    loss_mode_at_entry TEXT,
    exception_trigger_reason TEXT,
    fade_team TEXT
);
ALTER TABLE trades DISABLE ROW LEVEL SECURITY;

-- sessions: one record per bot session
CREATE TABLE IF NOT EXISTS sessions (
    id BIGSERIAL PRIMARY KEY,
    date DATE,
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    start_wallet DECIMAL(10,2),
    end_wallet DECIMAL(10,2),
    floor_value DECIMAL(10,2),
    working_capital DECIMAL(10,2),
    trades_total INTEGER DEFAULT 0,
    trades_won INTEGER DEFAULT 0,
    win_rate DECIMAL(10,4),
    session_pnl DECIMAL(10,2),
    session_pnl_pct DECIMAL(10,4),
    peak_daily_gain_pct DECIMAL(10,4),
    best_trade_pnl DECIMAL(10,2),
    worst_trade_pnl DECIMAL(10,2),
    floor_breached BOOLEAN DEFAULT FALSE,
    daily_halt_triggered BOOLEAN DEFAULT FALSE,
    profit_lock_triggered BOOLEAN DEFAULT FALSE,
    lock_reason TEXT,
    total_fees_paid DECIMAL(10,4),
    total_rebates_earned DECIMAL(10,4),
    exception_trades INTEGER DEFAULT 0,
    exception_pnl DECIMAL(10,2) DEFAULT 0,
    fade_trades INTEGER DEFAULT 0,
    fade_pnl DECIMAL(10,2) DEFAULT 0,
    paper_mode BOOLEAN DEFAULT TRUE,
    phase TEXT DEFAULT 'phase1'
);
ALTER TABLE sessions DISABLE ROW LEVEL SECURITY;

-- daily_snapshots: wallet value per day for charts
CREATE TABLE IF NOT EXISTS daily_snapshots (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    wallet_value DECIMAL(10,2),
    floor_value DECIMAL(10,2),
    session_pnl DECIMAL(10,2),
    cumulative_pnl DECIMAL(10,2),
    cumulative_pnl_pct DECIMAL(10,4),
    trades_today INTEGER,
    win_rate_today DECIMAL(10,4),
    projected_1pct DECIMAL(10,2),
    projected_15pct DECIMAL(10,2),
    projected_2pct DECIMAL(10,2),
    paper_mode BOOLEAN
);
ALTER TABLE daily_snapshots DISABLE ROW LEVEL SECURITY;

-- daily_stats: full analytics per calendar day
CREATE TABLE IF NOT EXISTS daily_stats (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    starting_wallet DECIMAL(10,2),
    ending_wallet DECIMAL(10,2),
    daily_pnl DECIMAL(10,2),
    daily_pnl_pct DECIMAL(10,4),
    trades_total INTEGER,
    trades_won INTEGER,
    win_rate DECIMAL(10,4),
    band_a_trades INTEGER DEFAULT 0,
    band_a_won INTEGER DEFAULT 0,
    band_a_pnl DECIMAL(10,2) DEFAULT 0,
    band_b_trades INTEGER DEFAULT 0,
    band_b_won INTEGER DEFAULT 0,
    band_b_pnl DECIMAL(10,2) DEFAULT 0,
    band_c_trades INTEGER DEFAULT 0,
    band_c_won INTEGER DEFAULT 0,
    band_c_pnl DECIMAL(10,2) DEFAULT 0,
    exception_trades INTEGER DEFAULT 0,
    exception_won INTEGER DEFAULT 0,
    exception_pnl DECIMAL(10,2) DEFAULT 0,
    fade_trades INTEGER DEFAULT 0,
    fade_won INTEGER DEFAULT 0,
    fade_pnl DECIMAL(10,2) DEFAULT 0,
    moneyline_trades INTEGER DEFAULT 0,
    spread_trades INTEGER DEFAULT 0,
    totals_trades INTEGER DEFAULT 0,
    prop_trades INTEGER DEFAULT 0,
    reprice_exits INTEGER DEFAULT 0,
    timeout_exits INTEGER DEFAULT 0,
    resolution_exits INTEGER DEFAULT 0,
    stop_loss_exits INTEGER DEFAULT 0,
    total_fees DECIMAL(10,4) DEFAULT 0,
    total_rebates DECIMAL(10,4) DEFAULT 0,
    estimated_incentive_rewards DECIMAL(10,4) DEFAULT 0,
    peak_profit_mode TEXT,
    sports_breakdown JSONB,
    paper_mode BOOLEAN
);
ALTER TABLE daily_stats DISABLE ROW LEVEL SECURITY;

-- market_mappings: Polymarket slug to Odds API
CREATE TABLE IF NOT EXISTS market_mappings (
    id BIGSERIAL PRIMARY KEY,
    polymarket_slug TEXT UNIQUE,
    odds_api_event_id TEXT,
    sport TEXT,
    teams TEXT,
    market_type TEXT,
    line_value DECIMAL(10,2),
    mapping_status TEXT,
    mapping_confidence DECIMAL(10,4),
    last_confirmed TIMESTAMPTZ,
    failure_reason TEXT
);
ALTER TABLE market_mappings DISABLE ROW LEVEL SECURITY;

-- system_events: crashes, reconnects, halts, errors
CREATE TABLE IF NOT EXISTS system_events (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    event_type TEXT,
    description TEXT,
    metadata JSONB
);
ALTER TABLE system_events DISABLE ROW LEVEL SECURITY;

-- incentive_log: reward-eligible order tracking
CREATE TABLE IF NOT EXISTS incentive_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    order_id TEXT,
    market_slug TEXT,
    order_type TEXT,
    fee_or_rebate DECIMAL(10,4),
    incentive_type TEXT,
    paper_mode BOOLEAN
);
ALTER TABLE incentive_log DISABLE ROW LEVEL SECURITY;

-- capital_events: deposits and withdrawals
CREATE TABLE IF NOT EXISTS capital_events (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    event_type TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    units_assigned DECIMAL(20,8),
    ownership_pct_after DECIMAL(10,4),
    wallet_value_at_event DECIMAL(10,2),
    notes TEXT
);
ALTER TABLE capital_events DISABLE ROW LEVEL SECURITY;

-- investors: one record per person
CREATE TABLE IF NOT EXISTS investors (
    id BIGSERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    created_date DATE,
    units_held DECIMAL(20,8) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);
ALTER TABLE investors DISABLE ROW LEVEL SECURITY;

-- bot_config: key-value store for persistent state
CREATE TABLE IF NOT EXISTS bot_config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated TIMESTAMPTZ
);
ALTER TABLE bot_config DISABLE ROW LEVEL SECURITY;

-- research_signals: Phase 1B statistical model
CREATE TABLE IF NOT EXISTS research_signals (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    game_id TEXT,
    sport TEXT,
    home_team TEXT,
    away_team TEXT,
    game_time TIMESTAMPTZ,
    direction TEXT,
    poly_price_at_signal DECIMAL(10,4),
    model_probability DECIMAL(10,4),
    model_edge DECIMAL(10,4),
    combined_confidence DECIMAL(10,4),
    filter_outputs JSONB,
    pitcher_home TEXT,
    pitcher_away TEXT,
    weather_conditions JSONB,
    lineup_home JSONB,
    lineup_away JSONB,
    action_taken TEXT,
    trade_id BIGINT,
    paper_mode BOOLEAN
);
ALTER TABLE research_signals DISABLE ROW LEVEL SECURITY;

-- team_splits: historical situational records
CREATE TABLE IF NOT EXISTS team_splits (
    id BIGSERIAL PRIMARY KEY,
    team TEXT NOT NULL,
    sport TEXT NOT NULL,
    split_type TEXT NOT NULL,
    split_value TEXT NOT NULL,
    games INTEGER,
    wins INTEGER,
    win_rate DECIMAL(10,4),
    season INTEGER,
    last_updated TIMESTAMPTZ
);
ALTER TABLE team_splits DISABLE ROW LEVEL SECURITY;
