class ImpresorFacturaConsola:
    def imprimir(self, factura):
        print(f"--- Factura tipo {factura.tipo_comprobante} ---")
        print(f"Neto: ${factura.calcular_total_neto():.2f}")
        print(f"IVA 21%: ${factura.calcular_total_iva_por_tasa(0.21):.2f}")
        print(f"IVA 10.5%: ${factura.calcular_total_iva_por_tasa(0.105):.2f}")
        print(f"IVA Total: ${factura.calcular_total_iva():.2f}")
        print(f"TOTAL A PAGAR: ${factura.calcular_total_final():.2f}")