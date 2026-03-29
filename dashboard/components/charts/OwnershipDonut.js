import { Doughnut } from 'react-chartjs-2'
import { formatCurrency } from '../../lib/calculations'

export default function OwnershipDonut({ investors, walletValue }) {
  if (!investors || investors.length === 0) {
    return <div className="card text-center text-neutral py-8">No investors yet</div>
  }
  const totalUnits = investors.reduce((s, i) => s + parseFloat(i.units_held || 0), 0)
  const data = {
    labels: investors.map(i => `${i.first_name} ${i.last_name}`),
    datasets: [{
      data: investors.map(i => parseFloat(i.units_held || 0)),
      backgroundColor: ['#2979ff', '#00c853', '#ffd700', '#ff9800', '#9c27b0', '#ff1744', '#607d8b', '#e91e63'],
      borderWidth: 0,
    }],
  }
  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'right', labels: { color: '#888', boxWidth: 12 } },
      tooltip: {
        callbacks: {
          label: ctx => {
            const units = ctx.raw
            const pct = totalUnits > 0 ? (units / totalUnits * 100).toFixed(1) : 0
            const val = totalUnits > 0 ? (units / totalUnits * (walletValue || 0)) : 0
            return `${pct}% — ${formatCurrency(val)}`
          }
        }
      }
    },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Doughnut data={data} options={options} /></div>
}
