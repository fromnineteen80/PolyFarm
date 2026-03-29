import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState } from 'react'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import ExportButton from '../components/ExportButton'
import OwnershipDonut from '../components/charts/OwnershipDonut'
import OwnershipAreaChart from '../components/charts/OwnershipAreaChart'
import { formatCurrency, calcOwnershipPct, calcInvestorValue } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [invRes, evtRes, cfgRes, snapRes] = await Promise.all([
    sb.from('investors').select('*').eq('is_active', true),
    sb.from('capital_events').select('*').order('timestamp', { ascending: false }),
    sb.from('bot_config').select('*'),
    sb.from('daily_snapshots').select('wallet_value').order('date', { ascending: false }).limit(1),
  ])
  const cfg = {}; cfgRes.data?.forEach(r => { cfg[r.key] = r.value })
  return { props: { session, investors: invRes.data || [], events: evtRes.data || [], config: cfg, walletValue: parseFloat(snapRes.data?.[0]?.wallet_value || 0) } }
}

export default function Investors({ investors, events, config, walletValue }) {
  const [form, setForm] = useState({ first_name: '', last_name: '', email: '', event_type: 'initial', date: new Date().toISOString().split('T')[0], amount: '', notes: '' })
  const [submitting, setSubmitting] = useState(false)
  const [msg, setMsg] = useState('')

  const totalUnits = parseFloat(config?.total_units_outstanding || 0)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true); setMsg('')
    const res = await fetch('/api/capital-event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
    const data = await res.json()
    setSubmitting(false)
    if (data.success) { setMsg('Capital event recorded.'); setForm({ ...form, amount: '', notes: '' }) }
    else setMsg(data.error || 'Error')
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Capital Management</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
        <StatCard title="Portfolio Value" value={formatCurrency(walletValue)} />
        <StatCard title="Total Units" value={totalUnits.toFixed(2)} />
        <StatCard title="Investors" value={investors.length} />
      </div>
      <div className="grid md:grid-cols-2 gap-4 mb-6">
        <OwnershipDonut investors={investors} walletValue={walletValue} />
        <OwnershipAreaChart events={events} investors={investors} />
      </div>

      <h2 className="text-lg font-semibold mb-3">Add Capital Event</h2>
      <form onSubmit={handleSubmit} className="card mb-6 grid md:grid-cols-3 gap-3">
        <input placeholder="First Name" required value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]" />
        <input placeholder="Last Name" required value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]" />
        <input placeholder="Email (optional)" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]" />
        <select value={form.event_type} onChange={e => setForm({ ...form, event_type: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]">
          <option value="initial">Initial Deposit</option>
          <option value="additional">Additional Deposit</option>
          <option value="withdrawal">Withdrawal</option>
        </select>
        <input type="date" value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]" />
        <input type="number" step="0.01" placeholder="Amount" required value={form.amount} onChange={e => setForm({ ...form, amount: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px]" />
        <input placeholder="Notes" value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} className="bg-surface border border-border rounded px-3 py-2 text-white min-h-[44px] md:col-span-2" />
        <button type="submit" disabled={submitting} className="bg-info text-white rounded py-2 min-h-[44px]">{submitting ? 'Saving...' : 'Add Event'}</button>
        {msg && <p className="text-sm text-neutral md:col-span-3">{msg}</p>}
      </form>

      <h2 className="text-lg font-semibold mb-3">Investor Portfolio</h2>
      {investors.length === 0 ? <div className="card text-center text-neutral py-8">No investors yet</div> : (
        <div className="table-scroll mb-6">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Investor</th>
              <th className="text-right text-neutral py-2 px-2">Units</th>
              <th className="text-right text-neutral py-2 px-2">Ownership</th>
              <th className="text-right text-neutral py-2 px-2">Value</th>
            </tr></thead>
            <tbody>
              {investors.map((inv, i) => {
                const units = parseFloat(inv.units_held || 0)
                const pct = calcOwnershipPct(units, totalUnits)
                const val = calcInvestorValue(units, totalUnits, walletValue)
                return (
                  <tr key={i} className="border-b border-border">
                    <td className="py-2 px-2">{inv.first_name} {inv.last_name}</td>
                    <td className="py-2 px-2 text-right font-financial">{units.toFixed(2)}</td>
                    <td className="py-2 px-2 text-right font-financial">{pct.toFixed(1)}%</td>
                    <td className="py-2 px-2 text-right font-financial">{formatCurrency(val)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold">Capital History</h2>
        <ExportButton data={events} filename="capital_events" />
      </div>
      <div className="table-scroll">
        <table className="w-full text-sm">
          <thead><tr className="border-b border-border">
            <th className="text-left text-neutral py-2 px-2">Date</th>
            <th className="text-left text-neutral py-2 px-2">Investor</th>
            <th className="text-left text-neutral py-2 px-2">Type</th>
            <th className="text-right text-neutral py-2 px-2">Amount</th>
            <th className="text-right text-neutral py-2 px-2">Units</th>
            <th className="text-right text-neutral py-2 px-2">Ownership</th>
          </tr></thead>
          <tbody>
            {events.map((e, i) => (
              <tr key={i} className="border-b border-border">
                <td className="py-2 px-2">{e.date}</td>
                <td className="py-2 px-2">{e.first_name} {e.last_name}</td>
                <td className="py-2 px-2">{e.event_type}</td>
                <td className="py-2 px-2 text-right font-financial">{formatCurrency(e.amount)}</td>
                <td className="py-2 px-2 text-right font-financial">{parseFloat(e.units_assigned || 0).toFixed(2)}</td>
                <td className="py-2 px-2 text-right font-financial">{parseFloat(e.ownership_pct_after || 0).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  )
}
