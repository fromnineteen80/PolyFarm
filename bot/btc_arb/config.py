"""
BTC Arbitrage Bot Configuration

Strategy: exploit the latency between real-time BTC price feeds
and Polymarket BTC prediction contract updates.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────
# PRICE FEED SOURCES
# ─────────────────────────────────────────────────────
# Binance WebSocket — primary (free, real-time, <10ms)
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
# Coinbase REST — secondary confirmation
COINBASE_TICKER_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
# CryptoQuant — on-chain signal (requires API key)
CRYPTOQUANT_API_KEY = os.environ.get("CRYPTOQUANT_API_KEY", "")
CRYPTOQUANT_BASE_URL = "https://api.cryptoquant.com/v1"

# ─────────────────────────────────────────────────────
# POLYMARKET BTC MARKETS
# ─────────────────────────────────────────────────────
POLYMARKET_PUBLIC_URL = "https://gateway.polymarket.us"
# Search for BTC bracket markets — "Will BTC be above $X?"
BTC_MARKET_KEYWORDS = ["bitcoin", "btc"]

# ─────────────────────────────────────────────────────
# LAG DETECTION THRESHOLDS
# ─────────────────────────────────────────────────────
# Minimum price lag to trigger a trade (0.3% = 0.003)
MIN_LAG_PCT = 0.003
# How stale a Polymarket price must be vs spot (seconds)
MIN_LAG_STALENESS_MS = 500
# Maximum age of spot price data before considered stale (ms)
MAX_SPOT_AGE_MS = 2000
# Minimum confidence from multiple feeds before acting
MIN_FEED_AGREEMENT = 2  # at least 2 feeds must agree

# ─────────────────────────────────────────────────────
# RISK MANAGEMENT
# ─────────────────────────────────────────────────────
# Maximum risk per trade as fraction of bankroll
RISK_PER_TRADE = 0.005  # 0.5%
# Maximum daily loss as fraction of bankroll
DAILY_LOSS_CAP = 0.02  # 2%
# Maximum concurrent open positions
MAX_CONCURRENT_POSITIONS = 5
# Maximum position size in USD
MAX_POSITION_USD = 50.0
# Minimum position size in USD
MIN_POSITION_USD = 5.0

# ─────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────
# Target execution latency (ms)
TARGET_EXEC_MS = 100
# Timeout for order placement (seconds)
ORDER_TIMEOUT_S = 5
# Price must still be lagging at execution time
RECHECK_LAG_BEFORE_EXEC = True

# ─────────────────────────────────────────────────────
# FEE OPTIMIZATION — MAKER vs TAKER ROUTING
# ─────────────────────────────────────────────────────
# If lag detected > this threshold, we have time to post
# a maker limit order and earn the rebate instead of paying taker fee.
# Below this, we take liquidity immediately (speed > savings).
MAKER_LAG_THRESHOLD = 0.005  # 0.5%+ lag = use maker order
# How long to wait for a maker fill before converting to taker (ms)
MAKER_FILL_TIMEOUT_MS = 3000  # 3 seconds
# Maker limit price offset — post slightly inside the spread
# e.g., if fair=0.65, post at 0.645 (0.005 below fair)
MAKER_PRICE_OFFSET = 0.005

# ─────────────────────────────────────────────────────
# BRACKET STACKING
# ─────────────────────────────────────────────────────
# When a BTC move misprices multiple brackets, trade them all.
# Max simultaneous bracket entries per BTC move event.
MAX_STACK_SIZE = 4
# Minimum seconds between stacked entries (avoid self-competition)
STACK_SPACING_MS = 200
# Scale down position size for stacked trades (2nd, 3rd, 4th)
STACK_SIZE_DECAY = [1.0, 0.8, 0.6, 0.4]

# ─────────────────────────────────────────────────────
# POLYMARKET WEBSOCKET — real-time contract prices
# ─────────────────────────────────────────────────────
WS_MARKETS_URL = "wss://api.polymarket.us/v1/ws/markets"
# Subscription batch size (same as sports bot)
WS_BATCH_SIZE = 10

# ─────────────────────────────────────────────────────
# EXIT STRATEGY
# ─────────────────────────────────────────────────────
# Take profit when contract catches up to fair value
TAKE_PROFIT_PCT = 0.002  # 0.2% (net of fees)
# Stop loss
STOP_LOSS_PCT = 0.005  # 0.5%
# Max hold time before forced exit (seconds)
MAX_HOLD_TIME_S = 300  # 5 minutes — these are fast trades
# Trailing stop activation
TRAILING_STOP_ACTIVATE_PCT = 0.003
TRAILING_STOP_FLOOR_PCT = 0.50  # keep 50% of peak gain

# ─────────────────────────────────────────────────────
# FEES
# ─────────────────────────────────────────────────────
TAKER_FEE = 0.003  # 0.3%
MAKER_REBATE = 0.002  # 0.2%

# ─────────────────────────────────────────────────────
# PAPER MODE
# ─────────────────────────────────────────────────────
PAPER_MODE = os.environ.get(
    "BTC_ARB_PAPER_MODE", "true"
).lower() == "true"
PAPER_SEED_BALANCE = float(os.environ.get(
    "BTC_ARB_SEED_BALANCE", "350"
))

# ─────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────
import logging
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
            "/var/log/polyfarm/btc_arb.log"
        )
    ]
)
logger = logging.getLogger("btc_arb")
