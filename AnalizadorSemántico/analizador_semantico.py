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

    def analyze(self, root):
        self.errors = []
        self.visit(root, self.global_table)
        return self.errors

    def visit(self, node, table):
        if not node: return

        # 1. Registro de Variables (DefVar)
        if node.symbol == "DefVar":
            # Estructura típica: tipo (child 0), id (child 1)
            if len(node.children) >= 2:
                tipo = node.children[0].lexeme
                nombre = node.children[1].lexeme
                table.define_var(nombre, tipo)

        # 2. Registro de Funciones (DefFunc)
        elif node.symbol == "DefFunc":
            if len(node.children) >= 2:
                tipo_ret = node.children[0].lexeme
                nombre_f = node.children[1].lexeme
                table.define_func(nombre_f, tipo_ret, [])
                
                # Creamos ámbito local y procesamos el cuerpo (BloqFunc suele ser el último hijo)
                local_table = SymbolTable(parent=table)
                for child in node.children:
                    if child.symbol in ["Parametros", "BloqFunc"]:
                        self.visit(child, local_table)
                return 

        # 3. Validación de Sentencias de Asignación
        elif node.symbol == "Sentencia":
            # Caso: id = Expresion ; (Basado en regla 36 de tu .lr)
            # Buscamos si alguno de los hijos es el operador '='
            has_assign = any(c.lexeme == "=" for c in node.children)
            if has_assign and len(node.children) >= 3:
                var_nombre = node.children[0].lexeme
                var_tipo = table.lookup_var(var_nombre)
                
                if not var_tipo:
                    self.errors.append(f"Error Semántico: Variable '{var_nombre}' no declarada.")
                else:
                    # Evaluamos el tipo del lado derecho
                    tipo_derecho = self.get_type(node.children[2], table)
                    if var_tipo == "int" and tipo_derecho == "float":
                        self.errors.append(f"Aviso Semántico: Asignando float a int en '{var_nombre}'.")

        # 4. Llamada a Función
        elif node.symbol == "LlamadaFunc":
            nombre_f = node.children[0].lexeme
            if not table.lookup_func(nombre_f):
                self.errors.append(f"Error Semántico: La función '{nombre_f}' no ha sido definida.")

        # Recorrido recursivo para no perder nodos
        for child in node.children:
            self.visit(child, table)

    def get_type(self, node, table) -> Optional[str]:
        """Infiere el tipo recorriendo hacia abajo hasta encontrar terminales."""
        if not node: return None
        
        if node.symbol == "real": return "float"
        if node.symbol == "entero": return "int"
        if node.symbol == "id": return table.lookup_var(node.lexeme)
        
        # Si es una expresión compleja, si uno es float, todo es float
        current_type = None
        for child in node.children:
            t = self.get_type(child, table)
            if t == "float": return "float"
            if t == "int": current_type = "int"
        
        return current_type