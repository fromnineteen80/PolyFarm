import { Line } from 'react-chartjs-2'

export default function WalletGrowthChart({ snapshots, floorData }) {
  if (!snapshots || snapshots.length === 0) {
    return <div className="card text-center text-neutral py-8">No wallet data yet</div>
  }
  const data = {
    labels: snapshots.map(s => s.date),
    datasets: [
      {
        label: 'Wallet Value',
        data: snapshots.map(s => parseFloat(s.wallet_value || 0)),
        borderColor: '#ffffff',
        borderWidth: 2,
        fill: false,
        tension: 0.1,
        pointRadius: 0,
      },
      ...(floorData ? [{
        label: 'Floor',
        data: snapshots.map(s => parseFloat(s.floor_value || 0)),
        borderColor: '#ff1744',
        borderWidth: 1,
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      }] : []),
    ],
  }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } }, zoom: { zoom: { drag: { enabled: true }, mode: 'x' } } },
    scales: {
      x: { ticks: { color: '#888', maxTicksLimit: 10 }, grid: { color: '#2a2a2a' } },
      y: { ticks: { color: '#888', callback: v => '$' + v.toLocaleString() }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Line data={data} options={options} /></div>
}
