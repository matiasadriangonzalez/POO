import math

from elemento_grafico import ElementoGrafico
from punto import Punto


class Circulo(ElementoGrafico):
    """
    Circulo que hereda directamente de ElementoGrafico, no de Elipse.

    Al no heredar el contrato de Elipse (dos radios independientes con
    setRadioMayor/setRadioMenor), no existe ningún método heredado cuyo
    comportamiento haya que corregir sobrescribiéndolo. El Circulo define
    su propio contrato con un único atributo radio, por lo que cualquier
    ElementoGrafico puede sustituirse por un Circulo sin sorpresas: se
    respeta el Principio de Sustitución de Liskov.
    """

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str, radio: float):
        super().__init__(colorHex, posicionCentro, nombreCapa)
        self._radio = radio

    # --- Getters y Setters ---

    def getRadio(self) -> float:
        return self._radio

    def setRadio(self, radio: float):
        self._radio = radio

    # --- Métodos de cálculo ---

    def calcularArea(self) -> float:
        return math.pi * self._radio ** 2

    def calcularPerimetro(self) -> float:
        return 2 * math.pi * self._radio

    def escalar(self, factor: float):
        # Factor 0: el círculo colapsaría a un punto sin área ni perímetro.
        # Factor negativo: produce un radio negativo, sin sentido geométrico.
        if factor <= 0:
            raise ValueError(f"El factor de escala ({factor}) debe ser un número positivo.")
        self._radio *= factor

    def __str__(self) -> str:
        return f"Circulo {super().__str__()} | Radio: {self._radio}"
