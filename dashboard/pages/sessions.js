import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import Layout from '../components/Layout'
import { formatCurrency } from '../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data } = await sb.from('sessions').select('*').order('start_time', { ascending: false }).limit(200)
  return { props: { session, sessions: data || [] } }
}

export default function Sessions({ sessions }) {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Session History</h1>
      {sessions.length === 0 ? (
        <div className="card text-center text-neutral py-8">No sessions recorded yet</div>
      ) : (
        <div className="table-scroll">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Date</th>
              <th className="text-left text-neutral py-2 px-2">Mode</th>
              <th className="text-right text-neutral py-2 px-2">Start</th>
              <th className="text-right text-neutral py-2 px-2">End</th>
              <th className="text-right text-neutral py-2 px-2">P&L</th>
              <th className="text-right text-neutral py-2 px-2">P&L%</th>
              <th className="text-right text-neutral py-2 px-2">Trades</th>
              <th className="text-right text-neutral py-2 px-2">WR</th>
              <th className="text-left text-neutral py-2 px-2">Lock</th>
            </tr></thead>
            <tbody>
              {sessions.map((s, i) => {
                const pnl = parseFloat(s.session_pnl || 0)
                const pnlPct = parseFloat(s.session_pnl_pct || 0) * 100
                return (
                  <tr key={i} className={`border-b border-border ${s.paper_mode ? 'bg-paper/5' : ''}`}>
                    <td className="py-2 px-2">{s.date}</td>
                    <td className="py-2 px-2"><span className={`px-1.5 py-0.5 rounded text-xs font-bold ${s.paper_mode ? 'bg-paper text-black' : 'bg-live text-black'}`}>{s.paper_mode ? 'PAPER' : 'LIVE'}</span></td>
                    <td className="py-2 px-2 text-right">{formatCurrency(s.start_wallet)}</td>
                    <td className="py-2 px-2 text-right">{formatCurrency(s.end_wallet)}</td>
                    <td className={`py-2 px-2 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                    <td className={`py-2 px-2 text-right ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnlPct >= 0 ? '+' : ''}{pnlPct.toFixed(1)}%</td>
                    <td className="py-2 px-2 text-right">{s.trades_total || 0}</td>
                    <td className="py-2 px-2 text-right">{parseFloat(s.win_rate || 0) * 100 > 0 ? (parseFloat(s.win_rate) * 100).toFixed(0) + '%' : '—'}</td>
                    <td className="py-2 px-2 text-sm">{s.lock_reason || '—'}</td>
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
