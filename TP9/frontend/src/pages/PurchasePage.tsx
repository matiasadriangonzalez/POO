import { useState } from 'react'
import { api } from '../api'
import { PageHeader } from '../components/PageHeader'
import { PaymentStep } from '../components/purchase/PaymentStep'
import { SelectionStep, type Selection } from '../components/purchase/SelectionStep'
import { Stepper } from '../components/purchase/Stepper'
import { SuccessView } from '../components/purchase/SuccessView'
import { useResource } from '../hooks/useResource'
import type { Navigate } from '../tabs'
import type { Cotizacion, EntradaPago, Pago } from '../types'

interface Props {
  onPurchased: (entradas: EntradaPago[]) => void
  onNavigate: Navigate
}

interface Quoted {
  selection: Selection
  quote: Cotizacion
}

export function PurchasePage({ onPurchased, onNavigate }: Props) {
  const eventos = useResource(api.listEventos)
  const sectores = useResource(api.listSectores)
  const clientes = useResource(api.listClientes)

  // the quote is kept here so the payment step pays exactly the reserved tickets
  const [quoted, setQuoted] = useState<Quoted | null>(null)
  const [pago, setPago] = useState<Pago | null>(null)

  const step = pago ? 3 : quoted ? 2 : 1

  function handlePaid(result: Pago) {
    setPago(result)
    onPurchased(result.entradas)
  }

  function restart() {
    setQuoted(null)
    setPago(null)
    eventos.reload()
  }

  return (
    <div className="narrow">
      <PageHeader
        title="Comprar entradas"
        subtitle="HU1 y HU2: elegí evento y sector, cotizá y pagá para recibir tus entradas con QR."
      />
      <Stepper current={step} />
      {pago ? (
        <SuccessView pago={pago} onRestart={restart} />
      ) : quoted ? (
        <PaymentStep
          selection={quoted.selection}
          quote={quoted.quote}
          clientes={clientes}
          onBack={() => setQuoted(null)}
          onPaid={handlePaid}
        />
      ) : (
        <SelectionStep
          eventos={eventos}
          sectores={sectores}
          onNavigate={onNavigate}
          onQuoted={(selection, quote) => setQuoted({ selection, quote })}
        />
      )}
    </div>
  )
}
