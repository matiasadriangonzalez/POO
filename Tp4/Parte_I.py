# Código generado por IA - CON EL ERROR INTENCIONAL
class Motor:
    def __init__(self, cilindros, combustible):
        self.cilindros = cilindros
        self.combustible = combustible
        self.encendido = False

    def encender(self):
        self.encendido = True
        print("Motor encendido")

    def apagar(self):
        self.encendido = False
        print("Motor apagado")

    def get_info(self):
        return f"Motor de {self.cilindros} cilindros, combustible: {self.combustible}"


# ERROR DE DISEÑO: Auto hereda de Motor
class Auto(Motor):
    def __init__(self, marca, modelo, cilindros, combustible):
        super().__init__(cilindros, combustible)
        self.marca = marca
        self.modelo = modelo

    def conducir(self):
        if self.encendido:
            print(f"Conduciendo el {self.marca} {self.modelo}")
        else:
            print("Primero enciende el motor")

    def get_info(self):
        return f"{self.marca} {self.modelo} - {super().get_info()}"


# Uso
auto = Auto("Toyota", "Corolla", 4, "Nafta")
auto.encender()       # Auto "es" un motor, puede encenderse a sí mismo 
auto.apagar()
print(auto.get_info())

