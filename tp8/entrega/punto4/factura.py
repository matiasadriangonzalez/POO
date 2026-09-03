class Factura:
    def __init__(self, tipo_comprobante, lineas):
        self.tipo_comprobante = tipo_comprobante
        self.lineas = lineas

    # SOLUCION PUNTO 4: Factura ya NO tiene ningun print().
    # Solo expone metodos de calculo. La presentacion es responsabilidad de OTRA clase.
    def calcular_total_neto(self):
        return sum(linea.calcular_subtotal_neto_con_descuento() for linea in self.lineas)

    def calcular_total_iva(self):
        return sum(linea.calcular_monto_iva() for linea in self.lineas)

    def calcular_total_final(self):
        return self.calcular_total_neto() + self.calcular_total_iva()
