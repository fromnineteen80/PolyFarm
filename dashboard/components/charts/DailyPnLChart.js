import { Bar } from 'react-chartjs-2'

export default function DailyPnLChart({ dailyData }) {
  if (!dailyData || dailyData.length === 0) {
    return <div className="card text-center text-neutral py-8">No daily P&L data yet</div>
  }
  const data = {
    labels: dailyData.map(d => d.date),
    datasets: [{
      label: 'Daily P&L',
      data: dailyData.map(d => parseFloat(d.pnl || d.session_pnl || 0)),
      backgroundColor: dailyData.map(d => parseFloat(d.pnl || d.session_pnl || 0) >= 0 ? '#00c853' : '#ff1744'),
      borderRadius: 2,
    }],
  }
  const options = {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: '#888', maxTicksLimit: 10 }, grid: { color: '#2a2a2a' } },
      y: { ticks: { color: '#888', callback: v => '$' + v }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card"><Bar data={data} options={options} /></div>
}
