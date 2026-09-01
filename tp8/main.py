from producto import Producto
from linea_factura import LineaFactura
from factura import Factura
from impresor_factura_consola import ImpresorFacturaConsola

if __name__ == "__main__":
    limpieza = Producto("Detergente", 6000.0, 0.21)
    carne = Producto("Asado", 4000.0, 0.105)
    descuento = 0.15

    linea1 = LineaFactura(1, limpieza, descuento)
    linea2 = LineaFactura(1, carne, descuento)
    factura = Factura("A", descuento, [linea1, linea2])

    impresor = ImpresorFacturaConsola()
    impresor.imprimir(factura)