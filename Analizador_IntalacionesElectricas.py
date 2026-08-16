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
raiz.geometry("600x600")
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
