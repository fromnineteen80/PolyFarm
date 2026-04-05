"""
BTC Arbitrage Bot — Main Orchestrator

Exploits latency between real-time BTC price feeds and
Polymarket BTC prediction contract price updates.

Architecture:
  1. PriceFeedManager — Binance WS + Coinbase + CryptoQuant
  2. MarketScanner — discovers BTC contracts on Polymarket
  3. ContractWebSocket — streams contract prices in real time
  4. LagDetector — compares spot vs contract, bracket stacking
  5. OrderExecutor — maker/taker fee routing, places trades
  6. RiskManager — 0.5% per trade, 2% daily cap

Enhancements over v1:
  - Fee optimization: maker orders earn +0.2% rebate (vs -0.3% taker)
  - Bracket stacking: one BTC move trades up to 4 brackets
  - Contract WebSocket: sub-second price updates (was 30s polling)

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
from btc_arb.ws_contracts import ContractWebSocket
from btc_arb.lag_detector import LagDetector, LagSignal
from btc_arb.risk_manager import RiskManager
from btc_arb.order_executor import OrderExecutor

ET = ZoneInfo("America/New_York")


class BTCArbitrageBot:
    """Main bot orchestrator."""

    def __init__(self, client=None):
        self.client = client
        self.feeds = PriceFeedManager()
        self.scanner = MarketScanner()
        self.contract_ws = ContractWebSocket(scanner=self.scanner)
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
        self._stack_count = 0

    async def _on_lag_signal(self, signal: LagSignal):
        """Handle a detected lag opportunity."""
        self._signal_count += 1
        if signal.stack_position > 0:
            self._stack_count += 1

        route = "MAKER" if signal.uses_maker else "TAKER"
        stack_label = (
            f" [STACK #{signal.stack_position+1}]"
            if signal.stack_position > 0 else ""
        )

        logger.info(
            f"LAG #{self._signal_count}{stack_label}: "
            f"{signal.side} {signal.market.slug} "
            f"| spot=${signal.spot_price:,.2f} "
            f"| strike=${signal.market.strike_price:,.0f} "
            f"| contract={signal.contract_price:.4f} "
            f"| fair={signal.fair_value:.4f} "
            f"| lag={signal.lag_pct:.3%} "
            f"| edge={signal.net_edge:.4f} "
            f"| route={route} "
            f"| size={signal.size_multiplier:.0%}"
        )

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
        logger.info(f"BTC Arbitrage Bot v2 starting [{mode}]")
        logger.info(f"Balance: ${self.risk.balance:.2f}")
        logger.info("Features: fee routing, bracket stacking, contract WS")

        # Register signal handler
        self.detector.on_signal(self._on_lag_signal)

        # Start price feeds (spot BTC)
        await self.feeds.start()
        await self.executor.start()

        # Start scanner (discovers BTC markets via REST)
        scanner_task = asyncio.create_task(
            self.scanner.scan_loop(interval_s=60)
        )

        # Wait briefly for initial market discovery
        await asyncio.sleep(2)

        # Start contract WebSocket (real-time contract prices)
        await self.contract_ws.start()
        ws_monitor_task = asyncio.create_task(
            self.contract_ws.monitor_loop()
        )

        # Start lag detector
        await self.detector.start()

        # Status + midnight reset
        status_task = asyncio.create_task(self._status_loop())
        reset_task = asyncio.create_task(self._midnight_reset())

        logger.info("All components running")

        try:
            await asyncio.gather(
                scanner_task,
                ws_monitor_task,
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
        await self.contract_ws.stop()
        await self.executor.stop()
        await self.feeds.stop()

        logger.info("BTC Arbitrage Bot stopped")
        logger.info(f"Session: {self.risk.status()}")
        logger.info(f"Fees: {self.executor.fee_stats()}")
        logger.info(
            f"Signals: {self._signal_count} total, "
            f"{self._stack_count} stacked, "
            f"{self._trade_count} executed"
        )

    async def _status_loop(self):
        """Print status every 60 seconds."""
        while self._running:
            await asyncio.sleep(60)
            try:
                spot = self.feeds.state.best_price
                markets = len(self.scanner.markets)
                ws_subs = len(self.contract_ws._subscribed_slugs)
                ws_updates = self.contract_ws.updates_received
                status = self.risk.status()
                fees = self.executor.fee_stats()

                spot_str = (
                    f"${spot:,.2f}" if spot else "waiting..."
                )
                logger.info(
                    f"STATUS | BTC={spot_str} "
                    f"| markets={markets} (ws={ws_subs}, "
                    f"updates={ws_updates}) "
                    f"| signals={self._signal_count} "
                    f"(stacked={self._stack_count}) "
                    f"| trades={self._trade_count} "
                    f"| fees={fees} "
                    f"| {status}"
                )
            except Exception as e:
                logger.error(f"Status error: {e}")

    async def _midnight_reset(self):
        """Reset daily stats at midnight ET."""
        while self._running:
            now = datetime.now(ET)
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
    logger.info("OracleFarming — BTC Arbitrage Module v2")
    logger.info("=" * 60)

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

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(bot.stop()),
        )

    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
