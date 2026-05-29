class Cancha:
    HORA_APERTURA = 14
    HORA_CIERRE = 23

    def __init__(self, numero):
        self.__numero = numero
        self.__turnos = [] 

    def get_numero(self):
        return self.__numero

    def es_hora_valida(self, hora):
        return self.HORA_APERTURA <= hora <= self.HORA_CIERRE

    def reservar_turno(self, turno):
        for t in self.__turnos:
            if t.get_hora() == turno.get_hora() and t.get_fecha() == turno.get_fecha():
                return False
        self.__turnos.append(turno)
        return True

    def cancelar_turno(self, hora, fecha):
        for t in self.__turnos:
            if t.get_hora() == hora and t.get_fecha() == fecha:
                self.__turnos.remove(t)
                return True
        return False

    def get_turno_por_hora(self, hora, fecha):
        for t in self.__turnos:
            if t.get_hora() == hora and t.get_fecha() == fecha:
                return t
        return None