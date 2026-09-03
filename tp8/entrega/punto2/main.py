from producto import Producto
from linea_factura import LineaFactura
from factura import Factura

if __name__ == "__main__":
    notebook = Producto("Notebook", 1000.0, 0.21)
    linea = LineaFactura(1, notebook)
    factura = Factura("A", [linea])

    print("=== Factura emitida HOY ===")
    factura.imprimir_factura()

    notebook.precio_base = 1500.0
    print(f"\nEl supermercado actualizo el precio a ${notebook.precio_base}")

    print("\n=== Reimpresion de la MISMA factura ===")
    factura.imprimir_factura()

    print("\n=== Verificacion Ley de Demeter ===")
    print("Subtotal calculado directamente por la linea:", linea.calcular_subtotal_neto_con_descuento())
