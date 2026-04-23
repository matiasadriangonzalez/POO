class Pais:
    def __init__(self, nombre, capital, superficie):
        self.__nombre = nombre
        self.__capital = capital
        self.__superficie = superficie
        self.__continente = None
        self.__provincias = []
        self.__limitrofes = []

    def get_nombre(self):
        return self.__nombre

    def get_capital(self):
        return self.__capital

    def get_superficie(self):
        return self.__superficie

    def get_continente(self):
        return self.__continente

    def set_continente(self, continente):
        self.__continente = continente

    def get_provincias(self):
        return self.__provincias

    def get_limitrofes(self):
        return self.__limitrofes

    def agregar_provincia(self, provincia):
        self.__provincias.append(provincia)

    def agregar_limitrofe(self, pais):
        self.__limitrofes.append(pais)

    def __str__(self):
        continente_nombre = self.__continente.get_nombre() if self.__continente else "Sin continente"
        return (f"{self.__nombre} | Capital: {self.__capital} | "
                f"Superficie: {self.__superficie:,} km² | Continente: {continente_nombre}")
