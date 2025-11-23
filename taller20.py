import math


xs = [0, 1, 2, 3, 4, 5, 6, 7]
ys = [5.5, 5.4, 4.0, 3.7, 3.0, 2.0, 2.0, 1.5]

n = len(xs)
sx = sum(xs)
sx2 = sum(x * x for x in xs)
sx3 = sum(x ** 3 for x in xs)
sx4 = sum(x ** 4 for x in xs)
sy = sum(ys)
sxy = sum(xs[i] * ys[i] for i in range(n))
sx2y = sum((xs[i] ** 2) * ys[i] for i in range(n))

A = np.array([[n, sx, sx2],
              [sx, sx2, sx3],
              [sx2, sx3, sx4]], dtype=float)
B = np.array([sy, sxy, sx2y], dtype=float)

a, b, c = np.linalg.solve(A, B)

y_hat = [a + b * x + c * x * x for x in xs]
media_y = sy / n
SST = sum((ys[i] - media_y) ** 2 for i in range(n))
SSE = sum((ys[i] - y_hat[i]) ** 2 for i in range(n))
r2 = 1 - SSE / SST
r = math.sqrt(r2)

print("Polinomio ajustado: y = {:.6f} + {:.6f} x + {:.6f} x^2".format(a, b, c))
print("Coeficiente de determinacion r^2 =", r2)
print("Coeficiente de correlacion r =", r)

xp = np.linspace(min(xs), max(xs), 200)
yp = a + b * xp + c * xp * xp

plt.scatter(xs, ys)
plt.plot(xp, yp)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Ajuste polinomial de segundo grado")
plt.grid(True)
plt.show()
