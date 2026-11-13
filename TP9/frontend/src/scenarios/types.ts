// Scenario engine types. Pure TypeScript: no React, no DOM, so the engine also runs in Node.
import type { HttpMethod } from '../api'
import type { EntradaPago } from '../types'

export type HuId = 'HU1' | 'HU2' | 'HU3'

/** One HTTP interaction (or a failure) recorded while a scenario runs. */
export interface Step {
  label: string
  request?: { method: HttpMethod; path: string; body?: unknown }
  response?: unknown
  /** HTTP status; 0 means the request never reached the backend. */
  status?: number
  /** True when the step behaved as the scenario expected (2xx by default, or as stated by `expect`). */
  ok: boolean
  /** Data preparation (find-or-create demo records), shown collapsed in the UI. */
  setup?: boolean
}

/** One comparison between what the scenario expected and what the backend answered. */
export interface Check {
  label: string
  passed: boolean
  expected: string
  actual: string
}

export interface ScenarioResult {
  steps: Step[]
  checks: Check[]
  /** Computed from the checks: every check passed and at least one ran. Never set by hand. */
  passed: boolean
  /** Tickets this scenario issued, so the UI can offer them in the gate screen. */
  qrs: EntradaPago[]
  /** True when the scenario was not executed because it cannot be automated. */
  skipped?: boolean
}

/** Result of one API call: HTTP errors do not throw, they come back with their status and message. */
export interface Outcome<T> {
  status: number
  data?: T
  /** Error `detail` from the backend (set on non-2xx). */
  message?: string
  step: Step
}

export interface Expectation {
  status: number
  /** Substring that must appear in the error `detail` or in the success `mensaje`. */
  message?: string
}

export interface ScenarioContext {
  call<T>(
    label: string,
    method: HttpMethod,
    path: string,
    body?: unknown,
    options?: { setup?: boolean },
  ): Promise<Outcome<T>>
  /** Compares an outcome with the expected HTTP status (and message substring) and records the checks. */
  expect(label: string, outcome: Outcome<unknown>, expectation: Expectation): void
  /** Records a comparison between two values (compared as strings). */
  equal(label: string, expected: string | number, actual: string | number | undefined): void
  /** Records a boolean condition with a readable expected/actual pair. */
  assert(label: string, passed: boolean, expected: string, actual: string): void
  /** Returns the data of a call the scenario depends on, or aborts the scenario with a failed check. */
  must<T>(label: string, outcome: Outcome<T>): T
  /** Marks tickets as produced by this scenario (replaces earlier ones with the same id). */
  remember(...entradas: EntradaPago[]): void
  /** Builds the final result from everything recorded so far. */
  result(): ScenarioResult
}

export interface Scenario {
  id: string
  hu: HuId
  code: string
  title: string
  dado: string[]
  cuando: string[]
  entonces: string[]
  /** Optional remark, e.g. rules that belong to our implementation and not to the statement. */
  note?: string
  automatable: boolean
  notAutomatableReason?: string
  run(ctx: ScenarioContext): Promise<ScenarioResult>
}

export interface HuInfo {
  id: HuId
  title: string
  /** Story in "Como / Necesito / Para" form. */
  story: { como: string; necesito: string; para: string }
}
