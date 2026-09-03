class LineaFactura:
    def __init__(self, cantidad, producto):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva

    # SOLUCION PUNTO 2 (Experto en Informacion + Ley de Demeter):
    # el calculo vive ACA, no en Factura. LineaFactura usa solo SUS propios atributos.
    def calcular_subtotal_neto_con_descuento(self):
        return self.cantidad * self.precio_unitario_historico
