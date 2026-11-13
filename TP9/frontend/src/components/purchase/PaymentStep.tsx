import { useState, type FormEvent } from 'react'
import { api } from '../../api'
import { formatDateTime, formatMoney } from '../../format'
import { APPROVED_CARD, REJECTED_CARD } from '../../content/useCases'
import { useAction } from '../../hooks/useAction'
import type { Resource } from '../../hooks/useResource'
import type { Cliente, Cotizacion, Pago } from '../../types'
import { ErrorMessage } from '../ErrorMessage'
import { Field } from '../Field'
import { Notice } from '../Notice'
import type { Selection } from './SelectionStep'

interface Props {
  selection: Selection
  quote: Cotizacion
  clientes: Resource<Cliente>
  onBack: () => void
  onPaid: (pago: Pago) => void
}

export function PaymentStep({ selection, quote, clientes, onBack, onPaid }: Props) {
  const [clienteId, setClienteId] = useState('')
  const [numero, setNumero] = useState('')
  const [titular, setTitular] = useState('')
  const { busy, error, run } = useAction()

  async function submit(event: FormEvent) {
    event.preventDefault()
    const pago = await run(() =>
      api.iniciarPago({
        cliente_id: Number(clienteId),
        entrada_ids: quote.entrada_ids,
        tarjeta: { numero: numero.replace(/\s+/g, ''), titular: titular.trim() },
      }),
    )
    if (pago) onPaid(pago)
  }

  return (
    <div className="stack">
      <section className="card">
        <h3>Cotización</h3>
        <p>
          <strong>{selection.evento.nombre}</strong> · {formatDateTime(selection.evento.fecha)}
        </p>
        <p>
          {selection.cantidad} × {selection.sector.nombre}
        </p>
        <p className="total">{formatMoney(quote.total)}</p>
        <p className="muted">Entradas elegidas: {quote.entrada_ids.map((id) => `#${id}`).join(', ')}</p>
        <button type="button" className="secondary" onClick={onBack} disabled={busy}>
          Cambiar selección
        </button>
      </section>

      <form onSubmit={submit} className="card">
        <h3>2. Pagar</h3>
        <ErrorMessage message={clientes.error} />
        {!clientes.loading && !clientes.error && clientes.data.length === 0 && (
          <Notice tone="warn">No hay clientes. Creá uno en Configuración (paso 3) y volvé a cotizar.</Notice>
        )}
        <Field label="Cliente">
          <select value={clienteId} onChange={(e) => setClienteId(e.target.value)} required>
            <option value="">{clientes.loading ? 'Cargando…' : 'Elegí un cliente…'}</option>
            {clientes.data.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nombre} ({c.email})
              </option>
            ))}
          </select>
        </Field>
        <Field label="Número de tarjeta">
          <input
            inputMode="numeric"
            autoComplete="off"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            required
          />
        </Field>
        <Field label="Titular">
          <input value={titular} onChange={(e) => setTitular(e.target.value)} required />
        </Field>

        <details className="test-cards">
          <summary>Tarjetas de prueba</summary>
          <ul>
            <li>
              <button type="button" className="link" onClick={() => setNumero(APPROVED_CARD)}>
                {APPROVED_CARD}
              </button>{' '}
              — aprobada
            </li>
            <li>
              <button type="button" className="link" onClick={() => setNumero(REJECTED_CARD)}>
                {REJECTED_CARD}
              </button>{' '}
              — rechazada (402)
            </li>
          </ul>
        </details>

        <ErrorMessage message={error} />
        <button type="submit" disabled={busy}>
          {busy ? 'Procesando pago…' : `Pagar ${formatMoney(quote.total)}`}
        </button>
      </form>
    </div>
  )
}
