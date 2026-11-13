import type { Step } from '../../scenarios'

const pretty = (value: unknown): string => (typeof value === 'string' ? value : JSON.stringify(value, null, 2))

function StepItem({ step, index }: { step: Step; index: number }) {
  const pending = step.status === undefined
  const tone = pending ? 'run' : step.ok ? 'pass' : 'fail'
  return (
    <li className="sc-step">
      <span className="sc-step-index" aria-hidden="true">
        {index}
      </span>
      <div className="sc-step-body">
        <p className="sc-step-title">
          {step.label}
          {step.request && (
            <code className="sc-req">
              {step.request.method} {step.request.path}
            </code>
          )}
          <span className={`sc-status ${tone}`}>{pending ? '…' : step.status === 0 ? 'sin conexión' : step.status}</span>
        </p>
        {step.request && (
          <details className="sc-json">
            <summary>Solicitud y respuesta</summary>
            {step.request.body !== undefined && (
              <>
                <h5>Solicitud</h5>
                <pre>{pretty(step.request.body)}</pre>
              </>
            )}
            <h5>Respuesta</h5>
            <pre>{step.response === undefined ? '(sin cuerpo)' : pretty(step.response)}</pre>
          </details>
        )}
      </div>
    </li>
  )
}

/** Live log of the steps: the scenario's own calls first-class, data preparation collapsed. */
export function StepLog({ steps }: { steps: readonly Step[] }) {
  const prep = steps.filter((step) => step.setup)
  const actions = steps.filter((step) => !step.setup)
  return (
    <div>
      {prep.length > 0 && (
        <details className="sc-prep">
          <summary>
            Preparación de datos ({prep.length} {prep.length === 1 ? 'paso' : 'pasos'})
          </summary>
          <ol className="sc-steps">
            {prep.map((step, i) => (
              <StepItem key={i} step={step} index={i + 1} />
            ))}
          </ol>
        </details>
      )}
      <ol className="sc-steps">
        {actions.map((step, i) => (
          <StepItem key={i} step={step} index={i + 1} />
        ))}
      </ol>
    </div>
  )
}
