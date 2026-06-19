import math

from elemento_grafico import ElementoGrafico
from punto import Punto


class Elipse(ElementoGrafico):

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str,
                 radioMayor: float, radioMenor: float):
        super().__init__(colorHex, posicionCentro, nombreCapa)
        self._radioMayor = radioMayor
        self._radioMenor = radioMenor

    # --- Getters y Setters ---

    def getRadioMayor(self) -> float:
        return self._radioMayor

    def setRadioMayor(self, radioMayor: float):
        self._radioMayor = radioMayor

    def getRadioMenor(self) -> float:
        return self._radioMenor

    def setRadioMenor(self, radioMenor: float):
        self._radioMenor = radioMenor

    # --- Métodos de cálculo ---

    def calcularArea(self) -> float:
        return math.pi * self._radioMayor * self._radioMenor

    def calcularPerimetro(self) -> float:
        # Aproximación de Ramanujan — alta precisión para toda proporción de radios.
        h = ((self._radioMayor - self._radioMenor) ** 2) / ((self._radioMayor + self._radioMenor) ** 2)
        return math.pi * (self._radioMayor + self._radioMenor) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

    def escalar(self, factor: float):
        # Factor 0: la elipse colapsaría a un segmento sin área.
        # Factor negativo: radios negativos no tienen sentido geométrico.
        if factor <= 0:
            raise ValueError(f"El factor de escala ({factor}) debe ser un número positivo.")
        self._radioMayor *= factor
        self._radioMenor *= factor

    def __str__(self) -> str:
        return (f"Elipse {super().__str__()} "
                f"| RadioMayor: {self._radioMayor} | RadioMenor: {self._radioMenor}")
