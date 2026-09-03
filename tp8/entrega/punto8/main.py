from producto import Producto
from linea_factura import LineaFactura
from factura import Factura
from impresor_factura_consola import ImpresorFacturaConsola
from descuento import Descuento3x2, DescuentoPorcentaje, DescuentoPorVolumen, SinDescuento

if __name__ == "__main__":
    detergente = Producto("Detergente", 1000.0, 0.21)
    asado = Producto("Asado", 4000.0, 0.105)

    promo_3x2 = Descuento3x2()
    descuento_jubilado = DescuentoPorcentaje(0.15)
    descuento_volumen = DescuentoPorVolumen(cantidad_minima=5, porcentaje=0.10)

    linea1 = LineaFactura(6, detergente, descuento_producto=promo_3x2, descuento_cliente=descuento_jubilado)
    linea2 = LineaFactura(6, asado, descuento_producto=SinDescuento(), descuento_cliente=descuento_volumen)

    factura = Factura("B", [linea1, linea2])

    impresor = ImpresorFacturaConsola()
    impresor.imprimir(factura)
