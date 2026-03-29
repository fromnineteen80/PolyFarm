import { Scatter, Line } from 'react-chartjs-2'

export default function CalibrationCurve({ trades }) {
  if (!trades || trades.length === 0) {
    return <div className="card text-center text-neutral py-8">No calibration data yet</div>
  }
  const resolved = trades.filter(t => t.resolution_outcome && t.sharp_prob_at_entry)
  if (resolved.length < 5) {
    return <div className="card text-center text-neutral py-8">Need more resolved trades for calibration</div>
  }
  const bins = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
  const points = []
  for (let i = 0; i < bins.length - 1; i++) {
    const inBin = resolved.filter(t => {
      const p = parseFloat(t.sharp_prob_at_entry)
      return p >= bins[i] && p < bins[i + 1]
    })
    if (inBin.length >= 2) {
      const wins = inBin.filter(t => t.resolution_outcome === 'win').length
      points.push({ x: (bins[i] + bins[i + 1]) / 2 * 100, y: wins / inBin.length * 100 })
    }
  }
  const data = {
    datasets: [
      { label: 'Perfect Calibration', data: [{ x: 50, y: 50 }, { x: 100, y: 100 }], type: 'line', borderColor: '#888', borderDash: [5, 5], borderWidth: 1, pointRadius: 0 },
      { label: 'Actual', data: points, backgroundColor: '#2979ff', pointRadius: 6, showLine: true, borderColor: '#2979ff', borderWidth: 2 },
    ],
  }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } } },
    scales: {
      x: { min: 50, max: 100, title: { display: true, text: 'Sharp Prob %', color: '#888' }, ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
      y: { min: 0, max: 100, title: { display: true, text: 'Actual Win Rate %', color: '#888' }, ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card"><Scatter data={data} options={options} /></div>
}
