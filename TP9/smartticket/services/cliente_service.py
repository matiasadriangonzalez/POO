from excepciones import ClienteNoEncontrado
from models import Cliente
from repositories import ClienteRepository


class ClienteService:
    def __init__(self, clientes: ClienteRepository):
        self._clientes = clientes

    def crear_cliente(self, nombre: str, email: str) -> Cliente:
        return self._clientes.guardar(Cliente(nombre=nombre, email=email))

    def listar_clientes(self) -> list[Cliente]:
        return self._clientes.listar()

    def obtener_cliente(self, cliente_id: int) -> Cliente:
        cliente = self._clientes.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNoEncontrado()
        return cliente
