def input_set(nombre):
    n = int(input(f"Ingrese la cardinalidad de {nombre}: "))
    elementos = set()
    for i in range(n):
        elem = input(f"Ingrese el elemento {i+1} de {nombre}: ")
        elementos.add(elem)
    return elementos

U = input_set("U")
A = input_set("A")

if A.issubset(U):
    print("A es subconjunto de U")
    print("(U - A) ⊕ A =", (U - A).symmetric_difference(A))
    print("(U ∩ A) - A =", (U.intersection(A)) - A)
    print("(U ∪ A) ∩ A =", (U.union(A)).intersection(A))
else:
    print("A no es subconjunto de U")
