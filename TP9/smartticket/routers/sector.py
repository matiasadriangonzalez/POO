from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import LugarRepositorySQL, SectorRepositorySQL
from schemas import SectorCreate, SectorRead
from services.sector_service import SectorService

router = APIRouter(prefix="/sectores", tags=["Sectores"])


def get_sector_service(db: Session = Depends(get_db)) -> SectorService:
    return SectorService(LugarRepositorySQL(db), SectorRepositorySQL(db))


@router.post("", response_model=SectorRead, status_code=201, summary="Crear un sector")
def crear_sector(datos: SectorCreate, servicio: SectorService = Depends(get_sector_service)):
    return servicio.crear_sector(datos.lugar_id, datos.nombre, datos.capacidad_maxima)


@router.get("", response_model=list[SectorRead], summary="Listar todos los sectores")
def listar_sectores(servicio: SectorService = Depends(get_sector_service)):
    return servicio.listar_sectores()


@router.get("/{sector_id}", response_model=SectorRead, summary="Buscar un sector por ID")
def obtener_sector(sector_id: int, servicio: SectorService = Depends(get_sector_service)):
    return servicio.obtener_sector(sector_id)
