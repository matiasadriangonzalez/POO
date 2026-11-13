import type { Scenario } from '../../scenarios'
import { Notice } from '../Notice'

const SECTIONS = [
  ['Dado', 'dado'],
  ['Cuando', 'cuando'],
  ['Entonces', 'entonces'],
] as const

/** What the selected scenario checks, in Dado / Cuando / Entonces form. */
export function ScenarioDetail({ scenario }: { scenario: Scenario }) {
  return (
    <section className="card" aria-labelledby="sc-detail-title">
      <header className="sc-detail-head">
        <p className="sc-eyebrow">
          {scenario.hu} · Escenario {scenario.code}
        </p>
        <h3 id="sc-detail-title">{scenario.title}</h3>
        <p className="muted">Qué se prueba, de lo que parte a lo que debería pasar:</p>
      </header>

      {scenario.note && <Notice tone="info">{scenario.note}</Notice>}
      {!scenario.automatable && <Notice tone="warn">{scenario.notAutomatableReason}</Notice>}

      <dl className="sc-gwt">
        {SECTIONS.map(([label, key]) => (
          <div key={key}>
            <dt>{label}</dt>
            <dd>
              {scenario[key].length === 1 ? (
                scenario[key][0]
              ) : (
                <ul>
                  {scenario[key].map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              )}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
