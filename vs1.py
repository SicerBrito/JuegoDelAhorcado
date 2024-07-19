import tkinter as tk
import random

class AhorcadoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego del Ahorcado")
        self.master.geometry("400x300")

        self.palabras = ["python", "programacion", "computadora", "algoritmo", "desarrollo"]
        self.palabra_secreta = ""
        self.letras_adivinadas = []
        self.intentos_restantes = 6

        self.label_palabra = tk.Label(master, text="", font=("Arial", 24))
        self.label_palabra.pack(pady=20)

        self.label_intentos = tk.Label(master, text="Intentos restantes: 6", font=("Arial", 14))
        self.label_intentos.pack()

        self.entry_letra = tk.Entry(master, font=("Arial", 14), width=5)
        self.entry_letra.pack(pady=10)

        self.boton_adivinar = tk.Button(master, text="Adivinar", command=self.adivinar_letra)
        self.boton_adivinar.pack()

        self.mensaje = tk.Label(master, text="", font=("Arial", 14))
        self.mensaje.pack(pady=20)

        self.iniciar_juego()

    def iniciar_juego(self):
        self.palabra_secreta = random.choice(self.palabras)
        self.letras_adivinadas = []
        self.intentos_restantes = 6
        self.actualizar_palabra_mostrada()
        self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
        self.mensaje.config(text="")

    def actualizar_palabra_mostrada(self):
        palabra_mostrada = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                palabra_mostrada += letra
            else:
                palabra_mostrada += "_"
        self.label_palabra.config(text=palabra_mostrada)

    def adivinar_letra(self):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        if len(letra) != 1:
            self.mensaje.config(text="Por favor, ingresa una sola letra.")
            return

        if letra in self.letras_adivinadas:
            self.mensaje.config(text="Ya has adivinado esa letra.")
            return

        self.letras_adivinadas.append(letra)

        if letra in self.palabra_secreta:
            self.mensaje.config(text="¡Bien hecho!")
        else:
            self.intentos_restantes -= 1
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
            self.mensaje.config(text="Letra incorrecta.")

        self.actualizar_palabra_mostrada()

        if "_" not in self.label_palabra.cget("text"):
            self.mensaje.config(text="¡Felicidades! ¡Has ganado!")
            self.boton_adivinar.config(state=tk.DISABLED)
        elif self.intentos_restantes == 0:
            self.mensaje.config(text=f"¡Game Over! La palabra era: {self.palabra_secreta}")
            self.boton_adivinar.config(state=tk.DISABLED)

root = tk.Tk()
juego = AhorcadoGUI(root)
root.mainloop()