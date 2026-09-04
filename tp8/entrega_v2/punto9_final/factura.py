from linea_factura import LineaFactura


class Factura:
    def __init__(self, tipo_comprobante):
        self.tipo_comprobante = tipo_comprobante
        self.lineas = []

    # PATRON CREADOR (punto 9): Factura es quien crea sus propias LineaFactura,
    # porque una linea no existe ni tiene sentido fuera de una factura (composicion
    # fuerte), y Factura ya tiene todo lo necesario (la coleccion self.lineas) para
    # inicializarla y guardarla.
    def agregar_linea(self, producto, cantidad, descuento_producto=None, descuento_cliente=None):
        linea = LineaFactura(cantidad, producto, descuento_producto, descuento_cliente)
        self.lineas.append(linea)
        return linea

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
