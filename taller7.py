def to_binary16(n):
    """Convierte un entero con signo (-32768 a 32767) a binario de 16 bits en complemento a dos"""
    return format(n & 0xFFFF, "016b")

def from_binary16(b):
    """Convierte un binario de 16 bits en complemento a dos a un entero con signo"""
    n = int(b, 2)
    if n >= 2**15:  # si el bit más significativo es 1
        n -= 2**16
    return n

# Entrada
a = int(input("Ingrese el primer número (-32768 a 32767): "))
b = int(input("Ingrese el segundo número (-32768 a 32767): "))

if not (-32768 <= a <= 32767 and -32768 <= b <= 32767):
    print("Error: los números deben estar en el rango [-32768, 32767]")
else:
    # Conversión a binario
    a_bin = to_binary16(a)
    b_bin = to_binary16(b)

    # Suma en complemento a dos (módulo 2^16)
    suma = (a + b) & 0xFFFF
    suma_bin = format(suma, "016b")

    # Convertir el resultado a entero con signo
    suma_int = from_binary16(suma_bin)

    # Salida
    print(f"A = {a} → {a_bin}")
    print(f"B = {b} → {b_bin}")
    print(f"A + B (binario 16 bits) = {suma_bin}")
    print(f"A + B (entero con signo) = {suma_int}")
