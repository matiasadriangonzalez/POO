export const TABS = [
  { id: 'guia', label: 'Casos de uso' },
  { id: 'config', label: 'Configuración' },
  { id: 'comprar', label: 'Comprar' },
  { id: 'puerta', label: 'Puerta' },
] as const

export type TabId = (typeof TABS)[number]['id']

/** Callback pages use to jump to another tab. */
export type Navigate = (tab: TabId) => void
