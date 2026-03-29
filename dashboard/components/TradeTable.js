import { useState } from 'react'
import { formatCurrency } from '../lib/calculations'

const STRATEGY_COLORS = { oracle_arb: 'text-profit', normal: 'text-profit', exception: 'text-bandA', fade: 'text-orange-500', overnight: 'text-info' }

export default function TradeTable({ trades, showFilters, onExport }) {
  const [page, setPage] = useState(0)
  const [sortKey, setSortKey] = useState('timestamp_entry')
  const [sortDir, setSortDir] = useState(-1)
  const perPage = 50

  if (!trades || trades.length === 0) {
    return <div className="card text-center text-neutral py-8">No trades yet</div>
  }

  const sorted = [...trades].sort((a, b) => {
    const av = a[sortKey], bv = b[sortKey]
    if (av == null) return 1
    if (bv == null) return -1
    return av > bv ? sortDir : av < bv ? -sortDir : 0
  })

  const paged = sorted.slice(page * perPage, (page + 1) * perPage)
  const totalPages = Math.ceil(sorted.length / perPage)

  const toggleSort = (key) => {
    if (sortKey === key) setSortDir(-sortDir)
    else { setSortKey(key); setSortDir(-1) }
  }

  const cols = [
    { key: 'timestamp_entry', label: 'Date' },
    { key: 'market_slug', label: 'Market' },
    { key: 'sport', label: 'Sport' },
    { key: 'position_type', label: 'Strategy' },
    { key: 'band', label: 'Band' },
    { key: 'entry_price', label: 'Entry' },
    { key: 'exit_price', label: 'Exit' },
    { key: 'pnl', label: 'P&L' },
    { key: 'exit_type', label: 'Exit Type' },
    { key: 'hold_duration_seconds', label: 'Hold' },
  ]

  return (
    <div>
      <div className="table-scroll">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              {cols.map(c => (
                <th key={c.key} onClick={() => toggleSort(c.key)}
                  className="text-left text-neutral py-2 px-2 cursor-pointer hover:text-white whitespace-nowrap">
                  {c.label} {sortKey === c.key ? (sortDir === 1 ? '▲' : '▼') : ''}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((t, i) => {
              const pnl = parseFloat(t.pnl || 0)
              const stratColor = STRATEGY_COLORS[t.position_type] || ''
              return (
                <tr key={i} className="border-b border-border hover:bg-surface">
                  <td className="py-2 px-2 whitespace-nowrap sticky left-0 bg-card">{t.timestamp_entry?.split('T')[0]}</td>
                  <td className="py-2 px-2 max-w-[150px] truncate">{t.market_slug}</td>
                  <td className="py-2 px-2">{t.sport}</td>
                  <td className={`py-2 px-2 ${stratColor}`}>{t.position_type}</td>
                  <td className="py-2 px-2">{t.band}</td>
                  <td className="py-2 px-2">{parseFloat(t.entry_price || 0).toFixed(4)}</td>
                  <td className="py-2 px-2">{t.exit_price ? parseFloat(t.exit_price).toFixed(4) : '—'}</td>
                  <td className={`py-2 px-2 ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                  <td className="py-2 px-2">{t.exit_type || '—'}</td>
                  <td className="py-2 px-2">{t.hold_duration_seconds ? Math.round(t.hold_duration_seconds / 60) + 'm' : '—'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center mt-3">
        <span className="text-sm text-neutral">{sorted.length} trades</span>
        <div className="flex gap-2">
          <button disabled={page === 0} onClick={() => setPage(page - 1)} className="px-3 py-1 border border-border rounded text-sm disabled:opacity-30 min-h-[44px]">Prev</button>
          <span className="text-sm text-neutral py-2">{page + 1}/{totalPages}</span>
          <button disabled={page >= totalPages - 1} onClick={() => setPage(page + 1)} className="px-3 py-1 border border-border rounded text-sm disabled:opacity-30 min-h-[44px]">Next</button>
        </div>
      </div>
    </div>
  )
}
