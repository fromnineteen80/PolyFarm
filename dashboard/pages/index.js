import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import SportIcon from '../components/SportIcon'
import EdgeBadge from '../components/EdgeBadge'
import DirectionArrow from '../components/DirectionArrow'
import LiveGameState from '../components/LiveGameState'
import { formatCurrency } from '../lib/calculations'
import supabase from '../lib/supabase'

const BAND_NAMES = { A: 'Prime', B: 'Standard', C: 'Value', EX: 'Exception', FADE: 'Fade' }

function timeAgo(ts) {
  if (!ts) return 'unknown'
  const diff = (Date.now() - new Date(ts).getTime()) / 1000
  if (diff < 60) return `${Math.round(diff)}s ago`
  if (diff < 3600) return `${Math.round(diff / 60)}m ago`
  return `${Math.round(diff / 3600)}h ago`
}

function statusDot(ts, warnSec, critSec) {
  if (!ts) return 'dot-grey'
  const age = (Date.now() - new Date(ts).getTime()) / 1000
  if (age > critSec) return 'dot-red'
  if (age > warnSec) return 'dot-yellow'
  return 'dot-green'
}

function calcScore(edge, direction, pressure) {
  const base = Math.min((edge || 0) / 0.10, 1.0) * 60
  const dir = direction === 'falling' ? 30 : direction === 'stable' ? 15 : 0
  const press = (pressure || 1) < 0.7 ? 10 : (pressure || 1) <= 1.3 ? 5 : 0
  return Math.round(base + dir + press)
}

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session?.user) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const today = new Date().toISOString().split('T')[0]
  let snap = null, openTrades = [], closedTrades = [], cfg = {}, todayTrades = [], markets = []
  try {
    const [snapRes, openRes, closedRes, cfgRes, todayRes, mktsRes] = await Promise.all([
      sb.from('daily_snapshots').select('*').order('date', { ascending: false }).limit(1),
      sb.from('trades').select('*').is('timestamp_exit', null).limit(50),
      sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(10),
      sb.from('bot_config').select('*'),
      sb.from('trades').select('*').gte('timestamp_entry', today + 'T00:00:00Z').not('timestamp_exit', 'is', null),
      sb.from('markets').select('*').order('game_start_time', { ascending: true }),
    ])
    snap = snapRes.data?.[0]
    openTrades = openRes.data || []
    closedTrades = closedRes.data || []
    cfgRes.data?.forEach(r => { cfg[r.key] = r.value })
    todayTrades = todayRes.data || []
    markets = mktsRes.data || []
  } catch (e) {}

  return { props: {
    session: JSON.parse(JSON.stringify(session)),
    snapshot: snap, openTrades, recentTrades: closedTrades,
    config: cfg, todayTrades, markets,
  }}
}

export default function Today({ snapshot, openTrades: initialOpen, recentTrades, config, todayTrades, markets: initialMarkets }) {
  const [openTrades, setOpenTrades] = useState(initialOpen)
  const [markets, setMarkets] = useState(initialMarkets)
  const [sysConfig, setSysConfig] = useState(config)
  const [dataStale, setDataStale] = useState(false)

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const [tradesRes, cfgRes, mktsRes] = await Promise.all([
          supabase.from('trades').select('*').is('timestamp_exit', null).limit(50),
          supabase.from('bot_config').select('*'),
          supabase.from('markets').select('*').order('game_start_time', { ascending: true }),
        ])
        if (tradesRes.data) setOpenTrades(tradesRes.data)
        if (cfgRes.data) { const c = {}; cfgRes.data.forEach(r => { c[r.key] = r.value }); setSysConfig(c) }
        if (mktsRes.data) setMarkets(mktsRes.data)
        setDataStale(false)
      } catch (e) { setDataStale(true) }
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const walletValue = parseFloat(snapshot?.wallet_value || 0)
  const floorValue = parseFloat(snapshot?.floor_value || 0)
  const sessionPnl = parseFloat(snapshot?.session_pnl || 0)
  const gap = walletValue - floorValue
  const paperCompleted = parseInt(String(config?.paper_trades_completed || 0).replace(/"/g, ''))
  const paperWinRate = parseFloat(String(config?.paper_win_rate || 0).replace(/"/g, ''))
  const isPaper = config?.current_mode !== 'live'

  // Today stats
  const tt = todayTrades || []
  const todayWins = tt.filter(t => parseFloat(t.pnl || 0) > 0).length
  const todayPnl = tt.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)

  // Signals — markets with edge > 2c
  const signals = (markets || [])
    .filter(m => (m.current_edge || 0) > 0.02)
    .map(m => ({ ...m, score: calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure) }))
    .sort((a, b) => b.score - a.score)

  // Today's games — all markets sorted by time
  const todaysGames = (markets || []).filter(m => !m.is_finished)

  return (
    <Layout>
      {dataStale && (
        <div className="card border-loss border mb-4 flex items-center gap-2">
          <span className="dot dot-red" />
          <span className="text-sm text-loss font-semibold">Connection lost. Showing last known data.</span>
        </div>
      )}

      {/* HERO ROW */}
      <div className="flex flex-col md:flex-row md:items-end gap-6 mb-8">
        <div>
          <p className="text-sm text-neutral mb-1">Portfolio Value</p>
          <p className="text-3xl font-bold">{formatCurrency(walletValue)}</p>
          <p className={`text-sm mt-1 ${sessionPnl >= 0 ? 'text-profit' : 'text-loss'}`}>
            {sessionPnl >= 0 ? '+' : ''}{formatCurrency(sessionPnl)} today
          </p>
        </div>
        <div>
          <p className="text-sm text-neutral mb-1">Paper Trading</p>
          <p className="text-3xl font-bold">{paperCompleted}/300</p>
          <div className="progress-track mt-1" style={{width: '200px'}}>
            <div className="progress-fill bg-info" style={{ width: `${Math.min(paperCompleted / 300 * 100, 100)}%` }} />
          </div>
          <p className="text-xs text-neutral mt-1">{(paperWinRate * 100).toFixed(0)}% win rate, need 70%</p>
        </div>
        <div className="md:ml-auto text-sm">
          <p className="text-neutral">Floor {formatCurrency(floorValue)} &middot; Gap {formatCurrency(gap)}</p>
          <p className="text-neutral">{openTrades.length} open positions</p>
        </div>
      </div>

      {/* LIVE SIGNALS */}
      <h2 className="text-lg font-semibold mb-3">
        Live Signals
        <span className="text-sm font-normal text-neutral ml-2">{signals.length} opportunities above 2c gap</span>
      </h2>
      {signals.length === 0 ? (
        <div className="card text-neutral text-sm py-6 text-center mb-6">
          No mispricing detected right now. Monitoring {sysConfig?.markets_matched_count || 0} matched markets.
        </div>
      ) : (
        <div className="space-y-2 mb-6">
          {signals.slice(0, 10).map((m, i) => (
            <div key={i} className="card flex flex-col sm:flex-row sm:items-center gap-3 py-3">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold">{m.home_team} vs {m.away_team}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <SportIcon sport={m.sport} showLabel />
                  {m.is_live ? <LiveGameState score={m.game_score} period={m.game_period} isLive /> : <span className="text-xs text-neutral">{m.game_start_time ? new Date(m.game_start_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) : ''}</span>}
                </div>
              </div>
              <div className="flex flex-wrap gap-4 text-xs">
                <div><span className="text-neutral">Market </span><span className="font-semibold">{((m.yes_price || 0) * 100).toFixed(0)}c</span></div>
                <div><span className="text-neutral">Fair Value </span><span className="font-semibold">{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</span></div>
                <div><span className="text-neutral">Gap </span><EdgeBadge edge={m.current_edge} size="sm" /></div>
                {m.current_price_direction && <DirectionArrow direction={m.current_price_direction} velocity={m.current_price_velocity} />}
                <div className="px-2 py-0.5 rounded bg-surface text-xs font-semibold">Strength {calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure)}</div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TODAY'S GAMES */}
      <h2 className="text-lg font-semibold mb-3">
        Today's Games
        <span className="text-sm font-normal text-neutral ml-2">{todaysGames.length} monitored</span>
      </h2>
      {todaysGames.length === 0 ? (
        <div className="card text-neutral text-sm py-6 text-center mb-6">No games loaded yet. Markets appear as they are listed.</div>
      ) : (
        <div className="table-scroll mb-6">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border text-neutral text-xs">
              <th className="text-left py-2 px-3">Game</th>
              <th className="text-right py-2 px-3">Market Price</th>
              <th className="text-right py-2 px-3">Fair Value</th>
              <th className="text-right py-2 px-3">Gap</th>
              <th className="text-left py-2 px-3 hidden md:table-cell">Trend</th>
              <th className="text-left py-2 px-3 hidden md:table-cell">Status</th>
            </tr></thead>
            <tbody>
              {todaysGames.map((m, i) => (
                <tr key={i} className="border-b border-border hover:bg-surface">
                  <td className="py-2 px-3">
                    <span className="text-sm">{m.home_team} vs {m.away_team}</span>
                    <span className="text-xs text-neutral ml-2"><SportIcon sport={m.sport} /></span>
                  </td>
                  <td className="py-2 px-3 text-right">{((m.yes_price || 0) * 100).toFixed(0)}c</td>
                  <td className="py-2 px-3 text-right">{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</td>
                  <td className="py-2 px-3 text-right">{m.current_edge ? <EdgeBadge edge={m.current_edge} size="sm" /> : <span className="text-neutral">--</span>}</td>
                  <td className="py-2 px-3 hidden md:table-cell">{m.current_price_direction ? <DirectionArrow direction={m.current_price_direction} /> : <span className="text-neutral">--</span>}</td>
                  <td className="py-2 px-3 hidden md:table-cell">{m.is_live ? <LiveGameState score={m.game_score} period={m.game_period} isLive /> : <span className="text-xs text-neutral">{m.game_start_time ? new Date(m.game_start_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) : 'TBD'}</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* OPEN POSITIONS */}
      {openTrades.length > 0 && (
        <>
          <h2 className="text-lg font-semibold mb-3">Open Positions</h2>
          <div className="table-scroll mb-6">
            <table className="w-full text-sm">
              <thead><tr className="border-b border-border text-neutral text-xs">
                <th className="text-left py-2 px-3">Market</th>
                <th className="text-left py-2 px-3">Strategy</th>
                <th className="text-right py-2 px-3">Entry</th>
                <th className="text-left py-2 px-3 hidden md:table-cell">Band</th>
              </tr></thead>
              <tbody>
                {openTrades.map((t, i) => (
                  <tr key={i} className="border-b border-border">
                    <td className="py-2 px-3 text-sm">{t.market_slug}</td>
                    <td className="py-2 px-3 text-sm">{t.position_type}</td>
                    <td className="py-2 px-3 text-right">{parseFloat(t.entry_price || 0).toFixed(4)}</td>
                    <td className="py-2 px-3 hidden md:table-cell">{BAND_NAMES[t.band] || t.band}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* RECENT TRADES */}
      {recentTrades.length > 0 && (
        <>
          <h2 className="text-lg font-semibold mb-3">Recent Trades</h2>
          <div className="table-scroll mb-6">
            <table className="w-full text-sm">
              <thead><tr className="border-b border-border text-neutral text-xs">
                <th className="text-left py-2 px-3">Market</th>
                <th className="text-right py-2 px-3">P&L</th>
                <th className="text-left py-2 px-3">Exit</th>
                <th className="text-left py-2 px-3 hidden md:table-cell">Date</th>
              </tr></thead>
              <tbody>
                {recentTrades.map((t, i) => {
                  const pnl = parseFloat(t.pnl || 0)
                  return (
                    <tr key={i} className="border-b border-border">
                      <td className="py-2 px-3 text-sm">{t.market_slug}</td>
                      <td className={`py-2 px-3 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                      <td className="py-2 px-3">{t.exit_type}</td>
                      <td className="py-2 px-3 hidden md:table-cell">{t.timestamp_exit?.split('T')[0]}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* TODAY SUMMARY + SYSTEM STATUS */}
      <div className="border-t border-border pt-6">
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral mb-3">TODAY</p>
            <div className="space-y-2 text-sm">
              <SummaryRow label="Trades" value={`${tt.length} executed &middot; ${todayWins} won &middot; ${tt.length - todayWins} lost`} />
              <SummaryRow label="P&L" value={`${todayPnl >= 0 ? '+' : ''}${formatCurrency(todayPnl)}`} color={todayPnl >= 0 ? 'text-profit' : 'text-loss'} />
              <SummaryRow label="Open" value={`${openTrades.length} positions`} />
              {isPaper && <SummaryRow label="Paper" value={`${paperCompleted}/300 trades &middot; ${(paperWinRate * 100).toFixed(0)}% win rate`} />}
            </div>
          </div>
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral mb-3">SYSTEM</p>
            <div className="space-y-2">
              <StatusRow label="Bot" dot={statusDot(sysConfig?.last_heartbeat, 180, 600)} value={`${isPaper ? 'Paper' : 'Live'} &middot; ${timeAgo(sysConfig?.last_heartbeat)}`} />
              <StatusRow label="Odds API" dot={statusDot(sysConfig?.odds_api_last_poll, 300, 900)} value={`${timeAgo(sysConfig?.odds_api_last_poll)}`} />
              <StatusRow label="Matching" dot={parseInt(sysConfig?.markets_unmatched_count || 0) <= 5 ? 'dot-green' : 'dot-red'} value={`${sysConfig?.markets_matched_count || '0'} matched`} />
              <StatusRow label="Database" dot={statusDot(sysConfig?.supabase_last_write, 60, 300)} value={`${timeAgo(sysConfig?.supabase_last_write)}`} />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

function SummaryRow({ label, value, color }) {
  return (
    <div className="flex justify-between">
      <span className="text-neutral">{label}</span>
      <span className={`font-semibold ${color || ''}`} dangerouslySetInnerHTML={{ __html: value }} />
    </div>
  )
}

function StatusRow({ label, dot, value }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className={`dot ${dot}`} />
      <span className="text-neutral w-16">{label}</span>
      <span className="font-semibold text-right flex-1" dangerouslySetInnerHTML={{ __html: value }} />
    </div>
  )
}
