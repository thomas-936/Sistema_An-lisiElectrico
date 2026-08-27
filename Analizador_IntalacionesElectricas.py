import tkinter as tk
from tkinter import messagebox, ttk
import math

# Tabla de resistividad de los materiales (Ohm*mm2/m a 20 grados C)
RESISTIVIDAD = {
    "Cobre": 0.0175,
    "Aluminio": 0.0282,
}

# Tabla de calibres AWG y su area en mm2 (Tabla 1 del material del curso)
TABLA_AWG = {
    "14 AWG": 2.082,
    "12 AWG": 3.307,
    "10 AWG": 5.260,
    "8 AWG": 8.367,
    "6 AWG": 13.300,
    "4 AWG": 21.150,
    "2 AWG": 33.620,
    "1/0 AWG": 53.480,
    "2/0 AWG": 67.430,
    "3/0 AWG": 85.010,
    "4/0 AWG": 107.200,
}

# Lista ordenada de menor a mayor area, para poder recorrerla al buscar un calibre adecuado
ORDEN_AWG = ["14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG", "2 AWG",
             "1/0 AWG", "2/0 AWG", "3/0 AWG", "4/0 AWG"]

# Tabla 4.4 del material: capacidad de corriente (ampacidad) segun el tipo de aislamiento
TABLA_AMPACIDAD = {
    "14 AWG":  {"TW": 20,  "THW": 20,  "THHN/THWN": 25},
    "12 AWG":  {"TW": 25,  "THW": 25,  "THHN/THWN": 30},
    "10 AWG":  {"TW": 30,  "THW": 35,  "THHN/THWN": 40},
    "8 AWG":   {"TW": 40,  "THW": 50,  "THHN/THWN": 55},
    "6 AWG":   {"TW": 55,  "THW": 65,  "THHN/THWN": 75},
    "4 AWG":   {"TW": 70,  "THW": 85,  "THHN/THWN": 95},
    "2 AWG":   {"TW": 95,  "THW": 115, "THHN/THWN": 130},
    "1/0 AWG": {"TW": 125, "THW": 150, "THHN/THWN": 170},
    "2/0 AWG": {"TW": 145, "THW": 175, "THHN/THWN": 195},
    "3/0 AWG": {"TW": 165, "THW": 200, "THHN/THWN": 225},
    "4/0 AWG": {"TW": 195, "THW": 230, "THHN/THWN": 260},
}

TIPOS_AISLAMIENTO = ["TW", "THW", "THHN/THWN"]


def abrir_calculadora_electrica():
    ventana = tk.Toplevel(raiz)
    ventana.title("Calculadora Electrica")
    ventana.geometry("400x420")
    ventana.bind("<Escape>", lambda evento: ventana.destroy())

    tk.Label(ventana, text="Círculo Eléctrico", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="Ingresa 2 valores cualquiera y calcula el resto",
             font=("Arial", 9)).pack(pady=(0, 15))

    frame = tk.Frame(ventana)
    frame.pack(pady=5)

    # Entradas: Voltaje, Corriente, Resistencia, Potencia
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
        indede_actual = campos.index(evento.widget)
        if indede_actual < len(campos) - 1:
            campos[indede_actual + 1].focus_set()
        return "break"

    def mover_anterior(evento):
        indede_actual = campos.index(evento.widget)
        if indede_actual > 0:
            campos[indede_actual - 1].focus_set()
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
            # Calculamos los 2 valores faltantes según cuáles ya conocemos
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

            # Actualizamos los campos con todos los valores
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
    ventana.geometry("480x680")
    ventana.bind("<Escape>", lambda evento: ventana.destroy())
    ventana.focus_force()

    tk.Label(ventana, text="Caída de Tensión", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="Circuito monofásico - Método de la resistividad",
             font=("Arial", 9)).pack(pady=(0, 15))

    frame = tk.Frame(ventana)
    frame.pack(pady=5)

    tk.Label(frame, text="Voltaje del sistema (V):", width=24, anchor="w").grid(row=0, column=0, padx=5, pady=6)
    entry_v = tk.Entry(frame, width=15)
    entry_v.grid(row=0, column=1)

    tk.Label(frame, text="Potencia de la carga (W):", width=24, anchor="w").grid(row=1, column=0, padx=5, pady=6)
    entry_p = tk.Entry(frame, width=15)
    entry_p.grid(row=1, column=1)

    tk.Label(frame, text="Corriente (A), si ya la conoces:", width=24, anchor="w").grid(row=2, column=0, padx=5, pady=6)
    entry_i = tk.Entry(frame, width=15)
    entry_i.grid(row=2, column=1)

    tk.Label(frame, text="Material del conductor:", width=24, anchor="w").grid(row=3, column=0, padx=5, pady=6)
    combo_material = ttk.Combobox(frame, values=list(RESISTIVIDAD.keys()), width=13, state="readonly")
    combo_material.grid(row=3, column=1)
    combo_material.current(0)

    tk.Label(frame, text="Longitud del circuito (m):", width=24, anchor="w").grid(row=4, column=0, padx=5, pady=6)
    entry_l = tk.Entry(frame, width=15)
    entry_l.grid(row=4, column=1)

    tk.Label(frame, text="Calibre del conductor (AWG):", width=24, anchor="w").grid(row=5, column=0, padx=5, pady=6)
    combo_calibre = ttk.Combobox(frame, values=ORDEN_AWG, width=13, state="readonly")
    combo_calibre.grid(row=5, column=1)
    combo_calibre.current(2)

    tk.Label(frame, text="O sección directa (mm²):", width=24, anchor="w").grid(row=6, column=0, padx=5, pady=6)
    entry_area_manual = tk.Entry(frame, width=15)
    entry_area_manual.grid(row=6, column=1)

    tk.Label(frame, text="Tipo de aislamiento:", width=24, anchor="w").grid(row=7, column=0, padx=5, pady=6)
    combo_aislamiento = ttk.Combobox(frame, values=TIPOS_AISLAMIENTO, width=13, state="readonly")
    combo_aislamiento.grid(row=7, column=1)
    combo_aislamiento.current(1)

    tk.Label(frame, text="Caída de tensión máx. permitida (%):", width=24, anchor="w").grid(row=8, column=0, padx=5, pady=6)
    entry_max = tk.Entry(frame, width=15)
    entry_max.grid(row=8, column=1)
    entry_max.insert(0, "3")

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

    def buscar_calibre_adecuado(v, i, l, rho, max_caida, aislamiento):
        # Recorre la tabla de menor a mayor area y devuelve el primer calibre que
        # cumpla TANTO la caida de tension COMO la ampacidad (capacidad de corriente)
        for calibre in ORDEN_AWG:
            area = TABLA_AWG[calibre]
            caida_v = (2 * l * i * rho) / area
            porcentaje = (caida_v / v) * 100
            ampacidad = TABLA_AMPACIDAD[calibre][aislamiento]
            if porcentaje <= max_caida and i <= ampacidad:
                return calibre
        return "Ninguno de la tabla cumple, se necesita un calibre mayor"

    def calcular():
        v = obtener(entry_v)
        p = obtener(entry_p)
        i = obtener(entry_i)
        l = obtener(entry_l)
        max_caida = obtener(entry_max)
        material = combo_material.get()
        calibre = combo_calibre.get()
        aislamiento = combo_aislamiento.get()
        area_manual = obtener(entry_area_manual)

        if v is None or l is None or max_caida is None or material == "" or aislamiento == "":
            messagebox.showwarning("Faltan datos", "Completa voltaje, longitud, material, aislamiento y caída máxima.")
            return

        if i is None:
            if p is None:
                messagebox.showwarning("Faltan datos", "Ingresa la potencia o la corriente de la carga.")
                return
            if v == 0:
                messagebox.showerror("Error", "El voltaje no puede ser 0.")
                return
            i = p / v  # I = P / V (monofasico, factor de potencia = 1)

        rho = RESISTIVIDAD[material]

        # Si el usuario escribio una seccion manual en mm2, esa tiene prioridad sobre el AWG
        if area_manual is not None:
            area = area_manual
        else:
            if calibre == "":
                messagebox.showwarning("Faltan datos", "Selecciona un calibre AWG o escribe la sección en mm².")
                return
            area = TABLA_AWG[calibre]

        # Formula de caida de tension por resistividad (circuito monofasico, ida y vuelta)
        caida_v = (2 * l * i * rho) / area
        porcentaje = (caida_v / v) * 100

        if porcentaje <= max_caida:
            estado = "CUMPLE"
            color_estado = "#1eb851"
        else:
            estado = "NO CUMPLE"
            color_estado = "#b11921"

        # Validacion de ampacidad: solo se puede comparar si el calibre es uno de la tabla AWG
        texto_ampacidad = ""
        if calibre != "" and calibre in TABLA_AMPACIDAD:
            ampacidad = TABLA_AMPACIDAD[calibre][aislamiento]
            if i <= ampacidad:
                texto_ampacidad = f"\nAmpacidad ({aislamiento}): {ampacidad} A -> OK"
            else:
                texto_ampacidad = f"\nAmpacidad ({aislamiento}): {ampacidad} A -> EXCEDE, sube de calibre"
                estado = "NO CUMPLE"
                color_estado = "#b11921"

        sugerencia = ""
        if estado == "NO CUMPLE":
            sugerencia = buscar_calibre_adecuado(v, i, l, rho, max_caida, aislamiento)

        texto_resultado = (
            f"Corriente: {i:.2f} A\n"
            f"Caída de tensión: {caida_v:.2f} V\n"
            f"Porcentaje de caída: {porcentaje:.2f} %\n"
            f"Estado: {estado}"
            f"{texto_ampacidad}"
        )
        if sugerencia:
            texto_resultado += f"\nCalibre sugerido: {sugerencia}"

        resultado_label.config(text=texto_resultado, fg=color_estado)

    def limpiar():
        entry_v.delete(0, tk.END)
        entry_p.delete(0, tk.END)
        entry_i.delete(0, tk.END)
        entry_l.delete(0, tk.END)
        entry_area_manual.delete(0, tk.END)
        entry_max.delete(0, tk.END)
        entry_max.insert(0, "3")
        resultado_label.config(text="")

    botones_frame = tk.Frame(ventana)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Calcular", command=calcular,
              bg="#1eb851", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Limpiar", command=limpiar,
              bg="#b11921", fg="white", width=12).grid(row=0, column=1, padx=5)

    ventana.bind("<Return>", lambda evento: calcular())


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
