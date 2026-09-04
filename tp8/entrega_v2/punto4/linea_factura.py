class LineaFactura:
    def __init__(self, cantidad, producto):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario_historico

    # NUEVO en el Punto 4: ahora que se necesita mostrar el IVA por separado,
    # se agrega el calculo de IVA. Todavia SIN descuento (nombre honesto: calcular_iva)
    def calcular_iva(self):
        return self.calcular_subtotal() * self.porcentaje_iva_historico
