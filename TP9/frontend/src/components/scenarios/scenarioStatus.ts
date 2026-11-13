import type { Scenario } from '../../scenarios'
import type { ScenarioRun } from '../../hooks/useScenarioRunner'

/** Mark, accessible text and tone for a scenario's row, from its latest run. */
export function statusOf(scenario: Scenario, run?: ScenarioRun): { mark: string; text: string; tone: string } {
  if (!scenario.automatable) return { mark: '–', text: 'No automatizable', tone: 'off' }
  if (run?.phase === 'running') return { mark: '…', text: 'Ejecutando', tone: 'run' }
  if (run?.phase === 'queued') return { mark: '·', text: 'En cola', tone: 'run' }
  if (run?.phase === 'done') return run.result?.passed ? { mark: '✓', text: 'Cumple', tone: 'pass' } : { mark: '✕', text: 'No cumple', tone: 'fail' }
  return { mark: '○', text: 'Sin ejecutar', tone: 'idle' }
}
