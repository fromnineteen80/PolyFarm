import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import SportIcon from '../components/SportIcon'
import EdgeBadge from '../components/EdgeBadge'
import DirectionArrow from '../components/DirectionArrow'
import ScoreBadge from '../components/ScoreBadge'
import MatchupDisplay from '../components/MatchupDisplay'
import LiveGameState from '../components/LiveGameState'
import { formatCurrency } from '../lib/calculations'
import supabase from '../lib/supabase'

const BAND_NAMES = { A: 'Prime', B: 'Standard', C: 'Value', EX: 'Exception', FADE: 'Fade' }

function timeAgo(ts) {
  if (!ts) return '--'
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

  const tt = todayTrades || []
  const todayWins = tt.filter(t => parseFloat(t.pnl || 0) > 0).length
  const todayPnl = tt.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)

  // Split by date
  const now = new Date()
  const todayStr = now.toISOString().split('T')[0]
  const twoDaysOut = new Date(now.getTime() + 2 * 86400000).toISOString().split('T')[0]
  const allGames = (markets || []).filter(m => !m.is_finished)

  // Today's games sorted by trading priority (edge/signal strength)
  const todaysGames = allGames
    .filter(m => m.game_start_time && m.game_start_time.startsWith(todayStr))
    .map(m => ({ ...m, score: calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure) }))
    .sort((a, b) => b.score - a.score)

  // Live signals — today's games with meaningful edge (no duplicates with today's table)
  const signals = todaysGames.filter(m => (m.current_edge || 0) > 0.02)

  // Upcoming (next 2 days) sorted by time with signal strength
  const upcomingGames = allGames
    .filter(m => m.game_start_time && !m.game_start_time.startsWith(todayStr) && m.game_start_time <= twoDaysOut + 'T23:59:59Z')
    .map(m => ({ ...m, score: calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure) }))
    .sort((a, b) => (a.game_start_time || '').localeCompare(b.game_start_time || ''))

  return (
    <Layout>
      {dataStale && (
        <div className="card border-loss border mb-4 flex items-center gap-2">
          <span className="dot dot-red" />
          <span className="text-sm text-loss font-semibold">Connection lost. Showing last known data.</span>
        </div>
      )}

      {/* HERO */}
      <div className="flex flex-col md:flex-row md:items-end gap-6 mb-8">
        <div>
          <p className="text-xs text-neutral uppercase tracking-wide mb-1">Portfolio Value</p>
          <p className="text-3xl font-bold">{formatCurrency(walletValue)}</p>
          <p className={`text-sm mt-1 ${sessionPnl >= 0 ? 'text-profit' : 'text-loss'}`}>
            {sessionPnl >= 0 ? '+' : ''}{formatCurrency(sessionPnl)} today
          </p>
        </div>
        <div>
          <p className="text-xs text-neutral uppercase tracking-wide mb-1">Paper Trading</p>
          <p className="text-3xl font-bold">{paperCompleted}<span className="text-lg text-neutral font-normal">/300</span></p>
          <div className="flex items-center gap-2 mt-1">
            <div className="progress-track flex-1" style={{maxWidth: '160px'}}>
              <div className="progress-fill bg-info" style={{ width: `${Math.min(paperCompleted / 300 * 100, 100)}%` }} />
            </div>
            <span className="text-xs text-neutral">{(paperWinRate * 100).toFixed(0)}% win rate</span>
          </div>
        </div>
        <div className="md:ml-auto text-right">
          <p className="text-xs text-neutral">Floor {formatCurrency(floorValue)} &middot; Gap {formatCurrency(gap)}</p>
          <p className="text-xs text-neutral">{openTrades.length} open &middot; {sysConfig?.markets_matched_count || 0} matched</p>
        </div>
      </div>

      {/* LIVE SIGNALS */}
      {signals.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">
            Live Signals
            <span className="text-sm font-normal text-neutral ml-2">{signals.length} above 2c gap</span>
          </h2>
          <GamesTable games={signals} showScore />
        </div>
      )}

      {/* TODAY'S GAMES */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">
          Today's Games
          <span className="text-sm font-normal text-neutral ml-2">{todaysGames.length} monitored</span>
        </h2>
        {todaysGames.length === 0 ? (
          <div className="card text-neutral text-sm py-6 text-center">No games loaded yet.</div>
        ) : (
          <GamesTable games={todaysGames} showTime />
        )}
      </div>

      {/* UPCOMING GAMES */}
      {upcomingGames.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">
            Upcoming
            <span className="text-sm font-normal text-neutral ml-2">{upcomingGames.length} next 2 days</span>
          </h2>
          <GamesTable games={upcomingGames} showTime showDate />
        </div>
      )}

      {/* OPEN POSITIONS */}
      {openTrades.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Open Positions</h2>
          <div className="space-y-2">
            {openTrades.map((t, i) => (
              <div key={i} className="card py-3 flex flex-col sm:flex-row sm:items-center gap-2">
                <span className="text-sm flex-1">{t.market_slug}</span>
                <span className="text-xs text-neutral">{t.position_type}</span>
                <span className="text-xs">{BAND_NAMES[t.band] || t.band}</span>
                <span className="text-xs text-neutral">Entry {parseFloat(t.entry_price || 0).toFixed(4)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RECENT TRADES */}
      {recentTrades.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Recent Trades</h2>
          <div className="card p-0 overflow-hidden">
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Market</th>
                    <th className="text-right">P&L</th>
                    <th className="hidden md:table-cell">Exit Type</th>
                    <th className="hidden md:table-cell">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentTrades.map((t, i) => {
                    const pnl = parseFloat(t.pnl || 0)
                    return (
                      <tr key={i}>
                        <td>{t.market_slug}</td>
                        <td className={`text-right font-semibold ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                        <td className="hidden md:table-cell">{t.exit_type}</td>
                        <td className="hidden md:table-cell text-neutral">{t.timestamp_exit?.split('T')[0]}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TODAY + SYSTEM — same line, left and right justified */}
      <div className="border-t border-gray-200 pt-6 flex flex-col sm:flex-row gap-8">
        <div className="text-sm space-y-1.5">
          <p className="text-xs font-bold tracking-widest text-neutral uppercase mb-2">Today</p>
          <p><span className="text-neutral">Trades</span> {tt.length} executed &middot; {todayWins} won</p>
          <p><span className="text-neutral">P&L</span> <span className={todayPnl >= 0 ? 'text-profit' : 'text-loss'}>{todayPnl >= 0 ? '+' : ''}{formatCurrency(todayPnl)}</span></p>
          <p><span className="text-neutral">Open</span> {openTrades.length} positions</p>
        </div>
        <div className="sm:ml-auto sm:text-right text-sm space-y-1.5">
          <p className="text-xs font-bold tracking-widest text-neutral uppercase mb-2">System</p>
          <p><span className={`dot ${statusDot(sysConfig?.last_heartbeat, 180, 600)} mr-1.5`} /><span className="text-neutral">Bot</span> {isPaper ? 'Paper' : 'Live'} &middot; {timeAgo(sysConfig?.last_heartbeat)}</p>
          <p><span className={`dot ${statusDot(sysConfig?.odds_api_last_poll, 300, 900)} mr-1.5`} /><span className="text-neutral">Odds</span> {timeAgo(sysConfig?.odds_api_last_poll)}</p>
          <p><span className={`dot ${parseInt(sysConfig?.markets_unmatched_count || 0) <= 5 ? 'dot-green' : 'dot-red'} mr-1.5`} /><span className="text-neutral">Match</span> {sysConfig?.markets_matched_count || 0} matched</p>
          <p><span className={`dot ${statusDot(sysConfig?.supabase_last_write, 60, 300)} mr-1.5`} /><span className="text-neutral">Data</span> {timeAgo(sysConfig?.supabase_last_write)}</p>
        </div>
      </div>
    </Layout>
  )
}

function GamesTable({ games, showScore, showTime, showDate }) {
  if (!games || games.length === 0) return null
  return (
    <div className="card p-0 overflow-hidden">
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>Strength</th>
              <th>Game</th>
              <th>{showScore ? 'Score' : 'Time'}</th>
              <th className="text-right">Market<br/>Price</th>
              <th className="text-right">Fair<br/>Value</th>
              <th className="text-right">Gap</th>
            </tr>
          </thead>
          <tbody>
            {games.map((m, i) => (
              <tr key={i}>
                <td><ScoreBadge score={m.score} /></td>
                <td><MatchupDisplay homeTeam={m.home_team} awayTeam={m.away_team} homeColor={m.home_color} awayColor={m.away_color} sport={m.sport} size="sm" /></td>
                <td>
                  {showScore && m.is_live && m.game_score ? (
                    <LiveGameState score={m.game_score} period={m.game_period} isLive />
                  ) : m.game_start_time ? (
                    <span className="text-sm text-neutral">
                      {showDate && new Date(m.game_start_time).toLocaleDateString([], { month: 'short', day: 'numeric' }) + ', '}
                      {new Date(m.game_start_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}
                    </span>
                  ) : <span className="text-neutral">TBD</span>}
                </td>
                <td className="text-right">{((m.yes_price || 0) * 100).toFixed(0)}c</td>
                <td className="text-right">{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</td>
                <td className="text-right">{m.current_edge ? <EdgeBadge edge={m.current_edge} size="sm" /> : <span className="text-neutral">--</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

