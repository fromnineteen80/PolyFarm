import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import SportIcon from '../components/SportIcon'
import StatCard from '../components/StatCard'
import ScoreBadge from '../components/ScoreBadge'
import EdgeBadge from '../components/EdgeBadge'
import DirectionArrow from '../components/DirectionArrow'
import BookCount from '../components/BookCount'
import LiveGameState from '../components/LiveGameState'
import Icon from '../components/Icon'
import supabase from '../lib/supabase'
import { formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [marketsRes, cfgRes] = await Promise.all([
    sb.from('markets').select('*').gt('current_edge', 0.02).order('current_edge', { ascending: false }),
    sb.from('bot_config').select('key, value').in('key', ['markets_matched_count', 'markets_unmatched_count']),
  ])
  const cfg = {}
  cfgRes.data?.forEach(r => { try { cfg[r.key] = JSON.parse(r.value) } catch(e) { cfg[r.key] = r.value } })
  return { props: { session, markets: marketsRes.data || [], config: cfg } }
}

function calcScore(edge, direction, pressure) {
  const base = Math.min((edge || 0) / 0.10, 1.0) * 60
  const dir = direction === 'falling' ? 30 : direction === 'stable' ? 15 : 0
  const press = (pressure || 1) < 0.7 ? 10 : (pressure || 1) <= 1.3 ? 5 : 0
  return Math.round(base + dir + press)
}

export default function Mispricing({ markets: initial, config }) {
  const [markets, setMarkets] = useState(initial)
  const [updating, setUpdating] = useState(false)
  const [filters, setFilters] = useState({ sport: '', minEdge: '' })

  const [dataStale, setDataStale] = useState(false)

  useEffect(() => {
    const interval = setInterval(async () => {
      setUpdating(true)
      try {
        const { data } = await supabase.from('markets').select('*').gt('current_edge', 0.02).order('current_edge', { ascending: false })
        if (data) setMarkets(data)
        setDataStale(false)
      } catch (e) {
        setDataStale(true)
      }
      setUpdating(false)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const filtered = markets.filter(m => {
    if (filters.sport && !m.sport?.includes(filters.sport)) return false
    if (filters.minEdge && (m.current_edge || 0) * 100 < parseFloat(filters.minEdge)) return false
    return true
  }).map(m => ({
    ...m,
    score: calcScore(m.current_edge, m.current_price_direction, m.current_net_buy_pressure),
  })).sort((a, b) => b.score - a.score)

  const avgEdge = filtered.length > 0 ? filtered.reduce((s, m) => s + (m.current_edge || 0), 0) / filtered.length : 0
  const fallingCount = filtered.filter(m => m.current_price_direction === 'falling').length
  const sports = [...new Set(markets.map(m => m.sport).filter(Boolean))]

  return (
    <Layout>
      {dataStale && (
        <div className="card border-loss border mb-4 flex items-center gap-2">
          <span className="dot dot-red" />
          <span className="text-sm text-loss font-semibold">Supabase connection lost. Showing last known data.</span>
        </div>
      )}
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Live Mispricing Monitor</h1>
        <span className={`text-xs ${updating ? 'text-info' : 'text-neutral'}`}>{updating ? 'updating...' : ''}</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <StatCard title="Active Signals" value={filtered.length} />
        <StatCard title="Avg Edge" value={`${(avgEdge * 100).toFixed(1)}¢`} />
        <StatCard title="Falling Markets" value={fallingCount} color="text-loss" />
        <StatCard title="Unmatched" value={config?.markets_unmatched_count || 0} subtitle="No Odds API data" />
      </div>

      <div className="flex flex-wrap gap-2 mb-4 items-center">
        <select value={filters.sport} onChange={e => setFilters({ ...filters, sport: e.target.value })} className="input w-auto">
          <option value="">All Sports</option>
          {sports.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <input type="number" placeholder="Min edge ¢" value={filters.minEdge} onChange={e => setFilters({ ...filters, minEdge: e.target.value })} className="input w-24" />
      </div>

      {filtered.length === 0 ? (
        <div className="card text-center text-neutral py-8">
          No mispricings detected above 2¢ edge. The bot is monitoring {config?.markets_matched_count || 0} markets.
        </div>
      ) : (
        <div className="table-scroll">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Score</th>
              <th className="text-left text-neutral py-2 px-2">Market</th>
              <th className="text-right text-neutral py-2 px-2">Poly</th>
              <th className="text-right text-neutral py-2 px-2">Sharp</th>
              <th className="text-right text-neutral py-2 px-2">Edge</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Movement</th>
              <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Pressure</th>
              <th className="text-right text-neutral py-2 px-2 hidden lg:table-cell">Match</th>
            </tr></thead>
            <tbody>
              {filtered.map((m, i) => {
                const pressureVal = m.current_net_buy_pressure || 1
                const pressureColor = pressureVal < 0.7 ? 'text-loss' : pressureVal > 1.3 ? 'text-profit' : 'text-neutral'
                const pressureLabel = pressureVal < 0.7 ? 'sell pressure' : pressureVal > 1.3 ? 'buy pressure' : 'neutral'
                return (
                  <tr key={i} className="border-b border-border hover:bg-surface">
                    <td className="py-2 px-2"><ScoreBadge score={m.score} /></td>
                    <td className="py-2 px-2">
                      <div className="min-w-0">
                        <p className="font-semibold truncate">{m.home_team} vs {m.away_team}</p>
                        <p className="text-xs text-neutral"><SportIcon sport={m.sport} showLabel /> {m.tournament_name ? `| ${m.tournament_name}` : ''}</p>
                        {m.is_live ? (
                          <LiveGameState score={m.game_score} period={m.game_period} elapsed={m.game_elapsed} isLive />
                        ) : (
                          <span className="text-xs text-neutral">Pre-game</span>
                        )}
                      </div>
                    </td>
                    <td className="py-2 px-2 text-right">{((m.yes_price || 0) * 100).toFixed(0)}¢</td>
                    <td className="py-2 px-2 text-right">
                      {m.current_sharp_prob ? `${(m.current_sharp_prob * 100).toFixed(0)}¢` : '-'}
                    </td>
                    <td className="py-2 px-2 text-right"><EdgeBadge edge={m.current_edge} /></td>
                    <td className="py-2 px-2 hidden md:table-cell">
                      <DirectionArrow direction={m.current_price_direction} velocity={m.current_price_velocity} />
                    </td>
                    <td className="py-2 px-2 text-right hidden md:table-cell">
                      <span className={`text-sm ${pressureColor}`}>{pressureVal.toFixed(1)}x</span>
                      <p className="text-xs text-neutral">{pressureLabel}</p>
                    </td>
                    <td className="py-2 px-2 text-right hidden lg:table-cell">
                      <span className="text-sm">{m.match_confidence ? `${(m.match_confidence * 100).toFixed(0)}%` : '-'}</span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  )
}
