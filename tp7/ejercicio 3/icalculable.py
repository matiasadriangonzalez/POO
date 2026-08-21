from abc import ABC, abstractmethod

class ICalculable(ABC):
    @abstractmethod
    def calcular_costo(self, peso):
        pass