export default function Icon({ name, size, className }) {
  const sizeClass = size === 'sm' ? 'icon-sm' : size === 'lg' ? 'icon-lg' : ''
  return <span className={`icon ${sizeClass} ${className || ''}`}>{name}</span>
}
