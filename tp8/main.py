from catalogo_productos import CatalogoProductos
from terminal_pos import TerminalPOS
from descuento import Descuento3x2, DescuentoPorcentaje, DescuentoPorVolumen, SinDescuento

if __name__ == "__main__":
    catalogo = CatalogoProductos()
    catalogo.registrar_producto("DET001", "Detergente", 1000.0, 0.21)
    catalogo.registrar_producto("CAR001", "Asado", 4000.0, 0.105)

    terminal = TerminalPOS(catalogo)

    promo_3x2 = Descuento3x2()
    descuento_jubilado = DescuentoPorcentaje(0.15)
    descuento_volumen = DescuentoPorVolumen(cantidad_minima=5, porcentaje=0.10)

    factura = terminal.iniciar_venta("B")

    terminal.registrar_item(factura, "DET001", 6, descuento_producto=promo_3x2, descuento_cliente=descuento_jubilado)
    terminal.registrar_item(factura, "CAR001", 6, descuento_producto=SinDescuento(), descuento_cliente=descuento_volumen)

    terminal.finalizar_venta(factura)