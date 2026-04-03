# ORACLEFARMING STRATEGY V2

## IMPORTANT CONTEXT

This strategy REPLACES the strategy sections in CLAUDE.md. The pipeline, team registry, APIs, Supabase schema, systemd, Telegram infrastructure, WebSocket connections, and everything documented as "working" in STAGING_REPAIR.md stays exactly as-is. We are ONLY fixing what is broken and adjusting the trading strategy per this document.

The architecture diagram in CLAUDE.md remains accurate for the pipeline and data flow. The changes below affect the TRADING ENGINE — everything from edge detection through position management through exits.

---

## What OracleFarming Does

OracleFarming is an automated probability execution system operating on Polymarket US. The system identifies, filters, and executes trades based on measurable mispricing between Polymarket's order book and normalized, vig-removed consensus probabilities from regulated sportsbooks. The system does not predict outcomes. It selectively participates only when a statistically valid and executable edge exists, and capital is deployed with strict discipline to preserve that edge through execution.

The system prioritizes consistency over volume. Trades are taken only when signal quality, persistence, and liquidity align. No trade is a valid outcome when conditions are not met.

## The Market Opportunity

Polymarket operates as a discrete order book driven by participant behavior. Prices move only when orders are placed. Sportsbooks operate as continuously updated probability engines informed by sharp money and models.

The opportunity is not simply that prices differ. The opportunity exists when a difference is both measurable and stable long enough to be executed without losing edge to slippage, spread, or latency.

The system therefore does not react to raw gaps. It trades only when a gap meets three criteria. It must exceed a minimum threshold after vig removal. It must persist over a defined time window. It must be executable at size given current liquidity.

Markets are normalized through the registry to ensure all comparisons are exact and no mismatches occur.

## Market Selection Framework

The system prioritizes totals and spreads as primary trading markets. Winner markets are secondary and used only under stricter conditions.

Totals and spreads are preferred because they are continuous pricing instruments shaped by sharper inputs. They exhibit tighter alignment across sportsbooks and more stable price movement. This stability allows the system to identify persistent, executable mispricing rather than transient noise.

Winner markets are more volatile and narrative-driven. Apparent edges are larger but less stable and degrade more frequently during execution. They are therefore treated as opportunistic rather than foundational.

## Capital Allocation Across Markets

Capital is allocated dynamically based on signal quality rather than evenly across opportunities.

Totals receive primary allocation due to signal stability.
Spreads receive secondary allocation with tighter persistence requirements.
Winner markets receive limited allocation only when edge strength and stability exceed higher thresholds.

No single sport may exceed 40% of exposure. This constraint remains unchanged.

## Strategy 1: Probability Arbitrage Engine

The primary engine operates across totals and spreads, with limited participation in winner markets.

A trade is eligible only when four conditions are satisfied.

1. A true edge exists after vig removal.
2. The edge persists for a defined interval.
3. Sufficient liquidity exists at the intended entry.
4. Market behavior supports the signal, either through stability or confirmation.

Edges are classified into tiers, but thresholds are adjusted upward to prioritize quality over volume.

- High-confidence tier requires stronger edge and persistence.
- Mid-tier requires moderate edge with strong liquidity.
- Low-tier is largely eliminated or minimally sized.

Real-time adjustments still exist but are constrained. Price direction and flow modify sizing slightly, not threshold integrity. A falling price with widening gap can increase size modestly. Rising prices reduce size or cancel entry.

Execution is limit-order driven. Orders are placed at prices that preserve edge. If not filled within a defined window or if edge deteriorates, orders are canceled and reassessed.

Exit logic captures partial correction rather than full reversion. However, exits are conditional on maintained edge rather than fixed percentages alone.

Position sizing is tiered. Larger, stable edges receive more capital. Smaller edges receive minimal allocation or are ignored. This replaces uniform deployment.

## Strategy 2: Dominant Team Repricing

This strategy remains but is tightened.

It activates only when multiple conditions confirm that the market has overreacted to a temporary deficit.

The key correction is that entry requires persistence and stability, not just instantaneous gap.

Dominant teams must meet stricter probability thresholds and liquidity requirements. Position size remains controlled and does not scale aggressively.

This strategy is treated as a separate module with independent risk limits.

## Strategy 3: Fade Strategy

Fade logic is retained but refined.

Trades occur only when weak teams are priced above their true probability and the edge is both measurable and stable.

The critical correction is stricter entry filtering. Gap alone is insufficient. The edge must persist and be executable.

Immediate exit on thesis break remains valid and unchanged.

Position sizing is reduced relative to primary strategies due to higher variance.

## Strategy 4: Pre-Market Positioning

Overnight positioning remains but is reframed as controlled early pricing capture.

Entries require large, stable gaps and confirmed liquidity. Positions are re-evaluated before market activity increases. Any compression below threshold triggers exit.

Exposure remains capped.

## Execution Layer

Execution is the primary determinant of success.

- All trades use limit orders.
- Fill quality is tracked continuously.
- Orders are canceled if not filled within defined time or if edge deteriorates.
- Slippage is measured and incorporated into future thresholds.

The system prioritizes realized edge over theoretical edge.

## Risk Engine

Risk control overrides all strategies.

- Daily profit lock halts new entries once +15% target is reached.
- Drawdown triggers progressive reduction: -5% reduce size, -10% pause (resume at -5%), -15% done for the day.
- Market cooldown prevents repeated entries in the same market.
- System health triggers pause under instability conditions.

Risk is based on realized outcomes, not temporary price movement.

## Position Management

Positions are evaluated continuously based on updated probabilities, not price movement alone.

If sharp consensus still supports the position, it is held through volatility.
If probability deteriorates, exit decisions are triggered based on structured thresholds.

Late-game liquidity realities are acknowledged and incorporated.

## Trade State Model

Every trade moves through four states: Entry → Advancement → Protection → Exit.

At entry, the system records three values: entry price, expected fair probability from normalized feed, initial edge. From this, it computes a target zone and a protection band.

### Ceiling Construction

No single fixed take-profit. Stepped ceiling:

**Step 1**: First realized gain threshold. When position reaches a defined percentage gain relative to entry, that becomes the first checkpoint. No exit occurs. Protection floor is raised to lock in part of that gain.

**Step 2**: Higher gain threshold. If reached, floor is raised again. System continues to allow the trade to run.

**Step 3**: Maximum expected correction zone. If reached, system exits fully. No further upside pursued because remaining edge is minimal relative to execution risk.

If price never reaches Step 2 or Step 3, system exits on raised floor from Step 1 once momentum stalls or reverses.

### Floor Construction

Downside is symmetrical but stricter.

**Initial floor**: Set based on acceptable loss relative to edge. NOT a fixed percentage. Tied to whether the underlying probability still supports the position.

- Price moves against but fair probability unchanged → hold (this is noise)
- Price moves against and probability deteriorates slightly → warning state, no exit
- Price continues to deteriorate AND crosses second floor threshold AND weakening probability → exit immediately

### Recovery Logic

If trade dips but does not breach second floor, and probability stabilizes or improves, system resets to advancement state and again pursues ceiling path.

If trade never achieves meaningful upward movement after entry and drifts sideways or weakly downward, exits at first floor threshold after defined time window.

### Time Constraint

Every trade has a time-based reevaluation. If expected correction has not materialized within a defined period, and edge has compressed, system exits regardless of price position.

### Critical Rule

Floors and ceilings must be anchored to PROBABILITY, not just price. If sportsbook-derived probability still supports the position, price movement alone is not a valid reason to exit. If probability breaks, holding is no longer justified.

## Exit Triggers (Refined)

Exit conditions are multi-factor, prioritizing probability integrity:

1. **Target capture**: Sufficient correction realized (stepped ceiling).
2. **Trailing protection**: Activates after meaningful gains (raised floors).
3. **Loss exit**: Requires BOTH price deterioration AND probability breakdown.
4. **Time exit**: Reassesses edge validity after defined period.
5. **End-of-game**: Holds winning positions to settlement.

## Daily Cycle

- **Midnight ET**: Reset all modes, re-anchor floor, clear exited games, fresh start
- **Morning**: Games post on Polymarket, pipeline matches, trading begins when edges found
- **During day**: Selective trading when quality signals appear
- **Hit +15%**: Stop new trades, let winners settle
- **Hit -15% realized**: Done for the day
- **30-minute Telegram**: Batched summary to investors

## Investor Details

- Colin Maynard: $1,200 initial capital
- Hugo Sanchez: $1,200 initial capital
- Total fund: $2,400
- Paper mode: 0/300 trades toward live unlock (need 70%+ win rate)

## Why the Shift to Spreads and Totals

Spreads and totals behave as structured probability markets. They reflect aggregated information and adjust continuously across sportsbooks. This creates tighter alignment and more stable mispricing opportunities.

Winner markets are influenced by public perception and exhibit larger but less reliable deviations. These deviations often collapse before execution or reverse under volatility.

Spreads and totals produce smaller edges but higher execution reliability. For a system focused on consistency, this produces a higher realized win rate over time.

Totals are particularly stable because they are less dependent on team narrative and more on game dynamics. This reduces noise and improves signal clarity.

The shift is not about increasing theoretical returns per trade. It is about increasing the probability that each trade behaves as expected.

## Final Position

The corrected system trades less, filters harder, sizes intelligently, and executes with discipline. It prioritizes stability, persistence, and liquidity over raw opportunity count.

This is what converts a high-activity strategy into a consistent one.
