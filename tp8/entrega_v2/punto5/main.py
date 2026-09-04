from producto import Producto
from linea_factura import LineaFactura
from factura import Factura
from impresor_factura_consola import ImpresorFacturaConsola

if __name__ == "__main__":
    limpieza = Producto("Detergente", 6000.0, 0.21)
    carne = Producto("Asado", 4000.0, 0.105)
    descuento = 0.15  # 15%, ej: Jubilados

    linea1 = LineaFactura(1, limpieza, descuento)
    linea2 = LineaFactura(1, carne, descuento)
    factura = Factura("B", [linea1, linea2])

    impresor = ImpresorFacturaConsola()
    impresor.imprimir(factura)

    print("\n--- Verificacion matematica (exige la impresora de ARCA) ---")
    neto = factura.calcular_total_neto()
    iva = factura.calcular_total_iva()
    total = factura.calcular_total_final()
    print(f"Neto + IVA = {neto:.2f} + {iva:.2f} = {neto + iva:.2f}")
    print(f"Total Final = {total:.2f}")
    print("Coinciden exactamente:", round(neto + iva, 2) == round(total, 2))
