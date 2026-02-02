#include <iostream>
#include <string>
#include <cctype>
using namespace std;

enum ListaTokens {
    IDENTIFICADOR,
    REAL,
    ERROR,
    FIN
};

struct Token {
    ListaTokens type;
    string lexema;
};

bool esLetra(char c) {
    return isalpha((unsigned char)c);
}

bool esDigito(char c) {
    return isdigit((unsigned char)c);
}

bool esEspacio(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

Token siguienteToken(const string& fuente, size_t &i) {
    while (i < fuente.size() && esEspacio(fuente[i])) i++;

    if (i >= fuente.size()) {
        return {FIN, ""};
    }

    char c = fuente[i];

    // regla identificador: letra(letra|digito)*
    if (esLetra(c)) {
        string lex;
        lex += fuente[i++];
        while (i < fuente.size() && (esLetra(fuente[i]) || esDigito(fuente[i]))) {
            lex += fuente[i++];
        }
        return {IDENTIFICADOR, lex};
    }

    // regla real: entero '.' entero+
    if (esDigito(c)) {
        string lex;

        // entero (uno o más dígitos)
        while (i < fuente.size() && esDigito(fuente[i])) {
            lex += fuente[i++];
        }

        // debe seguir un punto
        if (i < fuente.size() && fuente[i] == '.') {
            lex += fuente[i++];

            // y después al menos 1 dígito
            if (i < fuente.size() && esDigito(fuente[i])) {
                while (i < fuente.size() && esDigito(fuente[i])) {
                    lex += fuente[i++];
                }
                return {REAL, lex};
            } else {
                return {ERROR, lex}; 
            }
        }

        // si no hay punto- no es real
        return {ERROR, lex};
    }

    // no inicia ni identificador ni real
    return {ERROR, string(1, fuente[i++])};
}

string nombreToken(ListaTokens t) {
    switch (t) {
        case IDENTIFICADOR: return "IDENTIFICADOR";
        case REAL:          return "REAL";
        case ERROR:         return "ERROR";
        case FIN:           return "FIN";
    }
    return "???";
}

int main() {
    string entrada;
    cout << "Ingresa una cadena a analizar:\n";
    getline(cin, entrada);

    size_t i = 0;
    while (true) {
        Token tok = siguienteToken(entrada, i);
        if (tok.type == FIN) break;

        cout << tok.lexema << " -> " << nombreToken(tok.type) << "\n";
    }

    cin.get();
    return 0;
}
