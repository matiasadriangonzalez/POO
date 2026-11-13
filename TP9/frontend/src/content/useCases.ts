import type { TabId } from '../tabs'

// Content of the "Casos de uso" guide. Behavior is derived from smartticket/services/*.py,
// models.py, pasarela.py and manejador_excepciones.py: keep it in sync if the backend changes.

export const SWAGGER_URL = 'http://localhost:8001/docs'
export const APPROVED_CARD = '4242424242424242'
export const REJECTED_CARD = '4000000000000002'

/** Where an error case can be triggered from. */
export type Trigger = 'ui' | 'swagger' | 'db'

export const TRIGGER_LABEL: Record<Trigger, string> = {
  ui: 'Desde la UI',
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

export interface UseCase {
  id: 'HU1' | 'HU2' | 'HU3'
  title: string
  goal: string
  actor: string
  endpoint: string
  preconditions: string[]
  steps: string[]
  expected: string
  errors: ErrorCase[]
  jump: { tab: TabId; label: string }
}

export const USE_CASES: UseCase[] = [
  {
    id: 'HU1',
    title: 'Cotizar entradas',
    goal: 'Calcular el total de una compra y obtener las entradas elegidas, sin reservarlas ni cobrar.',
    actor: 'Comprador',
    endpoint: 'POST /cotizar',
    preconditions: [
      'Existe un lugar con al menos un sector.',
      'Existe un evento con precio para cada sector de su lugar. Al crearlo se generan tantas entradas como la capacidad de cada sector.',
      'Quedan entradas disponibles en el sector elegido.',
    ],
    steps: [
      'Abrí la pestaña Comprar (paso 1: Selección).',
      'Elegí un evento. Aparece su fecha y hora.',
      'Elegí un sector. Solo se listan los sectores con precio en ese evento.',
      'Dejá la cantidad en 1 o cambiala.',
      'Presioná Cotizar.',
    ],
    expected:
      'Respuesta 200 con el total (precio del sector × cantidad) y los ids de las entradas elegidas. La UI pasa al paso 2 (Pago) y muestra la cotización. Cotizar no reserva nada: las entradas siguen disponibles hasta que se paga.',
    errors: [
      {
        how: 'Pedir más entradas que las disponibles (por ejemplo 101 en un sector de capacidad 100, o repetir compras hasta agotarlo).',
        where: 'ui',
        status: 400,
        message: 'Capacidad insuficiente',
      },
      {
        how: 'Cantidad 0 o negativa: el campo tiene min=1 y el navegador bloquea el envío. En Swagger enviar "cantidad": 0.',
        where: 'swagger',
        status: 400,
        message: 'Cantidad inválida',
      },
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
    jump: { tab: 'comprar', label: 'Ir a Comprar' },
  },
  {
    id: 'HU2',
    title: 'Pagar y emitir entradas',
    goal: 'Cobrar con tarjeta las entradas cotizadas y emitirlas con su código QR.',
    actor: 'Comprador (cliente registrado)',
    endpoint: 'POST /iniciar-pago',
    preconditions: [
      'Hay una cotización (HU1) cuyas entradas siguen disponibles.',
      'Existe al menos un cliente.',
      'Número de tarjeta y titular. La pasarela es simulada y solo rechaza una tarjeta de prueba.',
    ],
    steps: [
      'En Comprar, completá HU1 hasta ver la cotización (paso 2: Pago).',
      'Elegí un cliente.',
      `Ingresá el número ${APPROVED_CARD} (o usá "Tarjetas de prueba") y un titular.`,
      'Presioná Pagar.',
    ],
    expected:
      'Respuesta 200: venta en estado Pagada con el total, y cada entrada pasa a Emitida con su código QR. La UI muestra los QR (se pueden copiar) y los recuerda para la pestaña Puerta.',
    errors: [
      {
        how: `Pagar con la tarjeta ${REJECTED_CARD}. Las entradas se liberan (vuelven a Disponible), así que se puede reintentar con otra tarjeta sobre la misma cotización.`,
        where: 'ui',
        status: 402,
        message: 'Pago denegado',
      },
      {
        how: 'Pagar dos veces las mismas entradas: abrí la app en dos pestañas del navegador, cotizá lo mismo en ambas (cotizar devuelve los mismos ids), pagá en una y después en la otra. En Swagger: repetir el mismo entrada_ids.',
        where: 'ui',
        status: 409,
        message: 'Los lugares seleccionados ya no se encuentran disponibles',
      },
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
    jump: { tab: 'comprar', label: 'Ir a Comprar' },
  },
  {
    id: 'HU3',
    title: 'Escanear acceso en puerta',
    goal: 'Validar el código QR de una entrada emitida y registrar el ingreso del espectador.',
    actor: 'Personal de puerta',
    endpoint: 'POST /escanear-acceso',
    preconditions: [
      'La entrada está Emitida (pagada, HU2) y todavía no se usó.',
      'El evento es de hoy: el backend compara solo la fecha con el día actual del servidor.',
    ],
    steps: [
      'Abrí la pestaña Puerta.',
      'Tocá un código de "Última compra" o pegá un código en el campo.',
      'Presioná Escanear (si tocaste un código, se escanea directo).',
    ],
    expected:
      'Respuesta 200 con "Acceso Permitido", el número de entrada y la hora de ingreso. La entrada pasa a Utilizada. La UI muestra un resultado verde.',
    errors: [
      {
        how: 'Escanear de nuevo el mismo código ya aceptado.',
        where: 'ui',
        status: 409,
        message: 'Entrada ya utilizada',
      },
      {
        how: 'Escribir cualquier texto que no sea un código real.',
        where: 'ui',
        status: 404,
        message: 'Ticket Inválido o Inexistente',
      },
      {
        how: 'Crear un evento con fecha de otro día (en Configuración), comprar una entrada y escanearla. La entrada no se consume: sigue Emitida.',
        where: 'ui',
        status: 400,
        message: 'La entrada no corresponde al evento del día',
      },
      {
        how: 'Escanear el código de una entrada Disponible o Reservada. Ningún endpoint expone ese código: solo se obtiene leyéndolo de la tabla entradas en smartticket.db.',
        where: 'db',
        status: 400,
        message: 'Ticket no emitido / Falta de pago',
      },
    ],
    jump: { tab: 'puerta', label: 'Ir a Puerta' },
  },
]

export const SUGGESTED_ORDER: string[] = [
  'Cargá los datos de ejemplo (o creá a mano en Configuración: lugar, sector, cliente y evento de hoy).',
  'HU1: en Comprar, cotizá 2 entradas y revisá que el total sea precio × 2.',
  'HU1: probá pedir más entradas que la capacidad del sector y verificá "Capacidad insuficiente".',
  `HU2: cotizá de nuevo y pagá con la tarjeta ${REJECTED_CARD}: debe dar 402 "Pago denegado".`,
  `HU2: reintentá con ${APPROVED_CARD} sobre la misma cotización: debe mostrar los QR.`,
  'HU3: en Puerta, escaneá un código: "Acceso Permitido".',
  'HU3: escaneá el mismo código otra vez: 409 "Entrada ya utilizada".',
  'Casos que solo se pueden probar en Swagger: cantidad 0, evento o cliente inexistente, ids mezclados.',
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
