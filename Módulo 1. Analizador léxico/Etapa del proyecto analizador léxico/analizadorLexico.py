# tipos
T_ID = 0
T_ENTERO = 1
T_REAL = 2
T_CADENA = 3
T_TIPO = 4
T_OPSUMA = 5
T_OPMUL = 6
T_OPRELAC = 7
T_OPOR = 8
T_OPAND = 9
T_OPNOT = 10
T_OPIGUALDAD = 11
T_PYC = 12
T_COMA = 13
T_PAR_IZQ = 14
T_PAR_DER = 15
T_LLA_IZQ = 16
T_LLA_DER = 17
T_ASIG = 18
T_IF = 19
T_WHILE = 20
T_RETURN = 21
T_ELSE = 22
T_FIN = 23
T_ERROR = -1

RESERVADAS = {
    "if": T_IF,
    "while": T_WHILE,
    "return": T_RETURN,
    "else": T_ELSE,
}

TIPOS = {"int", "float", "void"}

def lexer(cadena):
    tokens = []
    i = 0
    n = len(cadena)

    while i < n:
        c = cadena[i]

        if c in " \t\r\n":
            i += 1
            continue

        if c.isalpha():
            lex = c
            i += 1
            while i < n and (cadena[i].isalpha() or cadena[i].isdigit()):
                lex += cadena[i]
                i += 1

            if lex in RESERVADAS:
                tokens.append((RESERVADAS[lex], lex))
            elif lex in TIPOS:
                tokens.append((T_TIPO, lex))
            else:
                tokens.append((T_ID, lex))
            continue

        if c.isdigit():
            lex = ""
            while i < n and cadena[i].isdigit():
                lex += cadena[i]
                i += 1

            if i < n and cadena[i] == ".":
                if i + 1 < n and cadena[i + 1].isdigit():
                    lex += "."
                    i += 1
                    while i < n and cadena[i].isdigit():
                        lex += cadena[i]
                        i += 1
                    tokens.append((T_REAL, lex))
                else:
                    tokens.append((T_ERROR, lex + "."))
                    i += 1
            else:
                tokens.append((T_ENTERO, lex))
            continue

        if c == '"':
            lex = '"'
            i += 1
            while i < n and cadena[i] != '"':
                lex += cadena[i]
                i += 1
            if i < n and cadena[i] == '"':
                lex += '"'
                i += 1
                tokens.append((T_CADENA, lex))
            else:
                tokens.append((T_ERROR, lex))
            continue

        dos = cadena[i:i+2]

        if dos in ("<=", ">="):
            tokens.append((T_OPRELAC, dos))
            i += 2
            continue

        if dos in ("==", "!="):
            tokens.append((T_OPIGUALDAD, dos))
            i += 2
            continue

        if dos == "&&":
            tokens.append((T_OPAND, dos))
            i += 2
            continue

        if dos == "||":
            tokens.append((T_OPOR, dos))
            i += 2
            continue

        if c in "+-":
            tokens.append((T_OPSUMA, c))
            i += 1
            continue

        if c in "*/":
            tokens.append((T_OPMUL, c))
            i += 1
            continue

        if c in "<>":
            tokens.append((T_OPRELAC, c))
            i += 1
            continue

        if c == "!":
            tokens.append((T_OPNOT, c))
            i += 1
            continue

        if c == "=":
            tokens.append((T_ASIG, c))
            i += 1
            continue

        if c == ";":
            tokens.append((T_PYC, c))
            i += 1
            continue

        if c == ",":
            tokens.append((T_COMA, c))
            i += 1
            continue

        if c == "(":
            tokens.append((T_PAR_IZQ, c))
            i += 1
            continue

        if c == ")":
            tokens.append((T_PAR_DER, c))
            i += 1
            continue

        if c == "{":
            tokens.append((T_LLA_IZQ, c))
            i += 1
            continue

        if c == "}":
            tokens.append((T_LLA_DER, c))
            i += 1
            continue

        tokens.append((T_ERROR, c))
        i += 1

    tokens.append((T_FIN, "$"))
    return tokens


if __name__ == "__main__":
    s = input("Cadena: ")
    for t, lex in lexer(s):
        print(f"{lex} -> {t}")
