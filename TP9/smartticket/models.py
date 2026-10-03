import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from excepciones import (
    EntradaNoDisponible,
    EntradaYaUtilizada,
    EventoNoCorrespondeAlDia,
    SectorNoEncontradoEnEvento,
    TicketNoEmitido,
    TransicionInvalida,
)


class EstadoEntrada(enum.Enum):
    DISPONIBLE = "Disponible"
    RESERVADA = "Reservada"
    EMITIDA = "Emitida"
    UTILIZADA = "Utilizada"


class EstadoVenta(enum.Enum):
    PENDIENTE = "Pendiente"
    PAGADA = "Pagada"
    CANCELADA = "Cancelada"


class Lugar(Base):
    __tablename__ = "lugares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    direccion: Mapped[str] = mapped_column(String)

    sectores: Mapped[list["Sector"]] = relationship()


class Sector(Base):
    __tablename__ = "sectores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lugar_id: Mapped[int] = mapped_column(ForeignKey("lugares.id"))
    nombre: Mapped[str] = mapped_column(String)
    capacidad_maxima: Mapped[int] = mapped_column(Integer)


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lugar_id: Mapped[int] = mapped_column(ForeignKey("lugares.id"))
    nombre: Mapped[str] = mapped_column(String)
    fecha: Mapped[datetime] = mapped_column(DateTime)

    precios: Mapped[list["PrecioSector"]] = relationship(cascade="all, delete-orphan")
    entradas: Mapped[list["Entrada"]] = relationship(
        back_populates="evento", cascade="all, delete-orphan"
    )

    def precio_de(self, sector_id: int) -> "PrecioSector":
        for precio in self.precios:
            if precio.sector_id == sector_id:
                return precio
        raise SectorNoEncontradoEnEvento()

    def es_del_dia(self, ahora: datetime) -> bool:
        return self.fecha.date() == ahora.date()

    def generar_entradas(self) -> list["Entrada"]:
        """Crea una entrada por cada lugar físico de cada sector con precio."""
        for precio in self.precios:
            for _ in range(precio.sector.capacidad_maxima):
                self.entradas.append(
                    Entrada(sector_id=precio.sector.id, codigo_qr=uuid.uuid4().hex)
                )
        return self.entradas


class PrecioSector(Base):
    __tablename__ = "precios_sector"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id"))
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectores.id"))
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    sector: Mapped["Sector"] = relationship()

    def subtotal(self, cantidad: int) -> Decimal:
        return self.precio * cantidad


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    estado: Mapped[EstadoVenta] = mapped_column(
        Enum(EstadoVenta), default=EstadoVenta.PENDIENTE
    )
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))

    entradas: Mapped[list["Entrada"]] = relationship()

    def calcular_total(self) -> Decimal:
        self.total = sum((entrada.precio() for entrada in self.entradas), Decimal("0"))
        return self.total

    def confirmar_pago(self) -> None:
        if self.estado != EstadoVenta.PENDIENTE:
            raise TransicionInvalida()
        self.estado = EstadoVenta.PAGADA


class Entrada(Base):
    __tablename__ = "entradas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id"))
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectores.id"))
    venta_id: Mapped[int | None] = mapped_column(ForeignKey("ventas.id"), nullable=True)
    estado: Mapped[EstadoEntrada] = mapped_column(
        Enum(EstadoEntrada), default=EstadoEntrada.DISPONIBLE
    )
    codigo_qr: Mapped[str] = mapped_column(String, unique=True)
    hora_ingreso: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    evento: Mapped["Evento"] = relationship(back_populates="entradas")

    def precio(self) -> Decimal:
        return self.evento.precio_de(self.sector_id).precio

    def esta_disponible(self) -> bool:
        return self.estado == EstadoEntrada.DISPONIBLE

    def reservar(self) -> None:
        if not self.esta_disponible():
            raise EntradaNoDisponible()
        self.estado = EstadoEntrada.RESERVADA

    def liberar(self) -> None:
        if self.estado != EstadoEntrada.RESERVADA:
            raise TransicionInvalida()
        self.estado = EstadoEntrada.DISPONIBLE

    def emitir(self) -> None:
        if self.estado != EstadoEntrada.RESERVADA:
            raise TransicionInvalida()
        self.estado = EstadoEntrada.EMITIDA

    def registrar_ingreso(self, hora: datetime) -> None:
        # Orden de validacion: estado primero, fecha del evento despues. Si rechaza, no toca nada.
        if self.estado == EstadoEntrada.UTILIZADA:
            raise EntradaYaUtilizada()
        if self.estado != EstadoEntrada.EMITIDA:
            raise TicketNoEmitido()
        if not self.evento.es_del_dia(hora):
            raise EventoNoCorrespondeAlDia()
        self.estado = EstadoEntrada.UTILIZADA
        self.hora_ingreso = hora
