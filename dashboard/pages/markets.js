import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import SportIcon from '../components/SportIcon'
import FilterBar from '../components/FilterBar'
import EdgeBadge from '../components/EdgeBadge'
import DirectionArrow from '../components/DirectionArrow'
import LiveGameState from '../components/LiveGameState'
import supabase from '../lib/supabase'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data } = await sb.from('markets').select('*').order('volume', { ascending: false })
  return { props: { session, markets: data || [] } }
}

export default function Markets({ markets: initial }) {
  const [markets, setMarkets] = useState(initial)
  const [filters, setFilters] = useState({ sport: '', status: '', reference: '', sort: 'volume' })

  useEffect(() => {
    const interval = setInterval(async () => {
      const { data } = await supabase.from('markets').select('*').order('volume', { ascending: false })
      if (data) setMarkets(data)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const filtered = markets.filter(m => {
    if (filters.sport && !m.sport?.includes(filters.sport)) return false
    if (filters.status === 'live' && !m.is_live) return false
    if (filters.status === 'pregame' && m.is_live) return false
    if (filters.reference === 'sharp' && !m.current_sharp_prob) return false
    if (filters.reference === 'nosharp' && m.current_sharp_prob) return false
    return true
  }).sort((a, b) => {
    if (filters.sort === 'edge') return (b.current_edge || 0) - (a.current_edge || 0)
    if (filters.sort === 'start') return (a.game_start_time || '').localeCompare(b.game_start_time || '')
    return (b.volume || 0) - (a.volume || 0)
  })

  const sports = [...new Set(markets.map(m => m.sport).filter(Boolean))]

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Market Intelligence</h1>
      <div className="flex flex-wrap gap-2 mb-4 items-center">
        <select value={filters.sport} onChange={e => setFilters({ ...filters, sport: e.target.value })} className="input w-auto">
          <option value="">All Sports</option>
          {sports.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <select value={filters.status} onChange={e => setFilters({ ...filters, status: e.target.value })} className="input w-auto">
          <option value="">All Status</option>
          <option value="live">Live</option>
          <option value="pregame">Pre-game</option>
        </select>
        <select value={filters.reference} onChange={e => setFilters({ ...filters, reference: e.target.value })} className="input w-auto">
          <option value="">All</option>
          <option value="sharp">Has sharp ref</option>
          <option value="nosharp">No sharp ref</option>
        </select>
        <select value={filters.sort} onChange={e => setFilters({ ...filters, sort: e.target.value })} className="input w-auto">
          <option value="volume">Sort: Volume</option>
          <option value="edge">Sort: Edge</option>
          <option value="start">Sort: Start time</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <div className="card text-center text-neutral py-8">No markets found</div>
      ) : (
        <div className="table-scroll">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Market</th>
              <th className="text-right text-neutral py-2 px-2">Price</th>
              <th className="text-right text-neutral py-2 px-2">Edge</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Status</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Movement</th>
              <th className="text-right text-neutral py-2 px-2 hidden lg:table-cell">Volume</th>
            </tr></thead>
            <tbody>
              {filtered.map((m, i) => (
                <tr key={i} className="border-b border-border hover:bg-surface">
                  <td className="py-2 px-2">
                    <div className="max-w-[200px]">
                      <p className="font-semibold truncate">{m.home_team || 'Unknown'} vs {m.away_team || 'Unknown'}</p>
                      <p className="text-xs text-neutral">
                        {m.home_record && <span>{m.home_record}</span>}
                        {m.home_record && m.away_record && ' / '}
                        {m.away_record && <span>{m.away_record}</span>}
                      </p>
                      <p className="text-xs text-neutral"><SportIcon sport={m.sport} showLabel /> {m.tournament_name ? `| ${m.tournament_name}` : ''}</p>
                    </div>
                  </td>
                  <td className="py-2 px-2 text-right">
                    <span>{((m.yes_price || 0) * 100).toFixed(0)}¢</span>
                    {m.current_sharp_prob ? (
                      <p className="text-xs text-neutral">Sharp: {(m.current_sharp_prob * 100).toFixed(0)}¢</p>
                    ) : (
                      <p className="text-xs text-neutral">No reference</p>
                    )}
                  </td>
                  <td className="py-2 px-2 text-right">
                    {m.current_edge ? <EdgeBadge edge={m.current_edge} size="sm" /> : <span className="text-neutral">-</span>}
                  </td>
                  <td className="py-2 px-2 hidden md:table-cell">
                    {m.is_live ? (
                      <LiveGameState score={m.game_score} period={m.game_period} elapsed={m.game_elapsed} isLive />
                    ) : (
                      <span className="text-xs text-neutral">{m.game_start_time ? new Date(m.game_start_time).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) : 'TBD'}</span>
                    )}
                  </td>
                  <td className="py-2 px-2 hidden md:table-cell">
                    {m.current_price_direction ? (
                      <DirectionArrow direction={m.current_price_direction} velocity={m.current_price_velocity} />
                    ) : <span className="text-neutral">-</span>}
                  </td>
                  <td className="py-2 px-2 text-right hidden lg:table-cell">{m.volume ? `$${(m.volume / 1000).toFixed(0)}k` : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  )
}
