from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import ClienteRepositorySQL
from schemas import ClienteCreate, ClienteRead
from services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    return ClienteService(ClienteRepositorySQL(db))


@router.post("", response_model=ClienteRead, status_code=201, summary="Crear un cliente")
def crear_cliente(datos: ClienteCreate, servicio: ClienteService = Depends(get_cliente_service)):
    return servicio.crear_cliente(datos.nombre, datos.email)


@router.get("", response_model=list[ClienteRead], summary="Listar todos los clientes")
def listar_clientes(servicio: ClienteService = Depends(get_cliente_service)):
    return servicio.listar_clientes()


@router.get("/{cliente_id}", response_model=ClienteRead, summary="Buscar un cliente por ID")
def obtener_cliente(cliente_id: int, servicio: ClienteService = Depends(get_cliente_service)):
    return servicio.obtener_cliente(cliente_id)
