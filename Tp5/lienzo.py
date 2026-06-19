from typing import List
from elemento_grafico import ElementoGrafico


class Lienzo:
    """Motor de renderizado: contiene y gestiona la colección de elementos gráficos."""

    def __init__(self):
        self._elementos: List[ElementoGrafico] = []

    def agregar(self, elemento: ElementoGrafico):
        self._elementos.append(elemento)

    def getElementos(self) -> List[ElementoGrafico]:
        return self._elementos

    def __len__(self) -> int:
        return len(self._elementos)
