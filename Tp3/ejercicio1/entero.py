class Entero:
    def __init__(self, numero):
        self.__numero = numero

    def get_numero(self):
        return self.__numero

    def set_numero(self, numero):
        self.__numero = numero

    def cuadrado(self):
        return self.__numero * self.__numero

    def es_par(self):
        return self.__numero % 2 == 0

    def es_impar(self):
        return self.__numero % 2 != 0

    def factorial(self):
        if self.__numero < 0:
            return -1
        resultado = 1
        for i in range(1, self.__numero + 1):
            resultado *= i
        return resultado

    def es_primo(self):
        if self.__numero < 2:
            return False
        for i in range(2, self.__numero):
            if self.__numero % i == 0:
                return False
        return True
