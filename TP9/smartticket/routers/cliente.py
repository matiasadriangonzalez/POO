from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteRead

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteRead, status_code=201, summary="Crear un cliente")
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    cliente = Cliente(**datos.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.get("", response_model=list[ClienteRead], summary="Listar todos los clientes")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.get("/{cliente_id}", response_model=ClienteRead, summary="Buscar un cliente por ID")
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
