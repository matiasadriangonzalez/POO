class Factura:
    def __init__(self, tipo_comprobante, lineas):
        self.tipo_comprobante = tipo_comprobante
        self.lineas = lineas

    def imprimir_factura(self):
        total_neto = 0.0
        for linea in self.lineas:
            # Factura ya NO calcula: solo le pregunta a su colaborador directo (linea)
            # La palabra "producto" no aparece en ningun lado de este archivo
            neto_linea = linea.calcular_subtotal_neto_con_descuento()
            total_neto += neto_linea
        print(f"Total Neto: ${total_neto}")
