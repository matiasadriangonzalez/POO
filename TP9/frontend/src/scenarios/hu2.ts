import { APPROVED_CARD, REJECTED_CARD } from '../content/useCases'
import { cotizar, pagar } from './actions'
import { DEMO, prepareFreshEvent } from './fixtures'
import type { Scenario } from './types'

const sameIds = (a: number[] | undefined, b: number[] | undefined) =>
  a !== undefined && b !== undefined && a.length === b.length && a.every((id, i) => id === b[i])

export const HU2_SCENARIOS: Scenario[] = [
  {
    id: 'hu2-e1',
    hu: 'HU2',
    code: 'E1',
    title: 'Pago aprobado',
    dado: ['Hay una cotización de 2 entradas de Platea y un cliente registrado.'],
    cuando: [`El cliente paga con una tarjeta válida (${APPROVED_CARD}).`],
    entonces: [
      'El sistema responde 200 con la venta en estado Pagada.',
      'Las 2 entradas quedan Emitidas, cada una con su código QR.',
    ],
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx)
      const cot = ctx.must(
        'cotizar',
        await cotizar(ctx, 'Cotizar 2 entradas de Platea', { eventoId: evento.id, sectorId: platea.id, cantidad: 2 }),
      )
      const pago = await pagar(ctx, 'Pagar con tarjeta aprobada', {
        clienteId: cliente.id,
        entradaIds: cot.entrada_ids,
        tarjeta: APPROVED_CARD,
      })
      ctx.expect('Pago', pago, { status: 200 })
      ctx.equal('Estado de la venta', 'Pagada', pago.data?.estado)
      ctx.equal('Total cobrado (comparado como número)', 2 * DEMO.platea.precio, pago.data && Number(pago.data.total))
      ctx.equal('Cantidad de entradas', 2, pago.data?.entradas.length)
      ctx.assert(
        'Todas las entradas quedan Emitidas',
        pago.data?.entradas.every((entrada) => entrada.estado === 'Emitida') ?? false,
        'todas Emitida',
        pago.data?.entradas.map((entrada) => entrada.estado).join(', ') ?? '(sin entradas)',
      )
      ctx.assert(
        'Cada entrada tiene código QR',
        pago.data?.entradas.every((entrada) => entrada.codigo_qr.length > 0) ?? false,
        'codigo_qr no vacío',
        pago.data?.entradas.map((entrada) => entrada.codigo_qr).join(', ') ?? '(sin entradas)',
      )
      if (pago.data) ctx.remember(...pago.data.entradas)
      return ctx.result()
    },
  },
  {
    id: 'hu2-e2',
    hu: 'HU2',
    code: 'E2',
    title: 'Pago rechazado',
    dado: ['Hay una cotización de 2 entradas de Platea.'],
    cuando: [`El cliente paga con la tarjeta rechazada (${REJECTED_CARD}).`],
    entonces: [
      'El sistema responde 402 "Pago denegado".',
      'No se crea ninguna venta y las entradas siguen disponibles: cotizar de nuevo ofrece las mismas.',
    ],
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx)
      const first = ctx.must(
        'cotizar',
        await cotizar(ctx, 'Cotizar 2 entradas de Platea', { eventoId: evento.id, sectorId: platea.id, cantidad: 2 }),
      )
      const pago = await pagar(ctx, 'Pagar con tarjeta rechazada', {
        clienteId: cliente.id,
        entradaIds: first.entrada_ids,
        tarjeta: REJECTED_CARD,
      })
      ctx.expect('Pago rechazado', pago, { status: 402, message: 'Pago denegado' })
      const again = await cotizar(ctx, 'Cotizar otra vez lo mismo', { eventoId: evento.id, sectorId: platea.id, cantidad: 2 })
      ctx.expect('Nueva cotización', again, { status: 200 })
      ctx.assert(
        'Entradas intactas: se ofrecen los mismos ids',
        sameIds(first.entrada_ids, again.data?.entrada_ids),
        `[${first.entrada_ids.join(', ')}]`,
        again.data ? `[${again.data.entrada_ids.join(', ')}]` : '(sin cotización)',
      )
      return ctx.result()
    },
  },
  {
    id: 'hu2-e3',
    hu: 'HU2',
    code: 'E3',
    title: 'Entradas ya no disponibles',
    dado: ['Dos entradas ya fueron pagadas y emitidas.'],
    cuando: ['Se intenta pagar de nuevo las mismas entradas (por ejemplo, desde otra pestaña).'],
    entonces: ['El sistema responde 409 "Los lugares seleccionados ya no se encuentran disponibles".'],
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx)
      const cot = ctx.must(
        'cotizar',
        await cotizar(ctx, 'Cotizar 2 entradas de Platea', { eventoId: evento.id, sectorId: platea.id, cantidad: 2 }),
      )
      const request = { clienteId: cliente.id, entradaIds: cot.entrada_ids, tarjeta: APPROVED_CARD }
      const first = await pagar(ctx, 'Primer pago (aprobado)', request)
      ctx.expect('Primer pago', first, { status: 200 })
      if (first.data) ctx.remember(...first.data.entradas)
      const second = await pagar(ctx, 'Segundo pago de las mismas entradas', request)
      ctx.expect('Segundo pago', second, {
        status: 409,
        message: 'Los lugares seleccionados ya no se encuentran disponibles',
      })
      return ctx.result()
    },
  },
]
