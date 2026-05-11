import os
import analizadorLexico as lex
from arbol_sintactico_lr import load_lr_table, parse_lr_with_tree
from analizador_semantico import SemanticAnalyzer

def Exec(archivo_fuente):
    print(f"--- Ejecutando Análisis para: {archivo_fuente} ---")
    
    #cargar Recursos
    base_path = os.path.dirname(os.path.abspath(__file__))
    lr_table = load_lr_table(os.path.join(base_path, "compilador.lr"))
    
    with open(os.path.join(base_path, archivo_fuente), "r") as f:
        source = f.read()

    # lexer
    tokens = lex.lexer(source)
    success, tree, _ = parse_lr_with_tree(lr_table, tokens)
    
    if not success:
        print("Error Sintáctico. No se puede proceder al semántico.")
        return

    # Semántica
    analyzer = SemanticAnalyzer()
    errores_semanticos = analyzer.analiza(tree)

    print("\n--- Resultados del Análisis Semántico ---")
    if not errores_semanticos:
        print("El programa es semánticamente correcto.")
    else:
        print("LISTA DE ERRORES DETECTADOS:")
        for i, err in enumerate(errores_semanticos, 1):
            print(f"{i}. {err}")

if __name__ == "__main__":
    Exec("main.cpp")