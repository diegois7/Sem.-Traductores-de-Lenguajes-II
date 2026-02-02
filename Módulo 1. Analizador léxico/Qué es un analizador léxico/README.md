# ¿Qué es un analizador léxico?

## Abstract
El analizador léxico es una etapa esencial en el proceso de compilación: transforma un programa escrito como una secuencia de caracteres en una secuencia de **tokens** con significado. Estos tokens pueden representar identificadores, palabras reservadas, operadores y literales, y sirven como entrada para el analizador sintáctico. :contentReference[oaicite:0]{index=0}

**Palabras clave:** analizador léxico, compiladores. :contentReference[oaicite:1]{index=1}

---

## Introducción
En un compilador es necesario analizar el código fuente para comprender su estructura y significado. La primera fase suele consistir en identificar las unidades mínimas con sentido dentro del texto; a esta etapa se le conoce como **análisis léxico**, y su componente principal es el **analizador léxico**. :contentReference[oaicite:2]{index=2}

---

## Definición
Un analizador léxico es un programa que recibe como entrada una secuencia de caracteres (código fuente) y produce como salida una secuencia de tokens, donde cada token representa una categoría léxica válida del lenguaje (por ejemplo: identificadores, números, operadores o separadores). :contentReference[oaicite:3]{index=3}

Su propósito es agrupar caracteres en unidades significativas para el compilador, ignorando elementos no relevantes como espacios en blanco, tabulaciones o comentarios (dependiendo del lenguaje). :contentReference[oaicite:4]{index=4}

---

## Conceptos principales
- **Lexema:** cadena exacta de caracteres que aparece en el código y coincide con alguna regla léxica (ejemplos: `x`, `while`, `25`). :contentReference[oaicite:5]{index=5}  
- **Token:** categoría del tipo de lexema (ej.: `x` → identificador, `while` → palabra reservada, `25` → número). :contentReference[oaicite:6]{index=6}  
- **Patrón:** regla que describe la forma de un token; comúnmente se expresa con **expresiones regulares**. :contentReference[oaicite:7]{index=7}  

---

## Funciones del analizador léxico
1. Reconocer tokens válidos leyendo el código fuente de izquierda a derecha. :contentReference[oaicite:8]{index=8}  
2. Ignorar caracteres irrelevantes como espacios, tabulaciones o saltos de línea. :contentReference[oaicite:9]{index=9}  
3. Detectar errores léxicos (símbolos no permitidos o tokens mal formados). :contentReference[oaicite:10]{index=10}  
4. Entregar tokens al analizador sintáctico, que normalmente consume la salida del lexer. :contentReference[oaicite:11]{index=11}  

En general, el análisis léxico se construye con base en expresiones regulares que describen los tokens del lenguaje. :contentReference[oaicite:12]{index=12}

---

## Ejemplo
Cadena de entrada:
`X = a + b * 2;` :contentReference[oaicite:13]{index=13}

Salida aproximada:
- (IDENTIFICADOR, x)
- (OPERADOR, =)
- (IDENTIFICADOR, a)
- (OPERADOR, +)
- (IDENTIFICADOR, b)
- (OPERADOR, *)
- (NUMERO, 2)
- (PUNTO_Y_COMA, ;) :contentReference[oaicite:14]{index=14}

---

## Conclusión
El analizador léxico es una fase inicial crítica en compiladores e intérpretes, ya que convierte el código fuente en tokens y facilita el análisis estructural posterior del lenguaje. :contentReference[oaicite:15]{index=15}

---

## Referencias
[1] Wikipedia, “Analizador léxico”. :contentReference[oaicite:16]{index=16}  
[2] GeeksforGeeks, “Introduction of Lexical Analysis”. :contentReference[oaicite:17]{index=17}  
[3] Compiladores57 (Webnode), “Análisis léxico”. :contentReference[oaicite:18]{index=18}  
