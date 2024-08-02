import tkinter as tk
from tkinter import messagebox, simpledialog, font
import random
import json
import os

class AhorcadoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego del Ahorcado Mejorado")
        self.master.geometry("1000x700")
        self.master.resizable(False, False)
        
        self.cargar_palabras()
        self.cargar_estadisticas()
        
        self.categoria_actual = ""
        self.palabra_secreta = ""
        self.letras_adivinadas = set()
        self.intentos_restantes = 6
        self.letras_incorrectas = set()
        self.puntuacion = 0
        self.palabras_falladas = set()

        self.configurar_ui()
        self.mostrar_menu_principal()

    def configurar_ui(self):
        self.frame_principal = tk.Frame(self.master)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        self.frame_izquierdo = tk.Frame(self.frame_principal, width=500)
        self.frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.frame_derecho = tk.Frame(self.frame_principal, width=500)
        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label_ahorcado = tk.Label(self.frame_izquierdo, text="", font=("Courier", 14), justify=tk.LEFT)
        self.label_ahorcado.pack(pady=20)

        self.label_titulo = tk.Label(self.frame_derecho, text="Juego del Ahorcado", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

    def mostrar_menu_principal(self):
        self.limpiar_frame(self.frame_derecho)

        btn_nueva_partida = tk.Button(self.frame_derecho, text="Nueva Partida", command=self.mostrar_categorias, font=("Arial", 14))
        btn_nueva_partida.pack(pady=10)

        btn_practica = tk.Button(self.frame_derecho, text="Modo Práctica", command=self.iniciar_modo_practica, font=("Arial", 14))
        btn_practica.pack(pady=10)

        btn_estadisticas = tk.Button(self.frame_derecho, text="Ver Estadísticas", command=self.mostrar_estadisticas, font=("Arial", 14))
        btn_estadisticas.pack(pady=10)

        btn_agregar_palabra = tk.Button(self.frame_derecho, text="Agregar Palabra", command=self.agregar_palabra, font=("Arial", 14))
        btn_agregar_palabra.pack(pady=10)

        btn_salir = tk.Button(self.frame_derecho, text="Salir", command=self.master.quit, font=("Arial", 14))
        btn_salir.pack(pady=10)

    def limpiar_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def mostrar_categorias(self):
        self.limpiar_frame(self.frame_derecho)

        label_seleccion = tk.Label(self.frame_derecho, text="Selecciona una categoría:", font=("Arial", 16, "bold"))
        label_seleccion.pack(pady=10)

        for categoria in self.palabras_por_categoria.keys():
            btn = tk.Button(self.frame_derecho, text=categoria, 
                            command=lambda c=categoria: self.iniciar_juego(c),
                            font=("Arial", 12))
            btn.pack(pady=5)

        btn_volver = tk.Button(self.frame_derecho, text="Volver al Menú Principal", command=self.mostrar_menu_principal, font=("Arial", 12))
        btn_volver.pack(pady=20)

    def iniciar_juego(self, categoria):
        self.categoria_actual = categoria
        self.palabra_secreta = random.choice(self.palabras_por_categoria[categoria])
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = 6
        self.puntuacion = 0

        self.limpiar_frame(self.frame_derecho)

        self.label_categoria = tk.Label(self.frame_derecho, text=f"Categoría: {categoria}", font=("Arial", 14, "bold"))
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

        self.boton_adivinar = tk.Button(self.frame_derecho, text="Adivinar", command=self.adivinar_letra, font=("Arial", 12))
        self.boton_adivinar.pack()

        self.label_puntuacion = tk.Label(self.frame_derecho, text="Puntuación: 0", font=("Arial", 14))
        self.label_puntuacion.pack(pady=5)

        btn_volver = tk.Button(self.frame_derecho, text="Volver al Menú Principal", command=self.mostrar_menu_principal, font=("Arial", 12))
        btn_volver.pack(pady=20)

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
            self.puntuacion += 10
            self.actualizar_palabra_mostrada()
            if set(self.palabra_secreta) == self.letras_adivinadas:
                self.puntuacion += 50
                self.terminar_juego(True)
        else:
            self.intentos_restantes -= 1
            self.letras_incorrectas.add(letra)
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
            self.label_letras_incorrectas.config(text=f"Letras incorrectas: {', '.join(sorted(self.letras_incorrectas))}")
            self.label_ahorcado.config(text=self.ahorcado_ascii[6 - self.intentos_restantes])
            if self.intentos_restantes == 0:
                self.terminar_juego(False)

        self.label_puntuacion.config(text=f"Puntuación: {self.puntuacion}")

    def terminar_juego(self, ganado):
        self.boton_adivinar.config(state=tk.DISABLED)
        self.entry_letra.config(state=tk.DISABLED)
        
        self.estadisticas["partidas_jugadas"] += 1
        if ganado:
            self.estadisticas["partidas_ganadas"] += 1
            self.estadisticas["palabras_adivinadas"] += 1
            messagebox.showinfo("¡Felicidades!", f"¡Has ganado! La palabra era: {self.palabra_secreta}\nPuntuación final: {self.puntuacion}")
        else:
            self.palabras_falladas.add(self.palabra_secreta)
            messagebox.showinfo("Game Over", f"¡Has perdido! La palabra era: {self.palabra_secreta}\nPuntuación final: {self.puntuacion}")

        if self.puntuacion > self.estadisticas["mejor_puntuacion"]:
            self.estadisticas["mejor_puntuacion"] = self.puntuacion

        self.actualizar_categoria_favorita()
        self.guardar_estadisticas()

        btn_nueva_partida = tk.Button(self.frame_derecho, text="Nueva Partida", command=self.mostrar_categorias, font=("Arial", 12))
        btn_nueva_partida.pack(pady=10)

        btn_menu_principal = tk.Button(self.frame_derecho, text="Volver al Menú Principal", command=self.mostrar_menu_principal, font=("Arial", 12))
        btn_menu_principal.pack(pady=10)

    def actualizar_categoria_favorita(self):
        categorias = [self.categoria_actual]
        if self.estadisticas["categoria_favorita"]:
            categorias.append(self.estadisticas["categoria_favorita"])
        self.estadisticas["categoria_favorita"] = max(categorias, key=categorias.count)

    def mostrar_estadisticas(self):
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Estadísticas del Jugador")
        stats_window.geometry("400x300")

        for key, value in self.estadisticas.items():
            if key != "palabras_falladas":
                tk.Label(stats_window, text=f"{key.replace('_', ' ').title()}: {value}", font=("Arial", 12)).pack(pady=5)

        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy, font=("Arial", 12)).pack(pady=10)

    def iniciar_modo_practica(self):
        if not self.palabras_falladas:
            messagebox.showinfo("Modo Práctica", "No hay palabras para practicar. ¡Sigue jugando!")
            return

        self.palabra_secreta = random.choice(list(self.palabras_falladas))
        self.categoria_actual = "Práctica"
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = 6
        self.puntuacion = 0

        self.limpiar_frame(self.frame_derecho)

        self.label_categoria = tk.Label(self.frame_derecho, text="Categoría: Práctica", font=("Arial", 14, "bold"))
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

        self.boton_adivinar = tk.Button(self.frame_derecho, text="Adivinar", command=self.adivinar_letra, font=("Arial", 12))
        self.boton_adivinar.pack()

        self.label_puntuacion = tk.Label(self.frame_derecho, text="Puntuación: 0", font=("Arial", 14))
        self.label_puntuacion.pack(pady=5)

        btn_volver = tk.Button(self.frame_derecho, text="Volver al Menú Principal", command=self.mostrar_menu_principal, font=("Arial", 12))
        btn_volver.pack(pady=20)

        self.actualizar_palabra_mostrada()
        self.label_ahorcado.config(text=self.ahorcado_ascii[0])

    def agregar_palabra(self):
        categoria = simpledialog.askstring("Nueva Palabra", "Ingresa la categoría:")
        if categoria:
            palabra = simpledialog.askstring("Nueva Palabra", "Ingresa la nueva palabra:")
            if palabra:
                if categoria not in self.palabras_por_categoria:
                    self.palabras_por_categoria[categoria] = []
                self.palabras_por_categoria[categoria].append(palabra.lower())
                self.guardar_palabras()
                messagebox.showinfo("Palabra Agregada", f"La palabra '{palabra}' ha sido agregada a la categoría '{categoria}'.")

    def cargar_palabras(self):
        if os.path.exists('palabras.json'):
            with open('palabras.json', 'r', encoding='utf-8') as f:
                self.palabras_por_categoria = json.load(f)
        else:
            self.palabras_por_categoria = {
                "Animales": ["elefante", "jirafa", "cocodrilo", "pinguino", "murcielago"],
                "Países": ["españa", "argentina", "australia", "egipto", "tailandia"],
                "Profesiones": ["medico", "ingeniero", "profesor", "abogado", "astronauta"],
                "Frutas": ["manzana", "platano", "fresa", "kiwi", "melocoton"],
                "Deportes": ["futbol", "tenis", "natacion", "baloncesto", "atletismo"]
            }
            self.guardar_palabras()

    def guardar_palabras(self):
        with open('palabras.json', 'w', encoding='utf-8') as f:
            json.dump(self.palabras_por_categoria, f, ensure_ascii=False, indent=4)

    def cargar_estadisticas(self):
        if os.path.exists('estadisticas.json'):
            with open('estadisticas.json', 'r') as f:
                self.estadisticas = json.load(f)
        else:
            self.estadisticas = {
                "partidas_jugadas": 0,
                "partidas_ganadas": 0,
                "mejor_puntuacion": 0,
                "palabras_adivinadas": 0,
                "categoria_favorita": "",
                "palabras_falladas": []
            }

    def guardar_estadisticas(self):
        with open('estadisticas.json', 'w') as f:
            json.dump(self.estadisticas, f, indent=4)

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
        self.puntuacion = 0

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

        self.label_puntuacion = tk.Label(self.frame_derecho, text="Puntuación: 0", font=("Arial", 14))
        self.label_puntuacion.pack(pady=5)

        self.boton_nueva_partida = tk.Button(self.frame_derecho, text="Nueva Partida", command=self.mostrar_categorias)
        self.boton_nueva_partida.pack(pady=5)

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
            self.puntuacion += 10
            self.actualizar_palabra_mostrada()
            if set(self.palabra_secreta) == self.letras_adivinadas:
                self.puntuacion += 50
                self.terminar_juego(True)
        else:
            self.intentos_restantes -= 1
            self.letras_incorrectas.add(letra)
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")
            self.label_letras_incorrectas.config(text=f"Letras incorrectas: {', '.join(sorted(self.letras_incorrectas))}")
            self.label_ahorcado.config(text=self.ahorcado_ascii[6 - self.intentos_restantes])
            if self.intentos_restantes == 0:
                self.terminar_juego(False)

        self.label_puntuacion.config(text=f"Puntuación: {self.puntuacion}")

    def terminar_juego(self, ganado):
        self.boton_adivinar.config(state=tk.DISABLED)
        self.entry_letra.config(state=tk.DISABLED)
        
        self.estadisticas["partidas_jugadas"] += 1
        if ganado:
            self.estadisticas["partidas_ganadas"] += 1
            self.estadisticas["palabras_adivinadas"] += 1
            messagebox.showinfo("¡Felicidades!", f"¡Has ganado! La palabra era: {self.palabra_secreta}\nPuntuación final: {self.puntuacion}")
        else:
            self.palabras_falladas.add(self.palabra_secreta)
            messagebox.showinfo("Game Over", f"¡Has perdido! La palabra era: {self.palabra_secreta}\nPuntuación final: {self.puntuacion}")

        if self.puntuacion > self.estadisticas["mejor_puntuacion"]:
            self.estadisticas["mejor_puntuacion"] = self.puntuacion

        self.actualizar_categoria_favorita()
        self.guardar_estadisticas()

    def actualizar_categoria_favorita(self):
        categorias = [self.categoria_actual]
        if self.estadisticas["categoria_favorita"]:
            categorias.append(self.estadisticas["categoria_favorita"])
        self.estadisticas["categoria_favorita"] = max(categorias, key=categorias.count)

    def mostrar_estadisticas(self):
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Estadísticas del Jugador")
        stats_window.geometry("400x300")

        for key, value in self.estadisticas.items():
            if key != "palabras_falladas":
                tk.Label(stats_window, text=f"{key.replace('_', ' ').title()}: {value}", font=("Arial", 12)).pack(pady=5)

        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy).pack(pady=10)

    def iniciar_modo_practica(self):
        if not self.palabras_falladas:
            messagebox.showinfo("Modo Práctica", "No hay palabras para practicar. ¡Sigue jugando!")
            return

        self.palabra_secreta = random.choice(list(self.palabras_falladas))
        self.categoria_actual = "Práctica"
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = 6
        self.puntuacion = 0

        self.actualizar_palabra_mostrada()
        self.label_ahorcado.config(text=self.ahorcado_ascii[0])
        self.label_categoria.config(text="Categoría: Práctica")
        self.label_puntuacion.config(text="Puntuación: 0")
        self.label_intentos.config(text="Intentos restantes: 6")
        self.label_letras_incorrectas.config(text="Letras incorrectas:")

        self.boton_adivinar.config(state=tk.NORMAL)
        self.entry_letra.config(state=tk.NORMAL)

    def agregar_palabra(self):
        categoria = simpledialog.askstring("Nueva Palabra", "Ingresa la categoría:")
        if categoria:
            palabra = simpledialog.askstring("Nueva Palabra", "Ingresa la nueva palabra:")
            if palabra:
                if categoria not in self.palabras_por_categoria:
                    self.palabras_por_categoria[categoria] = []
                self.palabras_por_categoria[categoria].append(palabra.lower())
                self.guardar_palabras()
                messagebox.showinfo("Palabra Agregada", f"La palabra '{palabra}' ha sido agregada a la categoría '{categoria}'.")

    ahorcado_ascii = [
        # ... (incluye aquí tus representaciones ASCII del ahorcado)
    ]

if __name__ == "__main__":
    root = tk.Tk()
    juego = AhorcadoGUI(root)
    root.mainloop()