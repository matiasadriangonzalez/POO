import { useState } from 'react'
import { useAction } from '../hooks/useAction'
import { initialSeedSteps, seedSampleData, type SeedStep } from '../seed'
import { ErrorMessage } from './ErrorMessage'
import { Notice } from './Notice'

interface Props {
  /** Called after a successful run so the host page can refresh its lists. */
  onSeeded?: () => void
}

const STATUS_MARK: Record<SeedStep['status'], string> = {
  pending: '○',
  running: '…',
  done: '✓',
  error: '✗',
}

/** Explicit, user-triggered helper that creates a minimal lugar/sector/cliente/evento set. */
export function SeedSampleData({ onSeeded }: Props) {
  const [steps, setSteps] = useState<SeedStep[]>(initialSeedSteps)
  const [finished, setFinished] = useState(false)
  const { busy, error, run } = useAction()
  const started = steps.some((step) => step.status !== 'pending')

  async function load() {
    setSteps(initialSeedSteps())
    setFinished(false)
    const ok = await run(async () => {
      await seedSampleData((index, patch) =>
        setSteps((prev) => prev.map((step, i) => (i === index ? { ...step, ...patch } : step))),
      )
      return true
    })
    if (ok) {
      setFinished(true)
      onSeeded?.()
    }
  }

  return (
    <section className="card seed">
      <h3>Datos de ejemplo</h3>
      <p className="muted">
        Crea un lugar, un sector de 100 entradas, un cliente y un evento de hoy a las 20:00 con precio.
        Solo se ejecuta cuando presionás el botón, y se suma a lo que ya exista.
      </p>
      <button type="button" onClick={load} disabled={busy}>
        {busy ? 'Cargando datos…' : started ? 'Cargar de nuevo' : 'Cargar datos de ejemplo'}
      </button>

      {started && (
        <ol className="seed-steps" aria-live="polite">
          {steps.map((step) => (
            <li key={step.label} className={`seed-step ${step.status}`}>
              <span className="seed-mark" aria-hidden="true">
                {STATUS_MARK[step.status]}
              </span>
              <span>
                <strong>{step.label}</strong>
                {step.detail && <span className="muted"> — {step.detail}</span>}
              </span>
            </li>
          ))}
        </ol>
      )}
      <ErrorMessage message={error} />
      {error && <p className="muted">Lo que se creó antes del error queda guardado (el backend no permite borrar).</p>}
      {finished && <Notice tone="success">Listo: ya podés ir a Comprar o revisar Configuración.</Notice>}
    </section>
  )
}
