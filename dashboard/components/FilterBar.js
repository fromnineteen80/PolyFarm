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
          className="input w-auto">
          <option value="">{f.label}: All</option>
          {f.options?.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
      ))}
      <button onClick={() => onApply?.(values)} className="btn btn-primary">Apply</button>
      <button onClick={() => { const r = {}; filters?.forEach(f => { r[f.key] = f.default || '' }); setValues(r); onReset?.() }}
        className="btn btn-outline">Reset</button>
    </div>
  )
}
