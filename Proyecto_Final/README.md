# 🚀 Proyecto Final - Seminario de Traductores de Lenguajes II - Diego Alejandro Martínez Meléndez - 221349542

**🔗 Acceso Directo a la App:** [https://sem-traductores-de-lenguajes-ii-pf.streamlit.app/](https://sem-traductores-de-lenguajes-ii-pf.streamlit.app/)

Este proyecto es un compilador básico el cual permite analizar lexicamente y sintactimanete un código c++, así como convertirlo a un ASM **emu8086** (experimental).

## 🖥️ Interfaz del Proyecto
La aplicación cuenta con una interfaz moderna y limpia dividida en un área de edición de código y un panel de resultados detallados.

![Interfaz Principal](/Proyecto%20Final/img/Interfaz.png)
*Vista general del editor y panel de control.*

## 📊 Estructura AST (Árbol de Sintaxis Abstracta)
En esta sección se visualiza la jerarquía del código fuente, mostrando cómo el parser LR organiza los componentes gramaticales.

![Estructura AST](/Proyecto%20Final/img/EstructuraAST.png)
*Representación jerárquica de la estructura del programa.*

## 🔍 Análisis Semántico
Muestra la tabla de símbolos generada dinámicamente y el reporte de validaciones (errores de tipos, variables no declaradas, etc.).

![Ventana Semántica](/Proyecto%20Final/img/Semántica.png)
*Validación de coherencia y gestión de ámbitos (Global/Local).*

## 📜 Generación de ASM Final
Traducción directa a lenguaje ensamblador Intel 8086, optimizada para ser cargada y ejecutada en el emulador.

![Ventana ASM](/Proyecto%20Final/img/ASM.png)
*Código resultante listo para emu8086.*


---
*Proyecto final de la materia de Seminario de Traductores de Lenguajes II.*