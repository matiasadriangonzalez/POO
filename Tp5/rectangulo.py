from elemento_grafico import ElementoGrafico
from punto import Punto


class Rectangulo(ElementoGrafico):

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str, ladoMenor: float, ladoMayor: float):
        super().__init__(colorHex, posicionCentro, nombreCapa)
        self._ladoMenor = ladoMenor
        self._ladoMayor = ladoMayor

    # --- Getters y Setters ---

    def getLadoMenor(self) -> float:
        return self._ladoMenor

    def setLadoMenor(self, ladoMenor: float):
        self._ladoMenor = ladoMenor

    def getLadoMayor(self) -> float:
        return self._ladoMayor

    def setLadoMayor(self, ladoMayor: float):
        self._ladoMayor = ladoMayor

    # --- Métodos de cálculo ---

    def calcularArea(self) -> float:
        return self._ladoMenor * self._ladoMayor

    def calcularPerimetro(self) -> float:
        return 2 * (self._ladoMenor + self._ladoMayor)

    def escalar(self, factor: float):
        # Factor 0: la figura colapsaría a un punto sin área ni perímetro.
        # Factor negativo: produce dimensiones negativas, sin sentido geométrico.
        # En ambos casos se rechaza la operación lanzando una excepción.
        if factor <= 0:
            raise ValueError(f"El factor de escala ({factor}) debe ser un número positivo.")
        self._ladoMenor *= factor
        self._ladoMayor *= factor

    def __str__(self) -> str:
        return (f"Rectangulo {super().__str__()} "
                f"| LadoMenor: {self._ladoMenor} | LadoMayor: {self._ladoMayor}")
