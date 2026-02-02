# ¿Qué es un analizador léxico?

## Abstract
El analizador léxico es una etapa esencial en el proceso de compilación: transforma un programa escrito como una secuencia de caracteres en una secuencia de **tokens** con significado. Estos tokens pueden representar identificadores, palabras reservadas, operadores y literales, y sirven como entrada para el analizador sintáctico.

**Palabras clave:** analizador léxico, compiladores.

---

## Introducción
En un compilador es necesario analizar el código fuente para comprender su estructura y significado. La primera fase suele consistir en identificar las unidades mínimas con sentido dentro del texto; a esta etapa se le conoce como **análisis léxico**, y su componente principal es el **analizador léxico**.

---

## Definición
Un analizador léxico es un programa que recibe como entrada una secuencia de caracteres (código fuente) y produce como salida una secuencia de tokens, donde cada token representa una categoría léxica válida del lenguaje (por ejemplo: identificadores, números, operadores o separadores).

Su propósito es agrupar caracteres en unidades significativas para el compilador, ignorando elementos no relevantes como espacios en blanco, tabulaciones o comentarios (dependiendo del lenguaje). 

---

## Conceptos principales
- **Lexema:** cadena exacta de caracteres que aparece en el código y coincide con alguna regla léxica (ejemplos: `x`, `while`, `25`). 
- **Token:** categoría del tipo de lexema (ej.: `x` → identificador, `while` → palabra reservada, `25` → número). 
- **Patrón:** regla que describe la forma de un token; comúnmente se expresa con **expresiones regulares**. 

---

## Funciones del analizador léxico
1. Reconocer tokens válidos leyendo el código fuente de izquierda a derecha. 
2. Ignorar caracteres irrelevantes como espacios, tabulaciones o saltos de línea.
3. Detectar errores léxicos (símbolos no permitidos o tokens mal formados). 
4. Entregar tokens al analizador sintáctico, que normalmente consume la salida del lexer. 

En general, el análisis léxico se construye con base en expresiones regulares que describen los tokens del lenguaje. 

---

## Ejemplo
Cadena de entrada:
`X = a + b * 2;` 

Salida aproximada:
- (IDENTIFICADOR, x)
- (OPERADOR, =)
- (IDENTIFICADOR, a)
- (OPERADOR, +)
- (IDENTIFICADOR, b)
- (OPERADOR, *)
- (NUMERO, 2)
- (PUNTO_Y_COMA, ;) 

---

## Conclusión
El analizador léxico es una fase inicial crítica en compiladores e intérpretes, ya que convierte el código fuente en tokens y facilita el análisis estructural posterior del lenguaje. 

---

## Referencias
[1] Wikipedia, “Analizador léxico”.
[2] GeeksforGeeks, “Introduction of Lexical Analysis”.  
[3] Compiladores57 (Webnode), “Análisis léxico”. 
