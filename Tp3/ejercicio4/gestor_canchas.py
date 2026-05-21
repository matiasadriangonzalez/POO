from cancha import Cancha


class GestorCanchas:
    def __init__(self, cantidad_canchas):
        self.__canchas = [Cancha(i + 1) for i in range(cantidad_canchas)]

    def get_canchas(self):
        return self.__canchas

    def get_cancha_por_numero(self, numero):
        for cancha in self.__canchas:
            if cancha.get_numero() == numero:
                return cancha
        return None
