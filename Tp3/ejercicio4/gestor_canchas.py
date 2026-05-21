from datetime import date
from cancha import Cancha
from turno import Turno
from turno_estado_dto import TurnoEstadoDTO


class GestorCanchas:
    CANTIDAD_CANCHAS = 3

    def __init__(self):
        self.__canchas = [Cancha(i + 1) for i in range(self.CANTIDAD_CANCHAS)]

    def get_cancha_por_numero(self, numero):
        for cancha in self.__canchas:
            if cancha.get_numero() == numero:
                return cancha
        return None

    def get_horario(self) -> tuple:
        return (Cancha.HORA_APERTURA, Cancha.HORA_CIERRE)

    def get_estado_dia(self, fecha: date) -> list:
        estado = []
        for cancha in self.__canchas:
            for hora in range(Cancha.HORA_APERTURA, Cancha.HORA_CIERRE + 1):
                turno = cancha.get_turno_por_hora(hora, fecha)
                estado.append(TurnoEstadoDTO(
                    numero_cancha=cancha.get_numero(),
                    hora=hora,
                    libre=turno is None,
                    nombre_persona=turno.get_nombre_persona() if turno else None
                ))
        return estado

    def reservar(self, numero_cancha: int, fecha: date, hora: int, nombre: str) -> bool:
        cancha = self.get_cancha_por_numero(numero_cancha)
        if cancha is None or not cancha.es_hora_valida(hora):
            return False
        return cancha.reservar_turno(Turno(nombre, hora, fecha))

    def cancelar(self, numero_cancha: int, fecha: date, hora: int) -> bool:
        cancha = self.get_cancha_por_numero(numero_cancha)
        if cancha is None:
            return False
        return cancha.cancelar_turno(hora, fecha)
