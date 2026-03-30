export default function BookCount({ books, count }) {
  const n = count || (Array.isArray(books) ? books.length : typeof books === 'string' ? books.split(',').filter(Boolean).length : 0)
  const names = Array.isArray(books) ? books : typeof books === 'string' ? books.split(',').filter(Boolean) : []
  return (
    <span className="text-xs text-neutral" title={names.join(', ')}>
      {n} book{n !== 1 ? 's' : ''}
    </span>
  )
}
