import { useState } from 'react'
import { subDays, format } from 'date-fns'

export default function DateRangePicker({ startDate, endDate, onChange }) {
  const [start, setStart] = useState(startDate || format(subDays(new Date(), 30), 'yyyy-MM-dd'))
  const [end, setEnd] = useState(endDate || format(new Date(), 'yyyy-MM-dd'))

  const quickSelect = (days) => {
    const s = days === 'all' ? '2024-01-01' : format(subDays(new Date(), days), 'yyyy-MM-dd')
    const e = format(new Date(), 'yyyy-MM-dd')
    setStart(s)
    setEnd(e)
    onChange?.(s, e)
  }

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <input type="date" value={start} onChange={e => setStart(e.target.value)}
        className="bg-card border border-border rounded px-3 py-2 text-white text-sm min-h-[44px]" />
      <span className="text-neutral">to</span>
      <input type="date" value={end} onChange={e => setEnd(e.target.value)}
        className="bg-card border border-border rounded px-3 py-2 text-white text-sm min-h-[44px]" />
      <button onClick={() => onChange?.(start, end)} className="px-3 py-2 bg-info text-white rounded text-sm min-h-[44px]">Apply</button>
      <div className="flex gap-1">
        {[7, 30, 90].map(d => (
          <button key={d} onClick={() => quickSelect(d)} className="px-2 py-1 text-sm text-neutral hover:text-white border border-border rounded min-h-[44px]">{d}d</button>
        ))}
        <button onClick={() => quickSelect('all')} className="px-2 py-1 text-sm text-neutral hover:text-white border border-border rounded min-h-[44px]">All</button>
      </div>
    </div>
  )
}
