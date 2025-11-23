xs = [1, 2, 3, 4, 5, 6, 7, 8]
ys = [12, 8, 10, 4, 6, 3, 2, -1]

n = len(xs)
sx = sum(xs)
sy = sum(ys)
sxy = sum(xs[i] * ys[i] for i in range(n))
sx2 = sum(x * x for x in xs)

b = (n * sxy - sx * sy) / (n * sx2 - sx * sx)
a = (sy - b * sx) / n

print("Recta ajustada: y =", a, "+", b, "* x")

import matplotlib.pyplot as plt
import numpy as np

xp = np.linspace(min(xs), max(xs), 100)
yp = a + b * xp

plt.scatter(xs, ys)
plt.plot(xp, yp)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Regresión lineal por mínimos cuadrados")
plt.grid(True)
plt.show()
