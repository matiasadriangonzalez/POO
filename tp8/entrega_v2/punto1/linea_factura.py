class LineaFactura:
    def __init__(self, cantidad, producto):
        self.cantidad = cantidad
        self.producto = producto
        # SOLUCION PUNTO 1: se copian los valores en el momento de la venta
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva
        # Todavia NO hay ningun metodo de calculo aca (eso llega en el Punto 2)
