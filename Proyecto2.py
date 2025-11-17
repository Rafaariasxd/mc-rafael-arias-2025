import tkinter as tk
from tkinter import filedialog, messagebox

PI = 3.141592653589793


def deg_to_rad(grados):
    return grados * PI / 180.0


def sin_taylor(x):
    termino = x
    suma = x
    n = 1
    while n < 10:
        termino = -termino * x * x / ((2 * n) * (2 * n + 1))
        suma += termino
        n += 1
    return suma


def cos_taylor(x):
    termino = 1.0
    suma = 1.0
    n = 1
    while n < 10:
        termino = -termino * x * x / ((2 * n - 1) * (2 * n))
        suma += termino
        n += 1
    return suma


def photo_to_tensor(photo):
    width = photo.width()
    height = photo.height()
    tensor = []
    for y in range(height):
        fila = []
        for x in range(width):
            pixel = photo.get(x, y)
            if isinstance(pixel, str):
                r = int(pixel[1:3], 16)
                g = int(pixel[3:5], 16)
                b = int(pixel[5:7], 16)
            else:
                r, g, b = pixel
            fila.append([r, g, b])
        tensor.append(fila)
    return tensor


def tensor_to_photo(tensor):
    height = len(tensor)
    if height == 0:
        return tk.PhotoImage(width=1, height=1)
    width = len(tensor[0])
    photo = tk.PhotoImage(width=width, height=height)
    for y in range(height):
        partes = ["{"]
        for x in range(width):
            r, g, b = tensor[y][x]
            partes.append(f"#{r:02x}{g:02x}{b:02x}")
        partes.append("}")
        fila_str = " ".join(partes)
        photo.put(fila_str, to=(0, y))
    return photo


def get_size(tensor):
    h = len(tensor)
    w = len(tensor[0]) if h > 0 else 0
    return w, h


def to_grayscale(tensor):
    w, h = get_size(tensor)
    res = []
    for y in range(h):
        fila = []
        for x in range(w):
            r, g, b = tensor[y][x]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            fila.append([gray, gray, gray])
        res.append(fila)
    return res


def resize_tensor(tensor, porcentaje):
    old_w, old_h = get_size(tensor)
    new_w = max(1, int(old_w * porcentaje / 100))
    new_h = max(1, int(old_h * porcentaje / 100))
    res = [[[0, 0, 0] for _ in range(new_w)] for _ in range(new_h)]
    for y_n in range(new_h):
        for x_n in range(new_w):
            x_o = min(old_w - 1, int(x_n * old_w / new_w))
            y_o = min(old_h - 1, int(y_n * old_h / new_h))
            res[y_n][x_n] = tensor[y_o][x_o]
    return res


def flip_horizontal(tensor):
    w, h = get_size(tensor)
    res = []
    for y in range(h):
        fila = [None] * w
        for x in range(w):
            fila[w - 1 - x] = tensor[y][x]
        res.append(fila)
    return res


def flip_vertical(tensor):
    w, h = get_size(tensor)
    res = [None] * h
    for y in range(h):
        res[h - 1 - y] = tensor[y]
    return res


def rotate_tensor(tensor, angle_deg):
    w, h = get_size(tensor)
    rad = deg_to_rad(angle_deg)
    cos_a = cos_taylor(rad)
    sin_a = sin_taylor(rad)
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    for y_n in range(h):
        for x_n in range(w):
            x_rel = x_n - cx
            y_rel = y_n - cy
            x_o_rel = cos_a * x_rel + sin_a * y_rel
            y_o_rel = -sin_a * x_rel + cos_a * y_rel
            x_o = x_o_rel + cx
            y_o = y_o_rel + cy
            x0 = int(round(x_o))
            y0 = int(round(y_o))
            if 0 <= x0 < w and 0 <= y0 < h:
                res[y_n][x_n] = tensor[y0][x0]
    return res


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto - Transformaciones de imagen (solo Tkinter)")
        self.tensor = None
        self.photo = None

        frame_img = tk.Frame(root)
        frame_img.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(frame_img, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        vbar = tk.Scrollbar(frame_img, orient="vertical", command=self.canvas.yview)
        vbar.pack(side="right", fill="y")

        hbar = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        hbar.pack(fill="x")

        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas_image = None

        top = tk.Frame(root)
        top.pack(pady=5)
        tk.Button(top, text="Cargar imagen", command=self.cargar_imagen).grid(row=0, column=0, padx=5)
        tk.Button(top, text="Guardar imagen", command=self.guardar_imagen).grid(row=0, column=1, padx=5)

        options = tk.Frame(root)
        options.pack(pady=10)
        self.gray_var = tk.BooleanVar()
        tk.Checkbutton(options, text="Escala de grises", variable=self.gray_var).grid(row=0, column=0, sticky="w")
        self.scale_var = tk.BooleanVar()
        tk.Checkbutton(options, text="Cambiar tamaño (%)", variable=self.scale_var).grid(row=1, column=0, sticky="w")
        self.scale_entry = tk.Entry(options, width=5)
        self.scale_entry.insert(0, "100")
        self.scale_entry.grid(row=1, column=1, padx=5)
        self.flip_h_var = tk.BooleanVar()
        tk.Checkbutton(options, text="Invertir horizontal", variable=self.flip_h_var).grid(row=2, column=0, sticky="w")
        self.flip_v_var = tk.BooleanVar()
        tk.Checkbutton(options, text="Invertir vertical", variable=self.flip_v_var).grid(row=3, column=0, sticky="w")
        self.rotate_var = tk.BooleanVar()
        tk.Checkbutton(options, text="Rotar (0-180°)", variable=self.rotate_var).grid(row=4, column=0, sticky="w")
        self.angle_entry = tk.Entry(options, width=5)
        self.angle_entry.insert(0, "0")
        self.angle_entry.grid(row=4, column=1, padx=5)

        tk.Button(root, text="Aplicar transformaciones", command=self.aplicar_transformaciones).pack(pady=10)

    def mostrar_photo(self, photo):
        self.photo = photo
        self.canvas.delete("all")
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        w = self.photo.width()
        h = self.photo.height()
        self.canvas.config(scrollregion=(0, 0, w, h))

    def cargar_imagen(self):
        path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes PNG", "*.png"), ("Todos los archivos", "*.*")]
        )
        if not path:
            return
        try:
            photo = tk.PhotoImage(file=path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")
            return
        self.tensor = photo_to_tensor(photo)
        self.mostrar_photo(photo)

    def guardar_imagen(self):
        if self.tensor is None:
            messagebox.showinfo("Info", "No hay imagen para guardar.")
            return
        photo = tensor_to_photo(self.tensor)
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if not path:
            return
        try:
            photo.write(path, format="png")
            messagebox.showinfo("Éxito", "Imagen guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{e}")

    def aplicar_transformaciones(self):
        if self.tensor is None:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        tensor = self.tensor
        if self.gray_var.get():
            tensor = to_grayscale(tensor)
        if self.scale_var.get():
            try:
                p = int(self.scale_entry.get())
            except ValueError:
                p = 100
            if p < 1:
                p = 1
            tensor = resize_tensor(tensor, p)
        if self.flip_h_var.get():
            tensor = flip_horizontal(tensor)
        if self.flip_v_var.get():
            tensor = flip_vertical(tensor)
        if self.rotate_var.get():
            try:
                ang = int(self.angle_entry.get())
            except ValueError:
                ang = 0
            if ang < 0:
                ang = 0
            if ang > 180:
                ang = 180
            tensor = rotate_tensor(tensor, ang)
        self.tensor = tensor
        photo = tensor_to_photo(tensor)
        self.mostrar_photo(photo)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
