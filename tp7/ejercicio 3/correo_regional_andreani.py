from icalculable import ICalculable
from irastreable import IRastreable

class CorreoRegionalAndreani(ICalculable, IRastreable):
    def calcular_costo(self, peso):
        return peso * 20.0

    def rastrear_paquete_satelital(self):
        return "Ubicación satelital: depósito central, CABA"