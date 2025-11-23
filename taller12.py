import math

x0 = 0.8
x = 0.805
h = x - x0

f_real = math.exp(-x)      # e^{-0.805}
exp_x0 = math.exp(-x0)     # e^{-0.8}

aprox = 0.0

for n in range(0, 16):     # de orden 0 hasta orden 15
    # término de la serie
    term = ((-1)**n) * exp_x0 * (h**n) / math.factorial(n)
    aprox += term          # suma parcial = T_N
    
    # error relativo porcentual
    error_porcent = abs(f_real - aprox) / abs(f_real) * 100
    
    print(f"Orden {n:2d}: T_{n} = {aprox:.8f},  Error = {error_porcent:.6e} %")
