import random

n = int(input("Ingrese la longitud entera n: "))

v1 = [random.randint(-10, 10) for _ in range(n)]
v2 = [random.randint(-10, 10) for _ in range(n)]

print("Vector 1:", v1)
print("Vector 2:", v2)

producto_escalar = sum(v1[i] * v2[i] for i in range(n))

print("Producto escalar:", producto_escalar)

import random

def generar_matriz(filas, columnas):
    return [[random.randint(-10, 10) for _ in range(columnas)] for _ in range(filas)]

def imprimir_matriz(M, nombre):
    print(nombre + ":")
    for fila in M:
        print(fila)
    print()

op = input("Seleccione operación (1: suma, 2: multiplicación): ")

if op == "1":
    filas = random.randint(2, 8)
    columnas = random.randint(2, 8)
    A = generar_matriz(filas, columnas)
    B = generar_matriz(filas, columnas)
    C = [[A[i][j] + B[i][j] for j in range(columnas)] for i in range(filas)]
    imprimir_matriz(A, "Matriz A")
    imprimir_matriz(B, "Matriz B")
    imprimir_matriz(C, "A + B")

elif op == "2":
    filas_A = random.randint(2, 8)
    columnas_A = random.randint(2, 8)
    filas_B = columnas_A
    columnas_B = random.randint(2, 8)

    A = generar_matriz(filas_A, columnas_A)
    B = generar_matriz(filas_B, columnas_B)

    C = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]
    for i in range(filas_A):
        for j in range(columnas_B):
            s = 0
            for k in range(columnas_A):
                s += A[i][k] * B[k][j]
            C[i][j] = s

    imprimir_matriz(A, "Matriz A")
    imprimir_matriz(B, "Matriz B")
    imprimir_matriz(C, "A * B")

else:
    print("Opción no válida")
