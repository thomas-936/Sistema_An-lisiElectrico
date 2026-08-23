import tkinter as tk
from tkinter import messagebox
import math


def abrir_calculadora_electrica():
    ventana = tk.Toplevel(raiz)
    ventana.title("Calculadora Electrica")
    ventana.geometry("400x420")
    ventana.bind("<Escape>", lambda evento: ventana.destroy())
    ventana.focus_force()

    tk.Label(ventana, text="Círculo Eléctrico", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="Ingresa 2 valores cualquiera y calcula el resto",
             font=("Arial", 9)).pack(pady=(0, 15))

    frame = tk.Frame(ventana)
    frame.pack(pady=5)

    tk.Label(frame, text="Voltaje (V):", width=15, anchor="w").grid(row=0, column=0, padx=5, pady=8)
    entry_v = tk.Entry(frame, width=15)
    entry_v.grid(row=0, column=1)

    tk.Label(frame, text="Corriente (I):", width=15, anchor="w").grid(row=1, column=0, padx=5, pady=8)
    entry_i = tk.Entry(frame, width=15)
    entry_i.grid(row=1, column=1)

    tk.Label(frame, text="Resistencia (R):", width=15, anchor="w").grid(row=2, column=0, padx=5, pady=8)
    entry_r = tk.Entry(frame, width=15)
    entry_r.grid(row=2, column=1)

    tk.Label(frame, text="Potencia (W):", width=15, anchor="w").grid(row=3, column=0, padx=5, pady=8)
    entry_w = tk.Entry(frame, width=15)
    entry_w.grid(row=3, column=1)

    campos = [entry_v, entry_i, entry_r, entry_w]

    def mover_siguiente(evento):
        indice_actual = campos.index(evento.widget)
        if indice_actual < len(campos) - 1:
            campos[indice_actual + 1].focus_set()
        return "break"

    def mover_anterior(evento):
        indice_actual = campos.index(evento.widget)
        if indice_actual > 0:
            campos[indice_actual - 1].focus_set()
        return "break"

    for campo in campos:
        campo.bind("<Return>", mover_siguiente)
        campo.bind("<Up>", mover_anterior)
        campo.bind("<Down>", mover_siguiente)

    resultado_label = tk.Label(ventana, text="", font=("Arial", 10), fg="#1eb851", justify="left")
    resultado_label.pack(pady=15)

    def obtener(entry):
        texto = entry.get().strip()
        if texto == "":
            return None
        try:
            return float(texto)
        except ValueError:
            return None

    def calcular():
        v = obtener(entry_v)
        i = obtener(entry_i)
        r = obtener(entry_r)
        w = obtener(entry_w)

        conocidos = sum(x is not None for x in (v, i, r, w))

        if conocidos < 2:
            messagebox.showwarning("Faltan datos", "Ingresa al menos 2 valores.")
            return

        try:
            if v is not None and i is not None:
                r = v / i
                w = v * i
            elif v is not None and r is not None:
                i = v / r
                w = v * i
            elif v is not None and w is not None:
                i = w / v
                r = v / i
            elif i is not None and r is not None:
                v = i * r
                w = v * i
            elif i is not None and w is not None:
                v = w / i
                r = v / i
            elif r is not None and w is not None:
                i = math.sqrt(w / r)
                v = i * r
            else:
                messagebox.showwarning("Faltan datos", "Ingresa 2 valores válidos.")
                return

            entry_v.delete(0, tk.END)
            entry_v.insert(0, f"{v:.2f}")
            entry_i.delete(0, tk.END)
            entry_i.insert(0, f"{i:.2f}")
            entry_r.delete(0, tk.END)
            entry_r.insert(0, f"{r:.2f}")
            entry_w.delete(0, tk.END)
            entry_w.insert(0, f"{w:.2f}")

            resultado_label.config(
                text=f"V = {v:.2f} V\nI = {i:.2f} A\nR = {r:.2f} Ω\nW = {w:.2f} W"
            )
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero.")

    def limpiar():
        entry_v.delete(0, tk.END)
        entry_i.delete(0, tk.END)
        entry_r.delete(0, tk.END)
        entry_w.delete(0, tk.END)
        resultado_label.config(text="")

    botones_frame = tk.Frame(ventana)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Calcular", command=calcular,
              bg="#1eb851", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Limpiar", command=limpiar,
              bg="#b11921", fg="white", width=12).grid(row=0, column=1, padx=5)
    ventana.bind("<Return>", lambda event: calcular())


def abrir_caida_tension():
    ventana = tk.Toplevel(raiz)
    ventana.title("Caida de Tension")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Caída de Tensión", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="(Aqui va el contenido de esta seccion)").pack()


def abrir_factor_relleno():
    ventana = tk.Toplevel(raiz)
    ventana.title("Factor de Relleno")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Factor de Relleno", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="(Aqui va el contenido de esta seccion)").pack()


def abrir_conversion_unidades():
    ventana = tk.Toplevel(raiz)
    ventana.title("Conversion de Unidades")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Conversion de Unidades", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="(Aqui va el contenido de esta seccion)").pack()


raiz = tk.Tk()
raiz.title("Analizador de Instalaciones Eléctricas")
raiz.state("zoomed")
raiz.config(bg="#2c3e50")

titulo = tk.Label(raiz, text="Analizador de Instalaciones Eléctricas",
                   font=("Arial", 20, "bold"),
                   bg="#2c3e50", fg="white")
titulo.pack(pady=70)

boton1 = tk.Button(raiz, text="1. Calculadora Eléctrica", width=30, height=2, command=abrir_calculadora_electrica, bg="#1eb851", fg="white")
boton1.pack(pady=10)

boton2 = tk.Button(raiz, text="2. Caida de Tensión", width=30, height=2, command=abrir_caida_tension, bg="#c4d811", fg="white")
boton2.pack(pady=10)

boton3 = tk.Button(raiz, text="3. Calcular Factor de Relleno", width=30, height=2, command=abrir_factor_relleno, bg="#b11921", fg="white")
boton3.pack(pady=10)

boton4 = tk.Button(raiz, text="4. Conversión de Unidades ", width=30, height=2, command=abrir_conversion_unidades, bg="#1f40c3", fg="white")
boton4.pack(pady=10)

raiz.mainloop()
