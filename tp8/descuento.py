from abc import ABC, abstractmethod

class Descuento(ABC):
    @abstractmethod
    def aplicar(self, monto_base: float, cantidad: int = 1) -> float:
        pass


class SinDescuento(Descuento):
    def aplicar(self, monto_base: float, cantidad: int = 1) -> float:
        return 0.0


class Descuento3x2(Descuento):
    def aplicar(self, monto_base: float, cantidad: int = 1) -> float:
        if cantidad == 0:
            return 0.0
        precio_unitario = monto_base / cantidad
        unidades_gratis = cantidad // 3
        return precio_unitario * unidades_gratis


class DescuentoPorcentaje(Descuento):
    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje

    def aplicar(self, monto_base: float, cantidad: int = 1) -> float:
        return monto_base * self.porcentaje


class DescuentoPorVolumen(Descuento):
    def __init__(self, cantidad_minima: int, porcentaje: float):
        self.cantidad_minima = cantidad_minima
        self.porcentaje = porcentaje

    def aplicar(self, monto_base: float, cantidad: int = 1) -> float:
        if cantidad >= self.cantidad_minima:
            return monto_base * self.porcentaje
        return 0.0