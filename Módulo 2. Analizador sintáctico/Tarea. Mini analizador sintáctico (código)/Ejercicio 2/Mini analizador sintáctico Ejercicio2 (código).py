def Lexer(cadena):
    tokens = []
    for ch in cadena:
        if ch.isalpha():
            tokens.append(("id", ch))
        elif ch == "+":
            tokens.append(("+", "+"))
    tokens.append(("$", "$"))
    return tokens

Tabla_LR = {
    (0, "id"): "d2",
    (2, "+"):  "d3",
    (2, "$"):  "r2",
    (3, "id"): "d2",
    (4, "$"):  "r1",
    (1, "$"):  "aceptacion"
}

GOTO = {
    (0, "E"): 1,
    (3, "E"): 4
}

def pilaToSTR(pila):
    s = ""
    for x in pila:
        s += str(x)
    return s

def entradaToSTR(tokens, i):
    s = ""
    for typ, lex in tokens[i:]:
        s += lex
    return s

def parser_lr(cadena):
    tokens = Lexer(cadena)
    i = 0
    pila = ["$", 0]

    W_PILA = 45
    W_ENTR = 20

    print(f"{'Iter':>4}  {'Pila':<{W_PILA}}  {'Entrada':<{W_ENTR}}  Salida")
    iteracion = 1

    while True:
        estado = pila[-1]
        siguienteTipo, siguienteLexema = tokens[i]

        accion = Tabla_LR.get((estado, siguienteTipo), "error")

        pila_str = pilaToSTR(pila)
        entrada_str = entradaToSTR(tokens, i)

        if accion == "error":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  ERROR")
            break

        if accion == "aceptacion":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  r0 (aceptación)")
            break

        if accion[0] == "d":
            nuevo_estado = int(accion[1:])
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  {accion}")
            pila.append(siguienteLexema)
            pila.append(nuevo_estado)
            i += 1
            iteracion += 1
            continue

        if accion == "r2":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  r2  E -> id")
            pila.pop()
            pila.pop()
            estado_arriba = pila[-1]
            pila.append("E")
            pila.append(GOTO[(estado_arriba, "E")])
            iteracion += 1
            continue

        if accion == "r1":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  r1  E -> id + E")
            for _ in range(6):
                pila.pop()
            estado_arriba = pila[-1]
            pila.append("E")
            pila.append(GOTO[(estado_arriba, "E")])
            iteracion += 1
            continue


parser_lr("a+b+c+d+e+f")
