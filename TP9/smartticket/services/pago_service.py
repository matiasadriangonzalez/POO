from excepciones import (
    ClienteNoEncontrado,
    EntradaNoDisponible,
    EntradasDeDistintosEventos,
    PagoDenegado,
)
from models import Entrada, EstadoVenta, Venta
from pasarela import DatosTarjeta, PasarelaPago
from repositories import ClienteRepository, EntradaRepository, VentaRepository


class PagoService:
    def __init__(
        self,
        clientes: ClienteRepository,
        entradas: EntradaRepository,
        ventas: VentaRepository,
        pasarela: PasarelaPago,
    ):
        self._clientes = clientes
        self._entradas = entradas
        self._ventas = ventas
        self._pasarela = pasarela

    def iniciar_pago(
        self, cliente_id: int, entrada_ids: list[int], tarjeta: DatosTarjeta
    ) -> Venta:
        cliente = self._clientes.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNoEncontrado()

        entradas = self._cargar_entradas_disponibles(entrada_ids)

        # Se reserva antes de cobrar: el UPDATE condicional del repositorio garantiza
        # que dos pagos concurrentes no se queden con las mismas entradas.
        for entrada in entradas:
            entrada.reservar()
        self._entradas.reservar(entradas)

        venta = Venta(cliente_id=cliente.id, estado=EstadoVenta.PENDIENTE, entradas=entradas)
        total = venta.calcular_total()

        try:
            respuesta = self._pasarela.procesar_pago(tarjeta, total)
        except Exception:
            self._liberar(entradas)
            raise
        if not respuesta.aprobado:
            self._liberar(entradas)
            raise PagoDenegado()

        venta.confirmar_pago()
        for entrada in entradas:
            entrada.emitir()
        return self._ventas.guardar(venta)

    def _cargar_entradas_disponibles(self, entrada_ids: list[int]) -> list[Entrada]:
        """Aborta antes de tocar nada si falta, se repite o no esta disponible alguna entrada."""
        entradas = self._entradas.buscar_por_ids(entrada_ids)
        faltan_o_se_repiten = len(entradas) != len(entrada_ids)
        if faltan_o_se_repiten or not all(e.esta_disponible() for e in entradas):
            raise EntradaNoDisponible()
        if len({entrada.evento_id for entrada in entradas}) > 1:
            raise EntradasDeDistintosEventos()
        return entradas

    def _liberar(self, entradas: list[Entrada]) -> None:
        for entrada in entradas:
            entrada.liberar()
        self._entradas.guardar(entradas)
