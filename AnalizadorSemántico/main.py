import os
import analizadorLexico as lex
from arbol_sintactico_lr import load_lr_table, parse_lr_with_tree
from analizador_semantico import SemanticAnalyzer 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Añadimos 'archivo' como parámetro
def Exec(archivo): 
    ruta_tabla = os.path.join(BASE_DIR, "compilador.lr")
    ruta_fuente = os.path.join(BASE_DIR, archivo)

    # cargar lr
    lr_table = load_lr_table(ruta_tabla)
    
    try:
        with open(ruta_fuente, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo fuente en {ruta_fuente}")
        return

    tokens = lex.lexer(source)
    success, tree, error_msg = parse_lr_with_tree(lr_table, tokens)
    
    if not success:
        print(f"Error Sintáctico: {error_msg}")
        return

    print("Archivo valido sintácticamente.")

    print("\n--- Iniciando Análisis Semántico ---")
    analyzer = SemanticAnalyzer()
    sem_errors = analyzer.analyze(tree)

    if not sem_errors:
        print("Análisis semántico exitoso sin errores.")
    else:
        print(f"Se encontraron {len(sem_errors)} problemas semánticos:")
        for err in sem_errors:
            print(f" -> {err}")

if __name__ == "__main__":
    Exec("main.cpp")
    Exec("main2.cpp")