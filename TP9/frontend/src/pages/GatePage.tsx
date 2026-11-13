import { useState, type FormEvent } from 'react'
import { api } from '../api'
import { Field } from '../components/Field'
import { PageHeader } from '../components/PageHeader'
import { formatTimestamp } from '../format'
import type { Acceso, EntradaPago } from '../types'

type ScanResult = { ok: true; acceso: Acceso } | { ok: false; message: string }

interface Props {
  lastPurchase: EntradaPago[]
  /** QR to leave in the input, ready to scan (not scanned automatically). */
  initialCode?: string
}

export function GatePage({ lastPurchase, initialCode = '' }: Props) {
  const [codigo, setCodigo] = useState(initialCode)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [busy, setBusy] = useState(false)

  async function scan(code: string) {
    const trimmed = code.trim()
    if (!trimmed) return
    setBusy(true)
    setResult(null)
    try {
      setResult({ ok: true, acceso: await api.escanearAcceso(trimmed) })
    } catch (err) {
      setResult({ ok: false, message: err instanceof Error ? err.message : 'Error inesperado' })
    } finally {
      setBusy(false)
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault()
    void scan(codigo)
  }

  function pick(code: string) {
    setCodigo(code)
    void scan(code)
  }

  return (
    <div className="narrow">
      <PageHeader
        title="Puerta"
        subtitle="HU3: escaneá el código QR de una entrada para registrar el ingreso. El evento debe ser de hoy."
      />
      <form onSubmit={submit} className="card">
        <h3>Escanear acceso</h3>
        <Field label="Código QR">
          <input
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            autoComplete="off"
            spellCheck={false}
            required
          />
        </Field>
        <button type="submit" disabled={busy}>
          {busy ? 'Escaneando…' : 'Escanear'}
        </button>
      </form>

      <div aria-live="polite">
        {result?.ok && (
          <section className="gate-result granted">
            <h3>{result.acceso.mensaje}</h3>
            <p>Entrada #{result.acceso.id}</p>
            <p>Ingreso: {formatTimestamp(result.acceso.hora_ingreso)}</p>
          </section>
        )}
        {result && !result.ok && (
          <section className="gate-result denied" role="alert">
            <h3>Acceso Denegado</h3>
            <p>{result.message}</p>
          </section>
        )}
      </div>

      {lastPurchase.length === 0 ? (
        <section className="card">
          <h3>Última compra</h3>
          <p className="empty">Todavía no compraste entradas en este navegador. Los códigos aparecerán acá.</p>
        </section>
      ) : (
        <section className="card">
          <h3>Última compra</h3>
          <p className="muted">Tocá un código para escanearlo.</p>
          <ul className="codes">
            {lastPurchase.map((entrada) => (
              <li key={entrada.id}>
                <button type="button" className="link" onClick={() => pick(entrada.codigo_qr)} disabled={busy}>
                  {entrada.codigo_qr}
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
