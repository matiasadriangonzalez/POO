/**
 * Clase Auto.
 * No tiene relación de herencia con Edificio ni con Bicicleta; solo
 * comparte con ellas el hecho de implementar la interfaz ImpactoEcologico.
 */
public class Auto implements ImpactoEcologico {

    // Factores de emisión aproximados (kg de CO2 por litro de combustible)
    private static final double FACTOR_NAFTA = 2.31;
    private static final double FACTOR_GASOIL = 2.68;

    private String marca;
    private String modelo;
    private double kmRecorridosAnual;
    private double consumoLitrosPor100km;
    private String tipoCombustible; // "nafta" o "gasoil"

    public Auto(String marca, String modelo, double kmRecorridosAnual, double consumoLitrosPor100km,
            String tipoCombustible) {
        this.marca = marca;
        this.modelo = modelo;
        this.kmRecorridosAnual = kmRecorridosAnual;
        this.consumoLitrosPor100km = consumoLitrosPor100km;
        this.tipoCombustible = tipoCombustible;
    }

    public String getMarca() {
        return marca;
    }

    public String getModelo() {
        return modelo;
    }

    // Implementación específica del método de la interfaz para Auto
    @Override
    public double obtenerImpactoEcologico() {
        double litrosConsumidos = (kmRecorridosAnual / 100.0) * consumoLitrosPor100km;
        double factor = tipoCombustible.equalsIgnoreCase("gasoil") ? FACTOR_GASOIL : FACTOR_NAFTA;
        return litrosConsumidos * factor;
    }

    @Override
    public String toString() {
        return String.format("Auto     %-15s | %.0f km/año, %.1f L/100km, %s", marca + " " + modelo, kmRecorridosAnual,
                consumoLitrosPor100km, tipoCombustible);
    }

    // Comportamiento propio de Auto, sin ninguna relación con la interfaz
    // ImpactoEcologico. Ni Edificio ni Bicicleta tienen un método equivalente.
    public void acelerar() {
        System.out.println(marca + " " + modelo + ": acelerando...");
    }
}
