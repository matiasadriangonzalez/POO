import { useCallback, useState } from 'react'
import type { EntradaPago } from '../types'

const STORAGE_KEY = 'smartticket.lastPurchase'

function read(): EntradaPago[] {
  try {
    const parsed: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]')
    return Array.isArray(parsed) ? (parsed as EntradaPago[]) : []
  } catch {
    return []
  }
}

/** Remembers the tickets of the last purchase so the gate screen can offer them as shortcuts. */
export function useLastPurchase() {
  const [entradas, setEntradas] = useState<EntradaPago[]>(read)

  const save = useCallback((next: EntradaPago[]) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
    setEntradas(next)
  }, [])

  return { entradas, save }
}
