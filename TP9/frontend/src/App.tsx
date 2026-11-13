import { useCallback, useState } from 'react'
import { useLastPurchase } from './hooks/useLastPurchase'
import { useScenarioRunner } from './hooks/useScenarioRunner'
import { ConfigPage } from './pages/ConfigPage'
import { GatePage } from './pages/GatePage'
import { GuidePage } from './pages/GuidePage'
import { PurchasePage } from './pages/PurchasePage'
import { TABS, type TabId } from './tabs'

export default function App() {
  const [tab, setTab] = useState<TabId>('guia')
  const lastPurchase = useLastPurchase()
  // A new `nonce` remounts the gate page so the prefilled QR applies even when the code repeats.
  const [gatePrefill, setGatePrefill] = useState<{ code: string; nonce: number }>({ code: '', nonce: 0 })
  const runner = useScenarioRunner((_, result) => {
    if (result.qrs.length > 0) lastPurchase.save(result.qrs)
  })

  const navigate = useCallback((next: TabId) => {
    setTab(next)
    window.scrollTo({ top: 0 })
  }, [])

  const openGate = useCallback(
    (code: string) => {
      setGatePrefill((prev) => ({ code, nonce: prev.nonce + 1 }))
      navigate('puerta')
    },
    [navigate],
  )

  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark" aria-hidden="true">
              ST
            </span>
            <div>
              <h1>SmartTicket</h1>
              <p>Venta de entradas y control de acceso</p>
            </div>
          </div>
          <nav className="tabs" role="tablist" aria-label="Secciones">
            {TABS.map(({ id, label }) => (
              <button
                key={id}
                type="button"
                role="tab"
                id={`tab-${id}`}
                aria-selected={tab === id}
                aria-controls="main"
                className={tab === id ? 'tab active' : 'tab'}
                onClick={() => navigate(id)}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main id="main" role="tabpanel" aria-labelledby={`tab-${tab}`}>
        {tab === 'guia' && <GuidePage runner={runner} onOpenGate={openGate} />}
        {tab === 'config' && <ConfigPage />}
        {tab === 'comprar' && <PurchasePage onPurchased={lastPurchase.save} onNavigate={navigate} />}
        {tab === 'puerta' && <GatePage key={gatePrefill.nonce} initialCode={gatePrefill.code} lastPurchase={lastPurchase.entradas} />}
      </main>
    </>
  )
}
