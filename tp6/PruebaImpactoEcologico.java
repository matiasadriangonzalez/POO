import java.util.ArrayList;

/**
 * PruebaImpactoEcologico.
 * Crea objetos de Edificio, Auto y Bicicleta -tres clases sin relación
 * de herencia entre sí-, los coloca en una ArrayList<ImpactoEcologico>
 * y recorre esa lista invocando de forma POLIMÓRFICA el método
 * obtenerImpactoEcologico() de cada objeto: el mismo mensaje se envía
 * a todos, pero cada clase responde con su propio cálculo.
 */
public class PruebaImpactoEcologico {

    public static void main(String[] args) {
        // Se crean primero con su tipo concreto (Edificio, Auto, Bicicleta),
        // no con el tipo de la interfaz, para poder invocar el comportamiento
        // propio de cada una -encenderCalefaccion(), acelerar(), pedalear()-
        // que NO forma parte de ImpactoEcologico y por lo tanto no podría
        // invocarse a través de una variable de ese tipo (ver Ejercicio 2, TP6).
        Edificio oficina = new Edificio("Oficina Central", "electricidad", 45000);
        Edificio deposito = new Edificio("Depósito Norte", "gas natural", 3200);
        Auto corolla = new Auto("Toyota", "Corolla", 15000, 7.5, "nafta");
        Auto ranger = new Auto("Ford", "Ranger", 20000, 9.0, "gasoil");
        Bicicleta trek = new Bicicleta("Trek", "aluminio", 8);
        Bicicleta specialized = new Bicicleta("Specialized", "carbono", 10);

        System.out.println("=== Comportamiento propio de cada clase ===\n");
        oficina.encenderCalefaccion();
        corolla.acelerar();
        trek.pedalear();
        System.out.println();

        // A partir de acá se las trata "en forma general": todas se agregan
        // a una misma ArrayList<ImpactoEcologico> gracias a que las tres
        // implementan esa interfaz, aunque no tengan relación de herencia.
        ArrayList<ImpactoEcologico> lista = new ArrayList<>();
        lista.add(oficina);
        lista.add(deposito);
        lista.add(corolla);
        lista.add(ranger);
        lista.add(trek);
        lista.add(specialized);

        double impactoTotal = 0.0;

        System.out.println("=== Reporte de impacto ecológico ===\n");

        for (ImpactoEcologico objeto : lista) {
            // objeto es de tipo ImpactoEcologico (programación "en forma general"):
            // no sabemos ni nos importa si es un Edificio, un Auto o una Bicicleta.
            double impacto = objeto.obtenerImpactoEcologico();
            System.out.printf("%s%n   -> Impacto ecológico: %.2f kg de CO2e / año%n%n",
                    objeto, impacto);
            impactoTotal += impacto;
        }

        System.out.printf("Impacto ecológico TOTAL de la flota/parque: %.2f kg de CO2e / año%n",
                impactoTotal);
    }
}
