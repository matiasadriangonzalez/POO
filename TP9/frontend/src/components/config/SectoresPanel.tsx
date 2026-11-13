import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Lugar, Sector } from '../../types'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { ItemList } from '../ItemList'
import { Notice } from '../Notice'
import { Panel } from '../Panel'

interface Props {
  lugares: Resource<Lugar>
  sectores: Resource<Sector>
}

export function SectoresPanel({ lugares, sectores }: Props) {
  const [lugarId, setLugarId] = useState('')
  const [nombre, setNombre] = useState('')
  const [capacidad, setCapacidad] = useState('')
  const { busy, error, run } = useAction()

  const noLugares = !lugares.loading && lugares.data.length === 0
  const lugarName = (id: number) => lugares.data.find((l) => l.id === id)?.nombre ?? `Lugar #${id}`

  async function submit(event: FormEvent) {
    event.preventDefault()
    const created = await run(() =>
      api.createSector({
        lugar_id: Number(lugarId),
        nombre: nombre.trim(),
        capacidad_maxima: Number(capacidad),
      }),
    )
    if (!created) return
    setNombre('')
    setCapacidad('')
    sectores.reload()
  }

  return (
    <Panel
      step={2}
      done={sectores.data.length > 0}
      title="Sectores"
      subtitle="Zonas de un lugar. Cada lugar de la capacidad se convierte en una entrada."
    >
      {noLugares && <Notice tone="warn">Primero creá un lugar (paso 1).</Notice>}
      <form onSubmit={submit}>
        <Field label="Lugar">
          <select value={lugarId} onChange={(e) => setLugarId(e.target.value)} required>
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
        <Field label="Capacidad máxima">
          <input
            type="number"
            min={1}
            step={1}
            value={capacidad}
            onChange={(e) => setCapacidad(e.target.value)}
            required
          />
        </Field>
        <ErrorMessage message={error} />
        <button type="submit" disabled={busy || noLugares}>
          {busy ? 'Creando…' : 'Crear sector'}
        </button>
      </form>
      <ItemList
        items={sectores.data}
        loading={sectores.loading}
        error={sectores.error}
        empty="Todavía no hay sectores."
        render={(s) => (
          <>
            <strong>{s.nombre}</strong>
            <span className="muted">
              {lugarName(s.lugar_id)} · capacidad {s.capacidad_maxima}
            </span>
          </>
        )}
      />
    </Panel>
  )
}
