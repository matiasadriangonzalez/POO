from producto import Producto
from linea_factura import LineaFactura
from factura import Factura
from impresor_factura_consola import ImpresorFacturaConsola

if __name__ == "__main__":
    notebook = Producto("Notebook", 1000.0, 0.21)
    linea = LineaFactura(1, notebook)
    factura = Factura("A", [linea])

    impresor = ImpresorFacturaConsola()
    impresor.imprimir(factura)
