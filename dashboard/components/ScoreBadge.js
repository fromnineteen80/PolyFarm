export default function ScoreBadge({ score }) {
  if (score === null || score === undefined) return null
  const s = Math.round(score)
  let classes = 'bg-gray-100 text-gray-500'
  if (s >= 80) classes = 'bg-green-100 text-green-700'
  else if (s >= 60) classes = 'bg-green-50 text-green-600'
  else if (s >= 40) classes = 'bg-amber-50 text-amber-600'
  else if (s >= 20) classes = 'bg-orange-50 text-orange-600'
  return <span className={`inline-flex items-center justify-center w-10 h-10 rounded-lg text-sm font-bold ${classes}`}>{s}</span>
}
