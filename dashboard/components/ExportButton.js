import { exportToCSV } from '../lib/csv'

export default function ExportButton({ data, filename, label }) {
  return (
    <button
      onClick={() => exportToCSV(data, filename || 'export')}
      className="px-4 py-2 bg-card border border-border rounded text-white text-sm hover:bg-surface transition min-h-[44px]"
    >
      {label || 'Export CSV'}
    </button>
  )
}
