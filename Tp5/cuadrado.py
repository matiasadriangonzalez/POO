from rectangulo import Rectangulo
from punto import Punto


class Cuadrado(Rectangulo):

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str, lado: float):
        # super() recibe el mismo valor para ambos lados, garantizando que desde
        # su creación el cuadrado tenga todos sus lados iguales.
        super().__init__(colorHex, posicionCentro, nombreCapa, lado, lado)

    def setLadoMenor(self, lado: float):
        # Sobrescrito para mantener la integridad: al cambiar un lado, ambos cambian.
        self._ladoMenor = lado
        self._ladoMayor = lado

    def setLadoMayor(self, lado: float):
        # Sobrescrito para mantener la integridad: al cambiar un lado, ambos cambian.
        self._ladoMenor = lado
        self._ladoMayor = lado

    def __str__(self) -> str:
        return (f"Cuadrado [Capa: '{self._nombreCapa}' | Color: {self._colorHex} "
                f"| Centro: {self._posicionCentro} | Lado: {self._ladoMenor}]")
