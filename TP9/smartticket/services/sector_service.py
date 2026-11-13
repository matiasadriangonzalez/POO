from excepciones import LugarNoEncontrado, SectorNoEncontrado
from models import Sector
from repositories import LugarRepository, SectorRepository


class SectorService:
    def __init__(self, lugares: LugarRepository, sectores: SectorRepository):
        self._lugares = lugares
        self._sectores = sectores

    def crear_sector(self, lugar_id: int, nombre: str, capacidad_maxima: int) -> Sector:
        if self._lugares.buscar_por_id(lugar_id) is None:
            raise LugarNoEncontrado()
        sector = Sector(lugar_id=lugar_id, nombre=nombre, capacidad_maxima=capacidad_maxima)
        return self._sectores.guardar(sector)

    def listar_sectores(self) -> list[Sector]:
        return self._sectores.listar()

    def obtener_sector(self, sector_id: int) -> Sector:
        sector = self._sectores.buscar_por_id(sector_id)
        if sector is None:
            raise SectorNoEncontrado()
        return sector
