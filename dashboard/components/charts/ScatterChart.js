import { Scatter } from 'react-chartjs-2'

const BAND_COLORS = { A: '#ffd700', B: '#c0c0c0', C: '#cd7f32' }

export default function ScatterChart({ trades, xField, yField, xlabel, ylabel, colorByBand }) {
  if (!trades || trades.length === 0) {
    return <div className="card text-center text-neutral py-8">No scatter data yet</div>
  }
  const points = trades.map(t => ({
    x: parseFloat(t[xField] || 0) * 100,
    y: parseFloat(t[yField] || 0) * 100,
    band: t.band,
  }))
  const datasets = colorByBand
    ? Object.keys(BAND_COLORS).map(b => ({
        label: `Band ${b}`,
        data: points.filter(p => p.band === b),
        backgroundColor: BAND_COLORS[b],
        pointRadius: 4,
      }))
    : [{ label: 'Trades', data: points, backgroundColor: '#2979ff', pointRadius: 4 }]

  const data = { datasets }
  const options = {
    responsive: true,
    plugins: { legend: { labels: { color: '#888' } } },
    scales: {
      x: { title: { display: true, text: xlabel || xField, color: '#888' }, ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
      y: { title: { display: true, text: ylabel || yField, color: '#888' }, ticks: { color: '#888' }, grid: { color: '#2a2a2a' } },
    },
  }
  return <div className="card"><Scatter data={data} options={options} /></div>
}
