import Icon from './Icon'

export default function EdgeBadge({ edge, size }) {
  if (edge === null || edge === undefined) return null
  const cents = (edge * 100).toFixed(1)
  const isPositive = edge >= 0
  const color = isPositive ? 'text-profit' : 'text-loss'
  const textSize = size === 'sm' ? 'text-xs' : 'text-sm'
  return <span className={`${color} ${textSize} font-semibold`}>{isPositive ? '+' : ''}{cents}¢</span>
}
