from datetime import datetime
from typing import Callable

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import EntradaRepositorySQL
from schemas import AccesoRequest, AccesoResponse
from services.acceso_service import AccesoService

router = APIRouter(prefix="/escanear-acceso", tags=["Acceso"])


def get_reloj() -> Callable[[], datetime]:
    return datetime.now


def get_acceso_service(
    db: Session = Depends(get_db),
    reloj: Callable[[], datetime] = Depends(get_reloj),
) -> AccesoService:
    return AccesoService(EntradaRepositorySQL(db), reloj)


@router.post("", response_model=AccesoResponse, summary="Escanear QR en puerta (HU3)")
def escanear_acceso(
    datos: AccesoRequest,
    servicio: AccesoService = Depends(get_acceso_service),
):
    """Valida el código QR y registra el ingreso del espectador."""
    return servicio.escanear_acceso(datos.codigo_qr)
