import type { ReactNode } from 'react'

interface Props {
  number: number
  title: string
  hint?: ReactNode
  id?: string
}

/** Numbered heading for the guided flow (1 story, 2 scenario, 3 run). */
export function StepHeading({ number, title, hint, id }: Props) {
  return (
    <header className="sc-step-heading" id={id}>
      <span className="step-badge" aria-hidden="true">
        {number}
      </span>
      <div>
        <h3>
          <span className="sr-only">Paso {number}: </span>
          {title}
        </h3>
        {hint && <p className="muted">{hint}</p>}
      </div>
    </header>
  )
}
