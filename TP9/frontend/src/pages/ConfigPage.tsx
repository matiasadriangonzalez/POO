import { api } from '../api'
import { ClientesPanel } from '../components/config/ClientesPanel'
import { EventosPanel } from '../components/config/EventosPanel'
import { LugaresPanel } from '../components/config/LugaresPanel'
import { SectoresPanel } from '../components/config/SectoresPanel'
import { PageHeader } from '../components/PageHeader'
import { SeedSampleData } from '../components/SeedSampleData'
import { useResource } from '../hooks/useResource'

export function ConfigPage() {
  const lugares = useResource(api.listLugares)
  const sectores = useResource(api.listSectores)
  const clientes = useResource(api.listClientes)
  const eventos = useResource(api.listEventos)

  function reloadAll() {
    lugares.reload()
    sectores.reload()
    clientes.reload()
    eventos.reload()
  }

  return (
    <>
      <PageHeader
        title="Configuración"
        subtitle="Cargá los datos en orden: 1 Lugar, 2 Sector, 3 Cliente y 4 Evento. Cada paso usa lo anterior."
      />
      <SeedSampleData onSeeded={reloadAll} />
      <div className="grid">
        <LugaresPanel lugares={lugares} />
        <SectoresPanel lugares={lugares} sectores={sectores} />
        <ClientesPanel clientes={clientes} />
        <EventosPanel lugares={lugares} sectores={sectores} eventos={eventos} />
      </div>
    </>
  )
}
