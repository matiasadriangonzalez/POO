from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from models import EstadoEntrada, EstadoVenta


class LugarCreate(BaseModel):
    nombre: str
    direccion: str


class LugarRead(LugarCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SectorCreate(BaseModel):
    lugar_id: int
    nombre: str
    capacidad_maxima: int


class SectorRead(SectorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PrecioSectorCreate(BaseModel):
    sector_id: int
    precio: Decimal = Field(gt=0)


class PrecioSectorRead(PrecioSectorCreate):
    model_config = ConfigDict(from_attributes=True)


class EventoCreate(BaseModel):
    lugar_id: int
    nombre: str
    fecha: datetime
    precios: list[PrecioSectorCreate]


class EventoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lugar_id: int
    nombre: str
    fecha: datetime
    precios: list[PrecioSectorRead]


class CotizacionRequest(BaseModel):
    evento_id: int
    sector_id: int
    cantidad: int


class CotizacionResponse(BaseModel):
    total: Decimal
    entrada_ids: list[int]


class ClienteCreate(BaseModel):
    nombre: str
    email: str


class ClienteRead(ClienteCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TarjetaRequest(BaseModel):
    numero: str
    titular: str


class PagoRequest(BaseModel):
    cliente_id: int
    entrada_ids: list[int] = Field(min_length=1)
    tarjeta: TarjetaRequest


class EntradaPagoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo_qr: str
    estado: EstadoEntrada


class PagoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estado: EstadoVenta
    total: Decimal
    entradas: list[EntradaPagoRead]


class AccesoRequest(BaseModel):
    codigo_qr: str


class AccesoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mensaje: str = "Acceso Permitido"
    id: int
    codigo_qr: str
    estado: EstadoEntrada
    hora_ingreso: datetime
