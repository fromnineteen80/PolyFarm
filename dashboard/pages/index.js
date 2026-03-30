import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import { formatCurrency } from '../lib/calculations'
import supabase from '../lib/supabase'

const STRATEGY_CLASS = { normal: 'strategy-oracle', oracle_arb: 'strategy-oracle', exception: 'strategy-exception', fade: 'strategy-fade', overnight: 'strategy-overnight' }
const BAND_NAMES = { A: 'Prime', B: 'Standard', C: 'Value', EX: 'Exception', FADE: 'Fade' }

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

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session?.user) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const today = new Date().toISOString().split('T')[0]
  let snapRes, openRes, closedRes, cfgRes, todayTradesRes, sessionRes
  try {
    ;[snapRes, openRes, closedRes, cfgRes, todayTradesRes, sessionRes] = await Promise.all([
      sb.from('daily_snapshots').select('*').order('date', { ascending: false }).limit(1),
      sb.from('trades').select('*').is('timestamp_exit', null).limit(50),
      sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(10),
      sb.from('bot_config').select('*'),
      sb.from('trades').select('*').gte('timestamp_entry', today + 'T00:00:00Z').not('timestamp_exit', 'is', null),
      sb.from('sessions').select('*').order('start_time', { ascending: false }).limit(1),
    ])
  } catch (e) {
    snapRes = { data: [] }; openRes = { data: [] }; closedRes = { data: [] }
    cfgRes = { data: [] }; todayTradesRes = { data: [] }; sessionRes = { data: [] }
  }
  const cfg = {}
  cfgRes.data?.forEach(r => { cfg[r.key] = r.value })

  return {
    props: {
      session: JSON.parse(JSON.stringify(session)),
      snapshot: snapRes.data?.[0] || null,
      openTrades: openRes.data || [],
      recentTrades: closedRes.data || [],
      config: cfg,
      todayTrades: todayTradesRes.data || [],
      latestSession: sessionRes.data?.[0] || null,
    }
  }
}

export default function Overview({ snapshot, openTrades: initialOpen, recentTrades, config, todayTrades, latestSession }) {
  const [openTrades, setOpenTrades] = useState(initialOpen)
  const [sysConfig, setSysConfig] = useState(config)
  const [dataStale, setDataStale] = useState(false)
  const [lastSuccessfulPoll, setLastSuccessfulPoll] = useState(Date.now())

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
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
        setDataStale(false)
        setLastSuccessfulPoll(Date.now())
      } catch (e) {
        setDataStale(true)
      }
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const walletValue = parseFloat(snapshot?.wallet_value || 0)
  const floorValue = parseFloat(snapshot?.floor_value || 0)
  const sessionPnl = parseFloat(snapshot?.session_pnl || 0)
  const gap = walletValue - floorValue
  const utilization = walletValue > 0 ? ((walletValue - gap) / walletValue * 100).toFixed(0) : '0'
  const paperCompleted = parseInt(String(config?.paper_trades_completed || 0).replace(/"/g, ''))
  const paperWinRate = parseFloat(String(config?.paper_win_rate || 0).replace(/"/g, ''))
  const isPaper = config?.current_mode !== 'live'

  // Streak
  let currentStreak = 0, streakType = null
  for (const t of (recentTrades || [])) {
    const win = parseFloat(t.pnl || 0) > 0
    if (streakType === null) { streakType = win; currentStreak = 1 }
    else if (win === streakType) currentStreak++
    else break
  }

  // Today
  const tt = todayTrades || []
  const todayWins = tt.filter(t => parseFloat(t.pnl || 0) > 0).length
  const todayLosses = tt.length - todayWins
  const todayWR = tt.length > 0 ? (todayWins / tt.length * 100).toFixed(0) : '0'
  const todayPnl = tt.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
  const oracleCount = tt.filter(t => t.position_type === 'normal' || t.position_type === 'oracle_arb').length
  const fadeCount = tt.filter(t => t.position_type === 'fade').length
  const exceptionCount = tt.filter(t => t.position_type === 'exception').length
  const overnightCount = tt.filter(t => t.position_type === 'overnight').length

  const bestTrade = tt.length > 0
    ? tt.reduce((best, t) => parseFloat(t.pnl || 0) > parseFloat(best.pnl || 0) ? t : best, tt[0])
    : null
  const bestPnl = bestTrade ? parseFloat(bestTrade.pnl || 0) : 0

  return (
    <Layout>
      {dataStale && (
        <div className="card border-loss border mb-4 flex items-center gap-2">
          <span className="dot dot-red" />
          <span className="text-sm text-loss font-semibold">Connection lost. Showing data from {new Date(lastSuccessfulPoll).toLocaleTimeString()}.</span>
        </div>
      )}

      {/* HERO: Portfolio + Paper Status side by side */}
      <div className="flex flex-col md:flex-row gap-6 mb-6">
        <div className="flex-1">
          <p className="text-sm text-neutral">Portfolio Value</p>
          <p className="text-3xl font-bold">{formatCurrency(walletValue)}</p>
          <p className={`text-lg ${sessionPnl >= 0 ? 'text-profit' : 'text-loss'}`}>
            Today: {sessionPnl >= 0 ? '+' : ''}{formatCurrency(sessionPnl)}
          </p>
        </div>
        {isPaper && (
          <div className="flex-1 max-w-md">
            <p className="text-sm text-paper font-semibold mb-1">Paper Trading Active</p>
            <div className="progress-track mb-1">
              <div className="progress-fill bg-paper" style={{ width: `${Math.min(paperCompleted / 300 * 100, 100)}%` }} />
            </div>
            <p className="text-xs text-neutral">{paperCompleted}/300 trades | {(paperWinRate * 100).toFixed(0)}% win rate</p>
            <p className="text-xs text-neutral">Live mode unlocks at 300 trades with 70%+ win rate</p>
          </div>
        )}
      </div>

      {/* KEY METRICS ROW */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
        <div className="card">
          <p className="text-sm text-neutral">Floor</p>
          <p className="text-xl font-bold">{formatCurrency(floorValue)}</p>
          <p className="text-xs text-neutral">Gap: {formatCurrency(gap)} | Utilization: {utilization}%</p>
        </div>
        <div className="card">
          <p className="text-sm text-neutral">Open Positions</p>
          <p className="text-xl font-bold">{openTrades.length}</p>
          <p className="text-xs text-neutral">{isPaper ? 'Paper mode' : 'Live mode'}</p>
        </div>
        <div className="card">
          <p className="text-sm text-neutral">Current Streak</p>
          <div className="flex items-center gap-2">
            <p className={`text-xl font-bold ${streakType ? 'text-profit' : currentStreak > 0 ? 'text-loss' : ''}`}>
              {currentStreak > 0 ? `${currentStreak} ${streakType ? 'wins' : 'losses'}` : 'No trades yet'}
            </p>
          </div>
        </div>
      </div>

      {/* OPEN POSITIONS */}
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
                  <td className="py-2 px-2">{t.market_slug}</td>
                  <td className={`py-2 px-2 ${STRATEGY_CLASS[t.position_type] || ''}`}>{t.position_type}</td>
                  <td className="py-2 px-2 text-right">{parseFloat(t.entry_price || 0).toFixed(4)}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{t.sport}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{BAND_NAMES[t.band] || t.band}</td>
                  <td className="py-2 px-2 text-right hidden md:table-cell">{parseFloat(t.exit_price || t.entry_price || 0).toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* RECENT TRADES */}
      <h2 className="text-lg font-semibold mb-3">Recent Trades</h2>
      {recentTrades.length === 0 ? (
        <div className="card text-center text-neutral py-8">No trades yet. Trades appear here as the bot executes.</div>
      ) : (
        <div className="table-scroll mb-6">
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
                    <td className="py-2 px-2">{t.market_slug}</td>
                    <td className={`py-2 px-2 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                    <td className="py-2 px-2">{t.exit_type}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* TODAY + SYSTEM — side by side on desktop, stacked on mobile */}
      <div className="border-t border-border mt-6 pt-6">
        <div className="flex flex-col lg:flex-row gap-8">

          {/* TODAY — left side */}
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral mb-4">TODAY</p>
            <div className="space-y-2 text-sm">
              <Row label="Trades" value={`${tt.length} executed | ${todayWins} won | ${todayLosses} lost | ${todayWR}% win rate`} />
              <Row label="P&L" value={`${todayPnl >= 0 ? '+' : ''}${formatCurrency(todayPnl)}`} color={todayPnl >= 0 ? 'text-profit' : 'text-loss'} />
              <Row label="Strategies" value={`Oracle ${oracleCount} | Fade ${fadeCount} | Exception ${exceptionCount} | Overnight ${overnightCount}`} />
              <Row label="Best trade" value={bestTrade ? `${bestTrade.teams || bestTrade.market_slug} ${bestPnl >= 0 ? '+' : ''}${formatCurrency(bestPnl)}` : 'None yet'} />
              <Row label="Active" value={`${openTrades.length} open positions`} />
              {isPaper && <Row label="Paper" value={`${paperCompleted}/300 trades | ${(paperWinRate * 100).toFixed(0)}% win rate`} />}
            </div>
          </div>

          {/* SYSTEM — right side */}
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral mb-4">SYSTEM</p>
            <div className="space-y-2">
              <StatusRow label="Bot" dot={statusDot(sysConfig?.last_heartbeat, 180, 600)}
                value={`${isPaper ? 'Paper' : 'Live'} | heartbeat ${timeAgo(sysConfig?.last_heartbeat)}`} />
              <StatusRow label="Polymarket"
                dot={sysConfig?.ws_markets_status === 'CONNECTED' && sysConfig?.ws_private_status === 'CONNECTED' ? 'dot-green' : sysConfig?.ws_markets_status === 'CONNECTED' || sysConfig?.ws_private_status === 'CONNECTED' ? 'dot-yellow' : sysConfig?.ws_markets_status ? 'dot-red' : 'dot-grey'}
                value={`${sysConfig?.ws_markets_status || 'Unknown'} | markets + private`} />
              <StatusRow label="Odds API" dot={statusDot(sysConfig?.odds_api_last_poll, 300, 900)}
                value={`Poll ${timeAgo(sysConfig?.odds_api_last_poll)} | ${sysConfig?.odds_api_requests_used || '0'}/100k credits`} />
              <StatusRow label="Matching"
                dot={parseInt(sysConfig?.markets_unmatched_count || 0) === 0 ? 'dot-green' : parseInt(sysConfig?.markets_unmatched_count || 0) <= 5 ? 'dot-yellow' : 'dot-red'}
                value={`${sysConfig?.markets_matched_count || '0'} matched | ${sysConfig?.markets_unmatched_count || '0'} unmatched`} />
              <StatusRow label="Supabase" dot={statusDot(sysConfig?.supabase_last_write, 60, 300)}
                value={`${sysConfig?.supabase_last_write ? 'Connected' : 'Unknown'} | write ${timeAgo(sysConfig?.supabase_last_write)}`} />
              <StatusRow label="Telegram" dot={sysConfig?.telegram_last_alert ? 'dot-green' : 'dot-grey'}
                value={`${sysConfig?.telegram_last_alert ? 'Active' : 'Unknown'} | alert ${timeAgo(sysConfig?.telegram_last_alert)}`} />
            </div>
          </div>

        </div>
      </div>
    </Layout>
  )
}

function Row({ label, value, color }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-neutral">{label}</span>
      <span className={`font-semibold ${color || ''}`}>{value}</span>
    </div>
  )
}

function StatusRow({ label, dot, value }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <span className={`dot ${dot}`} />
      <span className="text-neutral w-20 flex-shrink-0">{label}</span>
      <span className="font-semibold">{value}</span>
    </div>
  )
}
