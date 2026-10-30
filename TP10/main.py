# PARTE D
from excepciones import (
    StringException,
    EnteroPositivoException,
    CollectionVaciaException,
    NoEncontradoException,
)
from empleado import Empleado
from empleado_service import EmpleadoService


if __name__ == "__main__":
    print("--- Empleados con datos inválidos ---")
    datos_invalidos = [
        ("Ana", -100),     
        ("Ma", 1000),      
        (None, 1000),      
        ("Luis", 0),       
        ("Marta", None),   
    ]
    for nombre, sueldo in datos_invalidos:
        try:
            Empleado(nombre, sueldo)
        except (StringException, EnteroPositivoException) as error:
            print(f"Empleado({nombre!r}, {sueldo!r}) -> {error}")

    print("\n--- Eliminar un empleado inexistente ---")
    EmpleadoService.agregar(Empleado("Carla", 250000))
    
    try:
        EmpleadoService.eliminar("Pedro")
    except NoEncontradoException as error:
        print(error)

    print("\n--- Promedio con lista vacía ---")
    EmpleadoService.eliminar("Carla")
    try:
        EmpleadoService.sueldo_promedio()
    except CollectionVaciaException as error:
        print(error)