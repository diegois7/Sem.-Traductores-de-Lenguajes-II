from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

import analizadorLexico as lex


@dataclass
class Rule:
    lhs_id: int
    rhs_len: int
    lhs_name: str


@dataclass
class LRTable:
    rules: List[Rule]
    n_rows: int
    n_cols: int
    table: List[List[int]]  # table[state][symbol_id] -> action/goto


def load_lr_table(path: str) -> LRTable:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = [ln.strip() for ln in f if ln.strip() != ""]

    i = 0
    n_rules = int(lines[i]); i += 1

    rules: List[Rule] = []
    for _ in range(n_rules):
        parts = lines[i].split()
        lhs_id = int(parts[0])
        rhs_len = int(parts[1])
        lhs_name = parts[2]
        rules.append(Rule(lhs_id, rhs_len, lhs_name))
        i += 1

    n_rows, n_cols = map(int, lines[i].split()); i += 1

    table: List[List[int]] = []
    for r in range(n_rows):
        row = list(map(int, lines[i + r].split()))
        if len(row) != n_cols:
            raise ValueError(f"Fila {r} con {len(row)} columnas, esperaba {n_cols}.")
        table.append(row)

    return LRTable(rules=rules, n_rows=n_rows, n_cols=n_cols, table=table)


def action_to_str(a: int) -> str:
    if a == 0:
        return "error"
    if a == -1:
        return "acceptacion R1"
    if a > 0:
        return f"D{a}"
    return f"R{(-a - 1)}"


def parse_lr(
    lr: LRTable,
    tokens: List[Tuple[int, str]],
    trace: bool = True
) -> Tuple[bool, Optional[str]]:

    # pila de pares (simbolo, estado)
    stack: List[Tuple[str, int]] = [("$", 0)]
    i = 0

    while True:
        state = stack[-1][1]
        if i >= len(tokens):
            return False, "Se acabaron tokens sin encontrar ACCEPT."

        tok_id, lexema = tokens[i]

        if tok_id < 0 or tok_id >= lr.n_cols:
            return False, f"Token id fuera de rango: {tok_id} (lexema={lexema})"

        a = lr.table[state][tok_id]

        if trace:
            pila_estados = " ".join(str(s) for _, s in stack)
            entrada = " ".join(lx for _, lx in tokens[i:i+8])
            print(f"ST={state:<3}  tok=({tok_id},{lexema:<10})  act={action_to_str(a):<12}  stack=[{pila_estados}]  in=[{entrada}]")

        if a == 0:
            return False, f"ERROR en estado {state} con token ({tok_id}, '{lexema}')."

        if a == -1:
            return True, None

        if a > 0:
            # desplazar apilar token y nuevo estado
            stack.append((lexema, a))
            i += 1
            continue

        # reduccione
        rule_index = (-a - 1)  # R1 => index 1, R2 => 2 ...
        if rule_index < 1 or rule_index > len(lr.rules):
            return False, f"Regla inválida: R{rule_index}"

        rule = lr.rules[rule_index - 1]

        # pop
        if rule.rhs_len > 0:
            if rule.rhs_len > (len(stack) - 1):
                return False, f"No hay suficientes elementos en pila para reducir por R{rule_index}"
            for _ in range(rule.rhs_len):
                stack.pop()

        top_state = stack[-1][1]
        lhs_id = rule.lhs_id

        if lhs_id < 0 or lhs_id >= lr.n_cols:
            return False, f"LHS id fuera de rango en R{rule_index}: {lhs_id}"

        goto = lr.table[top_state][lhs_id]
        if goto <= 0:
            return False, f"GOTO inválido desde estado {top_state} con {rule.lhs_name}(id={lhs_id}). valor={goto}"

        stack.append((rule.lhs_name, goto))


def main():
    lr = load_lr_table("compilador.lr")

    with open("main.cpp", "r", encoding="utf-8") as f:
        s = f.read()

    tokens = lex.lexer(s)


    # break
    for tid, lxma in tokens:
        if tid == lex.T_ERROR:
            print(f"Error léxico: '{lxma}'")
            return

    ok, err = parse_lr(lr, tokens, trace=True)
    if ok:
        print("\nGramatica aceptada")
    else:
        print("\nGramatica no aceptada")
        print(err)


if __name__ == "__main__":
    main()
