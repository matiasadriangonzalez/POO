from seeder import inicializar_datos


def buscar_continente(continentes, nombre):
    for continente in continentes:
        if continente.get_nombre().lower() == nombre.lower():
            return continente
    return None


def buscar_pais(continentes, nombre):
    for continente in continentes:
        for pais in continente.get_paises():
            if pais.get_nombre().lower() == nombre.lower():
                return pais
    return None


def obtener_todos_los_paises(continentes):
    todos = []
    for continente in continentes:
        for pais in continente.get_paises():
            todos.append(pais)
    return todos


def ordenar_por_superficie(paises):
    lista = list(paises)
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j].get_superficie() < lista[j + 1].get_superficie():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def main():
    print("Cargando datos del mapa mundial...")
    continentes = inicializar_datos()
    nombres_continentes = ", ".join([c.get_nombre() for c in continentes])
    print(f"Datos cargados. Continentes disponibles: {nombres_continentes}\n")

    while True:
        print("\n=== Mapa Mundial ===")
        print("1. Listar países de un continente")
        print("2. Listar provincias/estados de un país")
        print("3. Listar países limítrofes de un país")
        print("4. Listar todos los países por superficie (mayor a menor)")
        print("5. Comparar superficie de 2 países")
        print("6. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del continente: ")
            continente = buscar_continente(continentes, nombre)
            if continente is None:
                print(f"No se encontró '{nombre}'. Disponibles: {nombres_continentes}")
            else:
                paises = continente.get_paises()
                print(f"\nPaíses de {continente.get_nombre()} ({len(paises)} países):")
                for p in paises:
                    print(f"  - {p.get_nombre():<30} Capital: {p.get_capital():<25} {p.get_superficie():>12,} km²")

        elif opcion == "2":
            nombre = input("Ingrese el nombre del país: ")
            pais = buscar_pais(continentes, nombre)
            if pais is None:
                print(f"No se encontró el país '{nombre}'.")
            else:
                provincias = pais.get_provincias()
                print(f"\nProvincias/Estados de {pais.get_nombre()} ({len(provincias)}):")
                for prov in provincias:
                    print(f"  - {prov.get_nombre()}")

        elif opcion == "3":
            nombre = input("Ingrese el nombre del país: ")
            pais = buscar_pais(continentes, nombre)
            if pais is None:
                print(f"No se encontró el país '{nombre}'.")
            else:
                limitrofes = pais.get_limitrofes()
                if not limitrofes:
                    print(f"{pais.get_nombre()} no tiene países limítrofes (es una isla).")
                else:
                    print(f"\nPaíses limítrofes de {pais.get_nombre()} ({len(limitrofes)}):")
                    for lim in limitrofes:
                        print(f"  - {lim.get_nombre()}")

        elif opcion == "4":
            todos = obtener_todos_los_paises(continentes)
            ordenados = ordenar_por_superficie(todos)
            print(f"\nTodos los países ordenados por superficie ({len(ordenados)} países):")
            for i, p in enumerate(ordenados, 1):
                print(f"  {i:3}. {p.get_nombre():<30} {p.get_superficie():>12,} km²  ({p.get_continente().get_nombre()})")

        elif opcion == "5":
            nombre1 = input("Ingrese el nombre del primer país: ")
            nombre2 = input("Ingrese el nombre del segundo país: ")
            pais1 = buscar_pais(continentes, nombre1)
            pais2 = buscar_pais(continentes, nombre2)
            if pais1 is None:
                print(f"No se encontró el país '{nombre1}'.")
            elif pais2 is None:
                print(f"No se encontró el país '{nombre2}'.")
            else:
                print(f"\n{pais1.get_nombre()}: {pais1.get_superficie():,} km²")
                print(f"{pais2.get_nombre()}: {pais2.get_superficie():,} km²")
                if pais1.get_superficie() > pais2.get_superficie():
                    print(f"→ {pais1.get_nombre()} tiene mayor superficie.")
                elif pais2.get_superficie() > pais1.get_superficie():
                    print(f"→ {pais2.get_nombre()} tiene mayor superficie.")
                else:
                    print("→ Ambos países tienen la misma superficie.")

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
