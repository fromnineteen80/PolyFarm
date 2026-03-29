import { Bar } from 'react-chartjs-2'

export default function BandPerformanceChart({ bandData }) {
  if (!bandData) return <div className="card text-center text-neutral py-8">No band data yet</div>
  const labels = Object.keys(bandData)
  const data = {
    labels,
    datasets: [
      { label: 'Win Rate %', data: labels.map(b => bandData[b]?.winRate || 0), backgroundColor: '#2979ff', borderRadius: 2 },
      { label: 'Avg P&L $', data: labels.map(b => bandData[b]?.avgPnl || 0), backgroundColor: '#00c853', borderRadius: 2 },
    ],
  }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } } },
    scales: {
      x: { ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
      y: { ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Bar data={data} options={options} /></div>
}
