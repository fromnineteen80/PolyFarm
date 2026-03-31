import SportIcon from './SportIcon'
import LiveGameState from './LiveGameState'

export default function MatchupDisplay({ homeTeam, awayTeam, homeColor, awayColor, homeRecord, awayRecord, sport, isLive, gameScore, gamePeriod, gameTime, size }) {
  const compact = size === 'sm'

  return (
    <div className={compact ? '' : ''}>
      <div className="flex items-center gap-1.5">
        <TeamPill name={homeTeam} color={homeColor} record={homeRecord} compact={compact} />
        <span className="text-xs text-neutral">vs</span>
        <TeamPill name={awayTeam} color={awayColor} record={awayRecord} compact={compact} />
        <SportIcon sport={sport} />
      </div>
      <div className="flex items-center gap-2 mt-1">
        {isLive ? (
          <LiveGameState score={gameScore} period={gamePeriod} isLive />
        ) : gameTime ? (
          <span className="text-xs text-neutral">{new Date(gameTime).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}</span>
        ) : null}
      </div>
    </div>
  )
}

function TeamPill({ name, color, record, compact }) {
  if (!name) return null
  const bg = color ? `${color}18` : '#2a2a2a'
  const border = color || '#2a2a2a'

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border ${compact ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-sm'}`}
      style={{
        borderColor: border,
        backgroundColor: bg,
      }}
    >
      {color && <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />}
      <span className="font-medium">{name}</span>
      {record && <span className="text-neutral text-xs">{record}</span>}
    </span>
  )
}

export { TeamPill }
