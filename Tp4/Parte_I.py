class Motor:
    def __init__(self, cilindrada):
        self.cilindrada = cilindrada

    def encender_motor(self):
        print("Motor encendido")

# El Auto hereda de Motor (Error de diseño)
class Auto(Motor):
    def __init__(self, marca, cilindrada):
        super().__init__(cilindrada) # Inicializa la clase padre (Motor)
        self.marca = marca

    def conducir(self):
        print(f"Conduciendo el {self.marca}")

mi_auto = Auto("Toyota", 1.6)
mi_auto.encender_motor()
