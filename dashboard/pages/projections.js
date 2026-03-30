import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import ProjectionChart from '../components/charts/ProjectionChart'
import { calcProjectionSeries, calcProjection, formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [snapRes, cfgRes] = await Promise.all([
    sb.from('daily_snapshots').select('*').order('date', { ascending: true }),
    sb.from('bot_config').select('*'),
  ])
  const cfg = {}; cfgRes.data?.forEach(r => { cfg[r.key] = r.value })
  return { props: { session, snapshots: snapRes.data || [], config: cfg } }
}

export default function Projections({ snapshots, config }) {
  const firstDate = config?.first_live_trade_date
  const firstValue = parseFloat(config?.first_live_wallet_value || 0)

  if (!firstDate) {
    const completed = parseInt(config?.paper_trades_completed || 0)
    return (
      <Layout>
        <h1 className="text-2xl font-bold mb-4">Growth vs Actual</h1>
        <div className="card text-center py-12 text-neutral">
          <p className="text-lg mb-2">Projections appear after first live trade.</p>
          <p>Currently in paper mode: {completed}/300 trades.</p>
        </div>
      </Layout>
    )
  }

  const actual = snapshots.filter(s => s.date >= firstDate).map(s => ({ date: s.date, value: parseFloat(s.wallet_value || 0) }))
  const endDate = actual.length > 0 ? actual[actual.length - 1].date : undefined
  const proj1 = calcProjectionSeries(firstValue, firstDate, 0.01, endDate)
  const proj15 = calcProjectionSeries(firstValue, firstDate, 0.015, endDate)
  const proj2 = calcProjectionSeries(firstValue, firstDate, 0.02, endDate)

  const currentValue = actual.length > 0 ? actual[actual.length - 1].value : firstValue
  const days = actual.length || 1
  const actualRate = days > 1 ? (Math.pow(currentValue / firstValue, 1 / days) - 1) : 0
  const diff = actualRate - 0.015

  let trackingBadge = { text: 'ON TRACK', color: 'text-bandA' }
  if (diff > 0.002) trackingBadge = { text: `ABOVE BASE CASE +${(diff * 100).toFixed(2)}%/day`, color: 'text-profit' }
  else if (diff < -0.002) trackingBadge = { text: `BELOW BASE CASE ${(diff * 100).toFixed(2)}%/day`, color: 'text-loss' }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Growth vs Actual</h1>
      <div className={`text-sm font-semibold mb-4 ${trackingBadge.color}`}>{trackingBadge.text}</div>
      <ProjectionChart actual={actual} proj1={proj1} proj15={proj15} proj2={proj2} phase2Date={config?.phase2_activation_date} />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-4">
        <StatCard title="Actual Today" value={formatCurrency(currentValue)} />
        <StatCard title="1.0% Target" value={formatCurrency(calcProjection(firstValue, firstDate, 0.01))} />
        <StatCard title="1.5% Target" value={formatCurrency(calcProjection(firstValue, firstDate, 0.015))} />
        <StatCard title="2.0% Target" value={formatCurrency(calcProjection(firstValue, firstDate, 0.02))} />
        <StatCard title="Days Running" value={days} />
        <StatCard title="Avg Daily Rate" value={`${(actualRate * 100).toFixed(3)}%`} />
      </div>
    </Layout>
  )
}
