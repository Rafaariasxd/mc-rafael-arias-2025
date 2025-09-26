import math

x = float(input("Ingrese x en radianes: "))

es = 0.5 * 10**(2 - 8)   # 8 cifras significativas → 5e-7 %
max_iter = 10000

s = 0.0
term = x
k = 0
it = 0
ea = float("inf")

while it < max_iter:
    s_prev = s
    s += term
    it += 1
    if s != 0:
        ea = abs((s - s_prev) / s) * 100
    else:
        ea = float("inf")
    if ea < es:
        break
    k += 1
    term = -term * x * x / ((2 * k) * (2 * k + 1))

print(f"sen(x) ≈ {s:.10f}")
print(f"Error aproximado relativo porcentual εa = {ea:.10e}%")
print(f"Iteraciones = {it}")
