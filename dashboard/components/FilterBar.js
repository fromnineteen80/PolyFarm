import { useState } from 'react'

export default function FilterBar({ filters, onApply, onReset }) {
  const [values, setValues] = useState(() => {
    const init = {}
    filters?.forEach(f => { init[f.key] = f.default || '' })
    return init
  })

  return (
    <div className="flex flex-wrap gap-2 items-center mb-4">
      {filters?.map(f => (
        <select key={f.key} value={values[f.key]} onChange={e => setValues({ ...values, [f.key]: e.target.value })}
          className="bg-card border border-border rounded px-3 py-2 text-white text-sm min-h-[44px]">
          <option value="">{f.label}: All</option>
          {f.options?.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
      ))}
      <button onClick={() => onApply?.(values)} className="px-3 py-2 bg-info text-white rounded text-sm min-h-[44px]">Apply</button>
      <button onClick={() => { const r = {}; filters?.forEach(f => { r[f.key] = f.default || '' }); setValues(r); onReset?.() }}
        className="px-3 py-2 border border-border text-neutral rounded text-sm min-h-[44px]">Reset</button>
    </div>
  )
}
