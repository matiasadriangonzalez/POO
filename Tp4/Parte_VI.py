# 1. CLASE BASE
class Persona:
    def __init__(self, nombre: str, dni: str):
        self.nombre = nombre
        self.dni = dni

# 2. SUBCLASE ALUMNO
class Alumno(Persona):
    def __init__(self, nombre: str, dni: str, legajoAlumno: str):
        super().__init__(nombre, dni)
        self.legajoAlumno = legajoAlumno

# 3. SUBCLASE DOCENTE
class Docente(Persona):
    def __init__(self, nombre: str, dni: str, salario: float):
        super().__init__(nombre, dni)
        self.salario = salario

# 4. SUBCLASE COMBINADA (El Alumno que también es Docente auxiliar)
class AlumnoDocente(Persona):
    def __init__(self, nombre: str, dni: str, legajoAlumno: str, salario: float):
        super().__init__(nombre, dni)
        self.legajoAlumno = legajoAlumno
        self.salario = salario
    
    # Método exclusivo de esta transición de la regla de negocio
    def graduarse(self) -> Docente:
        # Retorna un nuevo objeto Docente con los datos que sobreviven
        return Docente(self.nombre, self.dni, self.salario)


# ==========================================
# EJEMPLO DE USO (Simulación del ciclo de vida)
# ==========================================

if __name__ == "__main__":
    # Paso 1: Entra a la universidad como Alumno
    juan = Alumno("Juan Perez", "12345678", "ALU-100")
    print(f"Paso 1 - Alumno: {juan.nombre}, Legajo: {juan.legajoAlumno}")

    # Paso 2: Es contratado como Docente Auxiliar
    # Creamos el nuevo objeto combinado copiando los datos del alumno original
    juanAuxiliar = AlumnoDocente(juan.nombre, juan.dni, juan.legajoAlumno, 50000.0)
    juan = None  # El objeto 'Alumno' original se descarta
    print(f"Paso 2 - Auxiliar: {juanAuxiliar.nombre}, Legajo: {juanAuxiliar.legajoAlumno}, Salario: ${juanAuxiliar.salario}")

    # Paso 3: Se recibe (Se gradúa)
    # El propio objeto AlumnoDocente genera la instancia de la clase destino final
    juanDocente = juanAuxiliar.graduarse()
    juanAuxiliar = None  # El objeto combinado se descarta
    print(f"Paso 3 - Solo Docente: {juanDocente.nombre}, Salario: ${juanDocente.salario}")
    
    # Si intentáramos acceder al legajo de alumno aquí, daría un error de atributo:
    # print(juanDocente.legajoAlumno)  # AttributeError