import type { Scenario } from '../../scenarios'
import type { ScenarioRun } from '../../hooks/useScenarioRunner'
import { CheckList } from './CheckList'
import { StepLog } from './StepLog'
import { VerdictBadge } from './VerdictBadge'

interface Props {
  scenario: Scenario
  run?: ScenarioRun
  /** Opens the Puerta tab with this code ready to scan. */
  onOpenGate: (code: string) => void
}

/** Body of step 3: verdict, what the app did, and the expected-vs-obtained checks. */
export function ResultPanel({ scenario, run, onOpenGate }: Props) {
  if (!scenario.automatable) return null
  if (!run) {
    return (
      <div className="sc-empty">
        <p>
          <strong>Todavía no ejecutaste este escenario.</strong>
        </p>
        <p className="muted">Apretá "Ejecutar escenario": vas a ver qué hace la app paso a paso y si el resultado cumple.</p>
      </div>
    )
  }

  const result = run.result
  const finished = run.phase === 'done'
  const passed = result?.passed ?? false

  return (
    <div className="sc-result" aria-busy={!finished}>
      <div className="sc-result-head" role="status" aria-live="polite">
        {finished ? (
          <>
            <VerdictBadge passed={passed} />
            <p className="sc-verdict-note">
              {passed
                ? 'El backend respondió lo que se esperaba.'
                : 'El backend respondió algo distinto a lo esperado. Revisá las comprobaciones.'}
            </p>
          </>
        ) : (
          <span className="sc-verdict run">{run.phase === 'queued' ? 'En cola…' : 'Ejecutando…'}</span>
        )}
      </div>

      <h4>Qué hizo la app</h4>
      {run.steps.length === 0 ? <p className="muted">Esperando el primer paso…</p> : <StepLog steps={run.steps} />}

      {result && (
        <>
          <h4>Esperado y obtenido</h4>
          <CheckList checks={result.checks} />
          {result.qrs.length > 0 && (
            <>
              <h4>Entradas emitidas</h4>
              <ul className="sc-qrs">
                {result.qrs.map((entrada) => (
                  <li key={entrada.id}>
                    <code>{entrada.codigo_qr}</code>
                    <button type="button" className="secondary" onClick={() => onOpenGate(entrada.codigo_qr)}>
                      Abrir en Puerta con este QR
                    </button>
                  </li>
                ))}
              </ul>
              <p className="muted">También quedan en "Última compra" de la pestaña Puerta.</p>
            </>
          )}
        </>
      )}
    </div>
  )
}
