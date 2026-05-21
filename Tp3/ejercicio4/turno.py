from datetime import date


class Turno:
    def __init__(self, nombre_persona, hora, fecha: date):
        self.__nombre_persona = nombre_persona
        self.__hora = hora
        self.__fecha = fecha

    def get_nombre_persona(self):
        return self.__nombre_persona

    def get_hora(self):
        return self.__hora

    def get_fecha(self):
        return self.__fecha

    def __str__(self):
        return f"{self.__fecha.strftime('%d/%m/%Y')} {self.__hora:02d}:00 — {self.__nombre_persona}"
