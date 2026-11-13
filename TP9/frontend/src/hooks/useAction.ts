import { useCallback, useState } from 'react'

/** Wraps an async action with busy/error state. `run` resolves to the result or undefined on failure. */
export function useAction() {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = useCallback(async <T,>(action: () => Promise<T>): Promise<T | undefined> => {
    setBusy(true)
    setError(null)
    try {
      return await action()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error inesperado')
      return undefined
    } finally {
      setBusy(false)
    }
  }, [])

  const clearError = useCallback(() => setError(null), [])

  return { busy, error, run, clearError }
}
