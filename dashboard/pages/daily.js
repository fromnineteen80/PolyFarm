import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import DateRangePicker from '../components/DateRangePicker'
import DailyPnLChart from '../components/charts/DailyPnLChart'
import WalletGrowthChart from '../components/charts/WalletGrowthChart'
import ExportButton from '../components/ExportButton'
import { formatCurrency } from '../lib/calculations'
import { useState } from 'react'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data } = await sb.from('daily_snapshots').select('*').order('date', { ascending: true })
  return { props: { session, snapshots: data || [] } }
}

export default function Daily({ snapshots }) {
  const [range, setRange] = useState({ start: null, end: null })
  const filtered = snapshots.filter(s => {
    if (range.start && s.date < range.start) return false
    if (range.end && s.date > range.end) return false
    return true
  })

  const totalPnl = filtered.reduce((s, d) => s + parseFloat(d.session_pnl || 0), 0)
  const avgPnl = filtered.length > 0 ? totalPnl / filtered.length : 0
  const bestDay = filtered.reduce((b, d) => parseFloat(d.session_pnl || 0) > b ? parseFloat(d.session_pnl || 0) : b, -Infinity)
  const worstDay = filtered.reduce((w, d) => parseFloat(d.session_pnl || 0) < w ? parseFloat(d.session_pnl || 0) : w, Infinity)
  const profDays = filtered.filter(d => parseFloat(d.session_pnl || 0) > 0).length
  const negDays = filtered.filter(d => parseFloat(d.session_pnl || 0) < 0).length

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Daily Results</h1>
      <DateRangePicker onChange={(s, e) => setRange({ start: s, end: e })} />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 my-4">
        <StatCard title="Total P&L" value={formatCurrency(totalPnl)} color={totalPnl >= 0 ? 'text-profit' : 'text-loss'} />
        <StatCard title="Avg Daily" value={formatCurrency(avgPnl)} />
        <StatCard title="Best Day" value={formatCurrency(bestDay === -Infinity ? 0 : bestDay)} color="text-profit" />
        <StatCard title="Worst Day" value={formatCurrency(worstDay === Infinity ? 0 : worstDay)} color="text-loss" />
        <StatCard title="Profitable Days" value={profDays} />
        <StatCard title="Negative Days" value={negDays} />
        <StatCard title="Win Rate" value={filtered.length > 0 ? `${(profDays / filtered.length * 100).toFixed(0)}%` : '0%'} />
        <StatCard title="Total Days" value={filtered.length} />
      </div>
      <div className="grid md:grid-cols-1 gap-4 mb-6">
        <DailyPnLChart dailyData={filtered} />
        <WalletGrowthChart snapshots={filtered} floorData />
      </div>
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold">Daily Detail</h2>
        <ExportButton data={filtered} filename="daily_results" />
      </div>
      <div className="table-scroll">
        <table className="w-full text-sm">
          <thead><tr className="border-b border-border">
            <th className="text-left text-neutral py-2 px-2">Date</th>
            <th className="text-right text-neutral py-2 px-2">Wallet</th>
            <th className="text-right text-neutral py-2 px-2">P&L</th>
            <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Floor</th>
            <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Trades</th>
          </tr></thead>
          <tbody>
            {[...filtered].reverse().map((d, i) => {
              const pnl = parseFloat(d.session_pnl || 0)
              return (
                <tr key={i} className="border-b border-border">
                  <td className="py-2 px-2">{d.date}</td>
                  <td className="py-2 px-2 text-right">{formatCurrency(d.wallet_value)}</td>
                  <td className={`py-2 px-2 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                  <td className="py-2 px-2 text-right hidden md:table-cell">{formatCurrency(d.floor_value)}</td>
                  <td className="py-2 px-2 text-right hidden md:table-cell">{d.trades_today || 0}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </Layout>
  )
}
