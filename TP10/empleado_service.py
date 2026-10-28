# PARTE C: servicio para administrar la colección de empleados.
from empleado import Empleado
from excepciones import CollectionVaciaException, NoEncontradoException


class EmpleadoService:
    # Atributos de clase: la colección y el contador se comparten entre llamadas.
    empleados = []
    proximo_legajo = 1

    @classmethod
    def agregar(cls, empleado: Empleado) -> bool:
        # Comprobación adicional: la consigna recibe un Empleado. Si el objeto
        # no lo es, se evita fallar más tarde con un error menos claro.
        if not isinstance(empleado, Empleado):
            raise TypeError("Se debe agregar una instancia de Empleado.")

        # set_legajo puede lanzar EnteroPositivoException. No se captura aquí:
        # la excepción se propaga al código que llamó a agregar().
        empleado.set_legajo(cls.proximo_legajo)
        cls.proximo_legajo += 1
        cls.empleados.append(empleado)
        return True

    @classmethod
    def mayor_sueldo(cls) -> Empleado:
        # max() requiere elementos; se verifica antes para lanzar la excepción
        # específica indicada en la consigna.
        if not cls.empleados:
            raise CollectionVaciaException("No hay empleados.")
        return max(cls.empleados, key=lambda empleado: empleado.sueldo)

    @classmethod
    def sueldo_promedio(cls) -> float:
        if not cls.empleados:
            raise CollectionVaciaException("No hay empleados.")
        return sum(empleado.sueldo for empleado in cls.empleados) / len(cls.empleados)

    @classmethod
    def eliminar(cls, nombre: str) -> None:
        # Se distinguen los dos casos pedidos: colección vacía y nombre ausente.
        if not cls.empleados:
            raise CollectionVaciaException("No hay empleados.")

        empleados_restantes = [empleado for empleado in cls.empleados if empleado.nombre != nombre]
        if len(empleados_restantes) == len(cls.empleados):
            raise NoEncontradoException("No se encontro el empleado.")

        # Solo se actualiza la colección si se encontró al menos una coincidencia.
        cls.empleados = empleados_restantes