export default function ScoreBadge({ score }) {
  if (score === null || score === undefined) return null
  const s = Math.round(score)
  let bg = ''
  if (s >= 80) bg = 'bg-profit/30 text-profit'
  else if (s >= 60) bg = 'bg-profit/15 text-profit'
  else if (s >= 40) bg = 'bg-yellow-900/30 text-bandA'
  else if (s >= 20) bg = 'bg-orange-900/30 text-paper'
  else bg = 'text-neutral'
  return <span className={`inline-block px-2 py-0.5 rounded text-sm font-bold ${bg}`}>{s}</span>
}
