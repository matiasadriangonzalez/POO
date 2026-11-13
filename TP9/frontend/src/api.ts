import type {
  Acceso,
  Cliente,
  ClienteCreate,
  Cotizacion,
  CotizacionRequest,
  Evento,
  EventoCreate,
  Lugar,
  LugarCreate,
  Pago,
  PagoRequest,
  Sector,
  SectorCreate,
} from './types'

const BASE_URL = '/api'

/** Single error type for every failed request: HTTP status (0 = network) + readable message. */
export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

interface ValidationIssue {
  loc?: (string | number)[]
  msg?: string
}

/** FastAPI sends `detail` as a string (domain errors) or an array (422 validation errors). */
function extractMessage(payload: unknown, fallback: string): string {
  if (typeof payload !== 'object' || payload === null || !('detail' in payload)) return fallback
  const { detail } = payload as { detail: unknown }
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const lines = (detail as ValidationIssue[]).map((issue) => {
      const field = issue.loc?.filter((part) => part !== 'body').join('.')
      return field ? `${field}: ${issue.msg ?? 'invalid'}` : (issue.msg ?? 'invalid')
    })
    return lines.join('; ') || fallback
  }
  return fallback
}

async function request<T>(method: 'GET' | 'POST', path: string, body?: unknown): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new ApiError(0, 'No se pudo conectar con el servidor. ¿Está corriendo el backend en el puerto 8001?')
  }

  const payload: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    throw new ApiError(response.status, extractMessage(payload, `Error ${response.status}`))
  }
  return payload as T
}

export const api = {
  listLugares: () => request<Lugar[]>('GET', '/lugares'),
  createLugar: (data: LugarCreate) => request<Lugar>('POST', '/lugares', data),

  listSectores: () => request<Sector[]>('GET', '/sectores'),
  createSector: (data: SectorCreate) => request<Sector>('POST', '/sectores', data),

  listEventos: () => request<Evento[]>('GET', '/eventos'),
  createEvento: (data: EventoCreate) => request<Evento>('POST', '/eventos', data),

  listClientes: () => request<Cliente[]>('GET', '/clientes'),
  createCliente: (data: ClienteCreate) => request<Cliente>('POST', '/clientes', data),

  cotizar: (data: CotizacionRequest) => request<Cotizacion>('POST', '/cotizar', data),
  iniciarPago: (data: PagoRequest) => request<Pago>('POST', '/iniciar-pago', data),
  escanearAcceso: (codigoQr: string) =>
    request<Acceso>('POST', '/escanear-acceso', { codigo_qr: codigoQr }),
}
