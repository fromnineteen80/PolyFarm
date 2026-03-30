import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import { formatCurrency } from '../lib/calculations'
import supabase from '../lib/supabase'

const STRATEGY_CLASS = { normal: 'strategy-oracle', oracle_arb: 'strategy-oracle', exception: 'strategy-exception', fade: 'strategy-fade', overnight: 'strategy-overnight' }

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const today = new Date().toISOString().split('T')[0]
  const [snapRes, openRes, closedRes, cfgRes, todayTradesRes, sessionRes] = await Promise.all([
    sb.from('daily_snapshots').select('*').order('date', { ascending: false }).limit(1),
    sb.from('trades').select('*').is('timestamp_exit', null).limit(50),
    sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(10),
    sb.from('bot_config').select('*'),
    sb.from('trades').select('*').gte('timestamp_entry', today + 'T00:00:00Z').not('timestamp_exit', 'is', null),
    sb.from('sessions').select('*').order('start_time', { ascending: false }).limit(1),
  ])
  const cfg = {}
  cfgRes.data?.forEach(r => { cfg[r.key] = r.value })

  return {
    props: {
      session,
      snapshot: snapRes.data?.[0] || null,
      openTrades: openRes.data || [],
      recentTrades: closedRes.data || [],
      config: cfg,
      todayTrades: todayTradesRes.data || [],
      latestSession: sessionRes.data?.[0] || null,
    }
  }
}

function timeAgo(ts) {
  if (!ts) return 'unknown'
  const diff = (Date.now() - new Date(ts).getTime()) / 1000
  if (diff < 60) return `${Math.round(diff)}s ago`
  if (diff < 3600) return `${Math.round(diff / 60)}m ago`
  if (diff < 86400) return `${Math.round(diff / 3600)}h ago`
  return `${Math.round(diff / 86400)}d ago`
}

function statusDot(ts, warnSec, critSec) {
  if (!ts) return 'dot-grey'
  const age = (Date.now() - new Date(ts).getTime()) / 1000
  if (age > critSec) return 'dot-red'
  if (age > warnSec) return 'dot-yellow'
  return 'dot-green'
}

export default function Overview({ snapshot, openTrades: initialOpen, recentTrades, config, todayTrades, latestSession }) {
  const [openTrades, setOpenTrades] = useState(initialOpen)
  const [sysConfig, setSysConfig] = useState(config)
  const [sysLoading, setSysLoading] = useState(false)

  useEffect(() => {
    const interval = setInterval(async () => {
      const [tradesRes, cfgRes] = await Promise.all([
        supabase.from('trades').select('*').is('timestamp_exit', null).limit(50),
        supabase.from('bot_config').select('*'),
      ])
      if (tradesRes.data) setOpenTrades(tradesRes.data)
      if (cfgRes.data) {
        const c = {}
        cfgRes.data.forEach(r => { c[r.key] = r.value })
        setSysConfig(c)
      }
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

  // Streak
  const streakTrades = recentTrades || []
  let currentStreak = 0
  let streakType = null
  for (const t of streakTrades) {
    const win = parseFloat(t.pnl || 0) > 0
    if (streakType === null) { streakType = win; currentStreak = 1 }
    else if (win === streakType) currentStreak++
    else break
  }

  // Today summary
  const tt = todayTrades || []
  const todayWins = tt.filter(t => parseFloat(t.pnl || 0) > 0).length
  const todayLosses = tt.length - todayWins
  const todayWR = tt.length > 0 ? (todayWins / tt.length * 100).toFixed(0) : '0'
  const todayPnl = tt.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
  const todayPnlPct = walletValue > 0 ? (todayPnl / walletValue * 100).toFixed(2) : '0.00'
  const oracleCount = tt.filter(t => t.position_type === 'normal' || t.position_type === 'oracle_arb').length
  const fadeCount = tt.filter(t => t.position_type === 'fade').length
  const exceptionCount = tt.filter(t => t.position_type === 'exception').length
  const overnightCount = tt.filter(t => t.position_type === 'overnight').length
  const profitMode = latestSession?.lock_reason || config?.profit_mode || 'NORMAL'
  const peakGain = parseFloat(latestSession?.peak_daily_gain_pct || 0) * 100
  const floorSafe = gap > 0

  const bestTrade = tt.length > 0
    ? tt.reduce((best, t) => parseFloat(t.pnl || 0) > parseFloat(best.pnl || 0) ? t : best, tt[0])
    : null
  const bestPnl = bestTrade ? parseFloat(bestTrade.pnl || 0) : 0

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
          <div className="progress-track mb-2">
            <div className="progress-fill bg-paper" style={{ width: `${Math.min(paperCompleted / 50 * 100, 100)}%` }} />
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
                  <td className={`py-2 px-2 ${STRATEGY_CLASS[t.position_type] || ''}`}>{t.position_type}</td>
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

      {/* TODAY SUMMARY */}
      <div className="border-t border-border mt-8 pt-6">
        <p className="text-xs font-bold tracking-widest text-neutral mb-4">TODAY</p>
        <div className="space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-neutral">Trades</span>
            <span className="font-semibold">{tt.length} executed · {todayWins} won · {todayLosses} lost · {todayWR}% win rate</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-neutral">P&L</span>
            <span className={`font-semibold ${todayPnl >= 0 ? 'text-profit' : 'text-loss'}`}>{todayPnl >= 0 ? '+' : ''}{formatCurrency(todayPnl)} · {todayPnl >= 0 ? '+' : ''}{todayPnlPct}% session</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-neutral">Strategies</span>
            <span className="font-semibold">Oracle {oracleCount} · Fade {fadeCount} · Exception {exceptionCount} · Overnight {overnightCount}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-neutral">Mode</span>
            <span className="font-semibold">{profitMode} · peaked +{peakGain.toFixed(1)}% · <span className={floorSafe ? 'text-profit' : 'text-loss'}>{floorSafe ? 'floor safe' : 'WARNING'}</span></span>
          </div>
          {isPaper && (
            <div className="flex justify-between text-sm">
              <span className="text-neutral">Paper</span>
              <span className="font-semibold">{paperCompleted}/50 trades · {(paperWinRate * 100).toFixed(0)}% win rate</span>
            </div>
          )}
          <div className="flex justify-between text-sm">
            <span className="text-neutral">Best trade</span>
            <span className="font-semibold">{bestTrade ? `${bestTrade.teams || bestTrade.market_slug} ${bestPnl >= 0 ? '+' : ''}${formatCurrency(bestPnl)} (${bestTrade.position_type})` : '--'}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-neutral">Active now</span>
            <span className="font-semibold">{openTrades.length} open positions</span>
          </div>
        </div>
      </div>

      {/* SYSTEM STATUS */}
      <div className="border-t border-border mt-8 pt-6 mb-4">
        <p className="text-xs font-bold tracking-widest text-neutral mb-4">SYSTEM</p>
        <div className="space-y-3">
          <StatusRow
            label="Bot"
            dot={statusDot(sysConfig?.last_heartbeat, 180, 600)}
            value={`${isPaper ? 'PAPER' : 'LIVE'} · last heartbeat ${timeAgo(sysConfig?.last_heartbeat)}`}
          />
          <StatusRow
            label="Polymarket"
            dot={sysConfig?.ws_markets_status === 'CONNECTED' && sysConfig?.ws_private_status === 'CONNECTED' ? 'dot-green' : sysConfig?.ws_markets_status === 'CONNECTED' || sysConfig?.ws_private_status === 'CONNECTED' ? 'dot-yellow' : sysConfig?.ws_markets_status ? 'dot-red' : 'dot-grey'}
            value={`${sysConfig?.ws_markets_status || 'UNKNOWN'} · markets + private WebSocket`}
          />
          <StatusRow
            label="Odds API"
            dot={statusDot(sysConfig?.odds_api_last_poll, 300, 900)}
            value={`Last poll ${timeAgo(sysConfig?.odds_api_last_poll)} · ${sysConfig?.odds_api_requests_used || '0'} / 100,000 credits used`}
          />
          <StatusRow
            label="Matching"
            dot={parseInt(sysConfig?.markets_unmatched_count || 0) === 0 ? 'dot-green' : parseInt(sysConfig?.markets_unmatched_count || 0) <= 5 ? 'dot-yellow' : 'dot-red'}
            value={`${sysConfig?.markets_matched_count || '0'} matched · ${sysConfig?.markets_unmatched_count || '0'} unmatched`}
          />
          <StatusRow
            label="WebSocket"
            dot={parseInt(sysConfig?.ws_reconnect_count || 0) === 0 ? 'dot-green' : parseInt(sysConfig?.ws_reconnect_count || 0) <= 3 ? 'dot-yellow' : 'dot-red'}
            value={`${(() => { try { return JSON.parse(sysConfig?.ws_markets_subscribed_slugs || '[]').length } catch(e) { return 0 } })()} subscribed · ${sysConfig?.ws_reconnect_count || '0'} reconnects`}
          />
          <StatusRow
            label="Supabase"
            dot={statusDot(sysConfig?.supabase_last_write, 60, 300)}
            value={`${sysConfig?.supabase_last_write ? 'CONNECTED' : 'UNKNOWN'} · last write ${timeAgo(sysConfig?.supabase_last_write)}`}
          />
          <StatusRow
            label="Telegram"
            dot={sysConfig?.telegram_last_alert ? 'dot-green' : 'dot-grey'}
            value={`${sysConfig?.telegram_last_alert ? 'ACTIVE' : 'UNKNOWN'} · last alert ${timeAgo(sysConfig?.telegram_last_alert)}`}
          />
        </div>
      </div>
    </Layout>
  )
}

function StatusRow({ label, dot, value }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <span className={`dot ${dot}`} />
      <span className="text-neutral w-24 flex-shrink-0">{label}</span>
      <span className="font-semibold">{value}</span>
    </div>
  )
}
