// Types mirroring smartticket/schemas.py.
// Pydantic serializes Decimal as a JSON string, so money may arrive as string or number.
export type Money = string | number

export type EntradaEstado = 'Disponible' | 'Reservada' | 'Emitida' | 'Utilizada'
export type VentaEstado = 'Pendiente' | 'Pagada' | 'Cancelada'

export interface LugarCreate {
  nombre: string
  direccion: string
}
export interface Lugar extends LugarCreate {
  id: number
}

export interface SectorCreate {
  lugar_id: number
  nombre: string
  capacidad_maxima: number
}
export interface Sector extends SectorCreate {
  id: number
}

export interface PrecioSector {
  sector_id: number
  precio: Money
}

export interface EventoCreate {
  lugar_id: number
  nombre: string
  fecha: string
  precios: PrecioSector[]
}
export interface Evento {
  id: number
  lugar_id: number
  nombre: string
  fecha: string
  precios: PrecioSector[]
}

export interface ClienteCreate {
  nombre: string
  email: string
}
export interface Cliente extends ClienteCreate {
  id: number
}

export interface CotizacionRequest {
  evento_id: number
  sector_id: number
  cantidad: number
}
export interface Cotizacion {
  total: Money
  entrada_ids: number[]
}

export interface Tarjeta {
  numero: string
  titular: string
}
export interface PagoRequest {
  cliente_id: number
  entrada_ids: number[]
  tarjeta: Tarjeta
}
export interface EntradaPago {
  id: number
  codigo_qr: string
  estado: EntradaEstado
}
export interface Pago {
  id: number
  estado: VentaEstado
  total: Money
  entradas: EntradaPago[]
}

export interface Acceso {
  mensaje: string
  id: number
  codigo_qr: string
  estado: EntradaEstado
  hora_ingreso: string
}
