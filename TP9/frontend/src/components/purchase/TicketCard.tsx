import { QRCodeSVG } from 'qrcode.react'
import { useState } from 'react'
import type { EntradaPago } from '../../types'

export function TicketCard({ entrada }: { entrada: EntradaPago }) {
  const [copied, setCopied] = useState(false)

  async function copy() {
    try {
      await navigator.clipboard.writeText(entrada.codigo_qr)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      // clipboard may be unavailable (insecure context); the code stays selectable as text
    }
  }

  return (
    <article className="ticket">
      <QRCodeSVG value={entrada.codigo_qr} size={150} title={`QR de la entrada ${entrada.id}`} />
      <p className="muted">Entrada #{entrada.id} · {entrada.estado}</p>
      <code>{entrada.codigo_qr}</code>
      <button type="button" className="secondary" onClick={copy}>
        {copied ? 'Copiado' : 'Copiar código'}
      </button>
    </article>
  )
}
