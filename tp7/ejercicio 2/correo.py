from abc import ABC, abstractmethod

class Correo(ABC):
    @abstractmethod
    def calcular_costo(self, peso: float) -> float:
        pass

    