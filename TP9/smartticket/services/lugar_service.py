from excepciones import LugarNoEncontrado
from models import Lugar
from repositories import LugarRepository


class LugarService:
    def __init__(self, lugares: LugarRepository):
        self._lugares = lugares

    def crear_lugar(self, nombre: str, direccion: str) -> Lugar:
        return self._lugares.guardar(Lugar(nombre=nombre, direccion=direccion))

    def listar_lugares(self) -> list[Lugar]:
        return self._lugares.listar()

    def obtener_lugar(self, lugar_id: int) -> Lugar:
        lugar = self._lugares.buscar_por_id(lugar_id)
        if lugar is None:
            raise LugarNoEncontrado()
        return lugar
