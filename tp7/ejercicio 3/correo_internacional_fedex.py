from icalculable import ICalculable
from irastreable import IRastreable
from iexportable import IExportable

class CorreoInternacionalFedEx(ICalculable, IRastreable, IExportable):
    def calcular_costo(self, peso):
        return peso * 45.0

    def rastrear_paquete_satelital(self):
        return "Ubicación satelital: en tránsito, Miami Hub"

    def generar_reporte_aduana(self):
        return "Reporte de aduana generado correctamente"