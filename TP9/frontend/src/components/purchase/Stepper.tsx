const STEPS = ['Selección', 'Pago', 'Entradas']

/** `current` is 1-based. */
export function Stepper({ current }: { current: number }) {
  return (
    <ol className="stepper" aria-label="Pasos de la compra">
      {STEPS.map((label, index) => {
        const number = index + 1
        const state = number < current ? 'done' : number === current ? 'current' : 'todo'
        return (
          <li key={label} className={`step ${state}`} aria-current={state === 'current' ? 'step' : undefined}>
            <span className="step-number">{number}</span>
            {label}
          </li>
        )
      })}
    </ol>
  )
}
