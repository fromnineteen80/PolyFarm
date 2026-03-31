import SportIcon from './SportIcon'

export default function MatchupDisplay({ homeTeam, awayTeam, homeColor, awayColor, homeRecord, awayRecord, sport, size }) {
  return (
    <div className="flex items-center gap-1.5 flex-wrap">
      <Team name={homeTeam} color={homeColor} record={homeRecord} sport={sport} size={size} />
      <span className="text-xs text-gray-400">vs</span>
      <Team name={awayTeam} color={awayColor} record={awayRecord} sport={sport} size={size} />
    </div>
  )
}

function Team({ name, color, record, sport, size }) {
  if (!name) return null
  const compact = size === 'sm'
  // Very subtle team color background wash
  const bg = color ? `${color}08` : 'transparent'

  return (
    <span
      className={`inline-flex items-center gap-1.5 ${compact ? 'px-2 py-0.5 text-xs rounded' : 'px-2.5 py-1 text-sm rounded-md'}`}
      style={{ backgroundColor: bg }}
    >
      <SportIcon sport={sport} />
      <span className="font-semibold text-gray-900">{name}</span>
      {record && !compact && <span className="text-gray-400 text-xs">{record}</span>}
    </span>
  )
}

export { Team }
