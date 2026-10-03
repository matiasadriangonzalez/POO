from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Lugar, Sector
from schemas import SectorCreate, SectorRead

router = APIRouter(prefix="/sectores", tags=["Sectores"])


@router.post("", response_model=SectorRead, status_code=201, summary="Crear un sector")
def crear_sector(datos: SectorCreate, db: Session = Depends(get_db)):
    if db.get(Lugar, datos.lugar_id) is None:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    sector = Sector(**datos.model_dump())
    db.add(sector)
    db.commit()
    db.refresh(sector)
    return sector


@router.get("", response_model=list[SectorRead], summary="Listar todos los sectores")
def listar_sectores(db: Session = Depends(get_db)):
    return db.query(Sector).all()


@router.get("/{sector_id}", response_model=SectorRead, summary="Buscar un sector por ID")
def obtener_sector(sector_id: int, db: Session = Depends(get_db)):
    sector = db.get(Sector, sector_id)
    if sector is None:
        raise HTTPException(status_code=404, detail="Sector no encontrado")
    return sector
