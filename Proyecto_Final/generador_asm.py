class ASMGenerator:
    def __init__(self):
        self.instructions = []
        self.data_segment = []
        self.vars_defined = set()

    def generate(self, node):
        self.instructions = []
        self.data_segment = []
        self.vars_defined = set()
        
        # 1. Fase de recolección: Buscar todas las variables en el árbol
        self.collect_vars(node)
        
        # 2. Fase de generación: Traducir lógica a instrucciones
        self.visit(node)
        
        # Construcción del código final para emu8086
        code = [
            "; --- CODIGO GENERADO PARA EMU8086 ---",
            "include 'emu8086.inc'",
            "org 100h",
            "",
            ".data"
        ]
        
        # Agregar variables al segmento de datos
        if self.data_segment:
            code.extend(self.data_segment)
        else:
            code.append("    ; (Sin variables declaradas)")
            
        code.extend([
            "",
            ".code",
            "main:",
            "    mov ax, @data",
            "    mov ds, ax",
            ""
        ])
        
        # Agregar instrucciones lógicas
        code.extend(self.instructions)
        
        # Cierre del programa
        code.extend([
            "",
            "    printn 'Ejecucion finalizada con exito.'",
            "    mov ah, 4ch",
            "    int 21h",
            "ret"
        ])
        
        return "\n".join(code)

    def collect_vars(self, node):
        """Recorre el árbol buscando DefVar para el segmento .data"""
        if not node: return
        if node.symbol == "DefVar" and len(node.children) >= 2:
            var_name = node.children[1].lexeme
            if var_name not in self.vars_defined:
                self.data_segment.append(f"    {var_name} dw 0")
                self.vars_defined.add(var_name)
        for child in node.children:
            self.collect_vars(child)

    def visit(self, node):
        if not node: return

        # Manejo de Asignaciones: variable = expresion;
        if node.symbol == "Sentencia":
            hijos_lexemas = [c.lexeme for c in node.children if c.lexeme]
            if "=" in hijos_lexemas:
                var_dest = node.children[0].lexeme
                expresion_node = node.children[2]
                
                self.instructions.append(f"    ; --- {var_dest} = ... ---")
                # Resolvemos el lado derecho y el resultado queda en AX
                self.gen_expression(expresion_node)
                # Guardamos AX en la variable de destino
                self.instructions.append(f"    mov {var_dest}, ax")
                return # Evitamos procesar hijos de nuevo

        for child in node.children:
            self.visit(child)

    def gen_expression(self, node):
        """Traduce expresiones aritméticas a AX"""
        # Caso 1: Es un número literal (entero)
        if node.symbol == "entero":
            self.instructions.append(f"    mov ax, {node.lexeme}")
            
        # Caso 2: Es una variable (id)
        elif node.symbol == "id":
            self.instructions.append(f"    mov ax, {node.lexeme}")
            
        # Caso 3: Es una suma (Expresion + Expresion)
        elif node.symbol == "Expresion" or node.symbol == "Termino":
            # Si tiene 3 hijos y el del medio es '+', es una suma
            if len(node.children) == 3 and node.children[1].lexeme == "+":
                # Lado izquierdo a AX
                self.gen_expression(node.children[0])
                self.instructions.append("    push ax")
                # Lado derecho a AX
                self.gen_expression(node.children[2])
                self.instructions.append("    mov bx, ax")
                self.instructions.append("    pop ax")
                self.instructions.append("    add ax, bx")
            else:
                # Si no es suma, seguir bajando por el árbol
                for child in node.children:
                    self.gen_expression(child)