from factura import Factura
from impresor_factura_consola import ImpresorFacturaConsola

class TerminalPOS:
    def __init__(self, catalogo_productos):
        self.catalogo_productos = catalogo_productos
        self.impresor = ImpresorFacturaConsola()

    def iniciar_venta(self, tipo_comprobante):
        return Factura(tipo_comprobante)

    def registrar_item(self, factura, codigo_producto, cantidad, descuento_producto=None, descuento_cliente=None):
        producto = self.catalogo_productos.buscar_por_codigo(codigo_producto)
        factura.agregar_linea(producto, cantidad, descuento_producto, descuento_cliente)

    def finalizar_venta(self, factura):
        self.impresor.imprimir(factura)