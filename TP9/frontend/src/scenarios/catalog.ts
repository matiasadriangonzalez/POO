import { HU1_SCENARIOS } from './hu1'
import { HU2_SCENARIOS } from './hu2'
import { HU3_SCENARIOS } from './hu3'
import type { HuId, HuInfo, Scenario } from './types'

export const HUS: HuInfo[] = [
  {
    id: 'HU1',
    title: 'Cotizar entradas',
    story: {
      como: 'comprador',
      necesito: 'cotizar entradas de un sector de un evento',
      para: 'conocer el total antes de pagar',
    },
  },
  {
    id: 'HU2',
    title: 'Pagar y emitir entradas',
    story: {
      como: 'comprador',
      necesito: 'pagar con tarjeta las entradas cotizadas',
      para: 'recibirlas emitidas con su código QR',
    },
  },
  {
    id: 'HU3',
    title: 'Escanear acceso',
    story: {
      como: 'personal de puerta',
      necesito: 'escanear el código QR de una entrada',
      para: 'validar el acceso y registrar el ingreso',
    },
  },
]

export const SCENARIOS: Scenario[] = [...HU1_SCENARIOS, ...HU2_SCENARIOS, ...HU3_SCENARIOS]

export const scenariosOf = (hu?: HuId): Scenario[] =>
  hu === undefined ? SCENARIOS : SCENARIOS.filter((scenario) => scenario.hu === hu)
