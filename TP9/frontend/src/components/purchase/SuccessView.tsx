import { formatMoney } from '../../format'
import type { Pago } from '../../types'
import { TicketCard } from './TicketCard'

interface Props {
  pago: Pago
  onRestart: () => void
}

export function SuccessView({ pago, onRestart }: Props) {
  return (
    <section className="card success-card">
      <h3>3. ¡Compra realizada!</h3>
      <p>
        Venta #{pago.id} · {pago.estado} · <strong>{formatMoney(pago.total)}</strong>
      </p>
      <div className="tickets">
        {pago.entradas.map((entrada) => (
          <TicketCard key={entrada.id} entrada={entrada} />
        ))}
      </div>
      <p className="muted">Estos códigos también quedan disponibles en la pestaña Puerta.</p>
      <button type="button" onClick={onRestart}>
        Nueva compra
      </button>
    </section>
  )
}
