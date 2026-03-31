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

  const signals = (markets || [])
    .filter(m => (m.current_edge || 0) > 0.02)
    .map(m => ({ ...m, score: calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure) }))
    .sort((a, b) => b.score - a.score)

  const todaysGames = (markets || []).filter(m => !m.is_finished)

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
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">
          Live Signals
          <span className="text-sm font-normal text-neutral ml-2">{signals.length} above 2c gap</span>
        </h2>
        {signals.length === 0 ? (
          <div className="card text-neutral text-sm py-6 text-center">
            No opportunities detected. Monitoring {sysConfig?.markets_matched_count || 0} markets.
          </div>
        ) : (
          <div className="space-y-2">
            {signals.slice(0, 10).map((m, i) => (
              <SignalCard key={i} market={m} />
            ))}
          </div>
        )}
      </div>

      {/* TODAY'S GAMES */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">
          Today's Games
          <span className="text-sm font-normal text-neutral ml-2">{todaysGames.length} monitored</span>
        </h2>
        {todaysGames.length === 0 ? (
          <div className="card text-neutral text-sm py-6 text-center">No games loaded yet.</div>
        ) : (
          <>
            {/* Desktop table */}
            <div className="hidden md:block table-scroll">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-100">
                    <th className="text-left py-2 px-3 table-col-header">Game</th>
                    <th className="text-right py-2 px-3 table-col-header">Market Price</th>
                    <th className="text-right py-2 px-3 table-col-header">Fair Value</th>
                    <th className="text-right py-2 px-3 table-col-header">Gap</th>
                    <th className="text-left py-2 px-3 table-col-header">Trend</th>
                    <th className="text-left py-2 px-3 table-col-header">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {todaysGames.map((m, i) => (
                    <tr key={i} className="border-b border-gray-100 hover:bg-surface">
                      <td className="py-2.5 px-3">
                        <MatchupDisplay
                          homeTeam={m.home_team} awayTeam={m.away_team}
                          homeColor={m.home_color} awayColor={m.away_color}
                          sport={m.sport} size="sm"
                        />
                      </td>
                      <td className="py-2.5 px-3 text-right">{((m.yes_price || 0) * 100).toFixed(0)}c</td>
                      <td className="py-2.5 px-3 text-right">{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</td>
                      <td className="py-2.5 px-3 text-right">{m.current_edge ? <EdgeBadge edge={m.current_edge} size="sm" /> : <span className="text-neutral">--</span>}</td>
                      <td className="py-2.5 px-3">{m.current_price_direction ? <DirectionArrow direction={m.current_price_direction} /> : <span className="text-neutral">--</span>}</td>
                      <td className="py-2.5 px-3">{m.is_live ? <LiveGameState score={m.game_score} period={m.game_period} isLive /> : <span className="text-xs text-neutral">{m.game_start_time ? new Date(m.game_start_time).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) : 'TBD'}</span>}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {/* Mobile cards */}
            <div className="md:hidden space-y-2">
              {todaysGames.map((m, i) => (
                <div key={i} className="card py-3">
                  <MatchupDisplay
                    homeTeam={m.home_team} awayTeam={m.away_team}
                    homeColor={m.home_color} awayColor={m.away_color}
                    homeRecord={m.home_record} awayRecord={m.away_record}
                    sport={m.sport} isLive={m.is_live}
                    gameScore={m.game_score} gamePeriod={m.game_period}
                    gameTime={m.game_start_time} size="sm"
                  />
                  <div className="flex flex-wrap gap-3 text-xs mt-2 pl-1">
                    <span><span className="text-neutral">Market </span>{((m.yes_price || 0) * 100).toFixed(0)}c</span>
                    <span><span className="text-neutral">Fair </span>{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</span>
                    {m.current_edge && <span><span className="text-neutral">Gap </span><EdgeBadge edge={m.current_edge} size="sm" /></span>}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

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
          <div className="hidden md:block table-scroll">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-2 px-3 table-col-header">Market</th>
                  <th className="text-right py-2 px-3 table-col-header">P&L</th>
                  <th className="text-left py-2 px-3 table-col-header">Exit Type</th>
                  <th className="text-left py-2 px-3 table-col-header">Date</th>
                </tr>
              </thead>
              <tbody>
                {recentTrades.map((t, i) => {
                  const pnl = parseFloat(t.pnl || 0)
                  return (
                    <tr key={i} className="border-b border-gray-100">
                      <td className="py-2 px-3 text-sm">{t.market_slug}</td>
                      <td className={`py-2 px-3 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                      <td className="py-2 px-3">{t.exit_type}</td>
                      <td className="py-2 px-3 text-neutral">{t.timestamp_exit?.split('T')[0]}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          <div className="md:hidden space-y-2">
            {recentTrades.map((t, i) => {
              const pnl = parseFloat(t.pnl || 0)
              return (
                <div key={i} className="card py-3 flex justify-between items-center">
                  <div>
                    <p className="text-sm">{t.market_slug}</p>
                    <p className="text-xs text-neutral">{t.exit_type} &middot; {t.timestamp_exit?.split('T')[0]}</p>
                  </div>
                  <span className={`text-sm font-semibold ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</span>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* TODAY + SYSTEM */}
      <div className="border-t border-border pt-6">
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral uppercase mb-3">Today</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-neutral">Trades</span><span>{tt.length} executed &middot; {todayWins} won</span></div>
              <div className="flex justify-between"><span className="text-neutral">P&L</span><span className={todayPnl >= 0 ? 'text-profit' : 'text-loss'}>{todayPnl >= 0 ? '+' : ''}{formatCurrency(todayPnl)}</span></div>
              <div className="flex justify-between"><span className="text-neutral">Open</span><span>{openTrades.length} positions</span></div>
            </div>
          </div>
          <div className="flex-1">
            <p className="text-xs font-bold tracking-widest text-neutral uppercase mb-3">System</p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center"><span className={`dot ${statusDot(sysConfig?.last_heartbeat, 180, 600)} mr-2`} /><span className="text-neutral w-16">Bot</span><span className="ml-auto">{isPaper ? 'Paper' : 'Live'} &middot; {timeAgo(sysConfig?.last_heartbeat)}</span></div>
              <div className="flex items-center"><span className={`dot ${statusDot(sysConfig?.odds_api_last_poll, 300, 900)} mr-2`} /><span className="text-neutral w-16">Odds</span><span className="ml-auto">{timeAgo(sysConfig?.odds_api_last_poll)}</span></div>
              <div className="flex items-center"><span className={`dot ${parseInt(sysConfig?.markets_unmatched_count || 0) <= 5 ? 'dot-green' : 'dot-red'} mr-2`} /><span className="text-neutral w-16">Match</span><span className="ml-auto">{sysConfig?.markets_matched_count || 0} matched</span></div>
              <div className="flex items-center"><span className={`dot ${statusDot(sysConfig?.supabase_last_write, 60, 300)} mr-2`} /><span className="text-neutral w-16">Data</span><span className="ml-auto">{timeAgo(sysConfig?.supabase_last_write)}</span></div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

function SignalCard({ market: m }) {
  const score = calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure)
  return (
    <div className="card py-3 flex flex-col sm:flex-row sm:items-center gap-3">
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <ScoreBadge score={score} />
        <MatchupDisplay
          homeTeam={m.home_team} awayTeam={m.away_team}
          homeColor={m.home_color} awayColor={m.away_color}
          homeRecord={m.home_record} awayRecord={m.away_record}
          sport={m.sport} isLive={m.is_live}
          gameScore={m.game_score} gamePeriod={m.game_period}
          gameTime={m.game_start_time} size="sm"
        />
      </div>
      <div className="flex flex-wrap gap-4 text-xs items-center">
        <div className="text-center">
          <p className="text-[10px] text-neutral uppercase">Market</p>
          <p className="font-semibold">{((m.yes_price || 0) * 100).toFixed(0)}c</p>
        </div>
        <div className="text-center">
          <p className="text-[10px] text-neutral uppercase">Fair Value</p>
          <p className="font-semibold">{m.current_sharp_prob ? (m.current_sharp_prob * 100).toFixed(0) + 'c' : '--'}</p>
        </div>
        <div className="text-center">
          <p className="text-[10px] text-neutral uppercase">Gap</p>
          <EdgeBadge edge={m.current_edge} size="sm" />
        </div>
        {m.current_price_direction && (
          <div className="text-center">
            <p className="text-[10px] text-neutral uppercase">Trend</p>
            <DirectionArrow direction={m.current_price_direction} />
          </div>
        )}
      </div>
    </div>
  )
}
