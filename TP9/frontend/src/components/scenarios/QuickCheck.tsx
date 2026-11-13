import { HUS, SCENARIOS, type HuId, type Scenario } from '../../scenarios'
import type { RunSummary, ScenarioRun } from '../../hooks/useScenarioRunner'
import { statusOf } from './scenarioStatus'

interface Props {
  busy: boolean
  summary: RunSummary
  runs: Readonly<Record<string, ScenarioRun>>
  onRun: (hu?: HuId) => void
  /** Opens one scenario (story, scenario and result) in the guided flow above. */
  onOpen: (scenario: Scenario) => void
}

/** Secondary block: run every scenario in a row and list which ones comply. */
export function QuickCheck({ busy, summary, runs, onRun, onOpen }: Props) {
  const automatable = SCENARIOS.filter((scenario) => scenario.automatable)
  return (
    <section className="card sc-quick" aria-labelledby="sc-quick-title">
      <h3 id="sc-quick-title">Verificación rápida: ejecutar todos los escenarios</h3>
      <p className="muted">
        Corre los {summary.total} escenarios seguidos y marca cuáles cumplen. Sirve para chequear que todo anda; tarda un rato y
        crea varios eventos de demostración.
      </p>
      <div className="sc-quick-actions">
        <button type="button" className="secondary" onClick={() => onRun()} disabled={busy}>
          {busy ? 'Ejecutando…' : `Ejecutar los ${summary.total} escenarios`}
        </button>
        {HUS.map((hu) => (
          <button key={hu.id} type="button" className="secondary small" onClick={() => onRun(hu.id)} disabled={busy}>
            Solo {hu.id}
          </button>
        ))}
      </div>
      <p className="sc-summary" role="status" aria-live="polite">
        {summary.done === 0
          ? 'Todavía no se ejecutó ninguno.'
          : `${summary.passed} de ${summary.total} cumplen${summary.done < summary.total ? ` (${summary.done} ejecutados)` : ''}.`}
      </p>
      <ul className="sc-quick-list" aria-label="Resultado por escenario">
        {automatable.map((scenario) => {
          const status = statusOf(scenario, runs[scenario.id])
          return (
            <li key={scenario.id}>
              <button type="button" className="sc-quick-item" onClick={() => onOpen(scenario)} title={`${status.text}: abrir el detalle`}>
                <span className={`sc-mark ${status.tone}`}>
                  <span aria-hidden="true">{status.mark}</span>
                  <span className="sr-only">{status.text}</span>
                </span>
                <span className="sc-quick-name">
                  <strong>
                    {scenario.hu} · {scenario.code}
                  </strong>{' '}
                  {scenario.title}
                </span>
              </button>
            </li>
          )
        })}
      </ul>
    </section>
  )
}
