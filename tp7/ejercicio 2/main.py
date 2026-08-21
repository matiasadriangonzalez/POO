from calculadora_envios import CalculadoraEnvios
from oca import OCA
from fedex import FedEx
from andreani import Andreani

if __name__ == "__main__":
    calculadora = CalculadoraEnvios()
    print("OCA 10kg:", calculadora.obtener_costo(OCA(), 10))
    print("FedEx 10kg:", calculadora.obtener_costo(FedEx(), 10))
    print("Andreani 10kg:", calculadora.obtener_costo(Andreani(), 10))