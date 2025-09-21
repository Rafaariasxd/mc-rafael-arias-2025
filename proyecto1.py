import tkinter as tk
from tkinter import messagebox

WIDTH = 16

def clamp_width(bits, width=WIDTH):
    if len(bits) > width:
        bits = bits[-width:]
    elif len(bits) < width:
        bits = [0] * (width - len(bits)) + bits
    return bits

def int_to_twos(n, width=WIDTH):
    n = n % (1 << width)
    out = [(n >> i) & 1 for i in range(width - 1, -1, -1)]
    return out

def twos_to_int(bits):
    bits = clamp_width(bits)
    if bits[0] == 1:
        unsigned = 0
        for b in bits:
            unsigned = (unsigned << 1) | b
        return unsigned - (1 << len(bits))
    else:
        val = 0
        for b in bits:
            val = (val << 1) | b
        return val

def add_bits(a, b, width=WIDTH):
    a = clamp_width(a, width)
    b = clamp_width(b, width)
    carry = 0
    res = [0] * width
    for i in range(width - 1, -1, -1):
        s = a[i] + b[i] + carry
        res[i] = s & 1
        carry = 1 if s >= 2 else 0
    return res

def not_bits(x):
    return [1 - b for b in x]

def inc_bits(x):
    return add_bits(x, int_to_twos(1, len(x)), len(x))

def neg_bits(x):
    return inc_bits(not_bits(x))

def sub_bits(a, b, width=WIDTH):
    return add_bits(a, neg_bits(b), width)

def shift_left(bits, k=1, width=WIDTH):
    bits = clamp_width(bits, width)
    for _ in range(k):
        bits = clamp_width(bits[1:] + [0], width)
    return bits

def shift_right_arith(bits, k=1, width=WIDTH):
    bits = clamp_width(bits, width)
    for _ in range(k):
        sign = bits[0]
        bits = [sign] + bits[:-1]
    return bits

def mul_bits(a, b, width=WIDTH):
    a_s = twos_to_int(a)
    b_s = twos_to_int(b)
    sign = 1
    if a_s < 0:
        a = neg_bits(a)
        sign *= -1
    if b_s < 0:
        b = neg_bits(b)
        sign *= -1
    result = int_to_twos(0, width)
    temp_a = a[:]
    for i in range(width):
        bit = b[-1 - i] if i < width else 0
        if bit == 1:
            result = add_bits(result, clamp_width(temp_a, width), width)
        temp_a = shift_left(temp_a, 1, width)
    if sign < 0:
        result = neg_bits(result)
    return clamp_width(result, width)

def compare_mag(a, b):
    if len(a) != len(b):
        a = clamp_width(a, max(len(a), len(b)))
        b = clamp_width(b, max(len(a), len(b)))
    for i in range(len(a)):
        if a[i] != b[i]:
            return 1 if a[i] > b[i] else -1
    return 0

def abs_bits(x):
    return neg_bits(x) if x[0] == 1 else x[:]

def div_bits(a, b, width=WIDTH):
    if all(bit == 0 for bit in b):
        raise ZeroDivisionError("División por cero")
    sign = -1 if (twos_to_int(a) < 0) ^ (twos_to_int(b) < 0) else 1
    A = abs_bits(a)
    B = abs_bits(b)
    quotient = [0] * width
    remainder = [0] * width
    for i in range(width):
        remainder = shift_left(remainder, 1, width)
        remainder[-1] = A[i]
        if compare_mag(remainder, B) >= 0:
            remainder = sub_bits(remainder, B, width)
            quotient[i] = 1
        else:
            quotient[i] = 0
    q = quotient
    if sign < 0:
        q = neg_bits(q)
    return clamp_width(q, width)

def tokenize(expr: str):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/":
            if c == '-' and (len(tokens) == 0 or tokens[-1] in ['+','-','*','/']):
                j = i + 1
                if j < len(expr) and expr[j].isdigit():
                    num = '-'
                    while j < len(expr) and expr[j].isdigit():
                        num += expr[j]
                        j += 1
                    tokens.append(num)
                    i = j
                    continue
            tokens.append(c)
            i += 1
        elif c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            raise ValueError(f"Carácter no válido: {c}")
    return tokens

def to_bits(token):
    return int_to_twos(int(token), WIDTH)

def eval_no_parens(expr: str):
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Expresión vacía")
    values = []
    ops = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ['+', '-']:
            i += 1
            continue
        if t in ['*', '/']:
            ops.append(t)
            i += 1
            continue
        a_bits = to_bits(t)
        if ops and ops[-1] in ['*', '/'] and len(values) > 0:
            op = ops.pop()
            left = values.pop()
            if op == '*':
                res = mul_bits(left, a_bits, WIDTH)
            else:
                res = div_bits(left, a_bits, WIDTH)
            values.append(res)
        else:
            values.append(a_bits)
        i += 1
    ops2 = [t for t in tokens if t in ['+','-']]
    res = values[0]
    idx_val = 1
    for op in ops2:
        right = values[idx_val]
        idx_val += 1
        if op == '+':
            res = add_bits(res, right, WIDTH)
        else:
            res = sub_bits(res, right, WIDTH)
    return clamp_width(res, WIDTH)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Binaria (16 bits, C2)")
        self.geometry("720x360")

        tk.Label(self, text="Escribe una expresión (sin paréntesis):").pack(anchor='w', padx=12, pady=(12, 4))
        self.entry = tk.Entry(self, font=("Consolas", 14))
        self.entry.pack(fill='x', padx=12)
        self.entry.insert(0, "4+5*2")

        tk.Button(self, text="Calcular", command=self.on_calc).pack(pady=8)

        self.dec_label = tk.Label(self, text="Resultado (decimal): —", font=("Consolas", 14))
        self.dec_label.pack(anchor='w', padx=12, pady=(6, 2))

        self.bin_label = tk.Label(self, text="Resultado (binario 16 bits): —", font=("Consolas", 14))
        self.bin_label.pack(anchor='w', padx=12)

        self.list_label = tk.Label(self, text="Lista de bits [MSB..LSB]: —", font=("Consolas", 12))
        self.list_label.pack(anchor='w', padx=12, pady=(6, 2))

        note = (
            
            "Soporta +, -, *, /. Sin paréntesis. División entera truncada hacia 0."
        )
        tk.Label(self, text=note, fg="#444").pack(anchor='w', padx=12, pady=(6, 2))

    def on_calc(self):
        expr = self.entry.get().strip()
        try:
            bits = eval_no_parens(expr)
            dec = twos_to_int(bits)
            bin_str = ''.join(str(b) for b in bits)
            grouped = ' '.join(bin_str[i:i+4] for i in range(0, len(bin_str), 4))
            self.dec_label.config(text=f"Resultado (decimal): {dec}")
            self.bin_label.config(text=f"Resultado (binario 16 bits): {grouped}")
            self.list_label.config(text=f"Lista de bits [MSB..LSB]: {bits}")
        except ZeroDivisionError:
            messagebox.showerror("Error", "División por cero")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    App().mainloop()
