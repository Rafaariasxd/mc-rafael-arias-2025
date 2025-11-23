import math
import matplotlib.pyplot as plt
import numpy as np

xs = [1, 2, 3, 4, 5, 6]
ys = [2.8, 5.1, 6.9, 9.2, 12.9, 18.1]

n = len(xs)
lnys = [math.log(y) for y in ys]

sx = sum(xs)
sy = sum(lnys)
sxy = sum(xs[i] * lnys[i] for i in range(n))
sx2 = sum(x * x for x in xs)

b = (n * sxy - sx * sy) / (n * sx2 - sx * sx)
A = (sy - b * sx) / n
a = math.exp(A)

print("Modelo exponencial: y = ", a, "* e^(", b, "* x)")

xp = np.linspace(min(xs), max(xs), 100)
yp = [a * math.exp(b * x) for x in xp]

plt.scatter(xs, ys)
plt.plot(xp, yp)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Regresion exponencial por minimos cuadrados")
plt.grid(True)
plt.show()
