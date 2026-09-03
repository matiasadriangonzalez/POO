from descuento import SinDescuento

class LineaFactura:
    def __init__(self, cantidad, producto, descuento_producto=None, descuento_cliente=None):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva
        # SOLUCION PUNTO 8: ya no es un "float" el descuento, son OBJETOS polimorficos
        self.descuento_producto = descuento_producto or SinDescuento()
        self.descuento_cliente = descuento_cliente or SinDescuento()

    def calcular_subtotal_bruto(self):
        return self.cantidad * self.precio_unitario_historico

    def calcular_subtotal_tras_descuento_producto(self):
        # Se aplica PRIMERO el descuento de producto (ej: 3x2)
        bruto = self.calcular_subtotal_bruto()
        descuento = self.descuento_producto.aplicar(bruto, self.cantidad)
        return bruto - descuento

    def calcular_subtotal_neto_con_descuento(self):
        # Y DESPUES, sobre ese resultado, el descuento de cliente (ej: Jubilado)
        subtotal_tras_producto = self.calcular_subtotal_tras_descuento_producto()
        descuento_cliente = self.descuento_cliente.aplicar(subtotal_tras_producto, self.cantidad)
        return subtotal_tras_producto - descuento_cliente

    def calcular_monto_iva(self):
        return self.calcular_subtotal_neto_con_descuento() * self.porcentaje_iva_historico

    def calcular_total_linea(self):
        return self.calcular_subtotal_neto_con_descuento() + self.calcular_monto_iva()
