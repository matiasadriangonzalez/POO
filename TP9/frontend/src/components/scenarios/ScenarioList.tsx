import type { Scenario } from '../../scenarios'
import type { ScenarioRun } from '../../hooks/useScenarioRunner'
import { statusOf } from './scenarioStatus'

interface Props {
  scenarios: Scenario[]
  selectedId: string
  runs: Readonly<Record<string, ScenarioRun>>
  onSelect: (id: string) => void
}

export function ScenarioList({ scenarios, selectedId, runs, onSelect }: Props) {
  return (
    <ul className="sc-list" aria-label="Escenarios">
      {scenarios.map((scenario) => {
        const status = statusOf(scenario, runs[scenario.id])
        return (
          <li key={scenario.id}>
            <button
              type="button"
              className="sc-chip"
              aria-pressed={selectedId === scenario.id}
              onClick={() => onSelect(scenario.id)}
            >
              <span className="sc-code">{scenario.code}</span>
              <span className="sc-chip-title">{scenario.title}</span>
              <span className={`sc-mark ${status.tone}`} title={status.text}>
                <span aria-hidden="true">{status.mark}</span>
                <span className="sr-only">{status.text}</span>
              </span>
            </button>
          </li>
        )
      })}
    </ul>
  )
}
