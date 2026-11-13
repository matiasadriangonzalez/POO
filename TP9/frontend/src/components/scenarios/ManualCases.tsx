import { MANUAL_CASES, SWAGGER_URL } from '../../content/useCases'
import { ErrorCasesTable } from '../guide/ErrorCasesTable'
import { UsefulData } from '../guide/UsefulData'

/** Collapsed reference for the cases the runner cannot reach, plus the Swagger link and test data. */
export function ManualCases() {
  return (
    <details className="card sc-manual">
      <summary>Más info: casos que se prueban a mano y datos útiles</summary>
      <p className="muted">
        Estos casos no se pueden ejecutar desde un escenario. Se prueban a mano en{' '}
        <a href={SWAGGER_URL} target="_blank" rel="noopener noreferrer">
          Swagger
        </a>{' '}
        o leyendo la base de datos.
      </p>
      {MANUAL_CASES.map((useCase) => (
        <section key={useCase.id}>
          <h4>
            {useCase.id} · {useCase.title}
          </h4>
          <ErrorCasesTable cases={useCase.errors} />
        </section>
      ))}
      <UsefulData />
    </details>
  )
}
