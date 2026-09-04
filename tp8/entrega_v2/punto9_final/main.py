from catalogo_productos import CatalogoProductos
from terminal_pos import TerminalPOS
from impresor_factura_consola import ImpresorFacturaConsola
from descuento import Descuento3x2, DescuentoPorcentaje, DescuentoPorVolumen, SinDescuento

if __name__ == "__main__":
    # 1) CatalogoProductos crea y guarda los Producto
    catalogo = CatalogoProductos()
    catalogo.registrar_producto("DET001", "Detergente", 1000.0, 0.21)
    catalogo.registrar_producto("ASA001", "Asado", 4000.0, 0.105)

    # 2) TerminalPOS conoce el catalogo y decide que descuentos aplicar
    terminal = TerminalPOS(catalogo)

    promo_3x2 = Descuento3x2()
    descuento_jubilado = DescuentoPorcentaje(0.15)
    descuento_volumen = DescuentoPorVolumen(cantidad_minima=5, porcentaje=0.10)

    # 3) TerminalPOS crea la Factura (via emitir_factura)
    factura = terminal.emitir_factura("B", [
        ("DET001", 6, promo_3x2, descuento_jubilado),
        ("ASA001", 6, SinDescuento(), descuento_volumen),
    ])

    # Internamente, factura.agregar_linea() fue quien creo cada LineaFactura
    impresor = ImpresorFacturaConsola()
    impresor.imprimir(factura)
