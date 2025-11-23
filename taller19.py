import math

def regresion_lineal(x, y):
    n = len(x)
    sx = sum(x)
    sy = sum(y)
    sxy = sum(x[i] * y[i] for i in range(n))
    sx2 = sum(v * v for v in x)
    sy2 = sum(v * v for v in y)
    b = (n * sxy - sx * sy) / (n * sx2 - sx * sx)
    a = (sy - b * sx) / n
    r = (n * sxy - sx * sy) / math.sqrt((n * sx2 - sx * sx) * (n * sy2 - sy * sy))
    return a, b, r * r

xs = [1, 2, 3, 4, 5, 6, 7, 8]
ys = [1.2, 3.3, 3.8, 4.0, 4.2, 4.4, 4.5, 4.6]

a_lin, b_lin, r2_lin = regresion_lineal(xs, ys)

lnys = [math.log(v) for v in ys]
a_exp_log, b_exp, r2_exp = regresion_lineal(xs, lnys)
a_exp = math.exp(a_exp_log)

lnxs = [math.log(v) for v in xs]
a_pot_log, b_pot, r2_pot = regresion_lineal(lnxs, lnys)
a_pot = math.exp(a_pot_log)

invxs = [1.0 / v for v in xs]
invys = [1.0 / v for v in ys]
a_gc_hat, b_gc_hat, r2_gc = regresion_lineal(invxs, invys)
a_gc = 1.0 / a_gc_hat
b_gc = b_gc_hat * a_gc

print("Modelo lineal:          y = {:.6f} + {:.6f} x".format(a_lin, b_lin))
print("r2 lineal:              {:.6f}".format(r2_lin))

print("Modelo exponencial:     y = {:.6f} * e^({:.6f} x)".format(a_exp, b_exp))
print("r2 exponencial:         {:.6f}".format(r2_exp))

print("Modelo potencias:       y = {:.6f} * x^{:.6f}".format(a_pot, b_pot))
print("r2 potencias:           {:.6f}".format(r2_pot))

print("Modelo razon crec.:     y = ({:.6f} * x) / ({:.6f} + x)".format(a_gc, b_gc))
print("r2 razon crec.:         {:.6f}".format(r2_gc))

modelos = {
    "Lineal": r2_lin,
    "Exponencial": r2_exp,
    "Potencias": r2_pot,
    "Razon de crecimiento": r2_gc
}

mejor = max(modelos, key=modelos.get)
print("Mejor modelo:", mejor, "con r2 =", modelos[mejor])
