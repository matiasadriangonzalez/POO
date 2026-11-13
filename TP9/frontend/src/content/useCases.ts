// Reference content for the "Casos de uso" tab. Behavior is derived from smartticket/services/*.py,
// models.py, pasarela.py and manejador_excepciones.py: keep it in sync if the backend changes.
// The scenario runner (src/scenarios) covers the main flows; this file only keeps the error cases
// it cannot reach, which are tried by hand in Swagger or the database.

export const SWAGGER_URL = 'http://localhost:8001/docs'
export const APPROVED_CARD = '4242424242424242'
export const REJECTED_CARD = '4000000000000002'

/** Where a case outside the runner can be triggered from. */
export type Trigger = 'swagger' | 'db'

export const TRIGGER_LABEL: Record<Trigger, string> = {
  swagger: 'Solo Swagger',
  db: 'Solo base de datos',
}

export interface ErrorCase {
  /** How to provoke it. */
  how: string
  where: Trigger
  status: number
  /** Message the backend answers in `detail` (or a description for 422). */
  message: string
}

export interface UseCaseErrors {
  id: 'HU1' | 'HU2' | 'HU3'
  title: string
  errors: ErrorCase[]
}

export const MANUAL_CASES: UseCaseErrors[] = [
  {
    id: 'HU1',
    title: 'Cotizar entradas',
    errors: [
      {
        how: 'Enviar un evento_id que no existe (la UI solo ofrece eventos existentes).',
        where: 'swagger',
        status: 404,
        message: 'Evento no encontrado',
      },
      {
        how: 'Enviar un sector_id sin precio en ese evento (la UI solo ofrece sectores con precio).',
        where: 'swagger',
        status: 404,
        message: 'El sector no tiene precio definido en este evento',
      },
    ],
  },
  {
    id: 'HU2',
    title: 'Pagar y emitir entradas',
    errors: [
      {
        how: 'Enviar ids de entradas inexistentes o repetidos dentro de la lista.',
        where: 'swagger',
        status: 409,
        message: 'Los lugares seleccionados ya no se encuentran disponibles',
      },
      {
        how: 'Enviar un cliente_id que no existe (la UI solo ofrece clientes existentes).',
        where: 'swagger',
        status: 404,
        message: 'Cliente no encontrado',
      },
      {
        how: 'Mezclar ids de entradas de dos eventos distintos (cotizar dos eventos y juntar los ids).',
        where: 'swagger',
        status: 400,
        message: 'Las entradas deben pertenecer a un mismo evento',
      },
      {
        how: 'Enviar "entrada_ids": [] (la UI nunca envía una lista vacía).',
        where: 'swagger',
        status: 422,
        message: 'Error de validación: entrada_ids debe tener al menos 1 elemento',
      },
    ],
  },
  {
    id: 'HU3',
    title: 'Escanear acceso en puerta',
    errors: [
      {
        how: 'E4: escanear el código de una entrada Disponible o Reservada. Ningún endpoint expone ese código: solo se obtiene leyéndolo de la tabla entradas en smartticket.db.',
        where: 'db',
        status: 400,
        message: 'Ticket no emitido / Falta de pago',
      },
    ],
  },
]

export interface UsefulItem {
  label: string
  /** Value shown in monospace when present. */
  code?: string
  text: string
}

export const USEFUL_DATA: UsefulItem[] = [
  { label: 'Tarjeta aprobada', code: APPROVED_CARD, text: 'Cualquier número distinto de la rechazada se aprueba.' },
  { label: 'Tarjeta rechazada', code: REJECTED_CARD, text: 'La pasarela simulada responde 402 "Pago denegado".' },
  {
    label: 'Fecha del evento',
    text: 'Para escanear en la puerta el evento debe ser de hoy. Usá el botón "Hoy 20:00" al crear un evento.',
  },
  {
    label: 'Precios',
    text: 'Un evento necesita un precio para cada sector de su lugar. Si falta alguno, la creación responde 400.',
  },
  {
    label: 'Entradas',
    text: 'Se generan al crear el evento: una por cada lugar de la capacidad de cada sector.',
  },
]
