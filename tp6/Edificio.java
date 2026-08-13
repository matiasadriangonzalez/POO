/**
 * Clase Edificio.
 * No tiene relación de herencia con Auto ni con Bicicleta; solo comparte
 * con ellas el hecho de implementar la interfaz ImpactoEcologico.
 */
public class Edificio implements ImpactoEcologico {

    // Factores de emisión aproximados (kg de CO2 por unidad de consumo)
    private static final double FACTOR_GAS_NATURAL = 2.75;  // kg CO2 por m3
    private static final double FACTOR_ELECTRICIDAD = 0.40; // kg CO2 por kWh
    private static final double FACTOR_GASOIL = 2.52;       // kg CO2 por litro

    private String nombre;
    private String tipoCombustible; // "gas natural", "electricidad" o "gasoil"
    private double consumoAnual;    // en la unidad correspondiente al combustible

    public Edificio(String nombre, String tipoCombustible, double consumoAnual) {
        this.nombre = nombre;
        this.tipoCombustible = tipoCombustible;
        this.consumoAnual = consumoAnual;
    }

    public String getNombre() {
        return nombre;
    }

    public String getTipoCombustible() {
        return tipoCombustible;
    }

    public double getConsumoAnual() {
        return consumoAnual;
    }

    // Implementación específica del método de la interfaz para Edificio
    @Override
    public double obtenerImpactoEcologico() {
        switch (tipoCombustible.toLowerCase()) {
            case "gas natural":
                return consumoAnual * FACTOR_GAS_NATURAL;
            case "electricidad":
                return consumoAnual * FACTOR_ELECTRICIDAD;
            case "gasoil":
                return consumoAnual * FACTOR_GASOIL;
            default:
                return 0.0;
        }
    }

    @Override
    public String toString() {
        return String.format("Edificio %-15s | combustible: %-12s | consumo anual: %.1f",
                nombre, tipoCombustible, consumoAnual);
    }

    // Comportamiento propio de Edificio, sin ninguna relación con la interfaz
    // ImpactoEcologico. Ni Auto ni Bicicleta tienen un método equivalente.
    public void encenderCalefaccion() {
        System.out.println(nombre + ": encendiendo el sistema de calefacción...");
    }
}
