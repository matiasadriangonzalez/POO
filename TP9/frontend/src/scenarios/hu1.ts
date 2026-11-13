import { cotizar } from './actions'
import { DEMO, prepareFreshEvent } from './fixtures'
import type { Scenario } from './types'

const PLATEA_TOTAL_FOR_TWO = DEMO.platea.precio * 2

export const HU1_SCENARIOS: Scenario[] = [
  {
    id: 'hu1-e1',
    hu: 'HU1',
    code: 'E1',
    title: 'Cotización correcta',
    dado: ['El evento Rock Fest tiene el sector Platea a $12.000 con entradas disponibles.'],
    cuando: ['El comprador cotiza 2 entradas de Platea.'],
    entonces: ['El sistema responde 200 con un total de $24.000 y los ids de 2 entradas.'],
    automatable: true,
    async run(ctx) {
      const { evento, platea } = await prepareFreshEvent(ctx)
      const cot = await cotizar(ctx, 'Cotizar 2 entradas de Platea', { eventoId: evento.id, sectorId: platea.id, cantidad: 2 })
      ctx.expect('Cotización', cot, { status: 200 })
      ctx.equal('Total = 2 x $12.000 (comparado como número)', PLATEA_TOTAL_FOR_TWO, cot.data && Number(cot.data.total))
      ctx.equal('Cantidad de entradas elegidas', 2, cot.data?.entrada_ids.length)
      return ctx.result()
    },
  },
  {
    id: 'hu1-e2',
    hu: 'HU1',
    code: 'E2',
    title: 'Capacidad insuficiente',
    dado: ['El sector VIP del evento tiene una sola entrada disponible.'],
    cuando: ['El comprador cotiza 3 entradas de VIP.'],
    entonces: ['El sistema responde 400 "Capacidad insuficiente" y no devuelve entradas.'],
    automatable: true,
    async run(ctx) {
      const { evento, vip } = await prepareFreshEvent(ctx)
      const control = await cotizar(ctx, 'Control: cotizar 1 entrada de VIP', { eventoId: evento.id, sectorId: vip.id, cantidad: 1 })
      ctx.expect('Control (hay exactamente 1 entrada)', control, { status: 200 })
      const cot = await cotizar(ctx, 'Cotizar 3 entradas de VIP', { eventoId: evento.id, sectorId: vip.id, cantidad: 3 })
      ctx.expect('Cotización excedida', cot, { status: 400, message: 'Capacidad insuficiente' })
      return ctx.result()
    },
  },
  {
    id: 'hu1-e3',
    hu: 'HU1',
    code: 'E3',
    title: 'Cantidad inválida',
    dado: ['El evento tiene entradas disponibles en Platea.'],
    cuando: ['El comprador cotiza 0 entradas, y luego una cantidad negativa.'],
    entonces: ['En ambos casos el sistema responde 400 "Cantidad inválida".'],
    automatable: true,
    async run(ctx) {
      const { evento, platea } = await prepareFreshEvent(ctx)
      const zero = await cotizar(ctx, 'Cotizar 0 entradas', { eventoId: evento.id, sectorId: platea.id, cantidad: 0 })
      ctx.expect('Cantidad 0', zero, { status: 400, message: 'Cantidad inválida' })
      const negative = await cotizar(ctx, 'Cotizar -1 entradas', { eventoId: evento.id, sectorId: platea.id, cantidad: -1 })
      ctx.expect('Cantidad negativa', negative, { status: 400, message: 'Cantidad inválida' })
      return ctx.result()
    },
  },
]
