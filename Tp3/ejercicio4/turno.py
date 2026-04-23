class Turno:
    def __init__(self, nombre_persona, hora):
        self.__nombre_persona = nombre_persona
        self.__hora = hora  # entero: 14 a 23

    def get_nombre_persona(self):
        return self.__nombre_persona

    def get_hora(self):
        return self.__hora

    def __str__(self):
        return f"{self.__hora:02d}:00 — {self.__nombre_persona}"
