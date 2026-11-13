import { comprarPlatea, escanear } from './actions'
import { prepareFreshEvent } from './fixtures'
import type { Scenario } from './types'

const UNKNOWN_QR = 'TKT-QR-INEXISTENTE-999'

export const HU3_SCENARIOS: Scenario[] = [
  {
    id: 'hu3-e1',
    hu: 'HU3',
    code: 'E1',
    title: 'Acceso permitido',
    dado: ['Existe una entrada Emitida de un evento de hoy.'],
    cuando: ['El personal de puerta escanea su código QR.'],
    entonces: ['El sistema responde 200 "Acceso Permitido", la entrada pasa a Utilizada y se registra la hora de ingreso.'],
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx)
      const [entrada] = await comprarPlatea(ctx, { eventoId: evento.id, plateaId: platea.id, clienteId: cliente.id, cantidad: 1 })
      const scan = await escanear(ctx, 'Escanear el QR', entrada.codigo_qr)
      ctx.expect('Escaneo', scan, { status: 200, message: 'Acceso Permitido' })
      ctx.equal('Estado de la entrada', 'Utilizada', scan.data?.estado)
      const hora = scan.data?.hora_ingreso
      ctx.assert(
        'Se registra la hora de ingreso',
        hora !== undefined && !Number.isNaN(Date.parse(hora)),
        'hora_ingreso con fecha válida',
        hora ?? '(sin valor)',
      )
      return ctx.result()
    },
  },
  {
    id: 'hu3-e2',
    hu: 'HU3',
    code: 'E2',
    title: 'Entrada ya utilizada',
    dado: ['Una entrada ya fue escaneada y está Utilizada.'],
    cuando: ['Se escanea el mismo código QR por segunda vez.'],
    entonces: ['El sistema responde 409 "Entrada ya utilizada" y no modifica la hora de ingreso original.'],
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx)
      const [entrada] = await comprarPlatea(ctx, { eventoId: evento.id, plateaId: platea.id, clienteId: cliente.id, cantidad: 1 })
      const first = await escanear(ctx, 'Primer escaneo', entrada.codigo_qr)
      ctx.expect('Primer escaneo', first, { status: 200, message: 'Acceso Permitido' })
      const second = await escanear(ctx, 'Segundo escaneo del mismo QR', entrada.codigo_qr)
      ctx.expect('Segundo escaneo', second, { status: 409, message: 'Entrada ya utilizada' })
      ctx.assert(
        'El rechazo no devuelve una nueva hora de ingreso (el backend no permite releer la entrada, así que la hora original no se puede comparar directamente)',
        second.data === undefined,
        'sin hora_ingreso en la respuesta',
        second.data ? `hora_ingreso ${second.data.hora_ingreso}` : 'sin hora_ingreso',
      )
      return ctx.result()
    },
  },
  {
    id: 'hu3-e3',
    hu: 'HU3',
    code: 'E3',
    title: 'Ticket inválido',
    dado: ['Existe un evento de hoy con entradas.'],
    cuando: [`Se escanea un código que no existe (${UNKNOWN_QR}).`],
    entonces: ['El sistema responde 404 "Ticket Inválido o Inexistente".'],
    automatable: true,
    async run(ctx) {
      const scan = await escanear(ctx, 'Escanear un QR inexistente', UNKNOWN_QR)
      ctx.expect('Escaneo', scan, { status: 404, message: 'Ticket Inválido o Inexistente' })
      return ctx.result()
    },
  },
  {
    id: 'hu3-e1b',
    hu: 'HU3',
    code: 'E1b',
    title: 'Evento de otro día',
    dado: ['Existe una entrada Emitida de un evento que es mañana.'],
    cuando: ['El personal de puerta escanea su código QR hoy.'],
    entonces: ['El sistema responde 400 "La entrada no corresponde al evento del día".'],
    note: 'Regla extra de nuestra implementación: no figura en el enunciado.',
    automatable: true,
    async run(ctx) {
      const { evento, platea, cliente } = await prepareFreshEvent(ctx, { dayOffset: 1 })
      const [entrada] = await comprarPlatea(ctx, { eventoId: evento.id, plateaId: platea.id, clienteId: cliente.id, cantidad: 1 })
      const scan = await escanear(ctx, 'Escanear el QR del evento de mañana', entrada.codigo_qr)
      ctx.expect('Escaneo', scan, { status: 400, message: 'La entrada no corresponde al evento del día' })
      return ctx.result()
    },
  },
  {
    id: 'hu3-e4',
    hu: 'HU3',
    code: 'E4',
    title: 'Ticket no emitido / falta de pago',
    dado: ['Existe una entrada que nunca se emitió (Disponible o Reservada).'],
    cuando: ['Se escanea su código QR.'],
    entonces: ['El sistema responde 400 "Ticket no emitido / Falta de pago".'],
    automatable: false,
    notAutomatableReason:
      'Ningún endpoint expone el QR de una entrada que nunca se emitió. Solo se reproduce leyendo el código de la tabla entradas (una entrada Disponible o Reservada) en la base de datos. Lo cubre el test del backend test_escanear_acceso.py.',
    run() {
      return Promise.reject(new Error('Scenario is not automatable'))
    },
  },
]
