class ErrorDeDominio(Exception):
    """Base de los errores de negocio. El router no los conoce: los traduce el manejador."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class LugarNoEncontrado(ErrorDeDominio):
    def __init__(self):
        super().__init__("Lugar no encontrado")


class SectorNoEncontrado(ErrorDeDominio):
    def __init__(self):
        super().__init__("Sector no encontrado")


class EventoNoEncontrado(ErrorDeDominio):
    def __init__(self):
        super().__init__("Evento no encontrado")


class SectorNoEncontradoEnEvento(ErrorDeDominio):
    def __init__(self):
        super().__init__("El sector no tiene precio definido en este evento")


class CantidadInvalida(ErrorDeDominio):
    def __init__(self):
        super().__init__("Cantidad inválida")


class CapacidadInsuficiente(ErrorDeDominio):
    def __init__(self):
        super().__init__("Capacidad insuficiente")


class PreciosInvalidos(ErrorDeDominio):
    def __init__(self):
        super().__init__(
            "Debe definirse un precio para cada sector del lugar, sin repetir ni agregar otros"
        )


class ClienteNoEncontrado(ErrorDeDominio):
    def __init__(self):
        super().__init__("Cliente no encontrado")


class EntradaNoDisponible(ErrorDeDominio):
    def __init__(self):
        super().__init__("Los lugares seleccionados ya no se encuentran disponibles")


class EntradasDeDistintosEventos(ErrorDeDominio):
    def __init__(self):
        super().__init__("Las entradas deben pertenecer a un mismo evento")


class PagoDenegado(ErrorDeDominio):
    def __init__(self):
        super().__init__("Pago denegado")


class TransicionInvalida(ErrorDeDominio):
    def __init__(self):
        super().__init__("Transición de estado inválida")


class TicketInvalido(ErrorDeDominio):
    def __init__(self):
        super().__init__("Ticket Inválido o Inexistente")


class TicketNoEmitido(ErrorDeDominio):
    def __init__(self):
        super().__init__("Ticket no emitido / Falta de pago")


class EntradaYaUtilizada(ErrorDeDominio):
    def __init__(self):
        super().__init__("Entrada ya utilizada")


class EventoNoCorrespondeAlDia(ErrorDeDominio):
    def __init__(self):
        super().__init__("La entrada no corresponde al evento del día")
