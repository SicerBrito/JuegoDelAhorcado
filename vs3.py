import tkinter as tk
from tkinter import messagebox
import random

class AhorcadoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego del Ahorcado")
        self.master.geometry("600x450")
        self.master.resizable(False, False)
        
        self.palabras_por_categoria = {
            "Animales": ["elefante", "jirafa", "cocodrilo", "pinguino", "murcielago"],
            "Países": ["españa", "argentina", "australia", "egipto", "tailandia"],
            "Profesiones": ["medico", "ingeniero", "profesor", "abogado", "astronauta"],
            "Frutas": ["manzana", "platano", "fresa", "kiwi", "melocoton"],
            "Deportes": ["futbol", "tenis", "natacion", "baloncesto", "atletismo"]
        }
        self.categoria_actual = ""
        self.palabra_secreta = ""
        self.letras_adivinadas = set()
        self.intentos_restantes = 6
        self.letras_incorrectas = set()

        self.ahorcado_ascii = [
            """
               +---+
               |   |
                   |
                   |
                   |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
                   |
                   |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
               |   |
                   |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
              /|   |
                   |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
              /|\  |
                   |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
              /|\  |
              /    |
                   |
            =========""",
            """
               +---+
               |   |
               O   |
              /|\  |
              / \  |
                   |
            ========="""
        ]

        self.frame_izquierdo = tk.Frame(master)
        self.frame_izquierdo.pack(side=tk.LEFT, padx=20)

        self.frame_derecho = tk.Frame(master)
        self.frame_derecho.pack(side=tk.RIGHT, padx=20)

        self.label_ahorcado = tk.Label(self.frame_izquierdo, text=self.ahorcado_ascii[0], font=("Courier", 14))
        self.label_ahorcado.pack()

        self.label_categoria = tk.Label(self.frame_derecho, text="Categoría: ", font=("Arial", 14))
        self.label_categoria.pack(pady=5)

        self.label_palabra = tk.Label(self.frame_derecho, text="", font=("Arial", 24))
        self.label_palabra.pack(pady=10)

        self.label_intentos = tk.Label(self.frame_derecho, text="Intentos restantes: 6", font=("Arial", 14))
        self.label_intentos.pack()

        self.label_letras_incorrectas = tk.Label(self.frame_derecho, text="Letras incorrectas:", font=("Arial", 12))
        self.label_letras_incorrectas.pack(pady=5)

        self.entry_letra = tk.Entry(self.frame_derecho, font=("Arial", 14), width=5)
        self.entry_letra.pack(pady=5)
        self.entry_letra.bind('<Return>', lambda event: self.adivinar_letra())

        self.boton_adivinar = tk.Button(self.frame_derecho, text="Adivinar", command=self.adivinar_letra)
        self.boton_adivinar.pack()

        self.boton_nueva_partida = tk.Button(self.frame_derecho, text="Nueva Partida", command=self.mostrar_categorias)
        self.boton_nueva_partida.pack(pady=10)

        self.mostrar_categorias()

    def mostrar_categorias(self):
        # Limpiar frame derecho
        for widget in self.frame_derecho.winfo_children():
            widget.destroy()

        label_seleccion = tk.Label(self.frame_derecho, text="Selecciona una categoría:", font=("Arial", 16))
        label_seleccion.pack(pady=10)

        for categoria in self.palabras_por_categoria.keys():
            btn = tk.Button(self.frame_derecho, text=categoria, 
                            command=lambda c=categoria: self.iniciar_juego(c))
            btn.pack(pady=5)

    def iniciar_juego(self, categoria):
        self.categoria_actual = categoria
        self.palabra_secreta = random.choice(self.palabras_por_categoria[categoria])
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = 6

        # Reconstruir la interfaz del juego
        for widget in self.frame_derecho.winfo_children():
            widget.destroy()

        self.label_categoria = tk.Label(self.frame_derecho, text=f"Categoría: {categoria}", font=("Arial", 14))
        self.label_categoria.pack(pady=5)

        self.label_palabra = tk.Label(self.frame_derecho, text="", font=("Arial", 24))
        self.label_palabra.pack(pady=10)

        self.label_intentos = tk.Label(self.frame_derecho, text="Intentos restantes: 6", font=("Arial", 14))
        self.label_intentos.pack()

        self.label_letras_incorrectas = tk.Label(self.frame_derecho, text="Letras incorrectas:", font=("Arial", 12))
        self.label_letras_incorrectas.pack(pady=5)

        self.entry_letra = tk.Entry(self.frame_derecho, font=("Arial", 14), width=5)
        self.entry_letra.pack(pady=5)
        self.entry_letra.bind('<Return>', lambda event: self.adivinar_letra())

        self.boton_adivinar = tk.Button(self.frame_derecho, text="Adivinar", command=self.adivinar_letra)
        self.boton_adivinar.pack()

        self.boton_nueva_partida = tk.Button(self.frame_derecho, text="Nueva Partida", command=self.mostrar_categorias)
        self.boton_nueva_partida.pack(pady=10)

        self.actualizar_palabra_mostrada()
        self.label_ahorcado.config(text=self.ahorcado_ascii[0])

    def actualizar_palabra_mostrada(self):
        palabra_mostrada = " ".join(letra if letra in self.letras_adivinadas else "_" for letra in self.palabra_secreta)
        self.label_palabra.config(text=palabra_mostrada)

    def adivinar_letra(self):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        if not letra.isalpha() or len(letra) != 1:
            messagebox.showwarning("Entrada inválida", "Por favor, ingresa una sola letra.")
            return

        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            messagebox.showinfo("Letra repetida", "Ya has intentado con esa letra.")
            return

        if letra in self.palabra_secreta:
            self.letras_adivinadas.add(letra)
            self.actualizar_palabra_mostrada()
            if set(self.palabra_secreta) == self.letras_adivinadas:
                self.terminar_juego(True)
        else:
            self.intentos_restantes -= 1
            self.letras_incorrectas.add(letra)
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
            self.label_letras_incorrectas.config(text=f"Letras incorrectas: {', '.join(sorted(self.letras_incorrectas))}")
            self.label_ahorcado.config(text=self.ahorcado_ascii[6 - self.intentos_restantes])
            if self.intentos_restantes == 0:
                self.terminar_juego(False)

    def terminar_juego(self, ganado):
        self.boton_adivinar.config(state=tk.DISABLED)
        self.entry_letra.config(state=tk.DISABLED)
        if ganado:
            messagebox.showinfo("¡Felicidades!", f"¡Has ganado! La palabra era: {self.palabra_secreta}")
        else:
            messagebox.showinfo("Game Over", f"¡Has perdido! La palabra era: {self.palabra_secreta}")

if __name__ == "__main__":
    root = tk.Tk()
    juego = AhorcadoGUI(root)
    root.mainloop()