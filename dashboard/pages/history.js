import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import FilterBar from '../components/FilterBar'
import TradeTable from '../components/TradeTable'
import ExportButton from '../components/ExportButton'
import { formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data } = await sb.from('trades').select('*').not('timestamp_exit', 'is', null).order('timestamp_exit', { ascending: false }).limit(2000)
  return { props: { session, trades: data || [] } }
}

export default function History({ trades }) {
  const [filters, setFilters] = useState({})
  const filtered = trades.filter(t => {
    if (filters.sport && t.sport !== filters.sport) return false
    if (filters.band && t.band !== filters.band) return false
    if (filters.exit_type && t.exit_type !== filters.exit_type) return false
    if (filters.strategy && t.position_type !== filters.strategy) return false
    return true
  })
  const totalPnl = filtered.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
  const wins = filtered.filter(t => parseFloat(t.pnl || 0) > 0).length

  const sports = [...new Set(trades.map(t => t.sport).filter(Boolean))]
  const exitTypes = [...new Set(trades.map(t => t.exit_type).filter(Boolean))]

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Trade History</h1>
      <FilterBar
        filters={[
          { key: 'sport', label: 'Sport', options: sports },
          { key: 'band', label: 'Band', options: ['A', 'B', 'C', 'EX', 'FADE'] },
          { key: 'exit_type', label: 'Exit Type', options: exitTypes },
          { key: 'strategy', label: 'Strategy', options: ['normal', 'exception', 'fade', 'overnight'] },
        ]}
        onApply={setFilters} onReset={() => setFilters({})}
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        <StatCard title="Total P&L" value={formatCurrency(totalPnl)} color={totalPnl >= 0 ? 'text-profit' : 'text-loss'} />
        <StatCard title="Trades" value={filtered.length} />
        <StatCard title="Win Rate" value={filtered.length > 0 ? `${(wins / filtered.length * 100).toFixed(0)}%` : '0%'} />
        <StatCard title="Avg P&L" value={formatCurrency(filtered.length > 0 ? totalPnl / filtered.length : 0)} />
      </div>
      <div className="flex justify-end mb-3">
        <ExportButton data={filtered} filename="trade_history" />
      </div>
      <TradeTable trades={filtered} />
    </Layout>
  )
}
