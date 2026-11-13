// Typed wrappers over the three use-case endpoints, recorded as steps of the running scenario.
import { APPROVED_CARD } from '../content/useCases'
import type { Acceso, Cotizacion, Pago } from '../types'
import type { Outcome, ScenarioContext } from './types'

const CARD_HOLDER = 'Cliente Demo'

export const cotizar = (
  ctx: ScenarioContext,
  label: string,
  req: { eventoId: number; sectorId: number; cantidad: number },
  options?: { setup?: boolean },
): Promise<Outcome<Cotizacion>> =>
  ctx.call<Cotizacion>(
    label,
    'POST',
    '/cotizar',
    { evento_id: req.eventoId, sector_id: req.sectorId, cantidad: req.cantidad },
    options,
  )

export const pagar = (
  ctx: ScenarioContext,
  label: string,
  req: { clienteId: number; entradaIds: number[]; tarjeta: string },
  options?: { setup?: boolean },
): Promise<Outcome<Pago>> =>
  ctx.call<Pago>(
    label,
    'POST',
    '/iniciar-pago',
    { cliente_id: req.clienteId, entrada_ids: req.entradaIds, tarjeta: { numero: req.tarjeta, titular: CARD_HOLDER } },
    options,
  )

export const escanear = (ctx: ScenarioContext, label: string, codigoQr: string): Promise<Outcome<Acceso>> =>
  ctx.call<Acceso>(label, 'POST', '/escanear-acceso', { codigo_qr: codigoQr })

/** Buys `cantidad` Platea tickets with the approved card as preparation and returns the issued entradas. */
export async function comprarPlatea(
  ctx: ScenarioContext,
  req: { eventoId: number; plateaId: number; clienteId: number; cantidad: number },
) {
  const cotizacion = ctx.must(
    'cotizar',
    await cotizar(ctx, 'Cotizar para comprar', { eventoId: req.eventoId, sectorId: req.plateaId, cantidad: req.cantidad }, { setup: true }),
  )
  const pago = ctx.must(
    'pagar',
    await pagar(ctx, 'Pagar con tarjeta aprobada', { clienteId: req.clienteId, entradaIds: cotizacion.entrada_ids, tarjeta: APPROVED_CARD }, { setup: true }),
  )
  ctx.remember(...pago.entradas)
  return pago.entradas
}
