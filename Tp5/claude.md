Trabajo Práctico 5 – Herencia y Polimorfismo
Metodología: En este práctico desarrollaremos el núcleo (backend) de un motor de
renderizado vectorial por consola, similar al que utilizan herramientas como Figma o los
motores de videojuegos 2D. Podrán usar IA para generar las fórmulas matemáticas o la
estructura base, pero respetando la regla arquitectónica de separar la lógica de la interacción
por consola.


1. El Elemento Base
Defina una clase ElementoGrafico (superclase) que represente cualquier objeto visual en la
pantalla. Debe tener los siguientes atributos:
• colorHex (String, ej. "#FF0000").
• posicionCentro (Defina previamente una clase Punto con atributos X e Y).
• nombreCapa (String, para identificar la capa en el software).
Y, al menos, los siguientes métodos:
• Constructores correspondientes.
• Getters y Setters.
• moverA(Punto nuevoDestino): Actualiza las coordenadas del centro.
• toString(): Sobrescribir el método heredado de Object para devolver un resumen del
elemento.
2. Las Formas Primitivas
Defina la subclase Rectangulo que herede de ElementoGrafico con los atributos ladoMenor y
ladoMayor.
• Sobrescriba el método toString() invocando internamente a super.toString() para
aprovechar el código de la clase base.
• Agregue los métodos calcularArea() y calcularPerimetro().
• Agregue el método escalar(double factor): Multiplica sus lados por el factor recibido.
Maneje conceptualmente (y comente en su código) qué debería ocurrir si el factor es 0 o
negativo.
Defina la subclase Elipse que herede de ElementoGrafico con los atributos radioMayor (R) y
radioMenor (r).
• Implemente los mismos métodos que en Rectángulo.
3. El Dilema del Cuadrado (Investigación con IA)
Defina una clase Cuadrado que herede de la clase Rectangulo.
• ¿Cómo debería ser el constructor de Cuadrado para usar la instrucción super()
correctamente?
• El desafío: Si Rectangulo tiene los métodos setLadoMenor() y setLadoMayor(), el
Cuadrado los hereda. Si alguien llama a miCuadrado.setLadoMayor(10), el cuadrado queda deformado. ¿Cómo debe sobrescribir el Cuadrado esos métodos para mantener
su integridad de lados iguales?
• Análisis con IA: Pregúntenle a la IA: "¿Por qué hacer que un Cuadrado herede de un
Rectángulo en Programación Orientada a Objetos se considera a menudo una violación
del Principio de Sustitución de Liskov (LSP)?". Lean la respuesta, discútanla en grupo y
escriban un breve párrafo en el TP con su conclusión.
Defina también la clase Circulo heredando de Elipse y aplique la misma lógica de
constructores.
4. El "Motor de Renderizado" y el Polimorfismo
Cree una clase Lienzo (Canvas) que contenga una Colección o Arreglo dinámico de tipo
ElementoGrafico.
• Cree un programa Main que instancie varios Rectángulos, Elipses, Cuadrados y Círculos,
y los agregue a la colección del Lienzo.
• Programe un bucle que recorra todos los elementos de la colección y ejecute dos
acciones: cambiarlos todos al color "#808080" (simulando un filtro de escala de grises)
y moverlos al punto (0,0).
• El problema: Dentro de ese mismo bucle, intente sumar el área de todos los elementos
para saber cuántos "píxeles" ocupan en total. Analice y explique: ¿Por qué el compilador
arroja un error si intentamos llamar a elemento.calcularArea() sobre una variable de tipo
ElementoGrafico?
5. Arquitectura Abstracta
Utilice la técnica del Polimorfismo y la Abstracción para arreglar el comportamiento anómalo
detectado en el paso anterior.
• Responda y aplique: ¿Cómo haría para obligar a que todas las clases futuras (ej.
Triángulo) que hereden de la clase base tengan garantizada la existencia de los
métodos para calcular área y perímetro? ¿Qué modificación específica debe hacerle a la
superclase ElementoGrafico (hacerla abstracta o usar interfaces)?
• Modifique su código para que el bucle del área total funcione perfectamente.
6. Diagramado
Haga un diagrama de clases (UML) que refleje la estructura final mejorada. Añadir las clases
Linea, Triangulo y Pentagono. Indique sus relaciones.