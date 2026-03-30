import { useState } from 'react'
import { formatCurrency } from '../lib/calculations'
import Icon from './Icon'

const STRATEGY_MAP = { oracle_arb: 'strategy-oracle', normal: 'strategy-oracle', exception: 'strategy-exception', fade: 'strategy-fade', overnight: 'strategy-overnight' }

function SortIcon({ active, dir }) {
  if (!active) return null
  return <Icon name={dir === 1 ? 'arrow_upward' : 'arrow_downward'} size="sm" />
}

export default function TradeTable({ trades }) {
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

  const TH = ({ k, label, hide }) => (
    <th onClick={() => toggleSort(k)} className={`text-left text-neutral py-2 px-2 cursor-pointer hover:text-white whitespace-nowrap ${hide || ''}`}>
      <span className="inline-flex items-center gap-1">{label} <SortIcon active={sortKey === k} dir={sortDir} /></span>
    </th>
  )

  return (
    <div>
      <div className="table-scroll">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <TH k="market_slug" label="Market" />
              <TH k="pnl" label="P&L" />
              <TH k="exit_type" label="Exit" />
              <TH k="timestamp_entry" label="Date" hide="hidden md:table-cell" />
              <TH k="sport" label="Sport" hide="hidden md:table-cell" />
              <TH k="position_type" label="Strategy" hide="hidden md:table-cell" />
              <TH k="band" label="Band" hide="hidden md:table-cell" />
              <TH k="edge_at_entry" label="Edge" hide="hidden lg:table-cell" />
              <TH k="price_direction_at_entry" label="Dir" hide="hidden lg:table-cell" />
              <TH k="entry_price" label="Entry" hide="hidden lg:table-cell" />
              <TH k="exit_price" label="Exit Price" hide="hidden lg:table-cell" />
              <TH k="hold_duration_seconds" label="Hold" hide="hidden lg:table-cell" />
            </tr>
          </thead>
          <tbody>
            {paged.map((t, i) => {
              const pnl = parseFloat(t.pnl || 0)
              const stratClass = STRATEGY_MAP[t.position_type] || ''
              return (
                <tr key={i} className="border-b border-border hover:bg-surface">
                  <td className="py-2 px-2 max-w-[150px] truncate">{t.market_slug}</td>
                  <td className={`py-2 px-2 ${pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{pnl >= 0 ? '+' : ''}{formatCurrency(pnl)}</td>
                  <td className="py-2 px-2">{t.exit_type || '-'}</td>
                  <td className="py-2 px-2 whitespace-nowrap hidden md:table-cell">{t.timestamp_entry?.split('T')[0]}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{t.sport}</td>
                  <td className={`py-2 px-2 hidden md:table-cell ${stratClass}`}>{t.position_type}</td>
                  <td className="py-2 px-2 hidden md:table-cell">{t.band}</td>
                  <td className={`py-2 px-2 hidden lg:table-cell ${parseFloat(t.edge_at_entry || 0) > 0 ? 'text-profit' : ''}`}>{t.edge_at_entry ? `+${(parseFloat(t.edge_at_entry) * 100).toFixed(1)}¢` : '-'}</td>
                  <td className="py-2 px-2 hidden lg:table-cell text-xs">{t.price_direction_at_entry === 'falling' ? '↓' : t.price_direction_at_entry === 'rising' ? '↑' : '→'}</td>
                  <td className="py-2 px-2 hidden lg:table-cell">{parseFloat(t.entry_price || 0).toFixed(4)}</td>
                  <td className="py-2 px-2 hidden lg:table-cell">{t.exit_price ? parseFloat(t.exit_price).toFixed(4) : '-'}</td>
                  <td className="py-2 px-2 hidden lg:table-cell">{t.hold_duration_seconds ? Math.round(t.hold_duration_seconds / 60) + 'm' : '-'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center mt-3">
        <span className="text-sm text-neutral">{sorted.length} trades</span>
        <div className="flex gap-2">
          <button disabled={page === 0} onClick={() => setPage(page - 1)} className="btn btn-outline"><Icon name="chevron_left" size="sm" /> Prev</button>
          <span className="text-sm text-neutral py-2">{page + 1}/{totalPages}</span>
          <button disabled={page >= totalPages - 1} onClick={() => setPage(page + 1)} className="btn btn-outline">Next <Icon name="chevron_right" size="sm" /></button>
        </div>
      </div>
    </div>
  )
}
