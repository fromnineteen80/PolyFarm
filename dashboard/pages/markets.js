import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import FilterBar from '../components/FilterBar'
import supabase from '../lib/supabase'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data } = await sb.from('market_mappings').select('*').order('mapping_confidence', { ascending: false })
  return { props: { session, mappings: data || [] } }
}

export default function Markets({ mappings: initial }) {
  const [mappings, setMappings] = useState(initial)
  const [filters, setFilters] = useState({})

  useEffect(() => {
    const interval = setInterval(async () => {
      const { data } = await supabase.from('market_mappings').select('*').order('mapping_confidence', { ascending: false })
      if (data) setMappings(data)
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const filtered = mappings.filter(m => {
    if (filters.sport && m.sport !== filters.sport) return false
    if (filters.status && m.mapping_status !== filters.status) return false
    return true
  })
  const sports = [...new Set(mappings.map(m => m.sport).filter(Boolean))]
  const unmapped = mappings.filter(m => m.mapping_status === 'UNCONFIRMED')

  const retryMapping = async (slug) => {
    await fetch('/api/retry-mapping', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ marketSlug: slug }) })
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Market Intelligence</h1>
      <FilterBar
        filters={[
          { key: 'sport', label: 'Sport', options: sports },
          { key: 'status', label: 'Status', options: ['CONFIRMED', 'FUZZY', 'UNCONFIRMED'] },
        ]}
        onApply={setFilters} onReset={() => setFilters({})}
      />
      {filtered.length === 0 ? (
        <div className="card text-center text-neutral py-8">No market mappings yet</div>
      ) : (
        <div className="table-scroll mb-6">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-border">
              <th className="text-left text-neutral py-2 px-2">Market</th>
              <th className="text-left text-neutral py-2 px-2">Status</th>
              <th className="text-right text-neutral py-2 px-2">Confidence</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Sport</th>
              <th className="text-left text-neutral py-2 px-2 hidden md:table-cell">Type</th>
              <th className="text-left text-neutral py-2 px-2 hidden lg:table-cell">Teams</th>
            </tr></thead>
            <tbody>
              {filtered.map((m, i) => {
                const statusColor = m.mapping_status === 'CONFIRMED' ? 'text-profit' : m.mapping_status === 'FUZZY' ? 'text-bandA' : 'text-loss'
                return (
                  <tr key={i} className="border-b border-border">
                    <td className="py-2 px-2 max-w-[150px] truncate">{m.polymarket_slug}</td>
                    <td className={`py-2 px-2 ${statusColor}`}>{m.mapping_status}</td>
                    <td className="py-2 px-2 text-right">{(parseFloat(m.mapping_confidence || 0) * 100).toFixed(0)}%</td>
                    <td className="py-2 px-2 hidden md:table-cell">{m.sport}</td>
                    <td className="py-2 px-2 hidden md:table-cell">{m.market_type}</td>
                    <td className="py-2 px-2 hidden lg:table-cell">{m.teams}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {unmapped.length > 0 && (
        <>
          <h2 className="text-lg font-semibold mb-3">Unmapped Markets ({unmapped.length})</h2>
          <div className="table-scroll">
            <table className="w-full text-sm">
              <thead><tr className="border-b border-border">
                <th className="text-left text-neutral py-2 px-2">Market</th>
                <th className="text-left text-neutral py-2 px-2">Reason</th>
                <th className="text-left text-neutral py-2 px-2">Action</th>
              </tr></thead>
              <tbody>
                {unmapped.map((m, i) => (
                  <tr key={i} className="border-b border-border">
                    <td className="py-2 px-2">{m.polymarket_slug}</td>
                    <td className="py-2 px-2 text-neutral">{m.failure_reason || 'Unknown'}</td>
                    <td className="py-2 px-2">
                      <button onClick={() => retryMapping(m.polymarket_slug)} className="text-info text-sm hover:underline min-h-[44px]">Retry</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </Layout>
  )
}
