import streamlit as st
import pandas as pd
import re
import os
import analizadorLexico as lex
import arbol_sintactico_lr as parser
from generador_asm import ASMGenerator
from analizador_semantico import SemanticAnalyzer
from parser_lr import load_lr_table

st.set_page_config(page_title="Proyecto Final. compilador SEM. Trad Lenguajes II.", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE APOYO ---
def tree_to_dict(node):
    if node is None: return None
    return {
        "símbolo": node.symbol,
        "lexema": node.lexeme if node.lexeme else "",
        "hijos": [tree_to_dict(c) for c in node.children] if node.children else []
    }

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("Proyecto final")
    st.write("🔥")

# --- CUERPO PRINCIPAL ---
st.title("Compilador de C++")
st.caption("Analizador léxico, sintáctico y semántico con generación de código ASM para 8086")
st.divider()

col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📝 Entrada de Código")
    archivo = st.file_uploader("Importar archivo .cpp", type=["cpp"])
    
    codigo_previo = ""
    if archivo:
        codigo_previo = archivo.read().decode("utf-8")
    
    codigo_fuente = st.text_area(
        "Editor:", 
        value=codigo_previo, 
        height=400, 
        placeholder="Escribe o carga tu código C++..."
    )
    
    btn_ejecutar = st.button("⚡ Compilar código", use_container_width=True, type="primary")

with col_output:
    if btn_ejecutar and codigo_fuente:
        # --- CORRECCIÓN DE RUTA PARA LA NUBE ---
        # Buscamos 'compilador.lr' en la misma carpeta donde está este archivo app.py
        base_path = os.path.dirname(__file__)
        path_tabla = os.path.join(base_path, "compilador.lr")
        
        try:
            # FASES INICIALES
            lr_t = load_lr_table(path_tabla) # Usamos la ruta absoluta
            tokens = lex.lexer(codigo_fuente)
            
            # 1. PARSER (Sintáctico)
            exito, tree, error_sint, historial = parser.parse_lr_with_tree(lr_t, tokens)
            
            if not exito:
                st.error(f"❌ Error Sintáctico: {error_sint}")
            else:
                # 2. SEMÁNTICO
                analyzer = SemanticAnalyzer()
                errores_sem = analyzer.analyze(tree)
                
                t1, t2, t3 = st.tabs(["📊 Estructura AST", "🔍 Semántica", "📜 ASM Final"])
                
                with t1:
                    st.write("**Árbol de Análisis (Interactivo):**")
                    st.json(tree_to_dict(tree), expanded=False)
                    with st.expander("Ver Pila de Estados (Parser)"):
                        st.dataframe(pd.DataFrame(historial), use_container_width=True)

                with t2:
                    st.write("**Tabla de Símbolos:**")
                    if analyzer.all_symbols_report:
                        st.table(pd.DataFrame(analyzer.all_symbols_report))
                    else:
                        st.info("No se definieron variables.")

                    if errores_sem:
                        st.write("**Reporte de Validaciones:**")
                        for msg in errores_sem:
                            if "Error" in msg:
                                st.error(str(msg))
                            else:
                                st.warning(str(msg))
                    else:
                        st.success("✅ Validación semántica exitosa.")

                with t3:
                    st.write("**Código Ensamblador Generado (emu8086):**")
                    asm_gen = ASMGenerator()
                    try:
                        codigo_asm = asm_gen.generate(tree)
                        st.code(codigo_asm, language="asm")
                        st.download_button(
                            label="📥 Descargar para emu8086",
                            data=codigo_asm,
                            file_name="compilado.asm",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Fallo en traducción ASM: {e}")

        except FileNotFoundError:
            st.error(f"Archivo 'compilador.lr' no encontrado en la ruta: {path_tabla}")
        except Exception as e:
            st.error(f"Error crítico en el motor: {e}")
    else:
        st.info("💡 Ingresa código en el editor para iniciar el análisis.")