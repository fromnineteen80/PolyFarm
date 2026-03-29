import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import WalletGrowthChart from '../components/charts/WalletGrowthChart'
import WinRateChart from '../components/charts/WinRateChart'
import ExitTypeChart from '../components/charts/ExitTypeChart'
import HeatmapChart from '../components/charts/HeatmapChart'
import ScatterChart from '../components/charts/ScatterChart'
import CalibrationCurve from '../components/charts/CalibrationCurve'
import { formatCurrency, calcSharpe, calcMaxDrawdown, calcRollingWinRate } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [tradeRes, snapRes] = await Promise.all([
    sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(5000),
    sb.from('daily_snapshots').select('*').order('date', { ascending: true }),
  ])
  return { props: { session, trades: tradeRes.data || [], snapshots: snapRes.data || [] } }
}

export default function Performance({ trades, snapshots }) {
  const totalPnl = trades.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
  const wins = trades.filter(t => parseFloat(t.pnl || 0) > 0).length
  const winRate = trades.length > 0 ? wins / trades.length * 100 : 0

  const dailyReturns = snapshots.filter(s => s.session_pnl && s.wallet_value).map(s => parseFloat(s.session_pnl) / parseFloat(s.wallet_value))
  const sharpe = calcSharpe(dailyReturns)
  const walletHistory = snapshots.map(s => parseFloat(s.wallet_value || 0))
  const { maxDrawdown } = calcMaxDrawdown(walletHistory)

  const wr7 = calcRollingWinRate(trades, 7)
  const wr30 = calcRollingWinRate(trades, 30)

  const exitCounts = {}; trades.forEach(t => { const e = t.exit_type || 'other'; exitCounts[e] = (exitCounts[e] || 0) + 1 })

  // Strategy breakdown
  const stratStats = {}
  for (const s of ['normal', 'exception', 'fade', 'overnight']) {
    const st = trades.filter(t => t.position_type === s || (s === 'normal' && t.position_type === 'oracle_arb'))
    const w = st.filter(t => parseFloat(t.pnl || 0) > 0).length
    stratStats[s] = { trades: st.length, winRate: st.length > 0 ? (w / st.length * 100).toFixed(0) : 0, pnl: st.reduce((a, t) => a + parseFloat(t.pnl || 0), 0) }
  }

  // Sport breakdown
  const sportStats = {}
  trades.forEach(t => {
    const sp = t.sport || 'unknown'
    if (!sportStats[sp]) sportStats[sp] = { trades: 0, wins: 0, pnl: 0 }
    sportStats[sp].trades++
    if (parseFloat(t.pnl || 0) > 0) sportStats[sp].wins++
    sportStats[sp].pnl += parseFloat(t.pnl || 0)
  })

  let sharpeBadge = 'Below Target'; let sharpeColor = 'text-loss'
  if (sharpe > 3) { sharpeBadge = 'Exceptional'; sharpeColor = 'text-profit' }
  else if (sharpe > 2) { sharpeBadge = 'Institutional'; sharpeColor = 'text-info' }
  else if (sharpe > 1) { sharpeBadge = 'Good'; sharpeColor = 'text-bandA' }

  // Streak
  let streak = 0, streakType = null
  for (const t of trades) {
    const w = parseFloat(t.pnl || 0) > 0
    if (streakType === null) { streakType = w; streak = 1 }
    else if (w === streakType) streak++
    else break
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Performance Analytics</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <StatCard title="All-Time P&L" value={formatCurrency(totalPnl)} color={totalPnl >= 0 ? 'text-profit' : 'text-loss'} />
        <StatCard title="Win Rate" value={`${winRate.toFixed(0)}%`} />
        <StatCard title="Total Trades" value={trades.length} />
        <StatCard title="Streak" value={`${streak}${streakType ? 'W' : 'L'}`} color={streakType ? 'text-profit' : 'text-loss'} />
        <StatCard title="Sharpe Ratio" value={sharpe.toFixed(2)} subtitle={sharpeBadge} color={sharpeColor} />
        <StatCard title="Max Drawdown" value={`${(maxDrawdown * 100).toFixed(1)}%`} color="text-loss" />
      </div>

      <div className="grid md:grid-cols-2 gap-4 mb-6">
        <WalletGrowthChart snapshots={snapshots} floorData />
        <WinRateChart data7d={wr7} data30d={wr30} />
        <ExitTypeChart exitCounts={exitCounts} />
        <HeatmapChart trades={trades} />
      </div>

      <ScatterChart trades={trades} xField="net_edge_at_entry" yField="pnl_pct" xlabel="Net Edge %" ylabel="P&L %" colorByBand />
      <CalibrationCurve trades={trades} />

      <h2 className="text-lg font-semibold mt-6 mb-3">By Strategy</h2>
      <div className="table-scroll mb-6">
        <table className="w-full text-sm"><thead><tr className="border-b border-border">
          <th className="text-left text-neutral py-2 px-2">Strategy</th>
          <th className="text-right text-neutral py-2 px-2">Trades</th>
          <th className="text-right text-neutral py-2 px-2">Win Rate</th>
          <th className="text-right text-neutral py-2 px-2">Total P&L</th>
        </tr></thead><tbody>
          {Object.entries(stratStats).map(([s, d]) => (
            <tr key={s} className="border-b border-border">
              <td className="py-2 px-2">{s}</td>
              <td className="py-2 px-2 text-right">{d.trades}</td>
              <td className="py-2 px-2 text-right">{d.winRate}%</td>
              <td className={`py-2 px-2 text-right ${d.pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{formatCurrency(d.pnl)}</td>
            </tr>
          ))}
        </tbody></table>
      </div>

      <h2 className="text-lg font-semibold mb-3">By Sport</h2>
      <div className="table-scroll">
        <table className="w-full text-sm"><thead><tr className="border-b border-border">
          <th className="text-left text-neutral py-2 px-2">Sport</th>
          <th className="text-right text-neutral py-2 px-2">Trades</th>
          <th className="text-right text-neutral py-2 px-2">Win Rate</th>
          <th className="text-right text-neutral py-2 px-2">P&L</th>
        </tr></thead><tbody>
          {Object.entries(sportStats).sort((a, b) => b[1].pnl - a[1].pnl).map(([sp, d]) => (
            <tr key={sp} className="border-b border-border">
              <td className="py-2 px-2">{sp}</td>
              <td className="py-2 px-2 text-right">{d.trades}</td>
              <td className="py-2 px-2 text-right">{d.trades > 0 ? (d.wins / d.trades * 100).toFixed(0) : 0}%</td>
              <td className={`py-2 px-2 text-right ${d.pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{formatCurrency(d.pnl)}</td>
            </tr>
          ))}
        </tbody></table>
      </div>
    </Layout>
  )
}
