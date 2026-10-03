from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Evento
from repositories import EventoRepositorySQL, LugarRepositorySQL
from schemas import EventoCreate, EventoRead
from services.evento_service import EventoService

router = APIRouter(prefix="/eventos", tags=["Eventos"])


def get_evento_service(db: Session = Depends(get_db)) -> EventoService:
    return EventoService(LugarRepositorySQL(db), EventoRepositorySQL(db))


@router.post(
    "",
    response_model=EventoRead,
    status_code=201,
    summary="Crear un evento con sus precios y generar sus entradas",
)
def crear_evento(datos: EventoCreate, servicio: EventoService = Depends(get_evento_service)):
    precios = [(p.sector_id, p.precio) for p in datos.precios]
    return servicio.crear_evento(datos.lugar_id, datos.nombre, datos.fecha, precios)


@router.get("", response_model=list[EventoRead], summary="Listar todos los eventos")
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()


@router.get("/{evento_id}", response_model=EventoRead, summary="Buscar un evento por ID")
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.get(Evento, evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento
