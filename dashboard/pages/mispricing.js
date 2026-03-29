import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import ScatterChart from '../components/charts/ScatterChart'
import supabase from '../lib/supabase'
import { formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [mapRes, tradeRes, snapRes] = await Promise.all([
    sb.from('market_mappings').select('*'),
    sb.from('trades').select('raw_edge_at_entry,pnl,pnl_pct,band').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(50),
    sb.from('daily_snapshots').select('wallet_value').order('date', { ascending: false }).limit(1),
  ])
  return { props: { session, mappings: mapRes.data || [], recentTrades: tradeRes.data || [], walletValue: parseFloat(snapRes.data?.[0]?.wallet_value || 1000) } }
}

const SPORT_CODES = { basketball_nba: 'NBA', icehockey_nhl: 'NHL', baseball_mlb: 'MLB', basketball_ncaab: 'NCB', americanfootball_nfl: 'NFL', americanfootball_ncaaf: 'NCF', soccer_epl: 'EPL', soccer_usa_mls: 'MLS', soccer_mls: 'MLS', tennis_atp: 'ATP', tennis_wta: 'WTA', mma_mixed_martial_arts: 'MMA', golf_pga_tour: 'PGA' }

export default function Mispricing({ mappings: initial, recentTrades, walletValue }) {
  const [mappings, setMappings] = useState(initial)
  const [filters, setFilters] = useState({ sport: '', minEdge: 0, liveOnly: false, confirmedOnly: false, band: '' })
  const [showFees, setShowFees] = useState(false)

  useEffect(() => {
    const interval = setInterval(async () => {
      const { data } = await supabase.from('market_mappings').select('*')
      if (data) setMappings(data)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  // Build rows with calculated fields
  const rows = mappings.map(m => {
    const polyPrice = parseFloat(m.yes_price || 0)
    const sharpPrice = parseFloat(m.sharp_prob || 0)
    const edge = sharpPrice - polyPrice
    const takerFee = polyPrice * 0.003
    const exitTarget = polyPrice + edge * 0.65
    const rebate = (1 - exitTarget) * 0.002
    const netPct = polyPrice > 0 ? ((edge - takerFee + rebate) / polyPrice) * 100 : 0
    let band = '--'
    if (polyPrice >= 0.70 && edge >= 0.08) band = 'A'
    else if (polyPrice >= 0.60 && edge >= 0.05) band = 'B'
    else if (polyPrice >= 0.55 && edge >= 0.03) band = 'C'
    return { ...m, polyPrice, sharpPrice, edge, takerFee, rebate, netPct, band, belowFloor: polyPrice < 0.55 }
  }).filter(r => {
    if (filters.sport && r.sport !== filters.sport) return false
    if (filters.minEdge && r.edge * 100 < parseFloat(filters.minEdge)) return false
    if (filters.liveOnly && r.mapping_status !== 'LIVE') return false
    if (filters.confirmedOnly && r.mapping_status === 'UNCONFIRMED') return false
    if (filters.band && r.band !== filters.band) return false
    return true
  }).sort((a, b) => b.netPct - a.netPct)

  const qualA = rows.filter(r => r.band === 'A').length
  const qualB = rows.filter(r => r.band === 'B').length
  const qualC = rows.filter(r => r.band === 'C').length
  const avgEdge = rows.filter(r => r.band !== '--').length > 0
    ? rows.filter(r => r.band !== '--').reduce((s, r) => s + r.edge, 0) / rows.filter(r => r.band !== '--').length : 0
  const best = rows.find(r => r.band !== '--')
  const sports = [...new Set(mappings.map(m => m.sport).filter(Boolean))]

  return (
    <Layout>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Live Mispricing Monitor</h1>
        <button onClick={() => window.location.reload()} className="px-3 py-2 border border-border rounded text-sm text-neutral hover:text-white min-h-[44px]">Refresh</button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-2 mb-4">
        <StatCard title="Monitored" value={mappings.length} />
        <StatCard title="Band A" value={qualA} color="text-bandA" />
        <StatCard title="Band B" value={qualB} color="text-bandB" />
        <StatCard title="Band C" value={qualC} color="text-bandC" />
        <StatCard title="Avg Edge" value={`${(avgEdge * 100).toFixed(1)}¢`} />
        <StatCard title="Best" value={best?.teams?.substring(0, 20) || '—'} subtitle={best ? `${(best.edge * 100).toFixed(1)}¢` : ''} />
      </div>

      <div className="flex flex-wrap gap-2 mb-4 items-center">
        <select value={filters.sport} onChange={e => setFilters({ ...filters, sport: e.target.value })} className="bg-card border border-border rounded px-3 py-2 text-white text-sm min-h-[44px]">
          <option value="">All Sports</option>
          {sports.map(s => <option key={s} value={s}>{SPORT_CODES[s] || s}</option>)}
        </select>
        <input type="number" placeholder="Min edge ¢" value={filters.minEdge || ''} onChange={e => setFilters({ ...filters, minEdge: e.target.value })} className="bg-card border border-border rounded px-3 py-2 text-white text-sm w-24 min-h-[44px]" />
        <select value={filters.band} onChange={e => setFilters({ ...filters, band: e.target.value })} className="bg-card border border-border rounded px-3 py-2 text-white text-sm min-h-[44px]">
          <option value="">All Bands</option>
          <option value="A">A</option><option value="B">B</option><option value="C">C</option>
        </select>
        <label className="flex items-center gap-1 text-sm text-neutral min-h-[44px]">
          <input type="checkbox" checked={filters.confirmedOnly} onChange={e => setFilters({ ...filters, confirmedOnly: e.target.checked })} /> Confirmed only
        </label>
      </div>

      {rows.length === 0 ? (
        <div className="card text-center text-neutral py-8 font-financial">No mispricing data available yet</div>
      ) : (
        <div className="table-scroll mb-4">
          <table className="w-full text-xs font-financial">
            <thead><tr className="border-b border-border">
              <th className="text-left py-1.5 px-1.5 text-neutral sticky left-0 bg-background">Market</th>
              <th className="text-left py-1.5 px-1.5 text-neutral">Sport</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Poly¢</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Sharp¢</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Edge¢</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Taker$</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Rebate$</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Net%</th>
              <th className="text-center py-1.5 px-1.5 text-neutral">Band</th>
              <th className="text-right py-1.5 px-1.5 text-neutral">Vol$k</th>
              <th className="text-center py-1.5 px-1.5 text-neutral">Map</th>
            </tr></thead>
            <tbody>
              {rows.map((r, i) => {
                let rowBg = ''
                if (r.belowFloor) rowBg = 'opacity-30 line-through'
                else if (r.netPct >= 8) rowBg = 'bg-profit/20'
                else if (r.netPct >= 5) rowBg = 'bg-profit/10'
                else if (r.netPct >= 3) rowBg = 'bg-yellow-900/20'
                else rowBg = 'opacity-60'
                const bandColor = r.band === 'A' ? 'text-bandA' : r.band === 'B' ? 'text-bandB' : r.band === 'C' ? 'text-bandC' : 'text-neutral'
                return (
                  <tr key={i} className={`border-b border-border ${rowBg}`}>
                    <td className="py-1.5 px-1.5 max-w-[140px] truncate sticky left-0 bg-card">{r.teams || r.polymarket_slug}</td>
                    <td className="py-1.5 px-1.5">{SPORT_CODES[r.sport] || r.sport}</td>
                    <td className="py-1.5 px-1.5 text-right">{(r.polyPrice * 100).toFixed(1)}</td>
                    <td className="py-1.5 px-1.5 text-right">{(r.sharpPrice * 100).toFixed(1)}</td>
                    <td className="py-1.5 px-1.5 text-right">{(r.edge * 100).toFixed(1)}</td>
                    <td className="py-1.5 px-1.5 text-right">${r.takerFee.toFixed(3)}</td>
                    <td className="py-1.5 px-1.5 text-right">${r.rebate.toFixed(3)}</td>
                    <td className={`py-1.5 px-1.5 text-right font-bold ${r.netPct >= 5 ? 'text-profit' : r.netPct >= 3 ? 'text-bandA' : 'text-neutral'}`}>{r.netPct.toFixed(1)}</td>
                    <td className={`py-1.5 px-1.5 text-center font-bold ${bandColor}`}>{r.band}</td>
                    <td className="py-1.5 px-1.5 text-right">{r.volume ? (parseFloat(r.volume) / 1000).toFixed(0) : '—'}</td>
                    <td className={`py-1.5 px-1.5 text-center ${r.mapping_status === 'CONFIRMED' ? 'text-profit' : 'text-bandA'}`}>{r.mapping_status === 'CONFIRMED' ? 'CONF' : r.mapping_status === 'FUZZY' ? 'FUZZ' : '—'}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      <p className="text-xs text-neutral mb-2">Net% = ((Edge x Shares) - Taker Fee + Maker Rebate) / Position Size. Calculated at Band position size for ${formatCurrency(walletValue)} portfolio.</p>

      <button onClick={() => setShowFees(!showFees)} className="text-xs text-info hover:underline mb-4 min-h-[44px]">{showFees ? 'Hide' : 'Show'} fee explanation</button>
      {showFees && (
        <div className="card text-xs text-neutral mb-4">
          <p>Taker fee: 0.30% of entry notional</p>
          <p>Maker rebate: 0.20% of exit notional</p>
          <p>Example: $30 Band A position at 65¢ entry</p>
          <p>Taker: $0.09 | Target: 70.2¢ | Rebate: $0.03 | Net profit: $2.33</p>
        </div>
      )}

      {recentTrades.length > 0 && (
        <>
          <h2 className="text-lg font-semibold mb-3">Capture Rate (Last 50 Trades)</h2>
          <ScatterChart trades={recentTrades} xField="raw_edge_at_entry" yField="pnl_pct" xlabel="Entry Edge %" ylabel="P&L Captured %" colorByBand />
        </>
      )}
    </Layout>
  )
}
