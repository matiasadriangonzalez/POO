import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { formatDateTime, formatMoney } from '../../format'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Cotizacion, Evento, Sector } from '../../types'
import type { Navigate } from '../../tabs'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { Notice } from '../Notice'

export interface Selection {
  evento: Evento
  sector: Sector
  cantidad: number
}

interface Props {
  eventos: Resource<Evento>
  sectores: Resource<Sector>
  onNavigate: Navigate
  onQuoted: (selection: Selection, quote: Cotizacion) => void
}

export function SelectionStep({ eventos, sectores, onNavigate, onQuoted }: Props) {
  const [eventoId, setEventoId] = useState('')
  const [sectorId, setSectorId] = useState('')
  const [cantidad, setCantidad] = useState('1')
  const { busy, error, run } = useAction()

  const noEventos = !eventos.loading && !eventos.error && eventos.data.length === 0
  const evento = eventos.data.find((e) => String(e.id) === eventoId)
  // only sectors that have a price in the chosen event can be bought
  const sellable = evento
    ? evento.precios
        .map((p) => ({ precio: p.precio, sector: sectores.data.find((s) => s.id === p.sector_id) }))
        .filter((item): item is { precio: typeof item.precio; sector: Sector } => item.sector !== undefined)
    : []
  const sector = sellable.find((item) => String(item.sector.id) === sectorId)?.sector

  function changeEvento(value: string) {
    setEventoId(value)
    setSectorId('')
  }

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!evento || !sector) return
    const qty = Number(cantidad)
    const quote = await run(() => api.cotizar({ evento_id: evento.id, sector_id: sector.id, cantidad: qty }))
    if (quote) onQuoted({ evento, sector, cantidad: qty }, quote)
  }

  return (
    <form onSubmit={submit} className="card">
      <h3>1. Elegí tus entradas</h3>
      <ErrorMessage message={eventos.error ?? sectores.error} />
      {noEventos && (
        <Notice tone="warn">
          Todavía no hay eventos para comprar.{' '}
          <button type="button" className="text-link" onClick={() => onNavigate('config')}>
            Crealos en Configuración
          </button>
          .
        </Notice>
      )}
      <Field label="Evento">
        <select value={eventoId} onChange={(e) => changeEvento(e.target.value)} required>
          <option value="">{eventos.loading ? 'Cargando…' : 'Elegí un evento…'}</option>
          {eventos.data.map((e) => (
            <option key={e.id} value={e.id}>
              {e.nombre} — {formatDateTime(e.fecha)}
            </option>
          ))}
        </select>
      </Field>
      <Field label="Sector">
        <select value={sectorId} onChange={(e) => setSectorId(e.target.value)} disabled={!evento} required>
          <option value="">{evento ? 'Elegí un sector…' : 'Primero elegí un evento'}</option>
          {sellable.map(({ sector: s, precio }) => (
            <option key={s.id} value={s.id}>
              {s.nombre} — {formatMoney(precio)}
            </option>
          ))}
        </select>
      </Field>
      <Field label="Cantidad">
        <input
          type="number"
          min={1}
          step={1}
          value={cantidad}
          onChange={(e) => setCantidad(e.target.value)}
          required
        />
      </Field>
      <ErrorMessage message={error} />
      <button type="submit" disabled={busy || !evento || !sector}>
        {busy ? 'Cotizando…' : 'Cotizar'}
      </button>
    </form>
  )
}
