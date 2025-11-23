import math
import matplotlib.pyplot as plt
import numpy as np

xs = [0, 2, 4, 6, 8, 10, 12]
ys = [0, 1, 4, 7, 9, 18, 27]

n = len(xs)
sx = sum(xs)
sy = sum(ys)
sxy = sum(xs[i] * ys[i] for i in range(n))
sx2 = sum(x * x for x in xs)
sy2 = sum(y * y for y in ys)

b = (n * sxy - sx * sy) / (n * sx2 - sx * sx)
a = (sy - b * sx) / n

media_y = sy / n
SST = sum((y - media_y) ** 2 for y in ys)
y_hat = [a + b * x for x in xs]
SSE = sum((ys[i] - y_hat[i]) ** 2 for i in range(n))

sy_std = math.sqrt(SST / (n - 1))
syx = math.sqrt(SSE / (n - 2))

r = (n * sxy - sx * sy) / math.sqrt((n * sx2 - sx * sx) * (n * sy2 - sy * sy))
r2 = r * r

print("Recta ajustada: y =", a, "+", b, "* x")
print("Desviacion estandar sy:", sy_std)
print("Error estandar de la estimacion sy/x:", syx)
print("Coeficiente de determinacion r^2:", r2)
print("Coeficiente de correlacion r:", r)

xp = np.linspace(min(xs), max(xs), 100)
yp = a + b * xp

plt.scatter(xs, ys)
plt.plot(xp, yp)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Regresion lineal")
plt.grid(True)
plt.show()
