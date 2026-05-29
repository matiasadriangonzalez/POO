// Superclase
class Archivo {
    private String nombre;
    private double pesoEnMB;

    // Constructor obligatorio con argumentos
    public Archivo(String nombre, double pesoEnMB) {
        this.nombre = nombre;
        this.pesoEnMB = pesoEnMB;
        System.out.println("Creando Archivo genÃ©rico...");
    }
}

// Subclase
class ArchivoVideo extends Archivo {
    // Constructor de la subclase
    public ArchivoVideo(String nombre, double pesoEnMB) {
        // Llamada obligatoria al constructor de la superclase
        super(nombre, pesoEnMB); 
        System.out.println("Creando Archivo de Video...");
    }
}

// Clase Principal para ejecutar
public class Main {
    public static void main(String[] args) {
        System.out.println("--- Instanciando ArchivoVideo ---");
        ArchivoVideo video = new ArchivoVideo("pelicula.mp4", 1200.5);
    }
}