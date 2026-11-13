import type { ReactNode } from 'react'

interface Props {
  title: string
  /** One line explaining what this panel is for. */
  subtitle?: string
  /** Position in the setup sequence; renders a numbered badge. */
  step?: number
  /** True once the panel's resource exists; the badge turns green. */
  done?: boolean
  children: ReactNode
}

export function Panel({ title, subtitle, step, done = false, children }: Props) {
  return (
    <section className="panel">
      <header className="panel-header">
        {step !== undefined && (
          <span className={done ? 'step-badge done' : 'step-badge'} aria-hidden="true">
            {done ? '✓' : step}
          </span>
        )}
        <div>
          <h3>
            {step !== undefined && <span className="sr-only">Paso {step}: </span>}
            {title}
          </h3>
          {subtitle && <p className="muted">{subtitle}</p>}
        </div>
      </header>
      {children}
    </section>
  )
}
