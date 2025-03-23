import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

def cargar_imagen():
    """Carga una imagen desde el sistema de archivos."""
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png;*.jpeg")])
    if ruta_imagen:
        global imagen_original
        imagen_original = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        mostrar_imagen(imagen_original, panel_original)

def guardar_imagen():
    """Guarda la imagen transformada en un archivo."""
    if imagen_transformada is None:
        messagebox.showerror("Error", "No hay una imagen transformada para guardar.")
        return
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
    if ruta_guardado:
        cv2.imwrite(ruta_guardado, imagen_transformada)
        messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

def mostrar_imagen(imagen, panel):
    """Muestra una imagen en un panel de Tkinter."""
    imagen_pil = Image.fromarray(imagen)
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    panel.config(image=imagen_tk)
    panel.image = imagen_tk

def aplicar_transformacion():
    """Aplica la transformación seleccionada a la imagen."""
    global imagen_transformada

    if imagen_original is None:
        messagebox.showerror("Error", "No se ha cargado una imagen.")
        return

    transformacion = opcion_transformacion.get()
    try:
        if transformacion == "Rotar":
            angulo = float(entrada_parametro_1.get())
            filas, columnas = imagen_original.shape
            matriz_rotacion = cv2.getRotationMatrix2D((columnas / 2, filas / 2), angulo, 1)
            imagen_transformada = cv2.warpAffine(imagen_original, matriz_rotacion, (columnas, filas))
        elif transformacion == "Escalar":
            fx = float(entrada_parametro_1.get())
            fy = float(entrada_parametro_2.get())
            imagen_transformada = cv2.resize(imagen_original, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
        elif transformacion == "Reflejar":
            eje = entrada_parametro_1.get().lower()
            if eje == "horizontal":
                imagen_transformada = cv2.flip(imagen_original, 0)
            elif eje == "vertical":
                imagen_transformada = cv2.flip(imagen_original, 1)
            else:
                raise ValueError("El eje debe ser 'horizontal' o 'vertical'.")
        elif transformacion == "Trasladar":
            dx = int(entrada_parametro_1.get())
            dy = int(entrada_parametro_2.get())
            filas, columnas = imagen_original.shape
            matriz_traslacion = np.float32([[1, 0, dx], [0, 1, dy]])
            imagen_transformada = cv2.warpAffine(imagen_original, matriz_traslacion, (columnas, filas))
        else:
            raise ValueError("Transformación no válida.")

        mostrar_imagen(imagen_transformada, panel_transformada)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al aplicar la transformación: {e}")

def actualizar_campos(*args):
    """Actualiza los campos visibles en función de la transformación seleccionada."""
    transformacion = opcion_transformacion.get()

    # Oculta todos los campos por defecto
    etiqueta_parametro_1.pack_forget()
    entrada_parametro_1.pack_forget()
    etiqueta_parametro_2.pack_forget()
    entrada_parametro_2.pack_forget()

    if transformacion == "Rotar":
        etiqueta_parametro_1.config(text="Ángulo (en grados):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5)
    elif transformacion == "Escalar":
        etiqueta_parametro_1.config(text="Factor X:")
        etiqueta_parametro_2.config(text="Factor Y:")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5)
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5)
    elif transformacion == "Reflejar":
        etiqueta_parametro_1.config(text="Eje (horizontal/vertical):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5)
    elif transformacion == "Trasladar":
        etiqueta_parametro_1.config(text="Desplazamiento X:")
        etiqueta_parametro_2.config(text="Desplazamiento Y:")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5)
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Transformaciones Geométricas de Imágenes")

# Paneles para las imágenes
panel_original = tk.Label(ventana)
panel_original.pack(side="left", padx=10, pady=10)
panel_transformada = tk.Label(ventana)
panel_transformada.pack(side="right", padx=10, pady=10)

# Opciones del menú
opcion_transformacion = tk.StringVar(value="Rotar")
opcion_transformacion.trace("w", actualizar_campos)
menu_transformaciones = tk.OptionMenu(ventana, opcion_transformacion, "Rotar", "Escalar", "Reflejar", "Trasladar")
menu_transformaciones.pack(pady=10)

# Campos de entrada
etiqueta_parametro_1 = tk.Label(ventana, text="")
entrada_parametro_1 = tk.Entry(ventana)
etiqueta_parametro_2 = tk.Label(ventana, text="")
entrada_parametro_2 = tk.Entry(ventana)
actualizar_campos()

# Botones
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(pady=5)

boton_aplicar = tk.Button(ventana, text="Aplicar Transformación", command=aplicar_transformacion)
boton_aplicar.pack(pady=5)

boton_guardar = tk.Button(ventana, text="Guardar Imagen", command=guardar_imagen)
boton_guardar.pack(pady=5)

# Variables globales
imagen_original = None
imagen_transformada = None

ventana.mainloop()
