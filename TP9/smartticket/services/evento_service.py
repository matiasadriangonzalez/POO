from datetime import datetime
from decimal import Decimal

from excepciones import EventoNoEncontrado, LugarNoEncontrado, PreciosInvalidos
from models import Evento, PrecioSector
from repositories import EventoRepository, LugarRepository


class EventoService:
    def __init__(self, lugares: LugarRepository, eventos: EventoRepository):
        self._lugares = lugares
        self._eventos = eventos

    def crear_evento(
        self,
        lugar_id: int,
        nombre: str,
        fecha: datetime,
        precios: list[tuple[int, Decimal]],
    ) -> Evento:
        lugar = self._lugares.buscar_por_id(lugar_id)
        if lugar is None:
            raise LugarNoEncontrado()

        sectores = {sector.id: sector for sector in lugar.sectores}
        ids_con_precio = [sector_id for sector_id, _ in precios]
        if len(ids_con_precio) != len(set(ids_con_precio)) or set(ids_con_precio) != set(sectores):
            raise PreciosInvalidos()

        evento = Evento(lugar_id=lugar.id, nombre=nombre, fecha=fecha)
        for sector_id, precio in precios:
            evento.precios.append(PrecioSector(sector=sectores[sector_id], precio=precio))
        evento.generar_entradas()
        return self._eventos.guardar(evento)

    def listar_eventos(self) -> list[Evento]:
        return self._eventos.listar()

    def obtener_evento(self, evento_id: int) -> Evento:
        evento = self._eventos.buscar_por_id(evento_id)
        if evento is None:
            raise EventoNoEncontrado()
        return evento
