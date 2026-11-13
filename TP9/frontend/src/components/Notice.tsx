import type { ReactNode } from 'react'

type Tone = 'info' | 'warn' | 'success'

/** Inline banner for hints, prerequisites and positive feedback. Errors use ErrorMessage. */
export function Notice({ tone = 'info', children }: { tone?: Tone; children: ReactNode }) {
  return (
    <p className={`notice ${tone}`} role={tone === 'success' ? 'status' : undefined}>
      {children}
    </p>
  )
}
