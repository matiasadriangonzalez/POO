import { HUS, type HuId } from '../../scenarios'
import { summarize, type ScenarioRun } from '../../hooks/useScenarioRunner'

interface Props {
  value: HuId
  runs: Readonly<Record<string, ScenarioRun>>
  onChange: (hu: HuId) => void
}

/** Segmented selector: one button per user story with its "Como / Necesito / Para" line. */
export function HuSelector({ value, runs, onChange }: Props) {
  return (
    <div className="sc-hus" role="group" aria-label="Historia de usuario">
      {HUS.map((hu) => {
        const summary = summarize(runs, hu.id)
        return (
          <button
            key={hu.id}
            type="button"
            className="sc-hu"
            aria-pressed={value === hu.id}
            onClick={() => onChange(hu.id)}
          >
            <span className="sc-hu-head">
              <strong>{hu.id}</strong> {hu.title}
              {summary.done > 0 && (
                <span className={summary.passed === summary.total ? 'sc-count pass' : 'sc-count fail'}>
                  {summary.passed}/{summary.total}
                </span>
              )}
            </span>
            <span className="sc-hu-story">
              Como {hu.story.como}, necesito {hu.story.necesito}, para {hu.story.para}.
            </span>
          </button>
        )
      })}
    </div>
  )
}
