from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Cotizacion:
    """Objeto de valor: no se persiste. Identifica las entradas elegidas y su costo total."""

    total: Decimal
    entrada_ids: list[int]
