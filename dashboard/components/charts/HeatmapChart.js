import { Chart } from 'react-chartjs-2'

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

export default function HeatmapChart({ trades }) {
  if (!trades || trades.length === 0) {
    return <div className="card text-center text-neutral py-8">No trade timing data yet</div>
  }
  const cells = []
  for (let day = 0; day < 7; day++) {
    for (let hour = 0; hour < 24; hour++) {
      const matching = trades.filter(t => {
        const d = new Date(t.timestamp_entry)
        return d.getDay() === (day + 1) % 7 && d.getHours() === hour
      })
      const wins = matching.filter(t => parseFloat(t.pnl || 0) > 0).length
      const wr = matching.length > 0 ? wins / matching.length : 0
      cells.push({ x: hour, y: day, v: wr, count: matching.length })
    }
  }
  const data = {
    datasets: [{
      label: 'Win Rate',
      data: cells.filter(c => c.count > 0),
      backgroundColor: ctx => {
        const v = ctx.raw?.v || 0
        if (v >= 0.7) return 'rgba(0,200,83,0.8)'
        if (v >= 0.5) return 'rgba(255,152,0,0.6)'
        return 'rgba(255,23,68,0.5)'
      },
      width: ctx => 20,
      height: ctx => 20,
    }],
  }
  const options = {
    responsive: true,
    plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => `WR: ${(ctx.raw.v * 100).toFixed(0)}% (${ctx.raw.count} trades)` } } },
    scales: {
      x: { type: 'linear', min: -0.5, max: 23.5, ticks: { color: '#888', stepSize: 1, callback: v => v + 'h' }, grid: { display: false } },
      y: { type: 'linear', min: -0.5, max: 6.5, ticks: { color: '#888', stepSize: 1, callback: v => DAYS[v] || '' }, grid: { display: false } },
    },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Chart type="matrix" data={data} options={options} /></div>
}
