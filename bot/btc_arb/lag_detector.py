"""
Lag Detector — the core edge engine.

Compares real-time BTC spot price against Polymarket contract
implied prices. When the contract hasn't caught up to a spot
move by >0.3%, that's our signal.

BRACKET STACKING:
  When BTC makes a sharp move, it doesn't just misprice one bracket.
  If BTC jumps from $84,000 to $84,500, the $84,100, $84,200, $84,300,
  and $84,400 "above" contracts ALL lag simultaneously.
  We emit signals for ALL of them, ranked by edge size.
  One spot move = multiple trades = linear revenue scaling.
"""
import asyncio
import logging
import math
import time
from dataclasses import dataclass
from typing import Optional

from btc_arb.config import (
    MIN_LAG_PCT,
    MIN_FEED_AGREEMENT,
    TAKER_FEE,
    MAKER_REBATE,
    MAKER_LAG_THRESHOLD,
    MAX_STACK_SIZE,
    STACK_SPACING_MS,
    STACK_SIZE_DECAY,
)
from btc_arb.price_feeds import PriceFeedManager, PriceTick
from btc_arb.market_scanner import MarketScanner, BTCMarket

logger = logging.getLogger("btc_arb.lag")


@dataclass
class LagSignal:
    """A detected lag opportunity."""
    market: BTCMarket
    side: str  # "YES" or "NO"
    spot_price: float
    contract_price: float  # current YES or NO price
    fair_value: float  # what the contract should be worth
    lag_pct: float  # how much the contract lags (as fraction)
    net_edge: float  # lag minus fees
    velocity: float  # BTC price velocity (confirms momentum)
    on_chain_signal: Optional[str]  # CryptoQuant signal
    timestamp_ms: int
    feed_count: int  # how many feeds confirmed the spot price
    stack_position: int = 0  # 0 = primary, 1-3 = stacked
    size_multiplier: float = 1.0  # position size scaling

    @property
    def is_actionable(self) -> bool:
        return (
            self.net_edge > 0
            and self.feed_count >= MIN_FEED_AGREEMENT
        )

    @property
    def uses_maker(self) -> bool:
        """Will this signal route to maker order?"""
        return self.lag_pct >= MAKER_LAG_THRESHOLD


def _estimate_fair_value(
    spot_price: float,
    strike: float,
    direction: str,
    time_to_expiry_hours: float = 24.0,
    velocity: float = 0.0,
) -> float:
    """
    Estimate fair value of a BTC bracket contract given spot price.

    Simple model: distance from strike as a fraction of typical
    daily BTC volatility (~2-3%), mapped to a probability.

    For very short-term contracts (hourly), the probability is
    more binary — if BTC is 1% above strike with 30 min left,
    YES is worth close to 1.0.
    """
    distance = (spot_price - strike) / strike

    # Volatility scaling — shorter expiry = more certainty
    hourly_vol = 0.003
    effective_vol = hourly_vol * (time_to_expiry_hours ** 0.5)
    if effective_vol == 0:
        effective_vol = 0.001

    z = distance / effective_vol

    # Velocity adjustment — if price is moving toward/away from strike
    if velocity != 0:
        vel_frac = (velocity / spot_price) * 3600
        z += vel_frac / effective_vol * 0.3

    # Sigmoid approximation of normal CDF
    try:
        prob_above = 1.0 / (1.0 + math.exp(-1.7 * z))
    except OverflowError:
        prob_above = 1.0 if z > 0 else 0.0

    prob_above = max(0.02, min(0.98, prob_above))

    if direction == "above":
        return prob_above
    else:
        return 1.0 - prob_above


def _fee_for_lag(lag_pct: float) -> float:
    """
    Fee-adjusted edge calculation.
    Large lag → maker route → we EARN rebate.
    Small lag → taker route → we PAY fee.
    """
    if lag_pct >= MAKER_LAG_THRESHOLD:
        return -MAKER_REBATE  # negative = we earn
    return TAKER_FEE


class LagDetector:
    """
    Monitors price feeds and Polymarket contracts for lag.
    Emits LagSignals — multiple per BTC move via bracket stacking.
    """

    def __init__(
        self,
        feeds: PriceFeedManager,
        scanner: MarketScanner,
    ):
        self.feeds = feeds
        self.scanner = scanner
        self._callbacks: list = []
        self._running = False
        self._last_check_ms = 0
        self._check_interval_ms = 200  # check every 200ms
        # Dedup: don't re-signal the same market within 5s
        self._recent_signals: dict[str, int] = {}
        self._signal_cooldown_ms = 5000

    def on_signal(self, callback):
        """Register callback for lag signals: callback(LagSignal)"""
        self._callbacks.append(callback)

    async def _notify(self, signal: LagSignal):
        for cb in self._callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(signal)
                else:
                    cb(signal)
            except Exception as e:
                logger.error(f"Signal callback error: {e}")

    def _is_cooled_down(self, slug: str, side: str) -> bool:
        """Check if we recently signaled this market+side."""
        key = f"{slug}:{side}"
        now = int(time.time() * 1000)
        last = self._recent_signals.get(key, 0)
        if (now - last) < self._signal_cooldown_ms:
            return False
        self._recent_signals[key] = now
        return True

    def _build_signal(
        self,
        mkt: BTCMarket,
        side: str,
        spot: float,
        contract_price: float,
        fair: float,
        lag_pct: float,
        velocity: float,
        on_chain: Optional[str],
        feed_count: int,
        stack_pos: int = 0,
    ) -> Optional[LagSignal]:
        """Build a LagSignal with fee-aware edge calculation."""
        fee = _fee_for_lag(lag_pct)
        lag_abs = fair - contract_price
        net_edge = lag_abs - fee  # if fee negative (maker), edge increases

        if lag_pct < MIN_LAG_PCT or net_edge <= 0:
            return None

        if not self._is_cooled_down(mkt.slug, side):
            return None

        size_mult = STACK_SIZE_DECAY[min(stack_pos, len(STACK_SIZE_DECAY) - 1)]

        return LagSignal(
            market=mkt,
            side=side,
            spot_price=spot,
            contract_price=contract_price,
            fair_value=fair,
            lag_pct=lag_pct,
            net_edge=net_edge,
            velocity=velocity,
            on_chain_signal=on_chain,
            timestamp_ms=int(time.time() * 1000),
            feed_count=feed_count,
            stack_position=stack_pos,
            size_multiplier=size_mult,
        )

    async def check_lag(self):
        """
        Check ALL tracked markets for price lag against spot.
        Implements bracket stacking: collects all lagging brackets,
        sorts by edge, emits top N as a stacked signal set.
        """
        spot = self.feeds.state.best_price
        if spot is None:
            return

        feed_count = self.feeds.state.feed_count
        velocity = self.feeds.state.price_velocity
        on_chain = self.feeds.state.cryptoquant_signal

        # Check ALL markets near current price (within 5%)
        nearby = self.scanner.get_markets_near_strike(spot)

        # Collect all lagging opportunities
        candidates: list[LagSignal] = []

        for mkt in nearby:
            if mkt.yes_price <= 0:
                continue

            fair = _estimate_fair_value(
                spot_price=spot,
                strike=mkt.strike_price,
                direction=mkt.direction,
                velocity=velocity,
            )

            # Check YES side
            yes_lag = fair - mkt.yes_price
            if yes_lag > 0:
                lag_pct = yes_lag / fair if fair > 0 else 0
                sig = self._build_signal(
                    mkt, "YES", spot, mkt.yes_price, fair,
                    lag_pct, velocity, on_chain, feed_count,
                )
                if sig and sig.is_actionable:
                    candidates.append(sig)

            # Check NO side
            no_fair = 1.0 - fair
            no_lag = no_fair - mkt.no_price
            if no_lag > 0:
                lag_pct = no_lag / no_fair if no_fair > 0 else 0
                sig = self._build_signal(
                    mkt, "NO", spot, mkt.no_price, no_fair,
                    lag_pct, velocity, on_chain, feed_count,
                )
                if sig and sig.is_actionable:
                    candidates.append(sig)

        if not candidates:
            return

        # Sort by net edge (highest first) — best opportunity goes first
        candidates.sort(key=lambda s: s.net_edge, reverse=True)

        # Emit top N as stacked signals
        stack_count = min(len(candidates), MAX_STACK_SIZE)

        if stack_count > 1:
            logger.info(
                f"BRACKET STACK: {len(candidates)} lagging, "
                f"emitting top {stack_count}"
            )

        for i in range(stack_count):
            sig = candidates[i]
            sig.stack_position = i
            sig.size_multiplier = STACK_SIZE_DECAY[
                min(i, len(STACK_SIZE_DECAY) - 1)
            ]
            await self._notify(sig)

            # Small delay between stacked entries
            if i < stack_count - 1:
                await asyncio.sleep(STACK_SPACING_MS / 1000)

    async def _on_tick(self, tick: PriceTick):
        """Called on every price feed update."""
        now = int(time.time() * 1000)
        if (now - self._last_check_ms) >= self._check_interval_ms:
            self._last_check_ms = now
            await self.check_lag()

    async def start(self):
        """Start monitoring for lag."""
        self._running = True
        self.feeds.on_price(self._on_tick)
        logger.info(
            "Lag detector started "
            f"(bracket stacking: max {MAX_STACK_SIZE})"
        )

    def stop(self):
        self._running = False
        logger.info("Lag detector stopped")
