import random

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def agregarValor(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._agregar(self.raiz, valor)

    def _agregar(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._agregar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._agregar(nodo.derecho, valor)

    def buscarValor(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        if valor < nodo.valor:
            return self._buscar(nodo.izquierdo, valor)
        else:
            return self._buscar(nodo.derecho, valor)

    def imprimirValores(self):
        valores = []
        self._inorden(self.raiz, valores)
        for v in valores:
            print(v, end=" ")
        print()

    def _inorden(self, nodo, salida):
        if nodo is not None:
            self._inorden(nodo.izquierdo, salida)
            salida.append(nodo.valor)
            self._inorden(nodo.derecho, salida)

arbol = ArbolBinario()
numeros = random.sample(range(1, 101), 20)
print("Numeros generados:", numeros)

for n in numeros:
    arbol.agregarValor(n)

while True:
    print("\nMenu:")
    print("1. Buscar un numero en el arbol")
    print("2. Imprimir elementos en forma ascendente")
    print("3. Salir")
    op = input("Opcion: ")

    if op == "1":
        try:
            v = int(input("Numero a buscar: "))
            if arbol.buscarValor(v):
                print("El numero esta en el arbol")
            else:
                print("El numero NO esta en el arbol")
        except ValueError:
            print("Entrada invalida")
    elif op == "2":
        print("Elementos en orden ascendente:")
        arbol.imprimirValores()
    elif op == "3":
        break
    else:
        print("Opcion invalida")
