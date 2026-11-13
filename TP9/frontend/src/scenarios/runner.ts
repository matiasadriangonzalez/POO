import { BackendUnavailableError, BACKEND_UNAVAILABLE, ScenarioAbortError, createContext } from './context'
import { scenariosOf } from './catalog'
import type { HuId, Scenario, ScenarioResult, Step } from './types'

/**
 * Runs one scenario and always resolves: HTTP errors are recorded as step outcomes, and a network
 * failure or unexpected exception becomes a failed step + failed check instead of a throw.
 */
export async function runScenario(
  scenario: Scenario,
  onStep?: (steps: readonly Step[]) => void,
): Promise<ScenarioResult> {
  if (!scenario.automatable) {
    return { steps: [], checks: [], passed: false, qrs: [], skipped: true }
  }
  const ctx = createContext(onStep)
  try {
    const result = await scenario.run(ctx)
    // The verdict is always recomputed from the recorded checks, never taken from the scenario.
    return { ...result, passed: result.checks.length > 0 && result.checks.every((check) => check.passed) }
  } catch (err) {
    if (err instanceof BackendUnavailableError) {
      ctx.assert('Conexión con el backend', false, 'respuesta del servidor', BACKEND_UNAVAILABLE)
    } else if (err instanceof ScenarioAbortError) {
      ctx.assert(err.check.label, false, err.check.expected, err.check.actual)
    } else {
      ctx.assert('Ejecución del escenario', false, 'sin errores inesperados', err instanceof Error ? err.message : String(err))
    }
    return ctx.result()
  }
}

export interface RunAllHooks {
  onStart?: (scenario: Scenario) => void
  onStep?: (scenario: Scenario, steps: readonly Step[]) => void
  onDone?: (scenario: Scenario, result: ScenarioResult) => void
}

export interface RunAllSummary {
  /** Automatable scenarios executed. */
  total: number
  passed: number
  /** Scenarios listed but not executed (not automatable). */
  skipped: number
  results: { scenario: Scenario; result: ScenarioResult }[]
}

/** Runs every automatable scenario (of one HU, or all) one after another; each creates its own fresh evento. */
export async function runAll(hu?: HuId, hooks: RunAllHooks = {}): Promise<RunAllSummary> {
  const summary: RunAllSummary = { total: 0, passed: 0, skipped: 0, results: [] }
  for (const scenario of scenariosOf(hu)) {
    if (!scenario.automatable) {
      summary.skipped += 1
      continue
    }
    hooks.onStart?.(scenario)
    const result = await runScenario(scenario, (steps) => hooks.onStep?.(scenario, steps))
    hooks.onDone?.(scenario, result)
    summary.results.push({ scenario, result })
    summary.total += 1
    if (result.passed) summary.passed += 1
  }
  return summary
}
