from datetime import date
from gestor_canchas import GestorCanchas


def pedir_fecha():
    texto = input("Fecha (DD/MM/AAAA): ")
    dia, mes, anio = texto.split("/")
    return date(int(anio), int(mes), int(dia))


def mostrar_estado(dtos):
    cancha_actual = None
    for dto in dtos:
        if dto.numero_cancha != cancha_actual:
            cancha_actual = dto.numero_cancha
            print(f"\n  Cancha {dto.numero_cancha}:")
        if dto.libre:
            print(f"    {dto.hora:02d}:00 — LIBRE")
        else:
            print(f"    {dto.hora:02d}:00 — OCUPADO  ({dto.nombre_persona})")


def main():
    gestor = GestorCanchas()
    apertura, cierre = gestor.get_horario()

    while True:
        print("\n=== Complejo Deportivo — Fútbol 5 ===")
        print(f"Horario: {apertura:02d}:00 a {cierre:02d}:00")
        print("1. Ver estado de las canchas")
        print("2. Registrar reserva")
        print("3. Cancelar reserva")
        print("4. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            fecha = pedir_fecha()
            print(f"\n--- Estado del {fecha.strftime('%d/%m/%Y')} ---")
            mostrar_estado(gestor.get_estado_dia(fecha))

        elif opcion == "2":
            numero = int(input("Número de cancha (1, 2 o 3): "))
            fecha = pedir_fecha()
            hora = int(input(f"Hora de la reserva ({apertura} a {cierre}): "))
            nombre = input("Nombre de la persona: ")
            if gestor.reservar(numero, fecha, hora, nombre):
                print("Reserva exitosa.")
            else:
                print("Error: Turno ocupado.")

        elif opcion == "3":
            numero = int(input("Número de cancha (1, 2 o 3): "))
            fecha = pedir_fecha()
            hora = int(input("Hora a cancelar: "))
            if gestor.cancelar(numero, fecha, hora):
                print(f"Reserva de las {hora:02d}:00 del {fecha.strftime('%d/%m/%Y')} cancelada correctamente.")
            else:
                print("No existe reserva para los datos ingresados.")

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
