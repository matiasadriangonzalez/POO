class Factura:
    def __init__(self, tipo_comprobante, lineas):
        self.tipo_comprobante = tipo_comprobante
        self.lineas = lineas

    def imprimir_factura(self):
        total_neto = 0.0
        for linea in self.lineas:
            # Factura TODAVIA calcula ella misma (esto se corrige en el Punto 2)
            # pero ya usa el precio HISTORICO, no el vivo del producto
            neto_linea = linea.cantidad * linea.precio_unitario_historico
            total_neto += neto_linea
        print(f"Total Neto: ${total_neto}")
