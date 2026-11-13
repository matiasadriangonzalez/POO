import { useCallback, useEffect, useRef, useState } from 'react'
import { HUS, SCENARIOS, runAll, runScenario, scenariosOf, type HuId, type Scenario, type ScenarioResult, type Step } from '../scenarios'

export type RunPhase = 'queued' | 'running' | 'done'

export interface ScenarioRun {
  phase: RunPhase
  /** Steps recorded so far (live while running). */
  steps: readonly Step[]
  result?: ScenarioResult
}

export interface RunSummary {
  total: number
  done: number
  passed: number
}

/** Counts the automatable scenarios of `hu` (or all) and how many already ran / passed. */
export function summarize(runs: Readonly<Record<string, ScenarioRun>>, hu?: HuId): RunSummary {
  const automatable = scenariosOf(hu).filter((scenario) => scenario.automatable)
  const finished = automatable.filter((scenario) => runs[scenario.id]?.phase === 'done')
  return {
    total: automatable.length,
    done: finished.length,
    passed: finished.filter((scenario) => runs[scenario.id]?.result?.passed).length,
  }
}

/**
 * Owns scenario results and the current selection. Lives in App so results survive tab switches and
 * a running batch keeps going while the user visits another tab. Only one run at a time.
 */
export function useScenarioRunner(onResult?: (scenario: Scenario, result: ScenarioResult) => void) {
  const [runs, setRuns] = useState<Record<string, ScenarioRun>>({})
  const [busy, setBusy] = useState(false)
  const [hu, setHu] = useState<HuId>(HUS[0].id)
  const [scenarioId, setScenarioId] = useState<string>(scenariosOf(HUS[0].id)[0].id)
  const busyRef = useRef(false)
  const onResultRef = useRef(onResult)

  useEffect(() => {
    onResultRef.current = onResult
  })

  const patch = useCallback((id: string, run: ScenarioRun) => setRuns((prev) => ({ ...prev, [id]: run })), [])

  const execute = useCallback(async (task: () => Promise<void>) => {
    if (busyRef.current) return
    busyRef.current = true
    setBusy(true)
    try {
      await task()
    } finally {
      busyRef.current = false
      setBusy(false)
    }
  }, [])

  const finish = useCallback(
    (scenario: Scenario, result: ScenarioResult) => {
      patch(scenario.id, { phase: 'done', steps: result.steps, result })
      onResultRef.current?.(scenario, result)
    },
    [patch],
  )

  const run = useCallback(
    (scenario: Scenario) =>
      execute(async () => {
        patch(scenario.id, { phase: 'running', steps: [] })
        finish(scenario, await runScenario(scenario, (steps) => patch(scenario.id, { phase: 'running', steps })))
      }),
    [execute, patch, finish],
  )

  const runGroup = useCallback(
    (group?: HuId) =>
      execute(async () => {
        const queued = scenariosOf(group).filter((scenario) => scenario.automatable)
        setRuns((prev) => {
          const next = { ...prev }
          for (const scenario of queued) next[scenario.id] = { phase: 'queued', steps: [] }
          return next
        })
        await runAll(group, {
          onStart: (scenario) => patch(scenario.id, { phase: 'running', steps: [] }),
          onStep: (scenario, steps) => patch(scenario.id, { phase: 'running', steps }),
          onDone: finish,
        })
      }),
    [execute, patch, finish],
  )

  const selectHu = useCallback((next: HuId) => {
    setHu(next)
    setScenarioId(scenariosOf(next)[0].id)
  }, [])

  const selected = SCENARIOS.find((scenario) => scenario.id === scenarioId) ?? SCENARIOS[0]

  return { runs, busy, hu, selected, selectHu, selectScenario: setScenarioId, run, runGroup }
}
