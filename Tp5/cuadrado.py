from rectangulo import Rectangulo
from punto import Punto

# ============================================================
# ANÁLISIS: Cuadrado hereda de Rectángulo y el Principio de Sustitución de Liskov (LSP)
# ============================================================
# El LSP establece que cualquier objeto de una subclase debe poder reemplazar
# a un objeto de la superclase sin alterar el comportamiento correcto del programa.
#
# El problema concreto: Rectangulo garantiza (postcondición) que setLadoMenor() y
# setLadoMayor() son INDEPENDIENTES: puedo tener ladoMenor=3 y ladoMayor=7.
# Cuadrado ROMPE esa garantía al forzar que ambos lados sean siempre iguales.
# Si el código cliente tiene una variable de tipo Rectangulo apuntando a un
# Cuadrado y llama miRectangulo.setLadoMayor(10), espera que solo cambie el
# lado mayor. En cambio, el cuadrado también cambia el lado menor, produciendo
# un comportamiento inesperado e incorrecto.
#
# CONCLUSIÓN: Aunque matemáticamente un cuadrado ES un rectángulo, en POO la
# relación "es-un" del LSP no se cumple porque las precondiciones y postcondiciones
# de los setters cambian en la subclase. La alternativa correcta sería modelar
# Cuadrado heredando directamente de ElementoGrafico (con su propio atributo
# "lado"), o utilizando composición en lugar de herencia, para no violar el
# contrato que Rectangulo establece con sus clientes.
# ============================================================


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
