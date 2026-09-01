class Factura:
    def __init__(self, tipo_comprobante, lineas):
        self.tipo_comprobante = tipo_comprobante
        self.lineas = lineas

    def calcular_total_neto(self):
        return sum(linea.calcular_subtotal_neto_con_descuento() for linea in self.lineas)

    def calcular_total_iva(self):
        return sum(linea.calcular_monto_iva() for linea in self.lineas)

    def calcular_total_iva_por_tasa(self, tasa):
        return sum(
            linea.calcular_monto_iva()
            for linea in self.lineas
            if linea.porcentaje_iva_historico == tasa
        )

    def calcular_total_final(self):
        return self.calcular_total_neto() + self.calcular_total_iva()