"""
Polymarket BTC Market Scanner.

Discovers and monitors BTC prediction markets on Polymarket.
These are bracket-style markets: "Will BTC be above $X by date?"

Each market has:
- A strike price (e.g., $65,000)
- An expiry (hourly, daily, weekly)
- YES/NO prices that imply a probability

When BTC spot moves but the contract price hasn't caught up,
that's our edge.
"""
import asyncio
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from btc_arb.config import (
    POLYMARKET_PUBLIC_URL,
    BTC_MARKET_KEYWORDS,
)

logger = logging.getLogger("btc_arb.scanner")


@dataclass
class BTCMarket:
    """A single Polymarket BTC prediction market."""
    slug: str
    question: str
    strike_price: float  # the threshold price (e.g., 65000)
    direction: str  # "above" or "below"
    expiry: Optional[str] = None  # ISO timestamp
    yes_price: float = 0.0
    no_price: float = 0.0
    last_update_ms: int = 0
    market_id: Optional[str] = None
    condition_id: Optional[str] = None
    # Derived
    implied_prob: float = 0.0  # yes_price as probability

    def update_prices(self, yes: float, no: float):
        self.yes_price = yes
        self.no_price = no
        self.implied_prob = yes
        self.last_update_ms = int(time.time() * 1000)


def _extract_strike(question: str) -> Optional[float]:
    """
    Extract the BTC strike price from a market question.
    Examples:
        "Will Bitcoin be above $65,000 on April 5?" → 65000.0
        "BTC above $100k by end of week?" → 100000.0
        "Will BTC reach $70,000?" → 70000.0
    """
    # Match dollar amounts with optional commas and k/K suffix
    patterns = [
        r'\$([0-9,]+(?:\.[0-9]+)?)\s*(?:k|K)',  # $65k
        r'\$([0-9,]+(?:\.[0-9]+)?)',  # $65,000
    ]
    for pattern in patterns:
        match = re.search(pattern, question)
        if match:
            val_str = match.group(1).replace(",", "")
            val = float(val_str)
            if pattern.endswith("k|K)"):
                val *= 1000
            # Sanity: BTC prices are in thousands
            if 1000 < val < 1_000_000:
                return val
    return None


def _extract_direction(question: str) -> str:
    """Determine if market is 'above' or 'below' threshold."""
    q = question.lower()
    if "below" in q or "under" in q or "drop" in q:
        return "below"
    return "above"


class MarketScanner:
    """Discovers and tracks active BTC markets on Polymarket."""

    def __init__(self):
        self.markets: dict[str, BTCMarket] = {}  # slug → BTCMarket
        self._running = False

    async def discover(self) -> list[BTCMarket]:
        """
        Scan Polymarket for active BTC prediction markets.
        Uses the public v2 API to find crypto/BTC events.
        """
        found = []
        async with httpx.AsyncClient(timeout=15) as client:
            # Search for BTC-related events
            for keyword in BTC_MARKET_KEYWORDS:
                try:
                    resp = await client.get(
                        f"{POLYMARKET_PUBLIC_URL}/v2/search",
                        params={
                            "query": keyword,
                            "limit": 50,
                            "active": True,
                        },
                    )
                    if resp.status_code != 200:
                        logger.warning(
                            f"Search failed for '{keyword}': {resp.status_code}"
                        )
                        continue

                    data = resp.json()
                    events = data if isinstance(data, list) else data.get("events", data.get("results", []))

                    for event in events:
                        markets = event.get("markets", [])
                        if not markets:
                            # Event might itself be a market
                            markets = [event]

                        for mkt in markets:
                            question = mkt.get("question", mkt.get("title", ""))
                            slug = mkt.get("slug", mkt.get("marketSlug", ""))
                            if not slug or not question:
                                continue

                            # Must be BTC-related
                            q_lower = question.lower()
                            if not any(
                                kw in q_lower
                                for kw in ["bitcoin", "btc"]
                            ):
                                continue

                            strike = _extract_strike(question)
                            if strike is None:
                                logger.debug(
                                    f"No strike found in: {question}"
                                )
                                continue

                            direction = _extract_direction(question)

                            # Extract prices from market sides
                            yes_price = 0.0
                            no_price = 0.0
                            sides = mkt.get("marketSides", [])
                            for side in sides:
                                label = side.get("label", "").lower()
                                price = float(
                                    side.get("price", 0)
                                )
                                if label == "yes":
                                    yes_price = price
                                elif label == "no":
                                    no_price = price

                            # Fallback: outcomePrices
                            if yes_price == 0:
                                outcome_prices = mkt.get(
                                    "outcomePrices", []
                                )
                                if len(outcome_prices) >= 2:
                                    yes_price = float(outcome_prices[0])
                                    no_price = float(outcome_prices[1])

                            btc_mkt = BTCMarket(
                                slug=slug,
                                question=question,
                                strike_price=strike,
                                direction=direction,
                                expiry=mkt.get("endDate"),
                                yes_price=yes_price,
                                no_price=no_price,
                                last_update_ms=int(time.time() * 1000),
                                market_id=str(
                                    mkt.get("id", "")
                                ),
                                condition_id=mkt.get(
                                    "conditionId", ""
                                ),
                                implied_prob=yes_price,
                            )
                            found.append(btc_mkt)
                            self.markets[slug] = btc_mkt

                except Exception as e:
                    logger.error(
                        f"Error scanning for '{keyword}': {e}"
                    )

        logger.info(
            f"Discovered {len(found)} BTC markets on Polymarket"
        )
        for m in found:
            logger.info(
                f"  {m.direction.upper()} ${m.strike_price:,.0f} "
                f"| YES={m.yes_price:.3f} | {m.slug}"
            )
        return found

    async def refresh_prices(self):
        """Refresh prices for all tracked markets."""
        async with httpx.AsyncClient(timeout=10) as client:
            for slug, mkt in self.markets.items():
                try:
                    resp = await client.get(
                        f"{POLYMARKET_PUBLIC_URL}/v2/markets/{slug}"
                    )
                    if resp.status_code != 200:
                        continue
                    data = resp.json()

                    # Extract updated prices
                    yes_price = 0.0
                    no_price = 0.0
                    sides = data.get("marketSides", [])
                    for side in sides:
                        label = side.get("label", "").lower()
                        price = float(side.get("price", 0))
                        if label == "yes":
                            yes_price = price
                        elif label == "no":
                            no_price = price

                    if yes_price == 0:
                        outcome_prices = data.get(
                            "outcomePrices", []
                        )
                        if len(outcome_prices) >= 2:
                            yes_price = float(outcome_prices[0])
                            no_price = float(outcome_prices[1])

                    if yes_price > 0:
                        mkt.update_prices(yes_price, no_price)

                except Exception as e:
                    logger.debug(
                        f"Price refresh failed for {slug}: {e}"
                    )

    def get_markets_near_strike(
        self, btc_price: float, range_pct: float = 0.05
    ) -> list[BTCMarket]:
        """
        Get markets whose strike is within range_pct of current BTC price.
        These are the ones most likely to have tradeable lag.
        """
        results = []
        for mkt in self.markets.values():
            distance = abs(btc_price - mkt.strike_price) / btc_price
            if distance <= range_pct:
                results.append(mkt)
        return results

    async def scan_loop(self, interval_s: float = 30.0):
        """Continuously scan for new markets and refresh prices."""
        self._running = True
        # Initial discovery
        await self.discover()

        while self._running:
            await asyncio.sleep(interval_s)
            try:
                await self.refresh_prices()
                # Re-discover every 5 minutes for new markets
                if int(time.time()) % 300 < interval_s:
                    await self.discover()
            except Exception as e:
                logger.error(f"Scan loop error: {e}")

    def stop(self):
        self._running = False
