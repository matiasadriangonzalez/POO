class Continente:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__paises = []

    def get_nombre(self):
        return self.__nombre

    def get_paises(self):
        return self.__paises

    def agregar_pais(self, pais):
        pais.set_continente(self)
        self.__paises.append(pais)

    def __str__(self):
        return f"{self.__nombre} ({len(self.__paises)} países)"
