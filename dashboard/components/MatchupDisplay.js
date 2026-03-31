import SportIcon from './SportIcon'

export default function MatchupDisplay({ homeTeam, awayTeam, homeColor, awayColor, homeRecord, awayRecord, sport, size }) {
  return (
    <div className="flex items-center gap-2">
      <Team name={homeTeam} color={homeColor} record={homeRecord} sport={sport} size={size} />
      <span className="text-xs text-gray-400 mx-0.5">vs</span>
      <Team name={awayTeam} color={awayColor} record={awayRecord} sport={sport} size={size} />
    </div>
  )
}

function Team({ name, color, record, sport, size }) {
  if (!name) return null
  const bg = color ? `${color}0c` : '#f9fafb'
  const compact = size === 'sm'

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded ${compact ? 'px-2 py-1 text-xs' : 'px-2.5 py-1.5 text-sm'}`}
      style={{ backgroundColor: bg }}
    >
      <SportIcon sport={sport} />
      <span className="font-semibold text-gray-900">{name}</span>
      {record && !compact && <span className="text-gray-400 text-xs ml-0.5">{record}</span>}
    </span>
  )
}

export { Team }
