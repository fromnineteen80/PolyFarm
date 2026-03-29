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
      <input type="date" value={start} onChange={e => setStart(e.target.value)} className="input w-auto" />
      <span className="text-neutral">to</span>
      <input type="date" value={end} onChange={e => setEnd(e.target.value)} className="input w-auto" />
      <button onClick={() => onChange?.(start, end)} className="btn btn-primary">Apply</button>
      <div className="flex gap-1">
        {[7, 30, 90].map(d => (
          <button key={d} onClick={() => quickSelect(d)} className="btn btn-outline">{d}d</button>
        ))}
        <button onClick={() => quickSelect('all')} className="btn btn-outline">All</button>
      </div>
    </div>
  )
}
