# Superclase
class Archivo:
    def __init__(self, nombre: str, peso_en_mb: float):
        self.nombre = nombre
        self.peso_en_mb = peso_en_mb
        print("Creando Archivo genérico...")

# Subclase
class ArchivoVideo(Archivo):
    def __init__(self, nombre: str, peso_en_mb: float):
        # Llamada obligatoria al constructor de la superclase
        super().__init__(nombre, peso_en_mb)
        print("Creando Archivo de Video...")

# Ejecución del programa
if __name__ == "__main__":
    print("--- Instanciando ArchivoVideo ---")
    video = ArchivoVideo("pelicula.mp4", 1200.5)
