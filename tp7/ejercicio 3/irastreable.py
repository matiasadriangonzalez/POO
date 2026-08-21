from abc import ABC, abstractmethod

class IRastreable(ABC):
    @abstractmethod
    def rastrear_paquete_satelital(self):
        pass