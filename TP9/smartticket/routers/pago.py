from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from pasarela import DatosTarjeta, PasarelaPago, PasarelaPagoSimulada
from repositories import ClienteRepositorySQL, EntradaRepositorySQL, VentaRepositorySQL
from schemas import PagoRequest, PagoResponse
from services.pago_service import PagoService

router = APIRouter(prefix="/iniciar-pago", tags=["Pago"])


def get_pasarela() -> PasarelaPago:
    return PasarelaPagoSimulada()


def get_pago_service(
    db: Session = Depends(get_db),
    pasarela: PasarelaPago = Depends(get_pasarela),
) -> PagoService:
    return PagoService(
        ClienteRepositorySQL(db),
        EntradaRepositorySQL(db),
        VentaRepositorySQL(db),
        pasarela,
    )


@router.post("", response_model=PagoResponse, summary="Pagar y emitir entradas (HU2)")
def iniciar_pago(
    datos: PagoRequest,
    servicio: PagoService = Depends(get_pago_service),
):
    """Procesa el pago con tarjeta y emite las entradas con su código QR."""
    tarjeta = DatosTarjeta(numero=datos.tarjeta.numero, titular=datos.tarjeta.titular)
    return servicio.iniciar_pago(datos.cliente_id, datos.entrada_ids, tarjeta)
