from entero import Entero

def main():
    print("=== Prueba de la Clase Entero ===")
    numero = int(input("Ingrese un número entero: "))
    e = Entero(numero)

    print(f"\nNúmero: {e.get_numero()}")
    print(f"Cuadrado: {e.cuadrado()}")

    if e.es_par():
        print("Es PAR")
    else:
        print("No es par")

    if e.es_impar():
        print("Es IMPAR")
    else:
        print("No es impar")

    fact = e.factorial()
    if fact == -1:
        print("Factorial: no definido para números negativos")
    else:
        print(f"Factorial: {fact}")

    if e.es_primo():
        print("Es PRIMO")
    else:
        print("No es primo")

if __name__ == "__main__":
    main()
