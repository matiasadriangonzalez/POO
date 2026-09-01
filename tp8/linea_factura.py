class LineaFactura:
    def __init__(self, cantidad, producto, porcentaje_descuento):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva
        self.porcentaje_descuento = porcentaje_descuento

    def calcular_subtotal_bruto(self):
        return self.cantidad * self.precio_unitario_historico

    def calcular_subtotal_neto_con_descuento(self):
        bruto = self.calcular_subtotal_bruto()
        descuento = bruto * self.porcentaje_descuento
        return bruto - descuento

    def calcular_monto_iva(self):
        return self.calcular_subtotal_neto_con_descuento() * self.porcentaje_iva_historico

    def calcular_total_linea(self):
        return self.calcular_subtotal_neto_con_descuento() + self.calcular_monto_iva()