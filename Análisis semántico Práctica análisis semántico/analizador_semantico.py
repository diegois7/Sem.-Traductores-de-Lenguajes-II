from typing import Dict, List, Optional, Tuple

class SymbolTable:
    def __init__(self, parent=None, ambito="global"):
        self.symbols: Dict[str, str] = {}  # nombre: tipo ('i', 'f', 'v', 's')
        self.functions: Dict[str, Tuple[str, List[str]]] = {}
        self.parent = parent
        self.ambito = ambito
        self.lista_errores = []

    def agrega_var(self, nombre: str, tipo_codificado: str):
        if nombre in self.symbols:
            self.lista_errores.append(f"Error Semántico: variable local '{nombre}' redefinid en ámbito {self.ambito}")
        else:
            self.symbols[nombre] = tipo_codificado

    def agrega_func(self, nombre: str, tipo_retorno: str):
        if nombre in self.functions:
            self.lista_errores.append(f"Error Semántico: función '{nombre}' ya definida")
        else:
            self.functions[nombre] = (tipo_retorno, [])

    def lookup(self, nombre: str):
        if nombre in self.symbols: return self.symbols[nombre]
        if self.parent: return self.parent.lookup(nombre)
        return None

    def lookup_func(self, nombre: str):
        if nombre in self.functions: return self.functions[nombre]
        if self.parent: return self.parent.lookup_func(nombre)
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.global_table = SymbolTable(ambito="global")
        self.errors = []

    def analiza(self, tree):
        self.errors = []
        self.valida_tipos(tree, self.global_table)
        # Consolidar errores de las tablas
        return self.errors + self.global_table.lista_errores

    def dime_tipo(self, lexema_tipo: str) -> str:
        mapeo = {"int": 'i', "float": 'f', "void": 'v', "string": 's'}
        return mapeo.get(lexema_tipo, 'v')

    def valida_tipos(self, node, table):
        if not node: return

        # Regla: DefVar -> tipo id ...
        if node.symbol == "DefVar":
            tipo_caracter = self.dime_tipo(node.children[0].lexeme)
            nombre_var = node.children[1].lexeme
            table.agrega_var(nombre_var, tipo_caracter)

        # Regla: DefFunc -> tipo id ( ... ) BloqFunc
        elif node.symbol == "DefFunc":
            tipo_ret = self.dime_tipo(node.children[0].lexeme)
            nombre_f = node.children[1].lexeme
            table.agrega_func(nombre_f, tipo_ret)
            
            # Nuevo ámbito con el nombre de la función
            local_table = SymbolTable(parent=table, ambito=nombre_f)
            for child in node.children:
                self.valida_tipos(child, local_table)
            self.errors.extend(local_table.lista_errores)
            return

        # Regla: Sentencia -> id = Expresion
        elif node.symbol == "Sentencia":
            es_asig = any(c.lexeme == "=" for c in node.children)
            if es_asig:
                nombre = node.children[0].lexeme
                tipo_izq = table.lookup(nombre)
                
                if not tipo_izq:
                    self.errors.append(f"Error: variable '{nombre}' no definida")
                else:
                    tipo_der = self.get_tipo_dato(node.children[2], table)
                    # Validación de tipos: coincidencia o coherencia
                    if tipo_izq == 'i' and tipo_der == 'f':
                        self.errors.append(f"Aviso: asignando 'f' a variable 'i' {nombre} (pérdida precisión)")

        # Recorrido recursivo
        for child in node.children:
            self.valida_tipos(child, table)

    def get_tipo_dato(self, node, table) -> str:
        if not node: return 'v'
        if node.symbol == "real": return 'f'
        if node.symbol == "entero": return 'i'
        if node.symbol == "id": 
            t = table.lookup(node.lexeme)
            return t if t else 'v'
        
        # Inferencia simple para expresiones binarias
        tipos_encontrados = [self.get_tipo_dato(c, table) for c in node.children]
        if 'f' in tipos_encontrados: return 'f'
        if 'i' in tipos_encontrados: return 'i'
        return 'v'