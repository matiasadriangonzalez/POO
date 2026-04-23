class Empleado:
    def __init__(self, nombre, dni, sueldo):
        self.__nombre = nombre
        self.__dni = dni
        self.__sueldo = sueldo

    def get_nombre(self):
        return self.__nombre

    def get_dni(self):
        return self.__dni

    def get_sueldo(self):
        return self.__sueldo

    def set_sueldo(self, sueldo):
        self.__sueldo = sueldo
