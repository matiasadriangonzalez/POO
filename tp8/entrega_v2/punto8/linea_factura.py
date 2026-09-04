from descuento import SinDescuento

class LineaFactura:
    def __init__(self, cantidad, producto, descuento_producto=None, descuento_cliente=None):
        self.cantidad = cantidad
        self.producto = producto
        self.precio_unitario_historico = producto.precio_base
        self.porcentaje_iva_historico = producto.porcentaje_iva
        # CAMBIO en el Punto 8: antes "porcentaje_descuento" era un float.
        # Ahora son OBJETOS Descuento (polimorficos). El nombre del metodo de
        # abajo NO cambia (sigue siendo "con_descuento", eso ya era correcto
        # desde el Punto 5) pero la LOGICA INTERNA si cambia.
        self.descuento_producto = descuento_producto or SinDescuento()
        self.descuento_cliente = descuento_cliente or SinDescuento()

    def calcular_subtotal_bruto(self):
        return self.cantidad * self.precio_unitario_historico

    def calcular_subtotal_tras_descuento_producto(self):
        bruto = self.calcular_subtotal_bruto()
        descuento = self.descuento_producto.aplicar(bruto, self.cantidad)
        return bruto - descuento

    def calcular_subtotal_neto_con_descuento(self):
        subtotal_tras_producto = self.calcular_subtotal_tras_descuento_producto()
        descuento_cliente = self.descuento_cliente.aplicar(subtotal_tras_producto, self.cantidad)
        return subtotal_tras_producto - descuento_cliente

    def calcular_monto_iva(self):
        return self.calcular_subtotal_neto_con_descuento() * self.porcentaje_iva_historico

    def calcular_total_linea(self):
        return self.calcular_subtotal_neto_con_descuento() + self.calcular_monto_iva()
