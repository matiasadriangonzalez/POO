from abc import ABC, abstractmethod
from punto import Punto


class ElementoGrafico(ABC):
    """
    Superclase abstracta de todos los elementos visuales del motor de renderizado.

    Punto 5 – Arquitectura Abstracta:
    Se declara como clase abstracta (ABC) con los métodos calcularArea() y
    calcularPerimetro() marcados como @abstractmethod. Esto obliga a que TODA
    subclase concreta (Rectangulo, Elipse, Triangulo futuro, etc.) implemente
    esos métodos, garantizando su existencia en tiempo de compilación/carga y
    permitiendo llamarlos de forma polimórfica sobre una variable de tipo
    ElementoGrafico sin riesgo de AttributeError.
    """

    def __init__(self, colorHex: str, posicionCentro: Punto, nombreCapa: str):
        self._colorHex = colorHex
        self._posicionCentro = posicionCentro
        self._nombreCapa = nombreCapa

    # --- Getters y Setters ---

    def getColorHex(self) -> str:
        return self._colorHex

    def setColorHex(self, colorHex: str):
        self._colorHex = colorHex

    def getPosicionCentro(self) -> Punto:
        return self._posicionCentro

    def setPosicionCentro(self, posicion: Punto):
        self._posicionCentro = posicion

    def getNombreCapa(self) -> str:
        return self._nombreCapa

    def setNombreCapa(self, nombreCapa: str):
        self._nombreCapa = nombreCapa

    # --- Métodos de comportamiento ---

    def moverA(self, nuevoDestino: Punto):
        self._posicionCentro = nuevoDestino

    @abstractmethod
    def calcularArea(self) -> float:
        pass

    @abstractmethod
    def calcularPerimetro(self) -> float:
        pass

    def __str__(self) -> str:
        return (f"[Capa: '{self._nombreCapa}' | Color: {self._colorHex} "
                f"| Centro: {self._posicionCentro}]")
