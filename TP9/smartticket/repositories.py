from abc import ABC, abstractmethod

from sqlalchemy import update
from sqlalchemy.orm import Session

from excepciones import EntradaNoDisponible, EntradaYaUtilizada
from models import Cliente, Entrada, EstadoEntrada, Evento, Lugar, Sector, Venta


class LugarRepository(ABC):
    @abstractmethod
    def buscar_por_id(self, lugar_id: int) -> Lugar | None: ...

    @abstractmethod
    def listar(self) -> list[Lugar]: ...

    @abstractmethod
    def guardar(self, lugar: Lugar) -> Lugar: ...


class SectorRepository(ABC):
    @abstractmethod
    def buscar_por_id(self, sector_id: int) -> Sector | None: ...

    @abstractmethod
    def listar(self) -> list[Sector]: ...

    @abstractmethod
    def guardar(self, sector: Sector) -> Sector: ...


class EventoRepository(ABC):
    @abstractmethod
    def buscar_por_id(self, evento_id: int) -> Evento | None: ...

    @abstractmethod
    def listar(self) -> list[Evento]: ...

    @abstractmethod
    def guardar(self, evento: Evento) -> Evento: ...


class EntradaRepository(ABC):
    @abstractmethod
    def buscar_disponibles(
        self, evento_id: int, sector_id: int, cantidad: int
    ) -> list[Entrada]:
        """Devuelve hasta `cantidad` entradas disponibles del evento y sector."""

    @abstractmethod
    def buscar_por_ids(self, entrada_ids: list[int]) -> list[Entrada]:
        """Devuelve las entradas que existen entre los ids pedidos."""

    @abstractmethod
    def reservar(self, entradas: list[Entrada]) -> None:
        """Persiste la reserva de forma atomica: todas o ninguna.

        Lanza EntradaNoDisponible si alguna dejo de estar disponible en la base.
        """

    @abstractmethod
    def guardar(self, entradas: list[Entrada]) -> None:
        """Persiste el estado actual de las entradas."""

    @abstractmethod
    def buscar_por_codigo_qr(self, codigo_qr: str) -> Entrada | None:
        """Devuelve la entrada con ese codigo QR o None si no existe."""

    @abstractmethod
    def registrar_ingreso(self, entrada: Entrada) -> None:
        """Persiste el ingreso (estado y hora) de forma atomica.

        Lanza EntradaYaUtilizada si la entrada dejo de estar emitida en la base.
        """


class ClienteRepository(ABC):
    @abstractmethod
    def buscar_por_id(self, cliente_id: int) -> Cliente | None: ...

    @abstractmethod
    def listar(self) -> list[Cliente]: ...

    @abstractmethod
    def guardar(self, cliente: Cliente) -> Cliente: ...


class VentaRepository(ABC):
    @abstractmethod
    def guardar(self, venta: Venta) -> Venta: ...


class LugarRepositorySQL(LugarRepository):
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_id(self, lugar_id: int) -> Lugar | None:
        return self._db.get(Lugar, lugar_id)

    def listar(self) -> list[Lugar]:
        return self._db.query(Lugar).all()

    def guardar(self, lugar: Lugar) -> Lugar:
        self._db.add(lugar)
        self._db.commit()
        self._db.refresh(lugar)
        return lugar


class SectorRepositorySQL(SectorRepository):
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_id(self, sector_id: int) -> Sector | None:
        return self._db.get(Sector, sector_id)

    def listar(self) -> list[Sector]:
        return self._db.query(Sector).all()

    def guardar(self, sector: Sector) -> Sector:
        self._db.add(sector)
        self._db.commit()
        self._db.refresh(sector)
        return sector


class EventoRepositorySQL(EventoRepository):
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_id(self, evento_id: int) -> Evento | None:
        return self._db.get(Evento, evento_id)

    def listar(self) -> list[Evento]:
        return self._db.query(Evento).all()

    def guardar(self, evento: Evento) -> Evento:
        self._db.add(evento)
        self._db.commit()
        self._db.refresh(evento)
        return evento


class EntradaRepositorySQL(EntradaRepository):
    def __init__(self, db: Session):
        self._db = db

    def buscar_disponibles(
        self, evento_id: int, sector_id: int, cantidad: int
    ) -> list[Entrada]:
        return (
            self._db.query(Entrada)
            .filter_by(
                evento_id=evento_id,
                sector_id=sector_id,
                estado=EstadoEntrada.DISPONIBLE,
            )
            .order_by(Entrada.id)
            .limit(cantidad)
            .all()
        )

    def buscar_por_ids(self, entrada_ids: list[int]) -> list[Entrada]:
        return self._db.query(Entrada).filter(Entrada.id.in_(entrada_ids)).all()

    def reservar(self, entradas: list[Entrada]) -> None:
        # UPDATE condicional: solo cambia las que siguen DISPONIBLES en la base. Si otro
        # pago se adelanto, el rowcount no coincide y se deshace todo.
        resultado = self._db.execute(
            update(Entrada)
            .where(
                Entrada.id.in_([entrada.id for entrada in entradas]),
                Entrada.estado == EstadoEntrada.DISPONIBLE,
            )
            .values(estado=EstadoEntrada.RESERVADA)
            .execution_options(synchronize_session=False)
        )
        if resultado.rowcount != len(entradas):
            self._db.rollback()
            raise EntradaNoDisponible()
        self._db.commit()

    def guardar(self, entradas: list[Entrada]) -> None:
        self._db.add_all(entradas)
        self._db.commit()

    def buscar_por_codigo_qr(self, codigo_qr: str) -> Entrada | None:
        return self._db.query(Entrada).filter_by(codigo_qr=codigo_qr).one_or_none()

    def registrar_ingreso(self, entrada: Entrada) -> None:
        # UPDATE condicional: solo entra si la entrada sigue EMITIDA en la base. Si otro
        # escaneo se adelanto, el rowcount es 0 y se deshace sin pisar su hora de ingreso.
        resultado = self._db.execute(
            update(Entrada)
            .where(
                Entrada.id == entrada.id,
                Entrada.estado == EstadoEntrada.EMITIDA,
            )
            .values(estado=EstadoEntrada.UTILIZADA, hora_ingreso=entrada.hora_ingreso)
            .execution_options(synchronize_session=False)
        )
        if resultado.rowcount != 1:
            self._db.rollback()
            raise EntradaYaUtilizada()
        self._db.commit()


class ClienteRepositorySQL(ClienteRepository):
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self._db.get(Cliente, cliente_id)

    def listar(self) -> list[Cliente]:
        return self._db.query(Cliente).all()

    def guardar(self, cliente: Cliente) -> Cliente:
        self._db.add(cliente)
        self._db.commit()
        self._db.refresh(cliente)
        return cliente


class VentaRepositorySQL(VentaRepository):
    def __init__(self, db: Session):
        self._db = db

    def guardar(self, venta: Venta) -> Venta:
        self._db.add(venta)
        self._db.commit()
        self._db.refresh(venta)
        return venta
