import { Doughnut } from 'react-chartjs-2'

const EXIT_COLORS = {
  reprice: '#00c853', profit_lock: '#ffd700', trailing_stop: '#2979ff',
  timeout: '#ff9800', resolution: '#9c27b0', stop_loss: '#ff1744',
  drain: '#607d8b', emergency: '#d50000', fade_deficit_closed: '#ff6d00',
  other: '#888888',
}

export default function ExitTypeChart({ exitCounts }) {
  if (!exitCounts || Object.keys(exitCounts).length === 0) {
    return <div className="card text-center text-neutral py-8">No exit data yet</div>
  }
  const labels = Object.keys(exitCounts)
  const data = {
    labels,
    datasets: [{
      data: labels.map(l => exitCounts[l]),
      backgroundColor: labels.map(l => EXIT_COLORS[l] || EXIT_COLORS.other),
      borderWidth: 0,
    }],
  }
  const options = {
    responsive: true,
    plugins: { legend: { position: 'right', labels: { color: '#888', boxWidth: 12, padding: 8 } } },
  }
  return <div className="card min-h-[200px] max-h-[400px] lg:max-h-none"><Doughnut data={data} options={options} /></div>
}
