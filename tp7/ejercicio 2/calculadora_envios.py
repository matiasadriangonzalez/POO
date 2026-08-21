from correo import Correo

class CalculadoraEnvios:
    def obtener_costo(self, correo: Correo, peso: float) -> float:
        return correo.calcular_costo(peso)