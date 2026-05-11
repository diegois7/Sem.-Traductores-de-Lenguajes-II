# Compilador de Lenguaje Tipo C Simplificado

Este repositorio contiene la implementación de un compilador funcional para un subconjunto del lenguaje C. El proyecto ha evolucionado desde el análisis léxico y sintáctico hasta la construcción de un **Árbol Sintáctico (AST)** y la ejecución de un **Analizador Semántico** basado en una tabla de símbolos.

---

## Contenido del Repositorio

- **`main.py`**: El punto de entrada principal. Coordina el flujo entre el lexer, parser y el analizador semántico.
- **`analizadorLexico.py`**: Transforma el código fuente en una secuencia de tokens categorizados.
- **`parser_lr.py`**: Contiene la lógica para interpretar la tabla LR y ejecutar acciones de desplazamiento y reducción.
- **`arbol_sintactico_lr.py`**: Define la estructura `ParseNode` y construye el árbol jerárquico durante el proceso de reducción del parser.
- **`analizador_semantico.py`**: Realiza la validación lógica (declaraciones, tipos y ámbitos) recorriendo el árbol sintáctico.
- **`compilador.lr`**: Tabla de estados y reglas de producción generada para la gramática.
- **`main.cpp`**: Archivo de prueba que contiene el código fuente a compilar.

---

##  Objetivo de la Etapa Actual

El objetivo principal es realizar la **Validación Semántica**. Mientras que el parser asegura que el código esté "bien escrito", el analizador semántico asegura que "tenga sentido". 

Las tareas clave incluyen:
1.  **Gestión de Ámbitos (Scopes):** Manejo de variables globales y locales (dentro de funciones).
2.  **Tabla de Símbolos:** Registro de nombres y tipos de variables y funciones.
3.  **Chequeo de Tipos:** Verificación de compatibilidad en asignaciones (ej. evitar o alertar sobre `float` a `int`).
4.  **Existencia de Identificadores:** Asegurar que no se usen variables o funciones que no hayan sido declaradas previamente.

---

## Flujo del Compilador

1.  **Análisis Léxico:** Se extraen los tokens del archivo `.cpp`.
2.  **Análisis Sintáctico:** Se procesan los tokens mediante el algoritmo LR. Si es válido, se genera un **Árbol Sintáctico**.
3.  **Análisis Semántico:** * Se recorre el árbol.
    * Se llenan las tablas de símbolos al encontrar definiciones (`DefVar`, `DefFunc`).
    * Se validan las sentencias de uso (`Sentencia`, `LlamadaFunc`).

---

## Ejemplo de Validación

Si el archivo `main.cpp` contiene errores de lógica:

```cpp
int main(){
    float a;
    int c;
    c = a + 10.5;   // Aviso: Asignación de float a int
    c = suma(8, 9); // Error: Función 'suma' no definida
}

Gramática aceptada.
--- Iniciando Análisis Semántico ---
Se encontraron 2 problemas semánticos:
 -> Aviso Semántico: Asignando float a int en 'c' (pérdida de precisión).
 -> Error Semántico: La función 'suma' no ha sido definida.