import { PageHeader } from '../components/PageHeader'
import { SeedSampleData } from '../components/SeedSampleData'
import { SuggestedOrder } from '../components/guide/SuggestedOrder'
import { UseCaseCard } from '../components/guide/UseCaseCard'
import { UsefulData } from '../components/guide/UsefulData'
import { USE_CASES } from '../content/useCases'
import type { Navigate } from '../tabs'

export function GuidePage({ onNavigate }: { onNavigate: Navigate }) {
  return (
    <>
      <PageHeader
        title="Casos de uso"
        subtitle="Qué hace cada historia de usuario, cómo probarla en esta interfaz y qué errores esperar."
      />
      <div className="guide-top">
        <SuggestedOrder />
        <div className="stack">
          <SeedSampleData />
          <UsefulData />
        </div>
      </div>
      <div className="stack">
        {USE_CASES.map((useCase) => (
          <UseCaseCard key={useCase.id} useCase={useCase} onNavigate={onNavigate} />
        ))}
      </div>
    </>
  )
}
