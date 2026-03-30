export default function TeamColor({ name, color, size }) {
  if (!color) return <span className={size === 'sm' ? 'text-sm' : ''}>{name}</span>
  return (
    <span className={size === 'sm' ? 'text-sm' : ''}>
      <span className="inline-block w-2 h-2 rounded-full mr-1.5" style={{ backgroundColor: color }} />
      {name}
    </span>
  )
}
