import random


def union(a,b):
    c = set()
    for elemento in a:
        c.add(elemento)
    for elemento in b:
        c.add(elemento)
    return c

def interseccion(a,b):
    c=set()
    for elemento in a:
        if elemento in b:
            c.add(elemento)
    return c

def diferencia(a,b):
    c=set()
    for elemento in a:
        if elemento not in b:
            c.add(elemento)
    return c

def diferencia_simetrica(a,b):
    c=set()
    for elemento in a:
        if elemento not in b:
            c.add(elemento)
    for elemento in b:
        if elemento not in a:
            c.add(elemento)
    return c

n1 = int(input("ingrese la cardinalidad del conjunto A:"))
n2 = int(input("ingrese la cardinalidad del conjubto B:"))

A = set(random.sample(range(31),n1))
B = set(random.sample(range(31),n2))

print(f"A= {A}")
print(f"B={B}")

print(f"A U B = {union(A,B)}")
print(f"A \u2229 B = {interseccion(A,B)}")
print(f"A - B = {diferencia(A,B)}")
print(f"A - B = {diferencia(B,A)}")
print(f"A \u2295 B = {diferencia_simetrica(A,B)}")


