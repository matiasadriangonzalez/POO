class TurnoEstadoDTO:
    def __init__(self, numero_cancha: int, hora: int, libre: bool, nombre_persona: str = None):
        self.numero_cancha = numero_cancha
        self.hora = hora
        self.libre = libre
        self.nombre_persona = nombre_persona
