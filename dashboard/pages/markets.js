import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import EdgeBadge from '../components/EdgeBadge'
import DirectionArrow from '../components/DirectionArrow'
import LiveGameState from '../components/LiveGameState'
import SportIcon, { SPORT_LABELS } from '../components/SportIcon'
import supabase from '../lib/supabase'

const SPORT_FILTER_OPTIONS = [
  { key: 'basketball_nba', label: 'NBA' },
  { key: 'basketball_ncaab', label: 'NCAAB' },
  { key: 'americanfootball_nfl', label: 'NFL' },
  { key: 'americanfootball_ncaaf', label: 'NCAAF' },
  { key: 'baseball_mlb', label: 'MLB' },
  { key: 'icehockey_nhl', label: 'NHL' },
  { key: 'soccer_epl', label: 'EPL' },
  { key: 'soccer_usa_mls', label: 'MLS' },
]

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session?.user) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  let data = []
  try {
    const res = await sb.from('markets').select('*').order('game_start_time', { ascending: true })
    data = res.data || []
  } catch (e) {}
  return { props: { session: JSON.parse(JSON.stringify(session)), markets: data } }
}

export default function Markets({ markets: initial }) {
  const [markets, setMarkets] = useState(initial)
  const [sportFilter, setSportFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [sortBy, setSortBy] = useState('time')
  const [dataStale, setDataStale] = useState(false)

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const { data } = await supabase.from('markets').select('*').order('game_start_time', { ascending: true })
        if (data) setMarkets(data)
        setDataStale(false)
      } catch (e) {
        setDataStale(true)
      }
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const filtered = markets.filter(m => {
    if (sportFilter && m.sport !== sportFilter) return false
    if (statusFilter === 'live' && !m.is_live) return false
    if (statusFilter === 'upcoming' && m.is_live) return false
    return true
  }).sort((a, b) => {
    if (sortBy === 'edge') return (b.current_edge || 0) - (a.current_edge || 0)
    return (a.game_start_time || '').localeCompare(b.game_start_time || '')
  })

  return (
    <Layout>
      {dataStale && (
        <div className="card border-loss border mb-4 flex items-center gap-2">
          <span className="dot dot-red" />
          <span className="text-sm text-loss font-semibold">Connection lost. Showing last known data.</span>
        </div>
      )}
      <h1 className="text-2xl font-bold mb-4">Markets</h1>

      <div className="flex flex-wrap gap-2 mb-4">
        <button onClick={() => setSportFilter('')} className={`btn ${!sportFilter ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>All</button>
        {SPORT_FILTER_OPTIONS.map(s => (
          <button key={s.key} onClick={() => setSportFilter(s.key)} className={`btn ${sportFilter === s.key ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>
            <SportIcon sport={s.key} /> {s.label}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        <button onClick={() => setStatusFilter('')} className={`btn ${!statusFilter ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>All Games</button>
        <button onClick={() => setStatusFilter('live')} className={`btn ${statusFilter === 'live' ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>Live</button>
        <button onClick={() => setStatusFilter('upcoming')} className={`btn ${statusFilter === 'upcoming' ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>Upcoming</button>
        <span className="text-border self-center">|</span>
        <button onClick={() => setSortBy('time')} className={`btn ${sortBy === 'time' ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>By Time</button>
        <button onClick={() => setSortBy('edge')} className={`btn ${sortBy === 'edge' ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>By Edge</button>
      </div>

      {filtered.length === 0 ? (
        <div className="card text-center text-neutral py-8">No markets found</div>
      ) : (
        <div className="space-y-3">
          {filtered.map((m, i) => (
            <div key={i} className="card flex flex-col md:flex-row md:items-center gap-3">
              <div className="flex-1 min-w-0">
                <p className="font-semibold">{m.home_team || 'TBD'} vs {m.away_team || 'TBD'}</p>
                <div className="flex items-center gap-2 text-xs text-neutral mt-1">
                  <SportIcon sport={m.sport} showLabel />
                  {m.home_record && <span>{m.home_record}</span>}
                  {m.home_record && m.away_record && <span>/</span>}
                  {m.away_record && <span>{m.away_record}</span>}
                </div>
              </div>

              <div className="flex flex-wrap gap-4 items-center text-sm">
                <div className="text-center">
                  <p className="text-xs text-neutral">Polymarket</p>
                  <p className="font-semibold">{((m.yes_price || 0) * 100).toFixed(0)}c</p>
                </div>

                {m.current_sharp_prob ? (
                  <div className="text-center">
                    <p className="text-xs text-neutral">Consensus</p>
                    <p className="font-semibold">{(m.current_sharp_prob * 100).toFixed(0)}c</p>
                  </div>
                ) : (
                  <div className="text-center">
                    <p className="text-xs text-neutral">Consensus</p>
                    <p className="text-neutral">--</p>
                  </div>
                )}

                <div className="text-center">
                  <p className="text-xs text-neutral">Edge</p>
                  {m.current_edge ? <EdgeBadge edge={m.current_edge} /> : <span className="text-neutral">--</span>}
                </div>

                <div className="text-center">
                  <p className="text-xs text-neutral">Movement</p>
                  {m.current_price_direction ? (
                    <DirectionArrow direction={m.current_price_direction} velocity={m.current_price_velocity} />
                  ) : <span className="text-neutral">--</span>}
                </div>

                <div className="text-center min-w-[100px]">
                  {m.is_live ? (
                    <LiveGameState score={m.game_score} period={m.game_period} elapsed={m.game_elapsed} isLive />
                  ) : (
                    <p className="text-xs text-neutral">{m.game_start_time ? new Date(m.game_start_time).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) : 'TBD'}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}
