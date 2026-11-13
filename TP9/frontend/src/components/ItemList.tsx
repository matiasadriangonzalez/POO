import type { ReactNode } from 'react'
import { ErrorMessage } from './ErrorMessage'

interface Props<T extends { id: number }> {
  items: T[]
  loading: boolean
  error: string | null
  empty: string
  render: (item: T) => ReactNode
}

export function ItemList<T extends { id: number }>({ items, loading, error, empty, render }: Props<T>) {
  return (
    <div className="list-wrap">
      <ErrorMessage message={error} />
      {loading && items.length === 0 ? (
        <p className="empty">Cargando…</p>
      ) : items.length === 0 ? (
        <p className="empty">{empty}</p>
      ) : (
        <ul className="list">
          {items.map((item) => (
            <li key={item.id}>
              <span className="badge">#{item.id}</span>
              <div>{render(item)}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
