from PIL import Image
import matplotlib.pyplot as plt

ruta = input("Ruta de la imagen (JPG o PNG): ")

img = Image.open(ruta).convert("RGB")
ancho, alto = img.size

tensor_rgb = []
for y in range(alto):
    fila = []
    for x in range(ancho):
        r, g, b = img.getpixel((x, y))
        fila.append([r, g, b])
    tensor_rgb.append(fila)

tensor_gris = []
for y in range(alto):
    fila = []
    for x in range(ancho):
        r, g, b = tensor_rgb[y][x]
        gris = int(0.299 * r + 0.587 * g + 0.114 * b)
        fila.append(gris)
    tensor_gris.append(fila)

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.title("Imagen RGB")
plt.imshow(tensor_rgb)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Imagen en gris")
plt.imshow(tensor_gris, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()
