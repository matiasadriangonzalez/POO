import { useCallback, useState } from 'react'
import { useLastPurchase } from './hooks/useLastPurchase'
import { ConfigPage } from './pages/ConfigPage'
import { GatePage } from './pages/GatePage'
import { GuidePage } from './pages/GuidePage'
import { PurchasePage } from './pages/PurchasePage'
import { TABS, type TabId } from './tabs'

export default function App() {
  const [tab, setTab] = useState<TabId>('guia')
  const lastPurchase = useLastPurchase()

  const navigate = useCallback((next: TabId) => {
    setTab(next)
    window.scrollTo({ top: 0 })
  }, [])

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
        {tab === 'guia' && <GuidePage onNavigate={navigate} />}
        {tab === 'config' && <ConfigPage />}
        {tab === 'comprar' && <PurchasePage onPurchased={lastPurchase.save} onNavigate={navigate} />}
        {tab === 'puerta' && <GatePage lastPurchase={lastPurchase.entradas} />}
      </main>
    </>
  )
}
