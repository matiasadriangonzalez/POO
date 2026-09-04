from factura import Factura


class TerminalPOS:
    """
    PATRON CREADOR (punto 9): TerminalPOS es la clase controladora del punto
    de venta. Es quien crea la Factura, porque es quien tiene el contexto
    completo de la operacion: sabe que tipo de comprobante corresponde
    ("A" o "B"), conoce al catalogo de productos, y decide que estrategias
    de descuento (objetos Descuento del punto 8) se aplican en cada linea.
    """

    def __init__(self, catalogo_productos):
        self.catalogo_productos = catalogo_productos

    def emitir_factura(self, tipo_comprobante, items):
        """
        items: lista de tuplas (codigo_producto, cantidad, descuento_producto, descuento_cliente)
        """
        factura = Factura(tipo_comprobante)
        for codigo, cantidad, descuento_producto, descuento_cliente in items:
            producto = self.catalogo_productos.buscar_por_codigo(codigo)
            factura.agregar_linea(producto, cantidad, descuento_producto, descuento_cliente)
        return factura
