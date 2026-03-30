export default function LiveGameState({ score, period, elapsed, isLive }) {
  if (!isLive) return null
  return (
    <span className="inline-flex items-center gap-1 text-xs">
      <span className="w-1.5 h-1.5 rounded-full bg-loss animate-pulse" />
      {score && <span className="font-semibold">{score}</span>}
      {period && <span className="text-neutral">| {period}</span>}
      {elapsed && <span className="text-neutral">| {elapsed}</span>}
    </span>
  )
}
