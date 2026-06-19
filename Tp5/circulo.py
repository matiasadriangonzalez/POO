from elipse import Elipse
from punto import Punto


class Circulo(Elipse):

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str, radio: float):
        # El radio es igual en ambas dimensiones: un círculo es una elipse con R == r.
        super().__init__(colorHex, posicionCentro, nombreCapa, radio, radio)

    def setRadioMayor(self, radio: float):
        # Misma lógica que en Cuadrado: mantener ambos radios iguales.
        self._radioMayor = radio
        self._radioMenor = radio

    def setRadioMenor(self, radio: float):
        # Misma lógica que en Cuadrado: mantener ambos radios iguales.
        self._radioMayor = radio
        self._radioMenor = radio

    def __str__(self) -> str:
        return (f"Circulo [Capa: '{self._nombreCapa}' | Color: {self._colorHex} "
                f"| Centro: {self._posicionCentro} | Radio: {self._radioMayor}]")
