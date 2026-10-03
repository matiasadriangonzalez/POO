from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Lugar
from schemas import LugarCreate, LugarRead

router = APIRouter(prefix="/lugares", tags=["Lugares"])


@router.post("", response_model=LugarRead, status_code=201, summary="Crear un lugar")
def crear_lugar(datos: LugarCreate, db: Session = Depends(get_db)):
    lugar = Lugar(**datos.model_dump())
    db.add(lugar)
    db.commit()
    db.refresh(lugar)
    return lugar


@router.get("", response_model=list[LugarRead], summary="Listar todos los lugares")
def listar_lugares(db: Session = Depends(get_db)):
    return db.query(Lugar).all()


@router.get("/{lugar_id}", response_model=LugarRead, summary="Buscar un lugar por ID")
def obtener_lugar(lugar_id: int, db: Session = Depends(get_db)):
    lugar = db.get(Lugar, lugar_id)
    if lugar is None:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar
