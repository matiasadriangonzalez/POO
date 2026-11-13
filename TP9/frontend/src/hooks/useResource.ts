import { useCallback, useEffect, useState } from 'react'

export interface Resource<T> {
  data: T[]
  loading: boolean
  error: string | null
  reload: () => void
}

/** Loads a list on mount and exposes `reload` to refetch it after a mutation. */
export function useResource<T>(fetcher: () => Promise<T[]>): Resource<T> {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [version, setVersion] = useState(0)

  useEffect(() => {
    let cancelled = false
    fetcher()
      .then((items) => {
        if (cancelled) return
        setData(items)
        setError(null)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Error inesperado')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [fetcher, version])

  const reload = useCallback(() => setVersion((v) => v + 1), [])

  return { data, loading, error, reload }
}
