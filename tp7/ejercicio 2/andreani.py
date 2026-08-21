from correo import Correo

class Andreani(Correo):
    def calcular_costo(self, peso: float) -> float:
        return peso * 20.0