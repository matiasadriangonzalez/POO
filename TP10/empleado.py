# PARTE B: clase Empleado con validaciones fail-fast.
from excepciones import StringException, EnteroPositivoException


class Empleado:
    def __init__(self, nombre: str, sueldo: int):
        # El legajo se asigna más tarde, cuando el servicio registra al empleado.
        self.legajo = None
        # Se reutilizan los setters para mantener una sola implementación de
        # las reglas de validación del nombre y del sueldo.
        self.set_nombre(nombre)
        self.set_sueldo(sueldo)

    def set_nombre(self, nombre: str) -> None:
        # Además de None y la longitud, se valida el tipo para evitar errores
        # inesperados al usar len() con un dato que no sea texto.
        if nombre is None or not isinstance(nombre, str) or len(nombre) < 3:
            raise StringException("El nombre del empleado debe tener 3 o mas caracteres.")
        self.nombre = nombre

    def set_sueldo(self, sueldo: int) -> None:
        # bool es una subclase de int en Python; se excluye para que True no
        # sea aceptado accidentalmente como sueldo 1.
        if sueldo is None or not isinstance(sueldo, int) or isinstance(sueldo, bool) or sueldo <= 0:
            raise EnteroPositivoException("El sueldo del empleado debe ser mayor a 0.")
        self.sueldo = sueldo

    def set_legajo(self, legajo: int) -> None:
        if legajo is None or not isinstance(legajo, int) or isinstance(legajo, bool) or legajo <= 0:
            raise EnteroPositivoException("El legajo del empleado debe ser mayor a 0.")
        self.legajo = legajo