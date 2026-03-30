import Icon from './Icon'

const CONFIG = {
  falling: { icon: 'south', color: 'text-loss', label: 'Falling' },
  stable: { icon: 'east', color: 'text-neutral', label: 'Stable' },
  rising: { icon: 'north', color: 'text-profit', label: 'Rising' },
}

export default function DirectionArrow({ direction, velocity }) {
  const cfg = CONFIG[direction] || CONFIG.stable
  const velStr = velocity ? `${velocity > 0 ? '+' : ''}${(velocity).toFixed(1)}¢/min` : ''
  return (
    <span className={`inline-flex items-center gap-1 ${cfg.color}`}>
      <Icon name={cfg.icon} size="sm" />
      <span className="text-xs">{cfg.label}</span>
      {velStr && <span className="text-xs text-neutral">{velStr}</span>}
    </span>
  )
}
