import { ApiError, send } from '../api'
import type { EntradaPago } from '../types'
import type { Check, Expectation, Outcome, ScenarioContext, ScenarioResult, Step } from './types'

export const BACKEND_UNAVAILABLE = 'Backend no disponible en :8001'

/** Thrown when the backend cannot be reached: the runner reports it as one failed step. */
export class BackendUnavailableError extends Error {
  constructor() {
    super(BACKEND_UNAVAILABLE)
    this.name = 'BackendUnavailableError'
  }
}

/** Thrown by `must` when a call a scenario depends on failed; the runner records it as a failed check. */
export class ScenarioAbortError extends Error {
  readonly check: Check

  constructor(check: Check) {
    super(check.label)
    this.name = 'ScenarioAbortError'
    this.check = check
  }
}

const show = (value: unknown): string => (value === undefined ? '(sin valor)' : String(value))

/** Message to compare: the error `detail` on failures, the `mensaje` field on successes. */
function messageOf(outcome: Outcome<unknown>): string | undefined {
  if (outcome.message !== undefined) return outcome.message
  const data = outcome.data
  if (typeof data === 'object' && data !== null && 'mensaje' in data) return String((data as { mensaje: unknown }).mensaje)
  return undefined
}

/**
 * Records steps and checks for one scenario run. `notify` fires after every change so a UI can render
 * the log live. The verdict is derived from the recorded checks only.
 */
export function createContext(notify?: (steps: readonly Step[]) => void): ScenarioContext {
  const steps: Step[] = []
  const checks: Check[] = []
  const qrs = new Map<number, EntradaPago>()
  const changed = () => notify?.(steps.map((step) => ({ ...step })))

  async function call<T>(
    label: string,
    method: 'GET' | 'POST',
    path: string,
    body?: unknown,
    options?: { setup?: boolean },
  ): Promise<Outcome<T>> {
    const step: Step = { label, request: { method, path, body }, ok: false, setup: options?.setup }
    steps.push(step)
    changed()
    try {
      const response = await send<T>(method, path, body)
      step.status = response.status
      step.response = response.payload
      step.ok = true
      changed()
      return { status: response.status, data: response.payload, step }
    } catch (err) {
      if (!(err instanceof ApiError)) throw err
      step.status = err.status
      step.response = err.payload ?? undefined
      changed()
      if (err.status === 0) {
        step.response = BACKEND_UNAVAILABLE
        changed()
        throw new BackendUnavailableError()
      }
      return { status: err.status, message: err.message, step }
    }
  }

  function assert(label: string, passed: boolean, expected: string, actual: string): void {
    checks.push({ label, passed, expected, actual })
    changed()
  }

  function expect(label: string, outcome: Outcome<unknown>, expectation: Expectation): void {
    const statusOk = outcome.status === expectation.status
    assert(`${label}: código HTTP`, statusOk, String(expectation.status), String(outcome.status))
    let messageOk = true
    if (expectation.message !== undefined) {
      const actual = messageOf(outcome)
      messageOk = actual?.includes(expectation.message) ?? false
      assert(`${label}: mensaje`, messageOk, `contiene "${expectation.message}"`, `"${show(actual)}"`)
    }
    outcome.step.ok = statusOk && messageOk
    changed()
  }

  function must<T>(label: string, outcome: Outcome<T>): T {
    if (outcome.data === undefined) {
      throw new ScenarioAbortError({
        label: `Preparación: ${label}`,
        passed: false,
        expected: 'respuesta 2xx',
        actual: `${outcome.status} ${show(outcome.message)}`,
      })
    }
    return outcome.data
  }

  return {
    call,
    expect,
    assert,
    equal: (label, expected, actual) =>
      assert(label, String(expected) === String(actual), String(expected), show(actual)),
    must,
    remember: (...entradas) => {
      for (const entrada of entradas) qrs.set(entrada.id, entrada)
    },
    result: (): ScenarioResult => ({
      steps: steps.map((step) => ({ ...step })),
      checks: checks.map((check) => ({ ...check })),
      passed: checks.length > 0 && checks.every((check) => check.passed),
      qrs: [...qrs.values()],
    }),
  }
}
