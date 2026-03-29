import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import { formatCurrency, formatPct } from '../lib/calculations'
import supabase from '../lib/supabase'

const STRATEGY_COLORS = { normal: '#00c853', oracle_arb: '#00c853', exception: '#ffd700', fade: '#ff6d00', overnight: '#2979ff' }

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [snapRes, openRes, closedRes, cfgRes] = await Promise.all([
    sb.from('daily_snapshots').select('*').order('date', { ascending: false }).limit(1),
    sb.from('trades').select('*').is('timestamp_exit', null).limit(50),
    sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(10),
    sb.from('bot_config').select('*'),
  ])
  const cfg = {}
  cfgRes.data?.forEach(r => { cfg[r.key] = r.value })

  return { props: { session, snapshot: snapRes.data?.[0] || null, openTrades: openRes.data || [], recentTrades: closedRes.data || [], config: cfg } }
}

export default function Overview({ snapshot, openTrades: initialOpen, recentTrades, config }) {
  const [openTrades, setOpenTrades] = useState(initialOpen)

  useEffect(() => {
    const interval = setInterval(async () => {
      const { data } = await supabase.from('trades').select('*').is('timestamp_exit', null).limit(50)
      if (data) setOpenTrades(data)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const walletValue = parseFloat(snapshot?.wallet_value || 0)
  const floorValue = parseFloat(snapshot?.floor_value || 0)
  const sessionPnl = parseFloat(snapshot?.session_pnl || 0)
  const gap = walletValue - floorValue
  const paperCompleted = parseInt(config?.paper_trades_completed || 0)
  const paperWinRate = parseFloat(config?.paper_win_rate || 0)
  const isPaper = config?.current_mode !== 'live'

  // Streak calculation
  const streakTrades = recentTrades || []
  let currentStreak = 0
  let streakType = null
  for (const t of streakTrades) {
    const win = parseFloat(t.pnl || 0) > 0
    if (streakType === null) { streakType = win; currentStreak = 1 }
    else if (win === streakType) currentStreak++
    else break
  }

  return (
    <Layout>
      <div className="mb-6">
        <p className="text-sm text-neutral">Portfolio Value</p>
        <p className="text-3xl font-bold">{formatCurrency(walletValue)}</p>
        <p className={`text-lg ${sessionPnl >= 0 ? 'text-profit' : 'text-loss'}`}>
          Today: {sessionPnl >= 0 ? '+' : ''}{formatCurrency(sessionPnl)}
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <StatCard title="Floor" value={formatCurrency(floorValue)} subtitle={`Gap: ${formatCurrency(gap)}`} />
        <StatCard title="Utilization" value={walletValue > 0 ? ((walletValue - gap) / walletValue * 100).toFixed(0) + '%' : '0%'} />
        <StatCard title="Open Positions" value={openTrades.length} />
        <StatCard title="Streak" value={`${currentStreak} ${streakType ? 'W' : 'L'}`} color={streakType ? 'text-profit' : 'text-loss'} />
      </div>

      {isPaper && (
        <div className="card mb-6 border-paper border">
          <p className="text-paper font-semibold mb-2">Paper Trading Active</p>
          <div className="w-full bg-surface rounded-full h-3 mb-2">
            <div className="bg-paper h-3 rounded-full" style={{ width: `${Math.min(paperCompleted / 50 * 100, 100)}%` }} />
          </div>
          <p className="text-sm text-neutral">{paperCompleted}/50 trades | {(paperWinRate * 100).toFixed(0)}% win rate</p>
          <p className="text-xs text-neutral mt-1">Live mode unlocks automatically at 50 trades with 70%+ win rate</p>
        </div>
      )}

      <h2 className="text-lg font-semibold mb-3">Open Positions</h2>
      {openTrades.length === 0 ? (
        <div className="card text-center text-neutral py-8">No open positions</div>
      ) : (
        <div className="table-scroll mb-6">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Market</th>
              <th className="text-left text-neutral py-2 px-2">Strategy</th>
              <th className="text-right text-neutral py-2 px-2">Entry</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Sport</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Band</th>
              <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Target</th>
            </tr></thead>
            <tbody>
              {openTrades.map((t, i) => (
                <tr key={i} className="border-b border-border">
                  <td className="py-2 px-2 max-w-[150px] truncate">{t.market_slug}</td>
                  <td className="py-2 px-2" style={{ color: STRATEGY_COLORS[t.position_type] || '#fff' }}>{t.position_type}</td>
                  <td className="py-2 px-2 text-right">{parseFloat(t.entry_price || 0).toFixed(4)}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{t.sport}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{t.band}</td>
                  <td className="py-2 px-2 text-right hidden md:table-cell">{parseFloat(t.exit_price || t.entry_price || 0).toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2 className="text-lg font-semibold mb-3">Recent Trades</h2>
      {recentTrades.length === 0 ? (
        <div className="card text-center text-neutral py-8">No trades yet — running in paper mode. Trades appear here live.</div>
      ) : (
        <div className="table-scroll">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Date</th>
              <th className="text-left text-neutral py-2 px-2">Market</th>
              <th className="text-right text-neutral py-2 px-2">P&L</th>
              <th className="text-left text-neutral py-2 px-2">Exit</th>
            </tr></thead>
            <tbody>
              {recentTrades.map((t, i) => {
                const pnl = parseFloat(t.pnl || 0)
                return (
                  <tr key={i} className="border-b border-border">
                    <td className="py-2 px-2">{t.timestamp_exit?.split('T')[0]}</td>
                    <td className="py-2 px-2 max-w-[150px] truncate">{t.market_slug}</td>
                    <td className={`py-2 px-2 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                    <td className="py-2 px-2">{t.exit_type}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      <div className="mt-6 flex items-center gap-3 text-sm text-neutral">
        <span className="w-2 h-2 rounded-full bg-profit inline-block" /> Supabase connected
        <span className={`px-2 py-0.5 rounded text-xs font-bold ${isPaper ? 'bg-paper text-black' : 'bg-live text-black'}`}>{isPaper ? 'PAPER' : 'LIVE'}</span>
      </div>
    </Layout>
  )
}
