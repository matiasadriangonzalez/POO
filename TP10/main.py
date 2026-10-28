# PARTE D: script principal para demostrar el manejo de excepciones.
from excepciones import (
    StringException,
    EnteroPositivoException,
    CollectionVaciaException,
    NoEncontradoException,
)
from empleado import Empleado
from empleado_service import EmpleadoService


if __name__ == "__main__":
    # 1. Se intenta crear empleados con datos inválidos. El objeto no llega
    # a construirse porque la validación lanza la excepción correspondiente.
    print("--- Empleados con datos inválidos ---")
    datos_invalidos = [
        ("Ana", -100),     # sueldo negativo
        ("Al", 1000),      # nombre muy corto
        (None, 1000),      # nombre None
        ("Luis", 0),       # sueldo cero
        ("Marta", None),   # sueldo None
    ]
    for nombre, sueldo in datos_invalidos:
        try:
            Empleado(nombre, sueldo)
        except (StringException, EnteroPositivoException) as error:
            print(f"Empleado({nombre!r}, {sueldo!r}) -> {error}")

    # 2. Se agrega un empleado válido para que la colección no esté vacía;
    # así eliminar("Pedro") demuestra específicamente NoEncontradoException.
    print("\n--- Eliminar un empleado inexistente ---")
    EmpleadoService.agregar(Empleado("Carla", 250000))

    try:
        EmpleadoService.eliminar("Pedro")
    except NoEncontradoException as error:
        print(error)

    # 3. Se elimina al único empleado para vaciar la colección y se calcula
    # el promedio para demostrar CollectionVaciaException.
    print("\n--- Promedio con lista vacía ---")
    EmpleadoService.eliminar("Carla")
    try:
        EmpleadoService.sueldo_promedio()
    except CollectionVaciaException as error:
        print(error)