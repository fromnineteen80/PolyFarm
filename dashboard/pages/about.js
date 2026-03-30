import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import Layout from '../components/Layout'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  return { props: { session } }
}

export default function About() {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">PolyFarm -- Strategy and Investment Overview</h1>

        <Section title="What PolyFarm Does">
          <p>
            PolyFarm is an automated prediction market trading system built on Polymarket US, the first federally regulated prediction market exchange in the United States. The system runs four complementary strategies simultaneously, generating returns through systematic exploitation of pricing inefficiencies between Polymarket's crowd-driven order book and sharp consensus odds from regulated US sportsbooks.
          </p>
          <p>
            The system takes no directional view on game outcomes. It profits from pricing corrections, not from predicting winners.
          </p>
        </Section>

        <Section title="The Market Opportunity">
          <p>
            Polymarket operates as a central limit order book where prices update only when traders actively post orders. US sportsbooks -- DraftKings, FanDuel, BetMGM, Caesars, BetRivers, and BetOnline -- update their lines continuously using professional money flow and sophisticated probability models. The gap between these two pricing mechanisms is structural and persistent.
          </p>
          <p>
            Polymarket prices based on general crowd sentiment. US sportsbooks price based on where large, sophisticated money is actually moving. When those two prices diverge meaningfully, the direction of the correct trade is knowable with high confidence before the crowd catches up.
          </p>
          <p>
            PolyFarm monitors every active sports moneyline market on Polymarket US simultaneously via real-time WebSocket connection, compares each market's implied probability against the vig-removed consensus fair line from The Odds API, and executes trades in real time when the gap exceeds the minimum qualifying threshold.
          </p>
          <p>
            One boundary the system never crosses is futures markets. Every position PolyFarm takes is on a live or same-day game with a defined resolution window. Futures contracts, season win totals, award markets, and any market resolving beyond 24 hours are excluded entirely. Capital must recycle continuously to compound.
          </p>
        </Section>

        <Section title="How Capital Deploys Across Sports">
          <p>
            The system deploys capital across every sport available on Polymarket US simultaneously. NBA, NFL, MLB, NHL, NCAA basketball, NCAA football, EPL, MLS, Champions League, and other soccer leagues discovered through The Odds API all run in parallel. The bot allocates based purely on where qualifying signals exist at any given moment, not on sport preference.
          </p>
          <p>
            No single sport may represent more than 40% of total open positions at any time. This prevents a single sport's bad night from disproportionately affecting the portfolio.
          </p>
          <p>
            Exception trades are capped at two per session. Fade trades are capped at three per session. Oracle arb has no trade count limit but portfolio profit tiers govern sizing as the session accumulates gains.
          </p>
        </Section>

        <Section title="Strategy 1: Oracle Arbitrage">
          <p>
            The primary engine. Runs continuously across every active moneyline market with sufficient volume.
          </p>
          <p>
            Signals are classified into three bands based on the pricing gap and the implied probability. Band A requires a gap above 8% with market price above 70 cents. Band B requires 5% to 8% with price between 60 and 70 cents. Band C requires 3% to 5% with price between 55 and 60 cents. The system never enters below 55 cents. Favorites only.
          </p>
          <p>
            Each entry triggers an immediate limit sell at the exit target, set at 65% of the detected gap above entry price. This captures the fastest portion of the market correction while minimizing hold time. The GTC limit sell earns a maker rebate when it fills, partially offsetting the taker fee paid on entry.
          </p>
          <p>
            For live in-game markets the minimum edge threshold reduces by 1 percentage point per band because repricing events are more frequent during play.
          </p>
          <p>
            Beyond the static edge from sportsbook consensus, PolyFarm incorporates real-time price movement analysis. A rolling 30-minute price history buffer tracks price velocity and direction. A trade flow tracker monitors buy versus sell dollar volume. These combine into a composite edge signal with three components:
          </p>
          <p>
            Static edge from the sportsbook consensus provides the base signal. Price direction modifies the entry threshold -- when the Polymarket crowd is actively selling (price falling away from the sharp line), the required edge threshold drops by 15% because the gap is widening and conviction is highest. When the crowd is buying (price rising toward the sharp line), the threshold increases by 20% because the gap may be closing. Net buy pressure modifies position sizing -- strong net selling with a falling price triggers 15% larger positions, while heavy buying or rising prices reduce position size by 15%.
          </p>
          <p>
            This means PolyFarm does not just detect that a gap exists. It detects whether the gap is growing or shrinking, and sizes accordingly. Standard oracle arbitrage treats every qualifying gap identically. PolyFarm trades larger when the crowd is creating the gap and smaller when the crowd is correcting it.
          </p>
          <p>
            Win rate expectations: Band A 88% to 93%. Band B 83% to 88%. Band C 78% to 83%. Blended target above 82%.
          </p>
          <p>
            Capital allocation: Band A at 4% of total wallet. Band B at 2.5%. Band C at 1.5%. Modified by the composite signal size multiplier.
          </p>
        </Section>

        <Section title="Strategy 2: Dominant Team Exception">
          <p>
            Activates only when the session has already produced meaningful gains and is operating in harvest, protection, or locked mode. This strategy exploits a documented market behavior: crowds overreact when elite teams fall behind, pricing them materially below their true probability of coming back.
          </p>
          <p>
            An exception signal requires all conditions to be simultaneously true. The team must be in the dominant teams list. It must be trailing within a defined deficit range. The game must be within the comeback window. The sportsbook consensus must price the team at least 10 cents above Polymarket. Volume must exceed $30,000. And the session exception budget must not be exhausted.
          </p>
          <p>
            Sport-specific rules are precise. Basketball: trailing 5 to 15 points in Q3 or Q4 with 8+ minutes remaining. Baseball: 1 to 3 runs behind in innings 6 through 8. Hockey: 1 to 2 goals behind in periods 2 or 3 with 8+ minutes. Football: 3 to 14 points behind in Q3 or Q4 with 8+ minutes. Soccer: exactly 1 goal between minute 55 and 80.
          </p>
          <p>
            The dominant teams list is curated based on documented comeback rates and confirmed market overreaction tendencies, including the Kansas City Chiefs, Los Angeles Dodgers, Oklahoma City Thunder, Denver Nuggets, Boston Celtics, Edmonton Oilers, Duke, UConn, Manchester City, and others.
          </p>
          <p>
            Exception trades are sized at 3% of wallet. Win rate expectation: 85% to 92%.
          </p>
        </Section>

        <Section title="Strategy 3: Fade Trading">
          <p>
            Fade trading does not mean buying underdogs. The system never buys below 55 cents. Fade trading means identifying situations where a structurally weak team is trailing and the crowd is still pricing their comeback probability too generously. The system buys YES on the opponent -- the leading team -- at a price the crowd has held artificially low.
          </p>
          <p>
            Example: the Pittsburgh Pirates are trailing 3-1 in the seventh inning. Polymarket has the opponent at 69 cents. The sportsbook consensus says the opponent should be at 78 cents. The system buys the opponent YES at 69 cents and exits when Polymarket corrects toward 78 cents.
          </p>
          <p>
            Minimum gap thresholds vary by confidence tier. Very high confidence fade teams (e.g., Chicago White Sox, Utah Jazz) require 8 cents minimum. High confidence requires 10 cents. Medium requires 12 cents.
          </p>
          <p>
            Fade trades include a unique exit trigger: if the score equalizes and the fade team catches up, the thesis is broken and the system exits immediately regardless of clock position.
          </p>
          <p>
            Win rate expectation: 78% to 86%.
          </p>
        </Section>

        <Section title="Strategy 4: Overnight Positioning">
          <p>
            Runs at midnight and 6 AM, scanning next-day markets where Polymarket has opened contracts but crowd pricing has not yet incorporated sharp line information. These thinner markets create larger and more persistent gaps.
          </p>
          <p>
            Requires minimum 12% edge. Total overnight exposure capped at 20% of working capital. At 6 AM the system re-evaluates and exits any position where the gap has compressed below 5%.
          </p>
          <p>
            Win rate expectation: 72% to 80%.
          </p>
        </Section>

        <Section title="How Every Position Avoids Liquidity Risk">
          <p>
            In prediction markets, liquidity is not guaranteed. Near the end of a game, the losing side of the order book thins because nobody wants to buy a position likely to settle at zero. A system not designed around this can find itself holding positions with no buyers.
          </p>
          <p>
            PolyFarm addresses this at multiple levels. Volume minimums at entry ensure enough active participants for reliable exits. Bid-ask spread checks filter deteriorating liquidity before entry.
          </p>
          <p>
            The timeout trigger is the primary safety mechanism. At 30 minutes for oracle arb, 15 for exception, 20 for fade -- if the GTC sell has not filled, the bot cancels it and evaluates current edge. If meaningful edge remains, it modifies the sell price. If edge has compressed, it places an IOC order at current best bid -- taking whatever the market pays right now and exiting cleanly.
          </p>
          <p>
            Pre-resolution triggers fire before the dangerous end-of-game window. NBA at 2 minutes remaining. NFL at 4 minutes. MLB at the 8th inning. NHL at 5 minutes of regulation. Soccer at minute 80. The system exits via IOC while liquidity still exists, before the final drain.
          </p>
          <p>
            The result is that PolyFarm holds most positions for two to fifteen minutes and exits during periods of high market liquidity. Hold-to-resolution positions represent at most 15% of open positions and only enter when original edge exceeded 12% with entry price above 65 cents.
          </p>
        </Section>

        <Section title="Five-Layer Exit System">
          <p>
            Every position carries five independent exit triggers evaluated every 30 seconds. The first to fire wins.
          </p>
          <p>
            Trigger 1: Passive reprice target. GTC limit sell at 65% of gap above entry. Earns maker rebate.
          </p>
          <p>
            Trigger 2: Profit lock. Band A locks at 12% gain. Band B at 10%. Band C at 8%. Exception at 8%. Fade at 7%. In protection mode these tighten by 50%.
          </p>
          <p>
            Trigger 3: Trailing stop. Activates at 6% peak gain. Exits if current gain falls below 50% of peak (65% in protection mode).
          </p>
          <p>
            Trigger 4: Timeout with re-evaluation. Checks remaining edge before forcing exit. Modifies GTC if edge remains, IOC if compressed.
          </p>
          <p>
            Trigger 5: Sport-specific pre-resolution logic. Exits before end-of-game liquidity drain.
          </p>
        </Section>

        <Section title="Session-Level Protection">
          <p>
            Portfolio profit tiers run every 10 seconds independently of individual positions.
          </p>
          <p>
            At +8% daily gain: harvest mode. Sizing reduces 25%.
          </p>
          <p>
            At +12%: protection mode. Band A only at 50% sizing. Profit locks tighten 50%. Trailing floor tightens to 65%.
          </p>
          <p>
            At +17%: session locks. No new oracle arb. Exception and fade remain active. All positions drain.
          </p>
          <p>
            At -10% daily loss: sizing reduces 50%. Exception and fade suspend.
          </p>
          <p>
            At -15%: all new entries pause.
          </p>
          <p>
            At -20%: emergency exit all positions. Session halts.
          </p>
          <p>
            The floor is fixed at 80% of session-start value. If portfolio reaches the floor, all positions exit immediately. The worst possible outcome in any session is a 20% drawdown.
          </p>
        </Section>

        <Section title="The Compounding Model">
          <p>
            PolyFarm's return profile comes from capital turnover velocity rather than maximizing individual trade returns. The same dollar cycling through multiple high-confidence reprice events throughout each day generates superior compounding compared to larger directional bets held for hours.
          </p>
          <p>
            The compounding formula is straightforward:
          </p>
          <p className="text-neutral text-sm my-4">
            V(n) = P x (1 + r)^n
          </p>
          <p className="text-neutral text-sm mb-4">
            Where P is starting principal, r is daily return rate, n is number of trading days, and V(n) is portfolio value after n days.
          </p>
          <p>
            At 1.0% daily: $700 grows to approximately $8,700 in 365 days.
          </p>
          <p>
            At 1.5% daily: $700 grows to approximately $160,000 in 365 days.
          </p>
          <p>
            At 2.0% daily: $700 grows to approximately $1.8 million in 365 days.
          </p>
          <p>
            These projections assume continuous compounding with no withdrawals and no drawdown days, which is not realistic. Actual performance will include losing days, reduced-sizing sessions from loss tiers, and periods with low market activity. The projections represent the mathematical ceiling, not guaranteed outcomes.
          </p>
          <p>
            Why this model should outperform standard oracle arbitrage: most oracle arb systems detect the same static gap and enter at a fixed size. PolyFarm's composite signal layer -- incorporating real-time price direction and trade flow pressure -- means the system enters larger when conditions are most favorable (crowd selling, gap widening) and smaller when conditions are deteriorating (crowd buying, gap narrowing). Over hundreds of trades this directional sizing creates a meaningful edge over flat-sized approaches, because winning trades are systematically larger than losing ones.
          </p>
          <p>
            The 300-trade paper validation period exists specifically to measure whether this theoretical advantage materializes in practice before real capital is deployed.
          </p>
        </Section>

        <Section title="Capital Structure">
          <p>
            Ownership is tracked using a unit-based model. The first depositor establishes 1,000 base units. Subsequent deposits purchase units at current portfolio value. Every investor buys in at fair market value with no dilution beyond proportional stake.
          </p>
          <p>
            Current portfolio value, total invested, unrealized gain, and ownership percentage are calculated in real time and visible through this dashboard.
          </p>
        </Section>

        <Section title="Current Status">
          <p>
            The system is in paper trading mode. All logic executes identically to live mode with simulated fills at mid-price. Live mode unlocks after 300 completed paper trades with a verified win rate above 70%.
          </p>
          <p>
            Milestone analysis reports are generated every 50 paper trades with performance breakdown by sport, band, entry direction, and edge size, along with automated recommendations for areas that need adjustment.
          </p>
          <p>
            Phase 2 infrastructure for crypto latency arbitrage on Bitcoin and Ethereum contracts is scaffolded and activates via configuration change when Polymarket US opens those markets.
          </p>
        </Section>
      </div>
    </Layout>
  )
}

function Section({ title, children }) {
  return (
    <div className="mb-8">
      <h2 className="text-lg font-semibold mb-3">{title}</h2>
      <div className="space-y-3 text-sm text-neutral leading-relaxed">
        {children}
      </div>
    </div>
  )
}
