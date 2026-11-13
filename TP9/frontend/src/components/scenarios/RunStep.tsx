import type { Scenario } from '../../scenarios'
import type { ScenarioRun } from '../../hooks/useScenarioRunner'
import { ResultPanel } from './ResultPanel'
import { StepHeading } from './StepHeading'

interface Props {
  scenario: Scenario
  run?: ScenarioRun
  busy: boolean
  onRun: () => void
  onOpenGate: (code: string) => void
}

/** Step 3 of the guided flow: the run button and, below it, the result (or a friendly empty state). */
export function RunStep({ scenario, run, busy, onRun, onOpenGate }: Props) {
  const running = run?.phase === 'running'
  return (
    <section className="card sc-run" aria-labelledby="sc-run-title">
      <StepHeading
        id="paso-3"
        number={3}
        title="Ejecutá y mirá el resultado"
        hint={`${scenario.hu} · ${scenario.code} ${scenario.title}`}
      />
      <div className="sc-run-action">
        <button type="button" className="sc-run-button" onClick={onRun} disabled={busy || !scenario.automatable}>
          {running ? 'Ejecutando…' : run ? 'Ejecutar de nuevo' : 'Ejecutar escenario'}
        </button>
        {!scenario.automatable && <span className="muted">Este escenario no se puede ejecutar desde la app.</span>}
      </div>
      <ResultPanel scenario={scenario} run={run} onOpenGate={onOpenGate} />
    </section>
  )
}
