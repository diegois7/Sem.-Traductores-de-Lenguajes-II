def Lexer(cadena):
    tokens = []
    i = 0
    n = len(cadena)

    while i < n:
        if cadena[i].isalpha():
            lex = ""
            while i < n and (cadena[i].isalpha() or cadena[i].isdigit() or cadena[i] == "_"):
                lex += cadena[i]
                i += 1
            tokens.append(("id", lex))
        elif cadena[i] == "+":
            tokens.append(("+", "+"))
            i += 1
        else:
            i += 1

    tokens.append(("$", "$"))
    return tokens


Tabla_LR = {
    (0, "id"): "d2",
    (2, "+"):  "d3",
    (3, "id"): "d4",
    (4, "$"):  "r1",
    (1, "$"):  "aceptacion"
}

GOTO = {
    (0, "E"): 1
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

def recorta(texto, ancho):
    if len(texto) <= ancho:
        return texto
    return texto[:ancho-3] + "..."

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

        pila_str = recorta(pilaToSTR(pila), W_PILA)
        entrada_str = recorta(entradaToSTR(tokens, i), W_ENTR)

        if accion == "error":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  ERROR")
            break

        if accion == "aceptacion":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  r0 (aceptación)")
            break

        if accion[0] == "d":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  {accion}")
            nuevo_estado = int(accion[1:])
            pila.append(siguienteLexema)
            pila.append(nuevo_estado)
            i += 1
            iteracion += 1
            continue

        if accion == "r1":
            print(f"{iteracion:>4}  {pila_str:<{W_PILA}}  {entrada_str:<{W_ENTR}}  r1  E -> id + id")
            for _ in range(6):
                pila.pop()

            estado_arriba = pila[-1]
            pila.append("E")
            pila.append(GOTO[(estado_arriba, "E")])

            iteracion += 1
            continue


parser_lr("hola+mundo")
