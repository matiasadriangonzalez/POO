/**
 * Clase Bicicleta.
 * No tiene relación de herencia con Edificio ni con Auto; solo comparte
 * con ellas el hecho de implementar la interfaz ImpactoEcologico.
 *
 * A diferencia de un Auto o un Edificio, una bicicleta no emite CO2
 * mientras se usa; su huella de carbono proviene de su fabricación.
 * Por eso el "impacto ecológico anual" se calcula amortizando esa huella
 * de fabricación a lo largo de la vida útil estimada del vehículo.
 */
public class Bicicleta implements ImpactoEcologico {

    // Huella de fabricación aproximada, en kg de CO2, según el material del cuadro
    private static final double HUELLA_ALUMINIO = 130.0;
    private static final double HUELLA_ACERO = 100.0;
    private static final double HUELLA_CARBONO = 180.0;

    private String marca;
    private String materialCuadro; // "aluminio", "acero" o "carbono"
    private int vidaUtilAnios;

    public Bicicleta(String marca, String materialCuadro, int vidaUtilAnios) {
        this.marca = marca;
        this.materialCuadro = materialCuadro;
        this.vidaUtilAnios = vidaUtilAnios;
    }

    public String getMarca() {
        return marca;
    }

    // Implementación específica del método de la interfaz para Bicicleta
    @Override
    public double obtenerImpactoEcologico() {
        double huellaFabricacion;
        switch (materialCuadro.toLowerCase()) {
            case "aluminio":
                huellaFabricacion = HUELLA_ALUMINIO;
                break;
            case "carbono":
                huellaFabricacion = HUELLA_CARBONO;
                break;
            default:
                huellaFabricacion = HUELLA_ACERO;
        }
        return huellaFabricacion / vidaUtilAnios;
    }

    @Override
    public String toString() {
        return String.format("Bicicleta %-14s | cuadro de %s, vida útil %d años", marca, materialCuadro, vidaUtilAnios);
    }

    // Comportamiento propio de Bicicleta, sin ninguna relación con la interfaz
    // ImpactoEcologico. Ni Edificio ni Auto tienen un método equivalente.
    public void pedalear() {
        System.out.println(marca + ": pedaleando...");
    }
}
