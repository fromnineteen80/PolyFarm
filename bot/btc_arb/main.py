"""
BTC Arbitrage Bot — Main Orchestrator

Exploits latency between real-time BTC price feeds and
Polymarket BTC prediction contract price updates.

Architecture:
  1. PriceFeedManager — Binance WS + Coinbase + CryptoQuant
  2. MarketScanner — discovers/tracks BTC contracts on Polymarket
  3. LagDetector — compares spot vs contract, emits signals
  4. OrderExecutor — places trades when lag > 0.3%
  5. RiskManager — 0.5% per trade, 2% daily cap

Usage:
  cd /home/user/PolyFarm/bot
  python -m btc_arb.main
"""
import asyncio
import logging
import os
import signal
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from btc_arb.config import PAPER_MODE, PAPER_SEED_BALANCE, logger
from btc_arb.price_feeds import PriceFeedManager
from btc_arb.market_scanner import MarketScanner
from btc_arb.lag_detector import LagDetector, LagSignal
from btc_arb.risk_manager import RiskManager
from btc_arb.order_executor import OrderExecutor

ET = ZoneInfo("America/New_York")


class BTCArbitrageBot:
    """Main bot orchestrator."""

    def __init__(self, client=None):
        """
        Args:
            client: Optional polymarket-us AsyncPolymarketUS instance.
                    Required for live trading, not needed for paper.
        """
        self.client = client
        self.feeds = PriceFeedManager()
        self.scanner = MarketScanner()
        self.risk = RiskManager(balance=PAPER_SEED_BALANCE)
        self.detector = LagDetector(
            feeds=self.feeds, scanner=self.scanner
        )
        self.executor = OrderExecutor(
            risk=self.risk, client=client
        )
        self._running = False
        self._signal_count = 0
        self._trade_count = 0

    async def _on_lag_signal(self, signal: LagSignal):
        """Handle a detected lag opportunity."""
        self._signal_count += 1

        logger.info(
            f"LAG DETECTED #{self._signal_count}: "
            f"{signal.side} {signal.market.slug} "
            f"| spot=${signal.spot_price:,.2f} "
            f"| strike=${signal.market.strike_price:,.0f} "
            f"| contract={signal.contract_price:.4f} "
            f"| fair={signal.fair_value:.4f} "
            f"| lag={signal.lag_pct:.3%} "
            f"| edge={signal.net_edge:.4f} "
            f"| vel={signal.velocity:+.2f}/s "
            f"| feeds={signal.feed_count}"
        )

        # Execute the trade
        pos = await self.executor.execute(signal)
        if pos:
            self._trade_count += 1
            logger.info(
                f"Trade #{self._trade_count} opened: "
                f"{pos.position_id}"
            )

    async def start(self):
        """Start all components."""
        self._running = True
        mode = "PAPER" if PAPER_MODE else "LIVE"
        logger.info(f"BTC Arbitrage Bot starting [{mode}]")
        logger.info(
            f"Balance: ${self.risk.balance:.2f}"
        )

        # Register signal handler
        self.detector.on_signal(self._on_lag_signal)

        # Start components
        await self.feeds.start()
        await self.executor.start()

        # Start scanner and detector
        scanner_task = asyncio.create_task(
            self.scanner.scan_loop(interval_s=30)
        )
        await self.detector.start()

        # Status reporting loop
        status_task = asyncio.create_task(self._status_loop())

        # Midnight reset loop
        reset_task = asyncio.create_task(self._midnight_reset())

        logger.info("All components running")
        logger.info(
            "Waiting for BTC markets and price feeds..."
        )

        try:
            # Run until stopped
            await asyncio.gather(
                scanner_task,
                status_task,
                reset_task,
            )
        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()

    async def stop(self):
        """Stop all components."""
        self._running = False
        self.detector.stop()
        self.scanner.stop()
        await self.executor.stop()
        await self.feeds.stop()
        logger.info("BTC Arbitrage Bot stopped")
        logger.info(f"Session stats: {self.risk.status()}")

    async def _status_loop(self):
        """Print status every 60 seconds."""
        while self._running:
            await asyncio.sleep(60)
            try:
                spot = self.feeds.state.best_price
                markets = len(self.scanner.markets)
                status = self.risk.status()

                spot_str = (
                    f"${spot:,.2f}" if spot else "waiting..."
                )
                logger.info(
                    f"STATUS | BTC={spot_str} "
                    f"| markets={markets} "
                    f"| signals={self._signal_count} "
                    f"| trades={self._trade_count} "
                    f"| {status}"
                )
            except Exception as e:
                logger.error(f"Status error: {e}")

    async def _midnight_reset(self):
        """Reset daily stats at midnight ET."""
        while self._running:
            now = datetime.now(ET)
            # Calculate seconds until midnight
            tomorrow = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if tomorrow <= now:
                from datetime import timedelta
                tomorrow += timedelta(days=1)
            wait = (tomorrow - now).total_seconds()

            await asyncio.sleep(wait)
            logger.info("Midnight ET — resetting daily stats")
            self.risk.reset_daily()


async def main():
    """Entry point."""
    logger.info("=" * 60)
    logger.info("OracleFarming — BTC Arbitrage Module")
    logger.info("=" * 60)

    # Initialize Polymarket client for live mode
    client = None
    if not PAPER_MODE:
        try:
            from polymarket_us import AsyncPolymarketUS
            client = AsyncPolymarketUS(
                key_id=os.environ["POLYMARKET_KEY_ID"],
                secret_key=os.environ["POLYMARKET_SECRET_KEY"],
            )
            logger.info("Polymarket SDK client initialized")
        except Exception as e:
            logger.critical(f"SDK init failed: {e}")
            raise SystemExit(1)

    bot = BTCArbitrageBot(client=client)

    # Graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(bot.stop()),
        )

    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
