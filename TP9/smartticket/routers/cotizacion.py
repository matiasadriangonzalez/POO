from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import EntradaRepositorySQL, EventoRepositorySQL
from schemas import CotizacionRequest, CotizacionResponse
from services.cotizacion_service import CotizacionService

router = APIRouter(prefix="/cotizar", tags=["Cotización"])


def get_cotizacion_service(db: Session = Depends(get_db)) -> CotizacionService:
    return CotizacionService(EventoRepositorySQL(db), EntradaRepositorySQL(db))


@router.post(
    "",
    response_model=CotizacionResponse,
    summary="Cotizar entradas (HU1)",
)
def cotizar(
    datos: CotizacionRequest,
    servicio: CotizacionService = Depends(get_cotizacion_service),
):
    """Calcula el costo total de una compra y devuelve las entradas elegidas."""
    return servicio.cotizar(datos.evento_id, datos.sector_id, datos.cantidad)
