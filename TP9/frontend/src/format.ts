import type { Money } from './types'

const currency = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' })
const dateTime = new Intl.DateTimeFormat('es-AR', { dateStyle: 'medium', timeStyle: 'short' })
const time = new Intl.DateTimeFormat('es-AR', { dateStyle: 'medium', timeStyle: 'medium' })

export const formatMoney = (value: Money) => currency.format(Number(value))
export const formatDateTime = (iso: string) => dateTime.format(new Date(iso))
export const formatTimestamp = (iso: string) => time.format(new Date(iso))

const pad = (value: number) => String(value).padStart(2, '0')

/** Today at `hour`:00 in the browser's timezone, as a `datetime-local` value (YYYY-MM-DDTHH:mm). */
export function todayAtLocalInput(hour: number): string {
  const now = new Date()
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(hour)}:00`
}
