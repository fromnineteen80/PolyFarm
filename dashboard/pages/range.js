import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import DateRangePicker from '../components/DateRangePicker'
import TradeTable from '../components/TradeTable'
import DailyPnLChart from '../components/charts/DailyPnLChart'
import ExportButton from '../components/ExportButton'
import { formatCurrency } from '../lib/calculations'
import supabase from '../lib/supabase'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  return { props: { session } }
}

export default function Range() {
  const [trades, setTrades] = useState([])
  const [snapshots, setSnapshots] = useState([])
  const [loading, setLoading] = useState(false)

  const loadRange = async (start, end) => {
    setLoading(true)
    const [tradeRes, snapRes] = await Promise.all([
      supabase.from('trades').select('*').gte('timestamp_entry', start).lte('timestamp_entry', end + 'T23:59:59Z').not('timestamp_exit', 'is', null),
      supabase.from('daily_snapshots').select('*').gte('date', start).lte('date', end).order('date', { ascending: true }),
    ])
    setTrades(tradeRes.data || [])
    setSnapshots(snapRes.data || [])
    setLoading(false)
  }

  const totalPnl = trades.reduce((s, t) => s + parseFloat(t.pnl || 0), 0)
  const wins = trades.filter(t => parseFloat(t.pnl || 0) > 0).length
  const wr = trades.length > 0 ? wins / trades.length * 100 : 0

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Date Range Deep Dive</h1>
      <DateRangePicker onChange={loadRange} />
      {loading && <p className="text-neutral mt-4">Loading...</p>}
      {trades.length > 0 && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 my-4">
            <StatCard title="Total P&L" value={formatCurrency(totalPnl)} color={totalPnl >= 0 ? 'text-profit' : 'text-loss'} />
            <StatCard title="Trades" value={trades.length} />
            <StatCard title="Win Rate" value={`${wr.toFixed(0)}%`} />
            <StatCard title="Avg P&L" value={formatCurrency(totalPnl / trades.length)} />
          </div>
          <DailyPnLChart dailyData={snapshots} />
          <div className="mt-6 flex justify-between items-center mb-3">
            <h2 className="text-lg font-semibold">Trades in Range</h2>
            <ExportButton data={trades} filename="range_trades" />
          </div>
          <TradeTable trades={trades} />
        </>
      )}
      {!loading && trades.length === 0 && <div className="card text-center text-neutral py-8 mt-4">Select a date range and click Apply to analyze.</div>}
    </Layout>
  )
}
