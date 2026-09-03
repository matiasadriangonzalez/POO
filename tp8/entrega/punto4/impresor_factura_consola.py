# Clase de Fabricacion Pura (GRASP): no representa ningun concepto
# del negocio de facturacion, existe solo para el detalle tecnico de imprimir.
class ImpresorFacturaConsola:
    def imprimir(self, factura):
        print(f"--- Factura tipo {factura.tipo_comprobante} ---")
        print(f"Neto: ${factura.calcular_total_neto():.2f}")
        print(f"IVA: ${factura.calcular_total_iva():.2f}")
        print(f"TOTAL A PAGAR: ${factura.calcular_total_final():.2f}")
