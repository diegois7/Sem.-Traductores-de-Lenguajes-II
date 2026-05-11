from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import analizadorLexico as lex
from parser_lr import LRTable, load_lr_table, action_to_str


TOKEN_NAMES = {
    lex.T_ID: "id",
    lex.T_ENTERO: "entero",
    lex.T_REAL: "real",
    lex.T_CADENA: "cadena",
    lex.T_TIPO: "tipo",
    lex.T_OPSUMA: "opSuma",
    lex.T_OPMUL: "opMul",
    lex.T_OPRELAC: "opRelac",
    lex.T_OPOR: "opOr",
    lex.T_OPAND: "opAnd",
    lex.T_OPNOT: "opNot",
    lex.T_OPIGUALDAD: "opIgualdad",
    lex.T_PYC: ";",
    lex.T_COMA: ",",
    lex.T_PAR_IZQ: "(",
    lex.T_PAR_DER: ")",
    lex.T_LLA_IZQ: "{",
    lex.T_LLA_DER: "}",
    lex.T_ASIG: "=",
    lex.T_IF: "if",
    lex.T_WHILE: "while",
    lex.T_RETURN: "return",
    lex.T_ELSE: "else",
    lex.T_FIN: "$",
}


@dataclass
class ParseNode:
    symbol: str
    lexeme: Optional[str] = None
    children: List["ParseNode"] = field(default_factory=list)

    def pretty(
        self,
        level: int = 0,
        last: bool = True,
        prefix: str = "",
        ascii_only: bool = True,
    ) -> str:
        if ascii_only:
            connector = "\\-- " if last else "|-- "
            child_bar = "    " if last else "|   "
        else:
            connector = "└── " if last else "├── "
            child_bar = "    " if last else "│   "

        label = self.symbol if self.lexeme is None else f"{self.symbol}: {self.lexeme}"
        line = (prefix + connector + label) if level > 0 else label
        lines = [line]

        child_prefix = prefix + child_bar
        for i, child in enumerate(self.children):
            lines.append(
                child.pretty(
                    level + 1,
                    i == len(self.children) - 1,
                    child_prefix,
                    ascii_only=ascii_only,
                )
            )
        return "\n".join(lines)


@dataclass
class StackEntry:
    symbol: str
    state: int
    node: Optional[ParseNode]


def parse_lr_with_tree(
    lr: LRTable,
    tokens: List[Tuple[int, str]],
    trace: bool = True,
) -> Tuple[bool, Optional[ParseNode], Optional[str], List[dict]]: # Añadimos List[dict] al retorno
    stack: List[StackEntry] = [StackEntry("$", 0, None)]
    i = 0
    historial = []  # <--- AQUÍ se guardarán los pasos para la tabla

    while True:
        state = stack[-1].state
        if i >= len(tokens):
            return False, None, "Se acabaron tokens sin encontrar ACCEPT.", historial

        tok_id, lexema = tokens[i]
        
        # Guardamos el estado ANTES de ejecutar la acción para la tabla visual
        pila_actual = " ".join(str(entry.state) for entry in stack)
        entrada_actual = " ".join(lx for _, lx in tokens[i:i+5]) # Mostramos los siguientes 5 tokens
        
        if tok_id < 0 or tok_id >= lr.n_cols:
            return False, None, f"Token id fuera de rango: {tok_id}", historial

        action = lr.table[state][tok_id]
        
        # Traducimos la acción a texto legible (D5, R3, etc.)
        accion_str = action_to_str(action)

        # Agregamos el paso al historial
        historial.append({
            "Pila": pila_actual,
            "Entrada": entrada_actual,
            "Acción": accion_str
        })

        if action == 0:
            return False, None, f"ERROR en estado {state} con token '{lexema}'.", historial

        # ACCEPT
        if action == -1:
            if len(stack) < 2 or stack[-1].node is None:
                return False, None, "La pila terminó sin un nodo raíz válido.", historial
            return True, stack[-1].node, None, historial

        # SHIFT (Desplazamiento)
        if action > 0:
            terminal_name = TOKEN_NAMES.get(tok_id, f"tok_{tok_id}")
            node = ParseNode(symbol=terminal_name, lexeme=lexema)
            stack.append(StackEntry(terminal_name, action, node))
            i += 1
            continue

        # REDUCE (Reducción)
        rule_index = (-action - 1)
        if rule_index < 1 or rule_index > len(lr.rules):
            return False, None, f"Regla inválida: R{rule_index}", historial

        rule = lr.rules[rule_index - 1]
        reduced_children: List[ParseNode] = []
        
        if rule.rhs_len > 0:
            popped_entries = stack[-rule.rhs_len:]
            del stack[-rule.rhs_len:]
            reduced_children = [entry.node for entry in popped_entries if entry.node is not None]

        new_node = ParseNode(symbol=rule.lhs_name, children=reduced_children)
        top_state = stack[-1].state
        goto = lr.table[top_state][rule.lhs_id]
        
        if goto <= 0:
            return False, None, f"GOTO inválido desde {top_state}", historial

        stack.append(StackEntry(rule.lhs_name, goto, new_node))
