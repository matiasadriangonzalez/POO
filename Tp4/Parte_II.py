# Superclase
class Archivo:
    def __init__(self, nombre: str, peso_en_mb: float):
        self.__nombre = nombre           
        self.__peso_en_mb = peso_en_mb   
        print("Creando Archivo genérico...")

    # Getters para acceder desde afuera
    def get_nombre(self):
        return self.__nombre

    def get_peso_en_mb(self):
        return self.__peso_en_mb


# Subclase
class ArchivoVideo(Archivo):
    def __init__(self, nombre: str, peso_en_mb: float):
        super().__init__(nombre, peso_en_mb)
        print("Creando Archivo de Video...")


if __name__ == "__main__":

    # CASO 1: con super() — funciona correctamente
    print("--- CASO 1: CON super() ---")
    video = ArchivoVideo("pelicula.mp4", 1200.5)
    print(f"Nombre: {video.get_nombre()}")
    print(f"Peso: {video.get_peso_en_mb()} MB")

    print()

    # CASO 2: sin super() — el objeto nace roto
    print("--- CASO 2: SIN super() ---")

    class ArchivoVideoSinSuper(Archivo):
        def __init__(self, nombre: str, peso_en_mb: float):
            # super().__init__(nombre, peso_en_mb)  ← comentado a propósito
            print("Creando Archivo de Video...")

    video2 = ArchivoVideoSinSuper("pelicula.mp4", 1200.5)

    try:
        print(f"Nombre: {video2.get_nombre()}")  # 💥 AttributeError
    except AttributeError as e:
        print(f"ERROR: {e}")
