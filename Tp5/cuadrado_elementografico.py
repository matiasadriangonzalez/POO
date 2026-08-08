from elemento_grafico import ElementoGrafico
from punto import Punto


class Cuadrado(ElementoGrafico):
    """
    Cuadrado que hereda directamente de ElementoGrafico, no de Rectangulo.

    Al no heredar el contrato de Rectangulo (dos lados independientes con
    setLadoMenor/setLadoMayor), no existe ningún método heredado cuyo
    comportamiento haya que corregir sobrescribiéndolo. El Cuadrado define
    su propio contrato con un único atributo lado, por lo que cualquier
    ElementoGrafico puede sustituirse por un Cuadrado sin sorpresas: se
    respeta el Principio de Sustitución de Liskov.
    """

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str, lado: float):
        super().__init__(colorHex, posicionCentro, nombreCapa)
        self._lado = lado

    # --- Getters y Setters ---

    def getLado(self) -> float:
        return self._lado

    def setLado(self, lado: float):
        self._lado = lado

    # --- Métodos de cálculo ---

    def calcularArea(self) -> float:
        return self._lado ** 2

    def calcularPerimetro(self) -> float:
        return 4 * self._lado

    def escalar(self, factor: float):
        # Factor 0: el cuadrado colapsaría a un punto sin área ni perímetro.
        # Factor negativo: produce un lado negativo, sin sentido geométrico.
        if factor <= 0:
            raise ValueError(f"El factor de escala ({factor}) debe ser un número positivo.")
        self._lado *= factor

    def __str__(self) -> str:
        return f"Cuadrado {super().__str__()} | Lado: {self._lado}"
