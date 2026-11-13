import { dayAtLocalInput } from '../format'
import type { Cliente, Evento, Lugar, Sector } from '../types'
import type { ScenarioContext } from './types'

export const DEMO = {
  lugar: { nombre: 'Estadio Demo (escenarios)', direccion: 'Av. Siempre Viva 123' },
  platea: { nombre: 'Platea', capacidad: 10, precio: 12000 },
  vip: { nombre: 'VIP', capacidad: 1, precio: 35000 },
  cliente: { nombre: 'Cliente Demo (escenarios)', email: 'escenarios@example.com' },
  eventoNombre: 'Rock Fest',
  eventHour: 20,
} as const

export interface DemoSetup {
  lugar: Lugar
  platea: Sector
  vip: Sector
  cliente: Cliente
}

const setup = { setup: true } as const

async function ensureLugar(ctx: ScenarioContext): Promise<Lugar> {
  const list = ctx.must('listar lugares', await ctx.call<Lugar[]>('Buscar el lugar demo', 'GET', '/lugares', undefined, setup))
  const found = list.find((lugar) => lugar.nombre === DEMO.lugar.nombre)
  if (found) return found
  return ctx.must('crear lugar', await ctx.call<Lugar>('Crear el lugar demo', 'POST', '/lugares', DEMO.lugar, setup))
}

async function ensureSector(
  ctx: ScenarioContext,
  lugar: Lugar,
  spec: { nombre: string; capacidad: number },
): Promise<Sector> {
  const list = ctx.must('listar sectores', await ctx.call<Sector[]>(`Buscar el sector ${spec.nombre}`, 'GET', '/sectores', undefined, setup))
  const found = list.find((sector) => sector.lugar_id === lugar.id && sector.nombre === spec.nombre)
  if (found) return found
  const body = { lugar_id: lugar.id, nombre: spec.nombre, capacidad_maxima: spec.capacidad }
  return ctx.must('crear sector', await ctx.call<Sector>(`Crear el sector ${spec.nombre}`, 'POST', '/sectores', body, setup))
}

async function ensureCliente(ctx: ScenarioContext): Promise<Cliente> {
  const list = ctx.must('listar clientes', await ctx.call<Cliente[]>('Buscar el cliente demo', 'GET', '/clientes', undefined, setup))
  const found = list.find((cliente) => cliente.email === DEMO.cliente.email)
  if (found) return found
  return ctx.must('crear cliente', await ctx.call<Cliente>('Crear el cliente demo', 'POST', '/clientes', DEMO.cliente, setup))
}

/**
 * Idempotent: finds (GET) or creates (POST) the demo lugar with its two sectors and the demo cliente.
 * The lugar must keep exactly these sectors, because an evento needs a price for every sector of its lugar.
 */
export async function prepareDemo(ctx: ScenarioContext): Promise<DemoSetup> {
  const lugar = await ensureLugar(ctx)
  const platea = await ensureSector(ctx, lugar, DEMO.platea)
  const vip = await ensureSector(ctx, lugar, DEMO.vip)
  const cliente = await ensureCliente(ctx)
  return { lugar, platea, vip, cliente }
}

const newRunId = (): string => Math.random().toString(36).slice(2, 6)

/**
 * ALWAYS creates a brand-new evento (unique name) so every scenario run owns its tickets:
 * Platea starts with 10 available entradas and VIP with exactly 1.
 */
export async function crearEventoFresco(
  ctx: ScenarioContext,
  demo: DemoSetup,
  options: { dayOffset?: number } = {},
): Promise<Evento> {
  const dayOffset = options.dayOffset ?? 0
  const body = {
    lugar_id: demo.lugar.id,
    nombre: `${DEMO.eventoNombre} ${newRunId()}`,
    fecha: dayAtLocalInput(dayOffset, DEMO.eventHour),
    precios: [
      { sector_id: demo.platea.id, precio: DEMO.platea.precio },
      { sector_id: demo.vip.id, precio: DEMO.vip.precio },
    ],
  }
  const when = dayOffset === 0 ? 'hoy' : 'mañana'
  return ctx.must('crear evento', await ctx.call<Evento>(`Crear un evento nuevo (${when} ${DEMO.eventHour}:00)`, 'POST', '/eventos', body, setup))
}

/** Convenience: demo records plus a fresh evento dated today (or `dayOffset` days from today). */
export async function prepareFreshEvent(ctx: ScenarioContext, options: { dayOffset?: number } = {}) {
  const demo = await prepareDemo(ctx)
  const evento = await crearEventoFresco(ctx, demo, options)
  return { ...demo, evento }
}
