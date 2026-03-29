import Icon from './Icon'

export default function StatCard({ title, value, subtitle, trend, color }) {
  const trendColor = trend > 0 ? 'text-profit' : trend < 0 ? 'text-loss' : 'text-neutral'
  return (
    <div className="card">
      <p className="text-sm text-neutral">{title}</p>
      <p className={`text-2xl font-bold ${color || ''}`}>
        {value ?? '$0.00'}
      </p>
      {subtitle && <p className="text-sm text-neutral mt-1">{subtitle}</p>}
      {trend !== undefined && trend !== null && (
        <p className={`text-sm mt-1 ${trendColor} flex items-center gap-1`}>
          {trend > 0 ? <Icon name="arrow_upward" size="sm" /> : trend < 0 ? <Icon name="arrow_downward" size="sm" /> : <Icon name="remove" size="sm" />}
          {typeof trend === 'number' ? Math.abs(trend).toFixed(2) + '%' : trend}
        </p>
      )}
    </div>
  )
}
