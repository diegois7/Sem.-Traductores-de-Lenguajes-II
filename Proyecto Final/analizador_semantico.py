from typing import Dict, List, Optional, Tuple

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols: Dict[str, str] = {}  
        self.functions: Dict[str, Tuple[str, List[str]]] = {} 
        self.parent = parent

    def define_var(self, name: str, dtype: str):
        self.symbols[name] = dtype

    def define_func(self, name: str, return_type: str, params: List[str]):
        self.functions[name] = (return_type, params)

    def lookup_var(self, name: str) -> Optional[str]:
        if name in self.symbols: return self.symbols[name]
        return self.parent.lookup_var(name) if self.parent else None

    def lookup_func(self, name: str) -> Optional[Tuple[str, List[str]]]:
        if name in self.functions: return self.functions[name]
        return self.parent.lookup_func(name) if self.parent else None

class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.global_table = SymbolTable()
        # Lista para el reporte en la interfaz de Streamlit
        self.all_symbols_report = []

    def analyze(self, root):
        self.errors = []
        self.all_symbols_report = []
        self.global_table = SymbolTable() # Reiniciar tabla en cada análisis
        self.visit(root, self.global_table, "Global")
        return self.errors

    def visit(self, node, table, scope_name):
        if not node: return

        # 1. Registro de Variables (DefVar)
        if node.symbol == "DefVar":
            if len(node.children) >= 2:
                tipo = node.children[0].lexeme
                nombre = node.children[1].lexeme
                table.define_var(nombre, tipo)
                self.all_symbols_report.append({
                    "Identificador": nombre,
                    "Tipo": tipo,
                    "Ámbito": scope_name
                })

        # 2. Registro de Funciones (DefFunc)
        elif node.symbol == "DefFunc":
            if len(node.children) >= 2:
                tipo_ret = node.children[0].lexeme
                nombre_f = node.children[1].lexeme
                table.define_func(nombre_f, tipo_ret, [])
                
                self.all_symbols_report.append({
                    "Identificador": nombre_f,
                    "Tipo": f"Función ({tipo_ret})",
                    "Ámbito": "Global"
                })
                
                # Creación de ámbito local para la función
                local_table = SymbolTable(parent=table)
                nuevo_scope = f"Local ({nombre_f})"
                
                for child in node.children:
                    # Entramos a los nodos que contienen definiciones o sentencias locales
                    if child.symbol in ["Parametros", "BloqFunc", "DefLocales", "Sentencias", "Cuerpo"]:
                        self.visit(child, local_table, nuevo_scope)
                return 

        # 3. Validación de Sentencias (Asignación)
        elif node.symbol == "Sentencia":
            # Verificar si es una asignación: id = Expresion ;
            # Buscamos el lexema '=' en los hijos directos
            hijos_lexemas = [c.lexeme for c in node.children if c.lexeme]
            if "=" in hijos_lexemas and len(node.children) >= 3:
                var_nombre = node.children[0].lexeme
                var_tipo = table.lookup_var(var_nombre)
                
                if not var_tipo:
                    self.errors.append(f"Error Semántico: Variable '{var_nombre}' no declarada en {scope_name}.")
                else:
                    # El tercer hijo suele ser la Expresion según la regla 36
                    tipo_derecho = self.get_type(node.children[2], table)
                    if var_tipo == "int" and tipo_derecho == "float":
                        self.errors.append(f"Aviso Semántico: Asignando float a int en '{var_nombre}' ({scope_name}).")

        # 4. Llamada a Función
        elif node.symbol == "LlamadaFunc":
            nombre_f = node.children[0].lexeme
            if not table.lookup_func(nombre_f):
                self.errors.append(f"Error Semántico: La función '{nombre_f}' no ha sido definida.")

        # Recorrido recursivo general para no saltar ningún nodo del árbol
        for child in node.children:
            self.visit(child, table, scope_name)

    def get_type(self, node, table) -> Optional[str]:
        """Infiere el tipo de dato recorriendo el subárbol de la expresión."""
        if not node: return None
        
        # Casos base: Terminales
        if node.symbol == "real": return "float"
        if node.symbol == "entero": return "int"
        if node.symbol == "id": return table.lookup_var(node.lexeme)
        
        # Caso recursivo: Inferencia
        current_type = None
        if node.children:
            for child in node.children:
                t = self.get_type(child, table)
                if t == "float": return "float" # El tipo float domina la expresión
                if t == "int": current_type = "int"
        
        return current_type