import tkinter as tk
from tkinter import messagebox


def abrir_calculadora_electrica():
    ventana = tk.Toplevel(raiz)
    ventana.title("Calculadora Electrica")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Calculadora Electrica", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="(Aqui va el contenido de esta seccion)").pack()


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
raiz.title("Analizador de Instalaciones Electricas")
raiz.geometry("400x400")

titulo = tk.Label(raiz, text="Analizador de Instalaciones Eléctricas", font=("Arial", 14, "bold"))
titulo.pack(pady=20)

boton1 = tk.Button(raiz, text="1. Calculadora Eléctrica", width=30, height=2, command=abrir_calculadora_electrica, bg="#3498db", fg="white")
boton1.pack(pady=10)

boton2 = tk.Button(raiz, text="2. Caida de Tensión", width=30, height=2, command=abrir_caida_tension)
boton2.pack(pady=10)

boton3 = tk.Button(raiz, text="3. Calcular Factor de Relleno", width=30, height=2, command=abrir_factor_relleno)
boton3.pack(pady=10)

boton4 = tk.Button(raiz, text="4. Conversión de Unidades electricas ", width=30, height=2, command=abrir_conversion_unidades)
boton4.pack(pady=10)

raiz.mainloop()
