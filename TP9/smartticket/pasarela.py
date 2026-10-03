from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

# Tarjeta de prueba que la pasarela simulada rechaza. Esta regla vive solo en PasarelaPagoSimulada.
TARJETA_RECHAZADA = "4000000000000002"


@dataclass(frozen=True)
class DatosTarjeta:
    numero: str
    titular: str


@dataclass(frozen=True)
class RespuestaPago:
    aprobado: bool


class PasarelaPago(ABC):
    @abstractmethod
    def procesar_pago(self, tarjeta: DatosTarjeta, monto: Decimal) -> RespuestaPago:
        """Cobra `monto` a la tarjeta e informa si el pago fue aprobado."""


class PasarelaPagoSimulada(PasarelaPago):
    """Simula una pasarela externa: rechaza solo TARJETA_RECHAZADA y aprueba el resto."""

    def procesar_pago(self, tarjeta: DatosTarjeta, monto: Decimal) -> RespuestaPago:
        return RespuestaPago(aprobado=tarjeta.numero != TARJETA_RECHAZADA)
