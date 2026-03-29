import { Line } from 'react-chartjs-2'

export default function OwnershipAreaChart({ events, investors }) {
  if (!events || events.length === 0) {
    return <div className="card text-center text-neutral py-8">No capital history yet</div>
  }
  const COLORS = ['#2979ff', '#00c853', '#ffd700', '#ff9800', '#9c27b0']
  const names = [...new Set(events.map(e => `${e.first_name} ${e.last_name}`))]
  const dates = [...new Set(events.map(e => e.date))].sort()
  const datasets = names.map((name, i) => ({
    label: name,
    data: dates.map(d => {
      const evts = events.filter(e => `${e.first_name} ${e.last_name}` === name && e.date <= d)
      return evts.reduce((s, e) => s + (e.event_type === 'withdrawal' ? -parseFloat(e.amount || 0) : parseFloat(e.amount || 0)), 0)
    }),
    backgroundColor: COLORS[i % COLORS.length] + '40',
    borderColor: COLORS[i % COLORS.length],
    fill: true,
    pointRadius: 0,
  }))
  const data = { labels: dates, datasets }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } } },
    scales: {
      x: { ticks: { color: '#888', maxTicksLimit: 10 }, grid: { color: '#2a2a2a' } },
      y: { stacked: true, ticks: { color: '#888', callback: v => '$' + v }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Line data={data} options={options} /></div>
}
