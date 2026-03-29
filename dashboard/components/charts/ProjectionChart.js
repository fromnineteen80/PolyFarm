import { Line } from 'react-chartjs-2'
import { useState } from 'react'

export default function ProjectionChart({ actual, proj1, proj15, proj2, phase2Date }) {
  const [logScale, setLogScale] = useState(false)
  if (!actual || actual.length === 0) {
    return <div className="card text-center text-neutral py-8">No projection data yet</div>
  }
  const labels = actual.map(d => d.date)
  const data = {
    labels,
    datasets: [
      { label: '1.0%/day', data: proj1?.map(d => d.value) || [], borderColor: '#888', borderDash: [5, 5], borderWidth: 1, pointRadius: 0, fill: false },
      { label: '1.5%/day', data: proj15?.map(d => d.value) || [], borderColor: '#2979ff', borderDash: [5, 5], borderWidth: 1, pointRadius: 0, fill: false },
      { label: '2.0%/day', data: proj2?.map(d => d.value) || [], borderColor: '#00c853', borderDash: [5, 5], borderWidth: 1, pointRadius: 0, fill: false },
      { label: 'Actual', data: actual.map(d => d.value), borderColor: '#ffffff', borderWidth: 3, pointRadius: 0, fill: false },
    ],
  }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } }, zoom: { zoom: { drag: { enabled: true }, mode: 'x' } } },
    scales: {
      x: { ticks: { color: '#888', maxTicksLimit: 10 }, grid: { color: '#2a2a2a' } },
      y: { type: logScale ? 'logarithmic' : 'linear', ticks: { color: '#888', callback: v => '$' + v.toLocaleString() }, grid: { color: '#2a2a2a' } },
    },
  }
  return (
    <div className="card">
      <div className="flex justify-end mb-2">
        <button onClick={() => setLogScale(!logScale)} className="text-sm text-info px-3 py-1 border border-border rounded">
          {logScale ? 'Linear' : 'Log'} Scale
        </button>
      </div>
      <Line data={data} options={options} />
    </div>
  )
}
