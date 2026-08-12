from punto import Punto
from rectangulo import Rectangulo
from elipse import Elipse
from cuadrado_elementografico import Cuadrado
from circulo_elementografico import Circulo
from lienzo import Lienzo


def main():
    lienzo = Lienzo()

    # --- Instanciación de figuras (Punto 4) ---
    r1  = Rectangulo("#FF0000", Punto(10, 20), "capa_rects",     3.0,  7.0)
    r2  = Rectangulo("#00FF00", Punto(5,  5),  "capa_rects",     4.0,  9.0)
    e1  = Elipse    ("#0000FF", Punto(15, 15), "capa_elipses",   6.0,  4.0)
    e2  = Elipse    ("#FFFF00", Punto(8,  12), "capa_elipses",   5.0,  3.0)
    c1  = Cuadrado  ("#FF00FF", Punto(2,  2),  "capa_cuadrados", 5.0)
    c2  = Cuadrado  ("#00FFFF", Punto(7,  7),  "capa_cuadrados", 8.0)
    ci1 = Circulo   ("#FFA500", Punto(0,  10), "capa_circulos",  4.0)
    ci2 = Circulo   ("#800080", Punto(3,  3),  "capa_circulos",  6.0)

    for figura in [r1, r2, e1, e2, c1, c2, ci1, ci2]:
        lienzo.agregar(figura)

    print("=" * 65)
    print("ESTADO INICIAL DEL LIENZO")
    print("=" * 65)
    for elemento in lienzo.getElementos():
        print(elemento)

    print("\n" + "=" * 65)
    print("APLICANDO FILTRO DE ESCALA DE GRISES Y CENTRANDO EN (0,0)")
    print("=" * 65)

    area_total = 0.0
    for elemento in lienzo.getElementos():
        elemento.setColorHex("#808080")
        elemento.moverA(Punto(0, 0))
        area_total += elemento.calcularArea()  # Seguro gracias a la abstracción

    print(f"\nÁrea total ocupada: {area_total:.2f} píxeles²")

    print("\nESTADO FINAL DEL LIENZO")
    print("-" * 65)
    for elemento in lienzo.getElementos():
        print(elemento)


if __name__ == "__main__":
    main()
