def mult_polinomios(p, q):
    r = [0.0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            r[i + j] += p[i] * q[j]
    return r

def lagrange(xs, ys):
    n = len(xs)
    P = [0.0] * n
    for i in range(n):
        Li = [1.0]
        denom = 1.0
        for j in range(n):
            if j != i:
                Li = mult_polinomios(Li, [-xs[j], 1.0])
                denom *= (xs[i] - xs[j])
        escala = ys[i] / denom
        Li = [c * escala for c in Li]
        for k in range(len(P)):
            P[k] += Li[k]
    return P

def imprimir_polinomio(coefs):
    partes = []
    for i, c in enumerate(coefs):
        if abs(c) < 1e-10:
            continue
        if i == 0:
            term = f"{c:.6f}"
        elif i == 1:
            term = f"{c:.6f}*x"
        else:
            term = f"{c:.6f}*x^{i}"
        partes.append(term)
    if not partes:
        print("0")
    else:
        print(" + ".join(partes))

xs = [0, 1, 2, 3, 4]
ys = [1.0, -0.5, -1.0, 2.5, 0.5]

coefs = lagrange(xs, ys)

print("Polinomio de interpolacion de Lagrange:")
imprimir_polinomio(coefs)

print("\nVerificacion en los puntos dados:")
for x, y in zip(xs, ys):
    val = sum(coefs[i] * (x ** i) for i in range(len(coefs)))
    print(f"x = {x}, y real = {y}, y polinomio = {val}")
