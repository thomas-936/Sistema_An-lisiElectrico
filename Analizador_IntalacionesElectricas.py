import tkinter as tk
from tkinter import messagebox, ttk
import math
import sqlite3
from datetime import datetime

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

# Tabla 4.5 del curso: area interna real de la tuberia conduit PVC (mm2)
TABLA_TUBERIA = {
    '1/2"': 260,
    '3/4"': 438,
    '1"': 723,
    '1 1/4"': 1170,
    '1 1/2"': 1534,
    '2"': 2397,
    '3"': 5350,
}

# Lista ordenada de menor a mayor area, para recorrerla al buscar una tuberia adecuada
ORDEN_TUBERIA = ['1/2"', '3/4"', '1"', '1 1/4"', '1 1/2"', '2"', '3"']

# Diametro nominal de cada tuberia en pulgadas (para el metodo de calculo del diametro minimo)
TUBERIA_PULGADAS = {
    '1/2"': 0.5, '3/4"': 0.75, '1"': 1.0, '1 1/4"': 1.25,
    '1 1/2"': 1.5, '2"': 2.0, '3"': 3.0,
}

MM2_POR_PULGADA2 = 645.2

# Tabla 4.7 del curso: area de los conductores CON aislamiento TW/THW, por conductor (mm2)
# (esta area es mas grande que el area del cobre desnudo, porque incluye el aislamiento)
TABLA_AREA_AISLADA = {
    "14 AWG": 9.24,
    "12 AWG": 12.0,
    "10 AWG": 16.1,
    "8 AWG": 29.2,
    "6 AWG": 48.0,
    "4 AWG": 64.2,
    "2 AWG": 87.8,
}

ORDEN_CALIBRE_RELLENO = ["14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG", "2 AWG"]


def limite_relleno(cantidad_conductores):
    # Factores de relleno aceptados por el RETIE (segun el material del curso)
    if cantidad_conductores == 1:
        return 55
    elif cantidad_conductores == 2:
        return 30
    else:
        return 40


NOMBRE_BD = "historial.db"


def conectar_bd():
    # Se conecta al archivo historial.db (lo crea si no existe) y se asegura
    # de que la tabla "historial" exista
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            tipo TEXT,
            resumen TEXT,
            estado TEXT
        )
    """)
    conexion.commit()
    return conexion


def guardar_historial(tipo, resumen, estado):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO historial (fecha, tipo, resumen, estado) VALUES (?, ?, ?, ?)",
        (fecha, tipo, resumen, estado)
    )
    conexion.commit()
    conexion.close()


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

    # Orden completo de campos (incluye los Entry y los Combobox) para navegar con Enter
    campos = [entry_v, entry_p, entry_i, combo_material, entry_l,
              combo_calibre, entry_area_manual, combo_aislamiento, entry_max]

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

    # Enter mueve al siguiente campo, sin importar si es Entry o Combobox
    for campo in campos:
        campo.bind("<Return>", mover_siguiente)

    # Las flechas arriba/abajo solo mueven el foco en los Entry (casillas de texto),
    # porque en los Combobox esas mismas flechas sirven para cambiar la opción elegida
    campos_entry = [entry_v, entry_p, entry_i, entry_l, entry_area_manual, entry_max]
    for campo in campos_entry:
        campo.bind("<Down>", mover_siguiente)
        campo.bind("<Up>", mover_anterior)

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
        guardar_historial("Caída de Tensión", texto_resultado, estado)

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
    ventana.geometry("520x700")
    ventana.bind("<Escape>", lambda evento: ventana.destroy())
    ventana.focus_force()

    tk.Label(ventana, text="Factor de Relleno de Tubería Conduit", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="Agrega un renglón por cada calibre distinto dentro de la tubería (TW/THW)",
             font=("Arial", 9)).pack(pady=(0, 10))

    encabezado = tk.Frame(ventana)
    encabezado.pack()
    tk.Label(encabezado, text="Cantidad", width=12, anchor="w").grid(row=0, column=0, padx=5)
    tk.Label(encabezado, text="Calibre AWG", width=14, anchor="w").grid(row=0, column=1, padx=5)
    tk.Label(encabezado, text="O área manual (mm²)", width=18, anchor="w").grid(row=0, column=2, padx=5)

    frame_filas = tk.Frame(ventana)
    frame_filas.pack(pady=5)

    filas = []  # cada elemento: (entry_cantidad, combo_calibre, entry_area_manual)

    def agregar_fila():
        idx = len(filas)
        entry_cant = tk.Entry(frame_filas, width=12)
        entry_cant.grid(row=idx, column=0, padx=5, pady=3)

        combo_cal = ttk.Combobox(frame_filas, values=ORDEN_CALIBRE_RELLENO, width=12, state="readonly")
        combo_cal.grid(row=idx, column=1, padx=5, pady=3)
        combo_cal.current(1)

        entry_area = tk.Entry(frame_filas, width=16)
        entry_area.grid(row=idx, column=2, padx=5, pady=3)

        filas.append((entry_cant, combo_cal, entry_area))
        entry_cant.focus_set()

    tk.Button(ventana, text="+ Agregar otro calibre", command=agregar_fila,
              bg="#1f40c3", fg="white").pack(pady=5)

    agregar_fila()  # primer renglón visible desde que se abre la ventana

    tk.Label(ventana, text="Tubería a verificar (opcional):", font=("Arial", 9)).pack(pady=(10, 0))
    combo_tuberia = ttk.Combobox(ventana, values=ORDEN_TUBERIA, width=13, state="readonly")
    combo_tuberia.pack(pady=5)

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
        area_total = 0.0
        total_conductores = 0
        detalle_lineas = []

        for entry_cant, combo_cal, entry_area in filas:
            cantidad = obtener(entry_cant)
            if cantidad is None:
                continue  # renglon vacio, se ignora
            if cantidad <= 0:
                messagebox.showwarning("Dato inválido", "La cantidad debe ser mayor a 0.")
                return

            cantidad = int(cantidad)
            area_manual = obtener(entry_area)
            calibre = combo_cal.get()

            if area_manual is not None:
                area_unitaria = area_manual
                etiqueta_calibre = f"{calibre} (área manual)" if calibre else "área manual"
            else:
                if calibre == "":
                    messagebox.showwarning("Faltan datos", "Selecciona un calibre o escribe el área manual.")
                    return
                area_unitaria = TABLA_AREA_AISLADA[calibre]
                etiqueta_calibre = calibre

            area_grupo = area_unitaria * cantidad
            area_total += area_grupo
            total_conductores += cantidad
            detalle_lineas.append(f"{cantidad} x {etiqueta_calibre} = {area_grupo:.2f} mm²")

        if total_conductores == 0:
            messagebox.showwarning("Faltan datos", "Ingresa al menos un renglón con cantidad y calibre.")
            return

        limite = limite_relleno(total_conductores)

        # Metodo del curso: AT = Ac / Fr  ->  area minima de tuberia requerida
        area_minima_mm2 = area_total / (limite / 100)
        area_minima_in2 = area_minima_mm2 / MM2_POR_PULGADA2
        diametro_necesario_in = 2 * math.sqrt(area_minima_in2 / math.pi)

        tuberia_recomendada = None
        for talla in ORDEN_TUBERIA:
            if TUBERIA_PULGADAS[talla] >= diametro_necesario_in:
                tuberia_recomendada = talla
                break
        if tuberia_recomendada is None:
            tuberia_recomendada = "Ninguna de la tabla alcanza, se necesita una tubería mayor"

        texto_resultado = (
            "Detalle de conductores:\n" + "\n".join(detalle_lineas) +
            f"\n\nTotal de conductores: {total_conductores}\n"
            f"Área total de conductores (Ac): {area_total:.2f} mm²\n"
            f"Factor de relleno máximo permitido: {limite} %\n"
            f"Diámetro mínimo requerido: {diametro_necesario_in:.2f} in\n"
            f"Tubería recomendada: {tuberia_recomendada}"
        )
        color_estado = "#1eb851"
        estado_historial = "Calculado (sin verificar tubería específica)"

        tuberia = combo_tuberia.get()
        if tuberia != "":
            area_tubo = TABLA_TUBERIA[tuberia]
            factor_real = (area_total / area_tubo) * 100
            if factor_real <= limite:
                estado = "CUMPLE"
                color_estado = "#1eb851"
            else:
                estado = "NO CUMPLE"
                color_estado = "#b11921"
            estado_historial = estado
            texto_resultado += (
                f"\n\nVerificación de la tubería {tuberia}:\n"
                f"Área interna (Tabla 4.5): {area_tubo} mm²\n"
                f"Factor de relleno real: {factor_real:.2f} %\n"
                f"Estado: {estado}"
            )

        resultado_label.config(text=texto_resultado, fg=color_estado)
        guardar_historial("Factor de Relleno", texto_resultado, estado_historial)

    def limpiar():
        for entry_cant, combo_cal, entry_area in filas:
            entry_cant.delete(0, tk.END)
            entry_area.delete(0, tk.END)
        resultado_label.config(text="")

    botones_frame = tk.Frame(ventana)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Calcular", command=calcular,
              bg="#1eb851", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Limpiar", command=limpiar,
              bg="#b11921", fg="white", width=12).grid(row=0, column=1, padx=5)

    ventana.bind("<Return>", lambda evento: calcular())


def abrir_conversion_unidades():
    ventana = tk.Toplevel(raiz)
    ventana.title("Conversion de Unidades")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Conversion de Unidades", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="(Aqui va el contenido de esta seccion)").pack()


def abrir_historial():
    ventana = tk.Toplevel(raiz)
    ventana.title("Historial de Cálculos")
    ventana.geometry("750x550")
    ventana.bind("<Escape>", lambda evento: ventana.destroy())
    ventana.focus_force()

    tk.Label(ventana, text="Historial de Cálculos", font=("Arial", 14, "bold")).pack(pady=10)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    columnas = ("id", "fecha", "tipo", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
    tabla.heading("id", text="ID")
    tabla.heading("fecha", text="Fecha y hora")
    tabla.heading("tipo", text="Tipo de cálculo")
    tabla.heading("estado", text="Estado")
    tabla.column("id", width=40, anchor="center")
    tabla.column("fecha", width=160, anchor="center")
    tabla.column("tipo", width=180, anchor="center")
    tabla.column("estado", width=120, anchor="center")
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tk.Label(ventana, text="Detalle del registro seleccionado:",
             font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

    detalle_texto = tk.Text(ventana, height=8, wrap="word", font=("Consolas", 9))
    detalle_texto.pack(fill="x", padx=10, pady=5)

    registros = {}  # id -> resumen completo, para mostrar el detalle sin volver a consultar la BD

    def cargar_datos():
        for fila in tabla.get_children():
            tabla.delete(fila)
        registros.clear()

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, fecha, tipo, resumen, estado FROM historial ORDER BY id DESC")
        filas = cursor.fetchall()
        conexion.close()

        for id_registro, fecha, tipo, resumen, estado in filas:
            tabla.insert("", "end", values=(id_registro, fecha, tipo, estado))
            registros[id_registro] = resumen

        detalle_texto.delete("1.0", tk.END)

    def mostrar_detalle(evento):
        seleccion = tabla.selection()
        if not seleccion:
            return
        id_registro = tabla.item(seleccion[0])["values"][0]
        detalle_texto.delete("1.0", tk.END)
        detalle_texto.insert("1.0", registros.get(id_registro, ""))

    tabla.bind("<<TreeviewSelect>>", mostrar_detalle)

    def borrar_historial():
        confirmar = messagebox.askyesno(
            "Confirmar borrado",
            "¿Seguro que quieres borrar TODO el historial? Esta acción no se puede deshacer."
        )
        if not confirmar:
            return
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM historial")
        conexion.commit()
        conexion.close()
        cargar_datos()

    botones_frame = tk.Frame(ventana)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Actualizar", command=cargar_datos,
              bg="#1f40c3", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Borrar Historial", command=borrar_historial,
              bg="#b11921", fg="white", width=14).grid(row=0, column=1, padx=5)

    cargar_datos()


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

boton5 = tk.Button(raiz, text="5. Ver Historial", width=30, height=2, command=abrir_historial, bg="#6c3483", fg="white")
boton5.pack(pady=10)

raiz.mainloop()