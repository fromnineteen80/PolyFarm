import { exportToCSV } from '../lib/csv'
import Icon from './Icon'

export default function ExportButton({ data, filename, label }) {
  return (
    <button
      onClick={() => exportToCSV(data, filename || 'export')}
      className="btn btn-export"
    >
      <Icon name="download" size="sm" />
      {label || 'Export CSV'}
    </button>
  )
}
