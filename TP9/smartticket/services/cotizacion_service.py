from cotizacion import Cotizacion
from excepciones import CantidadInvalida, CapacidadInsuficiente, EventoNoEncontrado
from repositories import EntradaRepository, EventoRepository


class CotizacionService:
    def __init__(self, eventos: EventoRepository, entradas: EntradaRepository):
        self._eventos = eventos
        self._entradas = entradas

    def cotizar(self, evento_id: int, sector_id: int, cantidad: int) -> Cotizacion:
        if cantidad <= 0:
            raise CantidadInvalida()

        evento = self._eventos.buscar_por_id(evento_id)
        if evento is None:
            raise EventoNoEncontrado()

        precio = evento.precio_de(sector_id)
        entradas = self._entradas.buscar_disponibles(evento_id, sector_id, cantidad)
        if len(entradas) < cantidad:
            raise CapacidadInsuficiente()

        return Cotizacion(
            total=precio.subtotal(cantidad),
            entrada_ids=[entrada.id for entrada in entradas],
        )
