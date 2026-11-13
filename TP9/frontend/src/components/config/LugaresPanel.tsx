import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Lugar } from '../../types'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { ItemList } from '../ItemList'
import { Panel } from '../Panel'

export function LugaresPanel({ lugares }: { lugares: Resource<Lugar> }) {
  const [nombre, setNombre] = useState('')
  const [direccion, setDireccion] = useState('')
  const { busy, error, run } = useAction()

  async function submit(event: FormEvent) {
    event.preventDefault()
    const created = await run(() => api.createLugar({ nombre: nombre.trim(), direccion: direccion.trim() }))
    if (!created) return
    setNombre('')
    setDireccion('')
    lugares.reload()
  }

  return (
    <Panel step={1} done={lugares.data.length > 0} title="Lugares" subtitle="Dónde se hacen los eventos. No necesita nada previo.">
      <form onSubmit={submit}>
        <Field label="Nombre">
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
        </Field>
        <Field label="Dirección">
          <input value={direccion} onChange={(e) => setDireccion(e.target.value)} required />
        </Field>
        <ErrorMessage message={error} />
        <button type="submit" disabled={busy}>
          {busy ? 'Creando…' : 'Crear lugar'}
        </button>
      </form>
      <ItemList
        items={lugares.data}
        loading={lugares.loading}
        error={lugares.error}
        empty="Todavía no hay lugares."
        render={(l) => (
          <>
            <strong>{l.nombre}</strong>
            <span className="muted">{l.direccion}</span>
          </>
        )}
      />
    </Panel>
  )
}
