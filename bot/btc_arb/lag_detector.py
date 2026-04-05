"""
Lag Detector — the core edge engine.

Compares real-time BTC spot price against Polymarket contract
implied prices. When the contract hasn't caught up to a spot
move by >0.3%, that's our signal.

For "above" markets:
  - BTC jumps UP past strike → YES should be worth more → buy YES
  - BTC drops DOWN past strike → NO should be worth more → buy NO (sell YES)

For "below" markets:
  - BTC drops DOWN past strike → YES should be worth more → buy YES
  - BTC jumps UP past strike → NO should be worth more → buy NO

The key insight: Polymarket market makers update prices on
intervals (seconds to minutes). Binance/Coinbase reflect
moves in milliseconds. We live in that gap.
"""
import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Optional

from btc_arb.config import (
    MIN_LAG_PCT,
    MIN_FEED_AGREEMENT,
    TAKER_FEE,
    TRAILING_STOP_ACTIVATE_PCT,
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

    @property
    def is_actionable(self) -> bool:
        return (
            self.net_edge > 0
            and self.feed_count >= MIN_FEED_AGREEMENT
        )


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
    # Distance from strike as fraction
    distance = (spot_price - strike) / strike

    # Volatility scaling — shorter expiry = more certainty
    # BTC daily vol ~2.5%, hourly vol ~0.3%
    hourly_vol = 0.003
    effective_vol = hourly_vol * (time_to_expiry_hours ** 0.5)
    if effective_vol == 0:
        effective_vol = 0.001

    # Standard normal approximation (simplified)
    # z = distance / volatility
    z = distance / effective_vol

    # Velocity adjustment — if price is moving toward/away from strike
    if velocity != 0:
        # Velocity in $/s, convert to fraction/hour
        vel_frac = (velocity / spot_price) * 3600
        z += vel_frac / effective_vol * 0.3  # 30% weight on momentum

    # Sigmoid approximation of normal CDF
    # P(above) = 1 / (1 + exp(-1.7 * z))
    import math
    try:
        prob_above = 1.0 / (1.0 + math.exp(-1.7 * z))
    except OverflowError:
        prob_above = 1.0 if z > 0 else 0.0

    # Clamp to reasonable range
    prob_above = max(0.02, min(0.98, prob_above))

    if direction == "above":
        return prob_above
    else:
        return 1.0 - prob_above


class LagDetector:
    """
    Monitors price feeds and Polymarket contracts for lag.
    Emits LagSignal when actionable opportunity detected.
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

    async def check_lag(self):
        """
        Check all tracked markets for price lag against spot.
        Called on every price tick from the feed.
        """
        spot = self.feeds.state.best_price
        if spot is None:
            return

        feed_count = self.feeds.state.feed_count
        velocity = self.feeds.state.price_velocity
        on_chain = self.feeds.state.cryptoquant_signal

        # Only check markets near current BTC price (within 5%)
        nearby = self.scanner.get_markets_near_strike(spot)

        for mkt in nearby:
            if mkt.yes_price <= 0:
                continue

            # Estimate what the contract should be worth
            fair = _estimate_fair_value(
                spot_price=spot,
                strike=mkt.strike_price,
                direction=mkt.direction,
                velocity=velocity,
            )

            # Check YES side — is YES underpriced?
            yes_lag = fair - mkt.yes_price
            if yes_lag > 0:
                lag_pct = yes_lag / fair if fair > 0 else 0
                net_edge = yes_lag - TAKER_FEE  # fee-adjusted
                if lag_pct >= MIN_LAG_PCT and net_edge > 0:
                    signal = LagSignal(
                        market=mkt,
                        side="YES",
                        spot_price=spot,
                        contract_price=mkt.yes_price,
                        fair_value=fair,
                        lag_pct=lag_pct,
                        net_edge=net_edge,
                        velocity=velocity,
                        on_chain_signal=on_chain,
                        timestamp_ms=int(time.time() * 1000),
                        feed_count=feed_count,
                    )
                    if signal.is_actionable:
                        await self._notify(signal)

            # Check NO side — is NO underpriced?
            no_fair = 1.0 - fair
            no_lag = no_fair - mkt.no_price
            if no_lag > 0:
                lag_pct = no_lag / no_fair if no_fair > 0 else 0
                net_edge = no_lag - TAKER_FEE
                if lag_pct >= MIN_LAG_PCT and net_edge > 0:
                    signal = LagSignal(
                        market=mkt,
                        side="NO",
                        spot_price=spot,
                        contract_price=mkt.no_price,
                        fair_value=no_fair,
                        lag_pct=lag_pct,
                        net_edge=net_edge,
                        velocity=velocity,
                        on_chain_signal=on_chain,
                        timestamp_ms=int(time.time() * 1000),
                        feed_count=feed_count,
                    )
                    if signal.is_actionable:
                        await self._notify(signal)

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
        logger.info("Lag detector started")

    def stop(self):
        self._running = False
        logger.info("Lag detector stopped")
