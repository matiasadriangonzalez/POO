from correo import Correo

class FedEx(Correo):
    def calcular_costo(self, peso: float) -> float:
        return (peso * 50.0) + 100.0