import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import DateRangePicker from '../components/DateRangePicker'
import TradeTable from '../components/TradeTable'
import ExportButton from '../components/ExportButton'
import BandPerformanceChart from '../components/charts/BandPerformanceChart'
import ScatterChart from '../components/charts/ScatterChart'
import ExitTypeChart from '../components/charts/ExitTypeChart'
import { formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data: trades } = await sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_entry', { ascending: false })
  return { props: { session, trades: trades || [] } }
}

export default function Bands({ trades }) {
  const [bandFilter, setBandFilter] = useState('All')
  const filtered = bandFilter === 'All' ? trades : trades.filter(t => t.band === bandFilter)

  const bandStats = {}
  for (const band of ['A', 'B', 'C']) {
    const bt = trades.filter(t => t.band === band)
    const wins = bt.filter(t => parseFloat(t.pnl || 0) > 0).length
    const totalPnl = bt.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
    bandStats[band] = {
      trades: bt.length, wins, winRate: bt.length > 0 ? wins / bt.length * 100 : 0,
      totalPnl, avgPnl: bt.length > 0 ? totalPnl / bt.length : 0,
      avgEdge: bt.length > 0 ? bt.reduce((s, t) => s + parseFloat(t.raw_edge_at_entry || 0), 0) / bt.length : 0,
      avgHold: bt.length > 0 ? bt.reduce((s, t) => s + parseInt(t.hold_duration_seconds || 0), 0) / bt.length / 60 : 0,
    }
  }

  const exitCounts = {}
  filtered.forEach(t => { const e = t.exit_type || 'other'; exitCounts[e] = (exitCounts[e] || 0) + 1 })

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Band Performance</h1>
      <div className="flex gap-2 mb-4">
        {['All', 'A', 'B', 'C'].map(b => (
          <button key={b} onClick={() => setBandFilter(b)}
            className={`btn ${bandFilter === b ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>{b === 'All' ? 'All Bands' : `Band ${b}`}</button>
        ))}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {['A', 'B', 'C'].map(b => (
          <StatCard key={b} title={`Band ${b}`} value={`${bandStats[b].winRate.toFixed(0)}% WR`}
            subtitle={`${bandStats[b].trades} trades | ${formatCurrency(bandStats[b].totalPnl)}`} />
        ))}
        <StatCard title="Combined" value={`${filtered.length} trades`}
          subtitle={formatCurrency(filtered.reduce((s, t) => s + parseFloat(t.pnl || 0), 0))} />
      </div>
      <div className="grid lg:grid-cols-2 gap-4 mb-6">
        <BandPerformanceChart bandData={bandStats} />
        <ExitTypeChart exitCounts={exitCounts} />
      </div>
      <ScatterChart trades={filtered} xField="raw_edge_at_entry" yField="pnl_pct" xlabel="Edge at Entry %" ylabel="P&L %" colorByBand />
      <div className="mt-6">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-lg font-semibold">Band Trades</h2>
          <ExportButton data={filtered} filename="band_trades" />
        </div>
        <TradeTable trades={filtered} />
      </div>
    </Layout>
  )
}
