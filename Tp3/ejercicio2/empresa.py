class Empresa:
    SALARIO_MINIMO = 360000  # Salario Mínimo Vital y Móvil vigente (actualizar si cambia)

    def __init__(self):
        self.__empleados = []

    def registrar_empleado(self, empleado):
        for e in self.__empleados:
            if e.get_dni() == empleado.get_dni():
                return False
        if empleado.get_sueldo() < Empresa.SALARIO_MINIMO:
            empleado.set_sueldo(Empresa.SALARIO_MINIMO)
        self.__empleados.append(empleado)
        return True

    def get_empleado_mayor_sueldo(self):
        if not self.__empleados:
            return None
        mayor = self.__empleados[0]
        for e in self.__empleados:
            if e.get_sueldo() > mayor.get_sueldo():
                mayor = e
        return mayor

    def get_sueldo_promedio(self):
        if not self.__empleados:
            return 0.0
        total = 0
        for e in self.__empleados:
            total += e.get_sueldo()
        return total / len(self.__empleados)

    def get_empleados(self):
        return self.__empleados
