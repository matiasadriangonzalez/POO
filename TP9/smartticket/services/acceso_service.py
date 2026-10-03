from datetime import datetime
from typing import Callable

from excepciones import TicketInvalido
from models import Entrada
from repositories import EntradaRepository


class AccesoService:
    def __init__(self, entradas: EntradaRepository, reloj: Callable[[], datetime]):
        self._entradas = entradas
        self._reloj = reloj

    def escanear_acceso(self, codigo_qr: str) -> Entrada:
        entrada = self._entradas.buscar_por_codigo_qr(codigo_qr)
        if entrada is None:
            raise TicketInvalido()

        # La entrada decide si puede entrar. El UPDATE condicional del repositorio garantiza
        # que dos escaneos simultaneos del mismo QR no hagan entrar a la entrada dos veces.
        entrada.registrar_ingreso(self._reloj())
        self._entradas.registrar_ingreso(entrada)
        return entrada
