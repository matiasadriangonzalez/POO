import { HuSelector } from '../components/scenarios/HuSelector'
import { ManualCases } from '../components/scenarios/ManualCases'
import { QuickCheck } from '../components/scenarios/QuickCheck'
import { RunStep } from '../components/scenarios/RunStep'
import { ScenarioDetail } from '../components/scenarios/ScenarioDetail'
import { ScenarioList } from '../components/scenarios/ScenarioList'
import { StepHeading } from '../components/scenarios/StepHeading'
import { Notice } from '../components/Notice'
import { PageHeader } from '../components/PageHeader'
import { summarize, type useScenarioRunner } from '../hooks/useScenarioRunner'
import { HUS, scenariosOf, type Scenario } from '../scenarios'

type Runner = ReturnType<typeof useScenarioRunner>

interface Props {
  runner: Runner
  /** Opens the Puerta tab with this QR ready to scan. */
  onOpenGate: (code: string) => void
}

export function GuidePage({ runner, onOpenGate }: Props) {
  const { runs, busy, hu, selected, selectHu, selectScenario, run, runGroup } = runner
  const huInfo = HUS.find((item) => item.id === hu)

  function openScenario(scenario: Scenario) {
    if (scenario.hu !== hu) selectHu(scenario.hu)
    selectScenario(scenario.id)
    document.getElementById('paso-3')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <>
      <PageHeader
        title="Casos de uso"
        subtitle="Elegí una historia y un escenario: la app prepara los datos, llama a la API y te dice si cumple."
      />
      <Notice tone="warn">
        Ojo: al ejecutar se guardan datos de demostración en la base real (eventos "Rock Fest") y no hay forma de borrarlos.
      </Notice>

      <section className="sc-flow" aria-labelledby="sc-hu-title">
        <StepHeading number={1} title="Elegí la historia" hint="Cada historia describe qué necesita hacer un usuario." id="sc-hu-title" />
        <HuSelector value={hu} runs={runs} onChange={selectHu} />
      </section>

      <div className="sc-flow">
        <StepHeading
          number={2}
          title="Elegí el escenario"
          hint={`Casos concretos de ${huInfo?.id} · ${huInfo?.title}.`}
        />
        <div className="sc-layout">
          <ScenarioList scenarios={scenariosOf(hu)} selectedId={selected.id} runs={runs} onSelect={selectScenario} />
          <ScenarioDetail scenario={selected} />
        </div>
      </div>

      <RunStep scenario={selected} run={runs[selected.id]} busy={busy} onRun={() => void run(selected)} onOpenGate={onOpenGate} />

      <QuickCheck busy={busy} summary={summarize(runs)} runs={runs} onRun={(group) => void runGroup(group)} onOpen={openScenario} />

      <ManualCases />
    </>
  )
}
