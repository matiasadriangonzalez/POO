/**
 * Interfaz ImpactoEcologico.
 * Especifica un comportamiento común (obtenerImpactoEcologico) para clases
 * que, aunque no tienen relación de herencia entre sí, comparten la
 * necesidad de reportar su huella de carbono anual, expresada en
 * kilogramos de CO2 equivalente (kg CO2e) emitidos por año.
 */
public interface ImpactoEcologico {

    /**
     * Calcula el impacto ecológico (huella de carbono) del objeto.
     * @return impacto ecológico en kg de CO2 equivalente por año
     */
    double obtenerImpactoEcologico();
}
