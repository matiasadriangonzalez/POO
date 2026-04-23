from cancha import Cancha
from turno import Turno


def mostrar_estado(canchas):
    for cancha in canchas:
        print(f"\n  Cancha {cancha.get_numero()}:")
        for hora in range(Cancha.HORA_APERTURA, Cancha.HORA_CIERRE + 1):
            turno = cancha.get_turno_por_hora(hora)
            if turno is None:
                print(f"    {hora:02d}:00 — LIBRE")
            else:
                print(f"    {hora:02d}:00 — OCUPADO  ({turno.get_nombre_persona()})")


def seleccionar_cancha(canchas):
    numero = int(input("Número de cancha (1, 2 o 3): "))
    for cancha in canchas:
        if cancha.get_numero() == numero:
            return cancha
    return None


def main():
    canchas = [Cancha(1), Cancha(2), Cancha(3)]

    while True:
        print("\n=== Complejo Deportivo — Fútbol 5 ===")
        print(f"Horario: {Cancha.HORA_APERTURA:02d}:00 a {Cancha.HORA_CIERRE:02d}:00")
        print("1. Ver estado de las canchas")
        print("2. Registrar reserva")
        print("3. Cancelar reserva")
        print("4. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\n--- Estado actual de las canchas ---")
            mostrar_estado(canchas)

        elif opcion == "2":
            cancha = seleccionar_cancha(canchas)
            if cancha is None:
                print("Número de cancha inválido. Ingrese 1, 2 o 3.")
            else:
                hora = int(input(f"Hora de la reserva ({Cancha.HORA_APERTURA} a {Cancha.HORA_CIERRE}): "))
                if not cancha.es_hora_valida(hora):
                    print(f"Hora inválida. El complejo abre de {Cancha.HORA_APERTURA:02d}:00 a {Cancha.HORA_CIERRE:02d}:00.")
                else:
                    nombre = input("Nombre de la persona: ")
                    turno = Turno(nombre, hora)
                    if cancha.reservar_turno(turno):
                        print("Reserva exitosa.")
                    else:
                        print("Error: Turno ocupado.")

        elif opcion == "3":
            cancha = seleccionar_cancha(canchas)
            if cancha is None:
                print("Número de cancha inválido. Ingrese 1, 2 o 3.")
            else:
                hora = int(input("Hora a cancelar: "))
                if cancha.cancelar_turno(hora):
                    print(f"Reserva de las {hora:02d}:00 cancelada correctamente.")
                else:
                    print(f"No existe reserva a las {hora:02d}:00 en la Cancha {cancha.get_numero()}.")

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
