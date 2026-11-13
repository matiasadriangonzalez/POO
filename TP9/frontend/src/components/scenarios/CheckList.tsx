import type { Check } from '../../scenarios'

export function CheckList({ checks }: { checks: readonly Check[] }) {
  if (checks.length === 0) return null
  return (
    <ul className="sc-checks">
      {checks.map((check, i) => (
        <li key={i} className={check.passed ? 'pass' : 'fail'}>
          <span className="sc-check-mark" aria-hidden="true">
            {check.passed ? '✓' : '✕'}
          </span>
          <div>
            <p>
              <span className="sr-only">{check.passed ? 'Cumple: ' : 'No cumple: '}</span>
              {check.label}
            </p>
            <p className="sc-expected">
              Esperado: <code>{check.expected}</code> · Obtenido: <code>{check.actual}</code>
            </p>
          </div>
        </li>
      ))}
    </ul>
  )
}
