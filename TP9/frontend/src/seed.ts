import { api } from './api'
import { todayAtLocalInput } from './format'

export type SeedStepStatus = 'pending' | 'running' | 'done' | 'error'

export interface SeedStep {
  label: string
  status: SeedStepStatus
  /** What was created, once the step is done. */
  detail?: string
}

export const SEED_LABELS = ['Lugar', 'Sector', 'Cliente', 'Evento de hoy'] as const

export const initialSeedSteps = (): SeedStep[] =>
  SEED_LABELS.map((label) => ({ label, status: 'pending' as const }))

const SECTOR_CAPACITY = 100
const SECTOR_PRICE = 5000
const EVENT_HOUR = 20

/**
 * Creates one lugar, one sector, one cliente and one evento dated today, in that order, through the
 * regular API. Reports each step via `onStep`. Stops at the first failure (there is no rollback:
 * the backend has no delete endpoints), so already created records stay and the error is rethrown.
 */
export async function seedSampleData(onStep: (index: number, step: Partial<SeedStep>) => void): Promise<void> {
  let current = 0
  const start = (index: number) => {
    current = index
    onStep(index, { status: 'running' })
  }
  const finish = (detail: string) => onStep(current, { status: 'done', detail })

  try {
    start(0)
    const lugar = await api.createLugar({ nombre: 'Estadio Demo', direccion: 'Av. Siempre Viva 123' })
    finish(`${lugar.nombre} (#${lugar.id})`)

    start(1)
    const sector = await api.createSector({
      lugar_id: lugar.id,
      nombre: 'Platea',
      capacidad_maxima: SECTOR_CAPACITY,
    })
    finish(`${sector.nombre} (#${sector.id}), capacidad ${sector.capacidad_maxima}`)

    start(2)
    const cliente = await api.createCliente({ nombre: 'Cliente Demo', email: 'demo@example.com' })
    finish(`${cliente.nombre} (#${cliente.id})`)

    start(3)
    const evento = await api.createEvento({
      lugar_id: lugar.id,
      nombre: 'Recital Demo',
      fecha: todayAtLocalInput(EVENT_HOUR),
      precios: [{ sector_id: sector.id, precio: SECTOR_PRICE }],
    })
    finish(`${evento.nombre} (#${evento.id}), hoy ${EVENT_HOUR}:00, ${sector.nombre} a $${SECTOR_PRICE}`)
  } catch (err) {
    onStep(current, { status: 'error' })
    throw err
  }
}
