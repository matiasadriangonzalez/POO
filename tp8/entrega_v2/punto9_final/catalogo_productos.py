from producto import Producto


class CatalogoProductos:
    """
    PATRON CREADOR (punto 9): esta clase es la unica responsable de crear
    (instanciar) los objetos Producto. Ninguna otra clase del sistema
    (ni Factura, ni TerminalPOS) crea un Producto directamente: se lo piden
    a este catalogo. Asi se evita que las clases transaccionales queden
    acopladas a como se arma el inventario.
    """

    def __init__(self):
        self.productos = {}  # codigo -> Producto

    def registrar_producto(self, codigo, nombre, precio_base, porcentaje_iva):
        producto = Producto(nombre, precio_base, porcentaje_iva)
        self.productos[codigo] = producto
        return producto

    def buscar_por_codigo(self, codigo):
        return self.productos[codigo]

    def actualizar_precio(self, codigo, nuevo_precio):
        self.productos[codigo].precio_base = nuevo_precio
