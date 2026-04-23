from empleado import Empleado
from empresa import Empresa

def main():
    empresa = Empresa()

    while True:
        print("\n=== Gestión de Empleados ===")
        print("1. Registrar empleado")
        print("2. Ver empleado con mayor sueldo")
        print("3. Ver sueldo promedio")
        print("4. Listar todos los empleados")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            dni = input("DNI: ")
            sueldo = float(input("Sueldo: "))
            empleado = Empleado(nombre, dni, sueldo)
            if empresa.registrar_empleado(empleado):
                print(f"Empleado '{nombre}' registrado correctamente.")
                if empleado.get_sueldo() != sueldo:
                    print(f"Aviso: el sueldo fue ajustado al mínimo de ${Empleado.SALARIO_MINIMO:,.0f}")
            else:
                print(f"Error: ya existe un empleado con DNI {dni}.")

        elif opcion == "2":
            mayor = empresa.get_empleado_mayor_sueldo()
            if mayor is None:
                print("No hay empleados registrados.")
            else:
                print(f"Mayor sueldo: {mayor.get_nombre()} (DNI: {mayor.get_dni()}) — ${mayor.get_sueldo():,.2f}")

        elif opcion == "3":
            promedio = empresa.get_sueldo_promedio()
            if promedio == 0.0:
                print("No hay empleados registrados.")
            else:
                print(f"Sueldo promedio: ${promedio:,.2f}")

        elif opcion == "4":
            empleados = empresa.get_empleados()
            if not empleados:
                print("No hay empleados registrados.")
            else:
                print("\n--- Lista de Empleados ---")
                for e in empleados:
                    print(f"  {e.get_nombre()} | DNI: {e.get_dni()} | Sueldo: ${e.get_sueldo():,.2f}")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
