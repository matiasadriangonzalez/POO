from producto import Producto

class CatalogoProductos:
    def __init__(self):
        self._productos = {}

    def registrar_producto(self, codigo, nombre, precio_base, porcentaje_iva):
        nuevo_producto = Producto(nombre, precio_base, porcentaje_iva)
        self._productos[codigo] = nuevo_producto
        return nuevo_producto

    def buscar_por_codigo(self, codigo):
        return self._productos.get(codigo)

    def actualizar_precio(self, codigo, nuevo_precio):
        producto = self.buscar_por_codigo(codigo)
        if producto:
            producto.precio_base = nuevo_precio