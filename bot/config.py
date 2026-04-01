import os
import logging
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────
# POLYMARKET API
# ─────────────────────────────────────────────────────
POLYMARKET_TRADING_URL = "https://api.polymarket.us"
POLYMARKET_PUBLIC_URL = "https://gateway.polymarket.us"
WS_MARKETS = "wss://api.polymarket.us/v1/ws/markets"
WS_PRIVATE = "wss://api.polymarket.us/v1/ws/private"

# ─────────────────────────────────────────────────────
# FEE STRUCTURE — Polymarket US published rates
# ─────────────────────────────────────────────────────
TAKER_FEE_RATE = 0.003
MAKER_REBATE_RATE = 0.002

# ─────────────────────────────────────────────────────
# ORACLE ARB BAND THRESHOLDS
# Fee-adjusted for high-volume farming.
# Round-trip cost ~0.6% of price. Bands set above
# fee break-even with profit margin.
# No price floor — trade any price where edge > fees.
# ─────────────────────────────────────────────────────
BAND_A_MIN_PRICE = 0.50
BAND_A_MIN_EDGE = 0.04
BAND_A_POSITION_PCT = 0.04

BAND_B_MIN_PRICE = 0.35
BAND_B_MAX_PRICE = 0.50
BAND_B_MIN_EDGE = 0.03
BAND_B_POSITION_PCT = 0.025

BAND_C_MIN_PRICE = 0.20
BAND_C_MAX_PRICE = 0.35
BAND_C_MIN_EDGE = 0.02
BAND_C_POSITION_PCT = 0.015

# No price floor — edge must cover fees, that's the only gate
FAVORITES_FLOOR = 0.15
# Reduce edge threshold by this amount for live games
LIVE_GAME_EDGE_REDUCTION = 0.01
CONFIDENCE_THRESHOLD = 0.85
MAX_SINGLE_SPORT_PCT = 0.40

# ─────────────────────────────────────────────────────
# PORTFOLIO STRUCTURE
# ─────────────────────────────────────────────────────
# Floor = 80% of session start wallet value
# If portfolio drops to floor: emergency exit
FLOOR_PCT = 0.80

# Exit target = entry + (edge × this multiplier)
REPRICE_EXIT_PCT = 0.65

# Hold-to-resolution qualification thresholds
HOLD_TO_RESOLUTION_MIN_EDGE = 0.12
HOLD_TO_RESOLUTION_MIN_PRICE = 0.65
HOLD_TO_RESOLUTION_MAX_PCT = 0.15

# ─────────────────────────────────────────────────────
# EXIT TRIGGER THRESHOLDS
# ─────────────────────────────────────────────────────
# Oracle arb profit lock by band
PROFIT_LOCK_BAND_A = 0.12
PROFIT_LOCK_BAND_B = 0.10
PROFIT_LOCK_BAND_C = 0.08
PROFIT_LOCK_OVERNIGHT = 0.15

# Trailing stop — let positions breathe
TRAILING_STOP_ACTIVATE = 0.06   # Activates at +6% gain
TRAILING_STOP_FLOOR = 0.50      # Floor = 50% of peak gain
TRAILING_STOP_FLOOR_PROTECTION = 0.65  # In PROTECTION mode

# Timeouts — hold through game volatility, exit if edge gone
REPRICE_TIMEOUT_MINUTES = 60
CRYPTO_REPRICE_TIMEOUT_MINUTES = 5

# ─────────────────────────────────────────────────────
# PORTFOLIO PROFIT TIERS — checked every 10 seconds
# ─────────────────────────────────────────────────────
HARVEST_THRESHOLD = 0.06         # +6% daily gain — reduce size
PROTECTION_THRESHOLD = 0.09      # +9% daily gain — tighten stops
LOCK_THRESHOLD = 0.12            # +12% daily gain — STOP TRADING
PORTFOLIO_TRAIL_REVERT = 0.04    # If was +9%, fell to +4%

# ─────────────────────────────────────────────────────
# PORTFOLIO LOSS TIERS — checked every 10 seconds
# ─────────────────────────────────────────────────────
DAILY_LOSS_REDUCE_TIER = -0.10   # -10%: size down 50%
DAILY_LOSS_PAUSE_TIER = -0.15    # -15%: no new entries
DAILY_LOSS_HALT_TIER = -0.20     # -20%: exit everything

# ─────────────────────────────────────────────────────
# EXCEPTION TRADE PARAMETERS
# Exception trades activate in HARVEST, PROTECTION,
# LOCKED, and PORTFOLIO_TRAIL modes only.
# ─────────────────────────────────────────────────────
EXCEPTION_POOL_PCT = 0.05
EXCEPTION_MAX_POSITION_PCT = 0.03
EXCEPTION_MAX_TRADES_PER_SESSION = 2
EXCEPTION_MIN_ORACLE_GAP = 0.10
EXCEPTION_MIN_VOLUME = 30000
EXCEPTION_REPRICE_PCT = 0.50
EXCEPTION_PROFIT_LOCK = 0.08
EXCEPTION_TRAILING_ACTIVATE = 0.04
EXCEPTION_TRAILING_FLOOR = 0.50
EXCEPTION_STOP_LOSS = -0.15
EXCEPTION_TIMEOUT_MINUTES = 60
EXCEPTION_MAX_BID_ASK_SPREAD = 0.04

# ─────────────────────────────────────────────────────
# FADE TRADE PARAMETERS
# Fade trades active in NORMAL, HARVEST, PROTECTION,
# LOCKED, and PORTFOLIO_TRAIL modes.
# Suspended in REDUCE, PAUSE, HALT, FLOOR_BREACH.
# ─────────────────────────────────────────────────────
FADE_POOL_PCT = 0.06
FADE_MAX_POSITION_PCT = 0.02
FADE_MAX_TRADES_PER_SESSION = 3
FADE_REPRICE_PCT = 0.50
FADE_PROFIT_LOCK = 0.07
FADE_TRAILING_ACTIVATE = 0.04
FADE_TRAILING_FLOOR = 0.50
FADE_STOP_LOSS = -0.15
FADE_TIMEOUT_MINUTES = 60
FADE_MIN_VOLUME = 25000
FADE_MAX_BID_ASK_SPREAD = 0.05

# Minimum oracle gap by fade team confidence tier
FADE_MIN_GAP = {
    "very_high": 0.08,
    "high":      0.10,
    "medium":    0.12,
}

# ─────────────────────────────────────────────────────
# OVERNIGHT PARAMETERS
# ─────────────────────────────────────────────────────
OVERNIGHT_MIN_EDGE = 0.12
OVERNIGHT_MIN_VOLUME = 20000
OVERNIGHT_MAX_POOL_PCT = 0.20
OVERNIGHT_REEVAL_HOUR = 6        # 6am re-evaluation
OVERNIGHT_EXIT_EDGE_THRESHOLD = 0.05

# ─────────────────────────────────────────────────────
# RESEARCH / PHASE 1B PARAMETERS
# ─────────────────────────────────────────────────────
PHASE1B_MAX_POOL_PCT = 0.15
PHASE1B_MAX_POSITION_PCT = 0.025
PHASE1B_MIN_EDGE = 0.08
PHASE1B_MIN_CONFIDENCE = 0.70
PHASE1B_STOP_LOSS = -0.08
PHASE1B_AUTO_ENTER = os.environ.get(
    "PHASE1B_AUTO_ENTER", "false"
).lower() == "true"
PHASE1B_ENABLED = os.environ.get(
    "PHASE1B_RESEARCH_ENABLED", "false"
).lower() == "true"

# ─────────────────────────────────────────────────────
# PAPER MODE AND LIVE UNLOCK
# ─────────────────────────────────────────────────────
PAPER_MODE = os.environ.get(
    "PAPER_MODE", "true"
).lower() == "true"
PAPER_TRADES_REQUIRED = 300
PAPER_WIN_RATE_REQUIRED = 0.70
PHASE2_ENABLED = os.environ.get(
    "PHASE2_CRYPTO_ENABLED", "false"
).lower() == "true"

# ─────────────────────────────────────────────────────
# DOMINANT TEAMS
# Team names must match Polymarket API exactly.
# Bot validates against actual market data at startup.
# Add/remove via Telegram: /addteam /removeteam
# Weekly auto-refresh from sports reference sites
# updates comeback_win_rate from live data.
# ─────────────────────────────────────────────────────
DOMINANT_TEAMS = {

    # NBA
    "Chicago Bulls": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.28,
        "deficit_range": (5, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "League leader in 10+ point comeback wins 2024-25"
    },
    "Indiana Pacers": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.32,
        "deficit_range": (5, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "12 wins from 15+ down in 2024-25 — NBA record"
    },
    "Oklahoma City Thunder": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.36,
        "deficit_range": (5, 12),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "SGA MVP. Best team in NBA 2025-26."
    },
    "Denver Nuggets": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.37,
        "deficit_range": (5, 12),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "Jokic efficiency. Home altitude advantage."
    },
    "Boston Celtics": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.35,
        "deficit_range": (5, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "very_high",
        "notes": "Championship experience. Market overreacts to deficits."
    },
    "Golden State Warriors": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.34,
        "deficit_range": (5, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "very_high",
        "notes": "Curry three-point runs erase deficits rapidly."
    },
    "Cleveland Cavaliers": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.35,
        "deficit_range": (5, 12),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "medium",
        "notes": "Best East record. Garland clutch play."
    },
    "Los Angeles Lakers": {
        "sport": "basketball_nba",
        "comeback_win_rate_when_trailing": 0.33,
        "deficit_range": (5, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "LeBron and Davis late game execution."
    },

    # MLB
    "Los Angeles Dodgers": {
        "sport": "baseball_mlb",
        "comeback_win_rate_when_trailing": 0.36,
        "deficit_range": (1, 3),
        "game_window_innings": (5, 8),
        "market_overreaction_tendency": "very_high",
        "notes": "Primary MLB target. Deepest lineup in baseball."
    },
    "New York Yankees": {
        "sport": "baseball_mlb",
        "comeback_win_rate_when_trailing": 0.33,
        "deficit_range": (1, 3),
        "game_window_innings": (5, 8),
        "market_overreaction_tendency": "high",
        "notes": "Historical comeback machine. High market volume."
    },
    "Houston Astros": {
        "sport": "baseball_mlb",
        "comeback_win_rate_when_trailing": 0.30,
        "deficit_range": (1, 2),
        "game_window_innings": (6, 8),
        "market_overreaction_tendency": "medium",
        "notes": "Elite process. Best late-inning manufacturing."
    },
    "Philadelphia Phillies": {
        "sport": "baseball_mlb",
        "comeback_win_rate_when_trailing": 0.29,
        "deficit_range": (1, 2),
        "game_window_innings": (6, 8),
        "market_overreaction_tendency": "medium",
        "notes": "Citizens Bank Park hitter-friendly. Power upside."
    },

    # NHL
    "Colorado Avalanche": {
        "sport": "icehockey_nhl",
        "comeback_win_rate_when_trailing": 0.34,
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "MacKinnon effect. Elite power play when trailing."
    },
    "Edmonton Oilers": {
        "sport": "icehockey_nhl",
        "comeback_win_rate_when_trailing": 0.35,
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "very_high",
        "notes": "McDavid and Draisaitl. Most dangerous trailing pair in NHL."
    },
    "Dallas Stars": {
        "sport": "icehockey_nhl",
        "comeback_win_rate_when_trailing": 0.31,
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "medium",
        "notes": "Elite defensive structure with explosive offense."
    },

    # NFL
    "Kansas City Chiefs": {
        "sport": "americanfootball_nfl",
        "comeback_win_rate_when_trailing": 0.44,
        "deficit_range": (3, 14),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "very_high",
        "notes": "Mahomes effect. Single best exception signal in all sports."
    },
    "San Francisco 49ers": {
        "sport": "americanfootball_nfl",
        "comeback_win_rate_when_trailing": 0.38,
        "deficit_range": (3, 14),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "Shanahan system. Second half trailing strength."
    },
    "Chicago Bears": {
        "sport": "americanfootball_nfl",
        "comeback_win_rate_when_trailing": 0.28,
        "deficit_range": (3, 10),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "medium",
        "notes": "Caleb Williams Year 2. Bot accumulates live data to confirm."
    },

    # NCAAB
    "Duke Blue Devils": {
        "sport": "basketball_ncaab",
        "comeback_win_rate_when_trailing": 0.38,
        "deficit_range": (5, 15),
        "game_window": {
            "halves": [2],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "very_high",
        "notes": "Brand effect. Cameron Indoor. Market overprices deficits."
    },
    "Kansas Jayhawks": {
        "sport": "basketball_ncaab",
        "comeback_win_rate_when_trailing": 0.36,
        "deficit_range": (5, 15),
        "game_window": {
            "halves": [2],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "Allen Fieldhouse. Home comeback rate exceptional."
    },
    "Kentucky Wildcats": {
        "sport": "basketball_ncaab",
        "comeback_win_rate_when_trailing": 0.35,
        "deficit_range": (5, 12),
        "game_window": {
            "halves": [2],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "Rupp Arena home court. Blue blood program."
    },
    "Connecticut Huskies": {
        "sport": "basketball_ncaab",
        "comeback_win_rate_when_trailing": 0.37,
        "deficit_range": (5, 12),
        "game_window": {
            "halves": [2],
            "min_seconds_remaining": 480
        },
        "market_overreaction_tendency": "high",
        "notes": "Back-to-back champions. Hurley coaching documented."
    },

    # Soccer
    "Manchester City": {
        "sport": "soccer_epl",
        "comeback_win_rate_when_trailing": 0.29,
        "deficit_range": (1, 1),
        "game_window": {"minute_range": (55, 80)},
        "market_overreaction_tendency": "high",
        "notes": "Guardiola adjustments. One goal deficit only."
    },
    "Arsenal": {
        "sport": "soccer_epl",
        "comeback_win_rate_when_trailing": 0.27,
        "deficit_range": (1, 1),
        "game_window": {"minute_range": (55, 80)},
        "market_overreaction_tendency": "medium",
        "notes": "Emirates home matches strongest signal."
    },
    "Los Angeles FC": {
        "sport": "soccer_usa_mls",
        "comeback_win_rate_when_trailing": 0.26,
        "deficit_range": (1, 1),
        "game_window": {"minute_range": (55, 80)},
        "market_overreaction_tendency": "medium",
        "notes": "Best MLS team. Markets less efficient — bigger gaps."
    },
}

# ─────────────────────────────────────────────────────
# FADE TEAMS
# We bet AGAINST these teams' comebacks by buying
# YES on their opponent (the leading team).
# ─────────────────────────────────────────────────────
FADE_TEAMS = {

    # MLB
    "Pittsburgh Pirates": {
        "sport": "baseball_mlb",
        "confidence": "very_high",
        "deficit_range": (2, 5),
        "game_window_innings": (6, 9),
        "reason": "Chronically thin roster. Market prices hope that never materializes."
    },
    "Chicago White Sox": {
        "sport": "baseball_mlb",
        "confidence": "very_high",
        "deficit_range": (2, 5),
        "game_window_innings": (5, 9),
        "reason": "101-223 combined record 2024-25. Historically bad."
    },
    "Milwaukee Brewers": {
        "sport": "baseball_mlb",
        "confidence": "high",
        "deficit_range": (2, 4),
        "game_window_innings": (6, 9),
        "reason": "Pitching dependent. Offense cannot manufacture late runs."
    },
    "Cleveland Guardians": {
        "sport": "baseball_mlb",
        "confidence": "high",
        "deficit_range": (2, 4),
        "game_window_innings": (6, 9),
        "reason": "Contact-heavy, no power. Cannot overcome quality relievers."
    },
    "Oakland Athletics": {
        "sport": "baseball_mlb",
        "confidence": "high",
        "deficit_range": (2, 5),
        "game_window_innings": (5, 9),
        "reason": "Rebuilding. Minimal talent. Widest applicable window."
    },
    "Colorado Rockies": {
        "sport": "baseball_mlb",
        "confidence": "high",
        "deficit_range": (2, 4),
        "game_window_innings": (6, 9),
        "reason": "Coors Field misleads market on road/pitching matchups."
    },
    "Miami Marlins": {
        "sport": "baseball_mlb",
        "confidence": "medium",
        "deficit_range": (2, 4),
        "game_window_innings": (6, 9),
        "reason": "Rebuild. Thin bullpen depth when trailing late."
    },
    "Texas Rangers": {
        "sport": "baseball_mlb",
        "confidence": "medium",
        "deficit_range": (2, 4),
        "game_window_innings": (6, 9),
        "reason": "Roster collapse post-championship. Market prices old identity."
    },

    # NBA
    "Utah Jazz": {
        "sport": "basketball_nba",
        "confidence": "very_high",
        "deficit_range": (8, 18),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 360
        },
        "reason": "20-47. Worst defense in NBA. 30th DRTG. Tanking."
    },
    "Brooklyn Nets": {
        "sport": "basketball_nba",
        "confidence": "very_high",
        "deficit_range": (8, 18),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 360
        },
        "reason": "Worst clutch record in entire NBA 2025-26."
    },
    "Washington Wizards": {
        "sport": "basketball_nba",
        "confidence": "high",
        "deficit_range": (8, 18),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 360
        },
        "reason": "Bottom two team in league. Trae Young arrival unstabilized."
    },
    "Sacramento Kings": {
        "sport": "basketball_nba",
        "confidence": "high",
        "deficit_range": (8, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 360
        },
        "reason": "29th net rating despite recognizable names."
    },
    "Charlotte Hornets": {
        "sport": "basketball_nba",
        "confidence": "medium",
        "deficit_range": (8, 15),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 360
        },
        "reason": "Consistent bottom-five team. No late-game execution."
    },

    # NHL — based on actual 2025-26 season data
    "Vancouver Canucks": {
        "sport": "icehockey_nhl",
        "confidence": "very_high",
        "deficit_range": (1, 3),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "reason": "21-40-8. Worst team in NHL. Minus-84 goal diff. Full fire sale. Quinn Hughes traded."
    },
    "New York Rangers": {
        "sport": "icehockey_nhl",
        "confidence": "very_high",
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "reason": "First team eliminated from playoffs in East. 29-35-9. Market prices historic brand."
    },
    "San Jose Sharks": {
        "sport": "icehockey_nhl",
        "confidence": "high",
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "reason": "Multi-year rebuild. Market prices contending-era name recognition."
    },
    "Chicago Blackhawks": {
        "sport": "icehockey_nhl",
        "confidence": "high",
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [2, 3],
            "min_seconds_remaining": 480
        },
        "reason": "Multi-year rebuild. Bedard developing but roster cannot execute comebacks."
    },
    "Winnipeg Jets": {
        "sport": "icehockey_nhl",
        "confidence": "medium",
        "deficit_range": (1, 2),
        "game_window": {
            "periods": [3],
            "min_seconds_remaining": 480
        },
        "reason": "Won Presidents Trophy last season. Now 30-30-12. Market still prices as dominant."
    },

    # NFL
    "New York Jets": {
        "sport": "americanfootball_nfl",
        "confidence": "very_high",
        "deficit_range": (5, 17),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "reason": "3-14 record. Organizational dysfunction. No offensive execution when trailing."
    },
    "Tennessee Titans": {
        "sport": "americanfootball_nfl",
        "confidence": "very_high",
        "deficit_range": (5, 17),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "reason": "3-14 record. Rebuilding. Cannot generate points against quality defenses."
    },
    "Las Vegas Raiders": {
        "sport": "americanfootball_nfl",
        "confidence": "high",
        "deficit_range": (5, 17),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "reason": "2-14 last season. Organizational chaos. Worst rushing offense."
    },
    "Arizona Cardinals": {
        "sport": "americanfootball_nfl",
        "confidence": "high",
        "deficit_range": (5, 14),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "reason": "3-14 record. Improving but bottom-three comeback efficiency."
    },
    "Carolina Panthers": {
        "sport": "americanfootball_nfl",
        "confidence": "medium",
        "deficit_range": (5, 14),
        "game_window": {
            "quarters": [3, 4],
            "min_seconds_remaining": 480
        },
        "reason": "Multi-year rebuild. No established late-game offensive identity."
    },
}

# ─────────────────────────────────────────────────────
# ACTIVE STRATEGY DETERMINATION
# Single source of truth for what is active and
# at what sizing in any given session state.
# Called before every entry decision.
# ─────────────────────────────────────────────────────
def get_active_strategies(profit_mode: str,
                           loss_mode: str) -> dict:
    """
    profit_mode: NORMAL | HARVEST | PROTECTION |
                 LOCKED | PORTFOLIO_TRAIL
    loss_mode:   NORMAL | REDUCE | PAUSE |
                 HALT | FLOOR_BREACH

    Returns dict of active strategies and their
    position size as fraction of total wallet.
    Empty dict means nothing is tradeable.
    """

    # Loss modes take absolute priority
    if loss_mode in ("FLOOR_BREACH", "HALT"):
        return {}

    if loss_mode == "PAUSE":
        return {}

    if loss_mode == "REDUCE":
        return {
            "band_a":    {"active": True,
                          "size": BAND_A_POSITION_PCT * 0.50},
            "band_b":    {"active": True,
                          "size": BAND_B_POSITION_PCT * 0.50},
            "band_c":    {"active": True,
                          "size": BAND_C_POSITION_PCT * 0.50},
            "exception": {"active": False},
            "fade":      {"active": False},
            "research":  {"active": False},
            "overnight": {"active": False},
        }

    # Profit modes — loss_mode is NORMAL from here
    if profit_mode == "LOCKED":
        return {
            "band_a":    {"active": False},
            "band_b":    {"active": False},
            "band_c":    {"active": False},
            "exception": {"active": True,
                          "size": EXCEPTION_MAX_POSITION_PCT},
            "fade":      {"active": True,
                          "size": FADE_MAX_POSITION_PCT * 0.75},
            "research":  {"active": False},
            "overnight": {"active": False},
        }

    if profit_mode == "PORTFOLIO_TRAIL":
        return {
            "band_a":    {"active": False},
            "band_b":    {"active": False},
            "band_c":    {"active": False},
            "exception": {"active": True,
                          "size": EXCEPTION_MAX_POSITION_PCT * 0.833},
            "fade":      {"active": True,
                          "size": FADE_MAX_POSITION_PCT * 0.75},
            "research":  {"active": False},
            "overnight": {"active": False},
        }

    if profit_mode == "PROTECTION":
        return {
            "band_a":    {"active": True,
                          "size": BAND_A_POSITION_PCT * 0.50},
            "band_b":    {"active": False},
            "band_c":    {"active": False},
            "exception": {"active": True,
                          "size": EXCEPTION_MAX_POSITION_PCT * 0.667},
            "fade":      {"active": True,
                          "size": FADE_MAX_POSITION_PCT * 0.75},
            "research":  {"active": False},
            "overnight": {"active": False},
        }

    if profit_mode == "HARVEST":
        return {
            "band_a":    {"active": True,
                          "size": BAND_A_POSITION_PCT * 0.75},
            "band_b":    {"active": True,
                          "size": BAND_B_POSITION_PCT * 0.75},
            "band_c":    {"active": True,
                          "size": BAND_C_POSITION_PCT * 0.75},
            "exception": {"active": True,
                          "size": EXCEPTION_MAX_POSITION_PCT},
            "fade":      {"active": True,
                          "size": FADE_MAX_POSITION_PCT},
            "research":  {"active": True,
                          "size": PHASE1B_MAX_POSITION_PCT},
            "overnight": {"active": False},
        }

    # NORMAL — everything at full size
    # Exception activates ABOVE normal only
    return {
        "band_a":    {"active": True,
                      "size": BAND_A_POSITION_PCT},
        "band_b":    {"active": True,
                      "size": BAND_B_POSITION_PCT},
        "band_c":    {"active": True,
                      "size": BAND_C_POSITION_PCT},
        "exception": {"active": False},
        "fade":      {"active": True,
                      "size": FADE_MAX_POSITION_PCT},
        "research":  {"active": True,
                      "size": PHASE1B_MAX_POSITION_PCT},
        "overnight": {"active": True,
                      "size": OVERNIGHT_MAX_POOL_PCT},
    }

# ─────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────
import pathlib
pathlib.Path("/var/log/polyfarm").mkdir(
    parents=True, exist_ok=True
)
logging.basicConfig(
    level=getattr(logging,
                  os.environ.get("LOG_LEVEL", "INFO")),
    format="%(asctime)s [%(levelname)s] "
           "%(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            "/var/log/polyfarm/bot.log"
        )
    ]
)
logger = logging.getLogger("polyfarm")
