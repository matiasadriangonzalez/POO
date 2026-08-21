from abc import ABC, abstractmethod

class IExportable(ABC):
    @abstractmethod
    def generar_reporte_aduana(self):
        pass