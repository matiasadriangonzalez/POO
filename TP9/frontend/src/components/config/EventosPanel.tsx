import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { formatDateTime, formatMoney, todayAtLocalInput } from '../../format'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Evento, Lugar, PrecioSector, Sector } from '../../types'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { ItemList } from '../ItemList'
import { Notice } from '../Notice'
import { Panel } from '../Panel'

interface Props {
  lugares: Resource<Lugar>
  sectores: Resource<Sector>
  eventos: Resource<Evento>
}

export function EventosPanel({ lugares, sectores, eventos }: Props) {
  const [lugarId, setLugarId] = useState('')
  const [nombre, setNombre] = useState('')
  const [fecha, setFecha] = useState('')
  // price typed per sector id; an empty price means "this sector is not sold at this event"
  const [prices, setPrices] = useState<Record<number, string>>({})
  const { busy, error, run } = useAction()

  const noLugares = !lugares.loading && lugares.data.length === 0
  const noSectores = !sectores.loading && sectores.data.length === 0
  const lugarSectores =sectores.data.filter((s) => String(s.lugar_id) === lugarId)
  const sectorName = (id: number) => sectores.data.find((s) => s.id === id)?.nombre ?? `Sector #${id}`
  const lugarName = (id: number) => lugares.data.find((l) => l.id === id)?.nombre ?? `Lugar #${id}`

  function changeLugar(value: string) {
    setLugarId(value)
    setPrices({})
  }

  async function submit(event: FormEvent) {
    event.preventDefault()
    const precios: PrecioSector[] = lugarSectores
      .filter((s) => (prices[s.id] ?? '').trim() !== '')
      .map((s) => ({ sector_id: s.id, precio: prices[s.id] }))
    const created = await run(() =>
      api.createEvento({ lugar_id: Number(lugarId), nombre: nombre.trim(), fecha, precios }),
    )
    if (!created) return
    setNombre('')
    setFecha('')
    setPrices({})
    eventos.reload()
  }

  return (
    <Panel
      step={4}
      done={eventos.data.length > 0}
      title="Eventos"
      subtitle="Fecha, lugar y precio de cada sector. Al crearlo se generan sus entradas."
    >
      {noLugares && <Notice tone="warn">Primero creá un lugar (paso 1) y al menos un sector (paso 2).</Notice>}
      {!noLugares && noSectores && <Notice tone="warn">Primero creá al menos un sector (paso 2).</Notice>}
      <form onSubmit={submit}>
        <Field label="Lugar">
          <select value={lugarId} onChange={(e) => changeLugar(e.target.value)} required>
            <option value="">Elegí un lugar…</option>
            {lugares.data.map((l) => (
              <option key={l.id} value={l.id}>
                {l.nombre}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Nombre">
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
        </Field>
        <Field label="Fecha y hora" hint="Para escanear en la puerta, el evento debe ser de hoy.">
          <div className="inline-row">
            <input type="datetime-local" value={fecha} onChange={(e) => setFecha(e.target.value)} required />
            <button type="button" className="secondary" onClick={() => setFecha(todayAtLocalInput(20))}>
              Hoy 20:00
            </button>
          </div>
        </Field>

        <fieldset>
          <legend>Precios por sector</legend>
          {!lugarId ? (
            <p className="muted">Elegí un lugar para cargar precios.</p>
          ) : lugarSectores.length === 0 ? (
            <p className="muted">Este lugar no tiene sectores. Creá uno primero.</p>
          ) : (
            lugarSectores.map((s) => (
              <Field key={s.id} label={s.nombre} hint="Cada sector del lugar necesita un precio">
                <input
                  type="number"
                  min={0.01}
                  step="0.01"
                  placeholder="Precio"
                  value={prices[s.id] ?? ''}
                  onChange={(e) => setPrices({ ...prices, [s.id]: e.target.value })}
                />
              </Field>
            ))
          )}
        </fieldset>

        <ErrorMessage message={error} />
        <button type="submit" disabled={busy || noLugares || noSectores}>
          {busy ? 'Creando…' : 'Crear evento'}
        </button>
      </form>
      <ItemList
        items={eventos.data}
        loading={eventos.loading}
        error={eventos.error}
        empty="Todavía no hay eventos."
        render={(e) => (
          <>
            <strong>{e.nombre}</strong>
            <span className="muted">
              {lugarName(e.lugar_id)} · {formatDateTime(e.fecha)}
            </span>
            <span className="muted">
              {e.precios.map((p) => `${sectorName(p.sector_id)}: ${formatMoney(p.precio)}`).join(' · ') ||
                'Sin precios'}
            </span>
          </>
        )}
      />
    </Panel>
  )
}
