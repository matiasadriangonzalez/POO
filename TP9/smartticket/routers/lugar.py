from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import LugarRepositorySQL
from schemas import LugarCreate, LugarRead
from services.lugar_service import LugarService

router = APIRouter(prefix="/lugares", tags=["Lugares"])


def get_lugar_service(db: Session = Depends(get_db)) -> LugarService:
    return LugarService(LugarRepositorySQL(db))


@router.post("", response_model=LugarRead, status_code=201, summary="Crear un lugar")
def crear_lugar(datos: LugarCreate, servicio: LugarService = Depends(get_lugar_service)):
    return servicio.crear_lugar(datos.nombre, datos.direccion)


@router.get("", response_model=list[LugarRead], summary="Listar todos los lugares")
def listar_lugares(servicio: LugarService = Depends(get_lugar_service)):
    return servicio.listar_lugares()


@router.get("/{lugar_id}", response_model=LugarRead, summary="Buscar un lugar por ID")
def obtener_lugar(lugar_id: int, servicio: LugarService = Depends(get_lugar_service)):
    return servicio.obtener_lugar(lugar_id)
