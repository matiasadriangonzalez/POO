class LineaFactura:
    def __init__(self, cantidad, producto, porcentaje_descuento=0.0):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva
        self.porcentaje_descuento = porcentaje_descuento

    def calcular_subtotal_bruto(self):
        # Renombrado: esto es el subtotal SIN descontar nada (antes se llamaba solo "calcular_subtotal")
        return self.cantidad * self.precio_unitario_historico

    # SOLUCION PUNTO 5: RECIEN ACA el nombre "con_descuento" es honesto,
    # porque RECIEN ACA el metodo realmente resta un descuento.
    def calcular_subtotal_neto_con_descuento(self):
        bruto = self.calcular_subtotal_bruto()
        descuento = bruto * self.porcentaje_descuento
        return bruto - descuento

    def calcular_monto_iva(self):
        # El IVA se calcula sobre el subtotal YA con descuento, linea por linea
        return self.calcular_subtotal_neto_con_descuento() * self.porcentaje_iva_historico
