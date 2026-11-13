import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Cliente } from '../../types'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { ItemList } from '../ItemList'
import { Panel } from '../Panel'

export function ClientesPanel({ clientes }: { clientes: Resource<Cliente> }) {
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const { busy, error, run } = useAction()

  async function submit(event: FormEvent) {
    event.preventDefault()
    const created = await run(() => api.createCliente({ nombre: nombre.trim(), email: email.trim() }))
    if (!created) return
    setNombre('')
    setEmail('')
    clientes.reload()
  }

  return (
    <Panel step={3} done={clientes.data.length > 0} title="Clientes" subtitle="Quién compra las entradas. No necesita nada previo.">
      <form onSubmit={submit}>
        <Field label="Nombre">
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
        </Field>
        <Field label="Email">
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </Field>
        <ErrorMessage message={error} />
        <button type="submit" disabled={busy}>
          {busy ? 'Creando…' : 'Crear cliente'}
        </button>
      </form>
      <ItemList
        items={clientes.data}
        loading={clientes.loading}
        error={clientes.error}
        empty="Todavía no hay clientes."
        render={(c) => (
          <>
            <strong>{c.nombre}</strong>
            <span className="muted">{c.email}</span>
          </>
        )}
      />
    </Panel>
  )
}
