import { Line } from 'react-chartjs-2'

export default function WinRateChart({ data7d, data30d }) {
  if ((!data7d || data7d.length === 0) && (!data30d || data30d.length === 0)) {
    return <div className="card text-center text-neutral py-8">No win rate data yet</div>
  }
  const labels = (data30d || data7d || []).map(d => d.date)
  const data = {
    labels,
    datasets: [
      ...(data7d ? [{ label: '7-day', data: data7d.map(d => (d.winRate * 100)), borderColor: '#2979ff', borderWidth: 2, pointRadius: 0, fill: false }] : []),
      ...(data30d ? [{ label: '30-day', data: data30d.map(d => (d.winRate * 100)), borderColor: '#ffffff', borderWidth: 2, pointRadius: 0, fill: false }] : []),
    ],
  }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } } },
    scales: {
      x: { ticks: { color: '#888', maxTicksLimit: 10 }, grid: { color: '#2a2a2a' } },
      y: { min: 0, max: 100, ticks: { color: '#888', callback: v => v + '%' }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card"><Line data={data} options={options} /></div>
}
