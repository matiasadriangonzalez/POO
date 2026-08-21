from correo import Correo

class OCA(Correo):
    def calcular_costo(self, peso: float) -> float:
        return peso * 15.0