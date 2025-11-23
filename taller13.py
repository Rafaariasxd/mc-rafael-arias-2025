import copy

def imprimirSistema(a, b, etiqueta):
    n = len(b)
    print(etiqueta)
    for i in range(n):
        for j in range(n):
            print(a[i][j], end=" ")
        print("|", b[i])
    print()

def buscar_fila_pivote(a, i):
    """Busca una fila debajo de i que tenga un pivote no cero en la columna i."""
    n = len(a)
    for k in range(i + 1, n):
        if a[k][i] != 0:
            return k
    return -1

def gaussJordan(ao, bo):
    a = copy.deepcopy(ao)
    b = copy.copy(bo)

    n = len(b)
    imprimirSistema(a, b, "Matriz inicial")

    for i in range(n):
        # --- nuevo: revisar si el pivote es cero y hacer intercambio de filas ---
        if a[i][i] == 0:
            fila = buscar_fila_pivote(a, i)
            if fila == -1:
                print("No hay pivote distinto de cero en la columna", i)
                return None
            # intercambio de filas en a y en b
            a[i], a[fila] = a[fila], a[i]
            b[i], b[fila] = b[fila], b[i]
            imprimirSistema(a, b, f"Intercambio filas {i+1} y {fila+1}")

        pivote = a[i][i]

        # dividir fila i por el pivote
        for j in range(n):
            a[i][j] /= pivote
        b[i] /= pivote
        imprimirSistema(a, b, f"Division por pivote (fila {i+1})")

        # reducción: hacer ceros en la columna i
        for k in range(n):
            if k != i:
                valorAux = -a[k][i]
                for j in range(n):
                    a[k][j] += a[i][j] * valorAux
                b[k] += b[i] * valorAux
        imprimirSistema(a, b, f"Reduccion columna {i+1}")

    return b

# --- datos del sistema del taller 13 ---
a = [[2, 0, 2],
     [4, 0, -1],
     [3, 2, -2]]

b = [7, 18, 16]

x = gaussJordan(a, b)

print("Respuesta:")
if x is not None:
    for i in range(len(x)):
        print(f"x{i+1} = {x[i]}")
