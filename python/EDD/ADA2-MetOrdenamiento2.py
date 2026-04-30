"""
Métodos de Ordenamiento en Python — Interfaz Gráfica
=====================================================
Implementación de: ShellSort, QuickSort, HeapSort y Radix Sort
con interfaz visual usando tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random


# ─────────────────────────────────────────────
#  ALGORITMOS DE ORDENAMIENTO
# ─────────────────────────────────────────────

def shell_sort(arr):
    arr = arr[:]
    n = len(arr)
    gap = n // 2
    pasos = []
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            pasos.append(arr[:])
        gap //= 2
    return arr, pasos


def quick_sort_steps(arr, pasos):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    result = quick_sort_steps(left, pasos) + mid + quick_sort_steps(right, pasos)
    pasos.append(result[:])
    return result

def quick_sort(arr):
    arr = arr[:]
    pasos = []
    result = quick_sort_steps(arr, pasos)
    return result, pasos


def heapify(arr, n, i, pasos):
    largest = i
    left  = 2 * i + 1
    right = 2 * i + 2
    if left  < n and arr[left]  > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        pasos.append(arr[:])
        heapify(arr, n, largest, pasos)

def heap_sort(arr):
    arr = arr[:]
    n = len(arr)
    pasos = []
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, pasos)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        pasos.append(arr[:])
        heapify(arr, i, 0, pasos)
    return arr, pasos


def counting_sort_by_digit(arr, exp, pasos):
    n = len(arr)
    output = [0] * n
    count  = [0] * 10
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    for i in range(n):
        arr[i] = output[i]
    pasos.append(arr[:])

def radix_sort(arr):
    arr = arr[:]
    pasos = []
    if not arr:
        return arr, pasos
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp, pasos)
        exp *= 10
    return arr, pasos


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────

COLORES = {
    "fondo":       "#0f0f1a",
    "panel":       "#1a1a2e",
    "acento":      "#7c3aed",
    "acento2":     "#a855f7",
    "texto":       "#e2e8f0",
    "texto_dim":   "#94a3b8",
    "barra":       "#7c3aed",
    "barra_ord":   "#10b981",
    "barra_hover": "#a855f7",
    "entrada":     "#0f172a",
    "borde":       "#2d2d4e",
    "error":       "#ef4444",
    "advertencia": "#f59e0b",
}

FUENTE_TITULO  = ("Courier New", 20, "bold")
FUENTE_SUBTIT  = ("Courier New", 11, "bold")
FUENTE_NORMAL  = ("Courier New", 10)
FUENTE_PEQUE   = ("Courier New", 9)
FUENTE_MONO    = ("Courier New", 10)


class VisualizadorOrdenamiento(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Algoritmos de Ordenamiento")
        self.configure(bg=COLORES["fondo"])
        self.resizable(True, True)
        self.minsize(900, 650)

        self.metodo_var  = tk.StringVar(value="Shell Sort")
        self.velocidad   = tk.IntVar(value=300)   # ms entre pasos
        self.animando    = False
        self.pasos_anim  = []
        self.paso_actual = 0
        self._job        = None

        self._construir_ui()
        self.center_window(1050, 700)

    def center_window(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── Construcción UI ──────────────────────────────────────────
    def _construir_ui(self):
        # Título
        tk.Label(self, text="◈  ORDENAMIENTO VISUAL  ◈",
                 font=FUENTE_TITULO, bg=COLORES["fondo"],
                 fg=COLORES["acento2"]).pack(pady=(18, 4))
        tk.Label(self, text="Shell · Quick · Heap · Radix",
                 font=FUENTE_PEQUE, bg=COLORES["fondo"],
                 fg=COLORES["texto_dim"]).pack(pady=(0, 12))

        contenedor = tk.Frame(self, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        # Panel izquierdo — controles
        panel_izq = tk.Frame(contenedor, bg=COLORES["panel"],
                             bd=0, relief="flat",
                             highlightbackground=COLORES["borde"],
                             highlightthickness=1)
        panel_izq.pack(side="left", fill="y", padx=(0, 12), pady=0, ipadx=14, ipady=10)
        self._panel_controles(panel_izq)

        # Panel derecho — canvas + log
        panel_der = tk.Frame(contenedor, bg=COLORES["fondo"])
        panel_der.pack(side="left", fill="both", expand=True)
        self._panel_visualizacion(panel_der)

    def _seccion(self, parent, texto):
        tk.Label(parent, text=texto, font=FUENTE_SUBTIT,
                 bg=COLORES["panel"], fg=COLORES["acento2"]).pack(anchor="w", pady=(14, 4))
        tk.Frame(parent, height=1, bg=COLORES["borde"]).pack(fill="x", pady=(0, 8))

    def _panel_controles(self, parent):
        tk.Label(parent, text="CONTROLES", font=FUENTE_SUBTIT,
                 bg=COLORES["panel"], fg=COLORES["acento"]).pack(anchor="w", pady=(4, 10))

        # Algoritmo
        self._seccion(parent, "① Algoritmo")
        metodos = ["Shell Sort", "Quick Sort", "Heap Sort", "Radix Sort"]
        for m in metodos:
            rb = tk.Radiobutton(parent, text=m, variable=self.metodo_var,
                                value=m, font=FUENTE_NORMAL,
                                bg=COLORES["panel"], fg=COLORES["texto"],
                                selectcolor=COLORES["acento"],
                                activebackground=COLORES["panel"],
                                activeforeground=COLORES["acento2"],
                                cursor="hand2")
            rb.pack(anchor="w", pady=2)

        # Números
        self._seccion(parent, "② Números")
        tk.Label(parent, text="Ingresa números (separados\npor comas o espacios):",
                 font=FUENTE_PEQUE, bg=COLORES["panel"],
                 fg=COLORES["texto_dim"], justify="left").pack(anchor="w")

        self.entrada_txt = tk.Text(parent, height=4, width=22,
                                   font=FUENTE_MONO,
                                   bg=COLORES["entrada"], fg=COLORES["texto"],
                                   insertbackground=COLORES["acento2"],
                                   relief="flat", bd=4,
                                   wrap="word")
        self.entrada_txt.pack(pady=6, fill="x")

        # Botones de datos
        fila_btn = tk.Frame(parent, bg=COLORES["panel"])
        fila_btn.pack(fill="x", pady=(0, 4))
        self._btn(fila_btn, "Aleatorio", self._generar_aleatorio, small=True).pack(side="left", padx=(0, 4))
        self._btn(fila_btn, "Limpiar",   self._limpiar_entrada,  small=True).pack(side="left")

        # Velocidad
        self._seccion(parent, "③ Velocidad")
        fila_vel = tk.Frame(parent, bg=COLORES["panel"])
        fila_vel.pack(fill="x")
        tk.Label(fila_vel, text="Rápido", font=FUENTE_PEQUE,
                 bg=COLORES["panel"], fg=COLORES["texto_dim"]).pack(side="left")
        tk.Scale(fila_vel, from_=50, to=900, orient="horizontal",
                 variable=self.velocidad, showvalue=False,
                 bg=COLORES["panel"], fg=COLORES["texto"],
                 troughcolor=COLORES["entrada"], highlightthickness=0,
                 sliderrelief="flat", bd=0).pack(side="left", fill="x", expand=True, padx=4)
        tk.Label(fila_vel, text="Lento", font=FUENTE_PEQUE,
                 bg=COLORES["panel"], fg=COLORES["texto_dim"]).pack(side="left")

        # Botones principales
        self._seccion(parent, "④ Acción")
        self._btn(parent, "▶  ORDENAR", self._iniciar_ordenamiento).pack(fill="x", pady=3)
        self._btn(parent, "⏹  DETENER", self._detener, secundario=True).pack(fill="x", pady=3)
        self._btn(parent, "↺  REINICIAR", self._reiniciar, secundario=True).pack(fill="x", pady=3)

        # Info paso
        self.lbl_paso = tk.Label(parent, text="",
                                  font=FUENTE_PEQUE,
                                  bg=COLORES["panel"], fg=COLORES["texto_dim"],
                                  wraplength=170, justify="left")
        self.lbl_paso.pack(anchor="w", pady=(12, 0))

    def _btn(self, parent, texto, comando, small=False, secundario=False):
        fg   = COLORES["texto"]
        bg   = COLORES["acento"] if not secundario else COLORES["entrada"]
        font = FUENTE_PEQUE if small else FUENTE_NORMAL
        b = tk.Button(parent, text=texto, command=comando,
                      font=font, bg=bg, fg=fg,
                      activebackground=COLORES["acento2"],
                      activeforeground="#fff",
                      relief="flat", cursor="hand2",
                      padx=8, pady=5 if not small else 3,
                      bd=0)
        b.bind("<Enter>", lambda e, w=b, c=COLORES["acento2"]: w.config(bg=c))
        b.bind("<Leave>", lambda e, w=b, c=bg: w.config(bg=c))
        return b

    def _panel_visualizacion(self, parent):
        # Canvas de barras
        self.canvas = tk.Canvas(parent, bg=COLORES["fondo"],
                                highlightthickness=1,
                                highlightbackground=COLORES["borde"])
        self.canvas.pack(fill="both", expand=True, pady=(0, 8))

        # Log de pasos
        log_frame = tk.Frame(parent, bg=COLORES["panel"],
                             highlightbackground=COLORES["borde"],
                             highlightthickness=1)
        log_frame.pack(fill="x")

        tk.Label(log_frame, text=" LOG DE PASOS", font=FUENTE_PEQUE,
                 bg=COLORES["panel"], fg=COLORES["acento"],
                 anchor="w").pack(fill="x", padx=6, pady=(4, 0))

        self.log_txt = tk.Text(log_frame, height=5, font=FUENTE_PEQUE,
                               bg=COLORES["entrada"], fg=COLORES["texto_dim"],
                               state="disabled", relief="flat", bd=0,
                               wrap="word")
        self.log_txt.pack(fill="x", padx=6, pady=4)

    # ── Dibujo ──────────────────────────────────────────────────
    def _dibujar(self, arr, destacar=None, ordenado=False):
        self.canvas.delete("all")
        if not arr:
            return

        c_w   = self.canvas.winfo_width()  or 600
        c_h   = self.canvas.winfo_height() or 400
        n     = len(arr)
        m_x   = 20
        m_y   = 30
        ancho_barra = max(6, (c_w - 2 * m_x) // n - 2)
        espacio     = (c_w - 2 * m_x) // n
        max_val     = max(arr) if max(arr) != 0 else 1

        for i, v in enumerate(arr):
            x1  = m_x + i * espacio
            h   = max(4, int((v / max_val) * (c_h - m_y - 30)))
            y1  = c_h - 30 - h
            x2  = x1 + ancho_barra
            y2  = c_h - 30

            color = COLORES["barra_ord"] if ordenado else (
                    COLORES["barra_hover"] if destacar and i in destacar else
                    COLORES["barra"])

            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=color, outline="", width=0)
            # valor encima si caben
            if ancho_barra >= 14:
                self.canvas.create_text(x1 + ancho_barra // 2, y1 - 8,
                                        text=str(v), font=FUENTE_PEQUE,
                                        fill=COLORES["texto_dim"])

        # línea base
        self.canvas.create_line(m_x, c_h - 30, c_w - m_x, c_h - 30,
                                fill=COLORES["borde"], width=1)

    # ── Acciones ────────────────────────────────────────────────
    def _generar_aleatorio(self):
        nums = random.sample(range(1, 100), min(18, 18))
        self.entrada_txt.delete("1.0", "end")
        self.entrada_txt.insert("end", " ".join(map(str, nums)))

    def _limpiar_entrada(self):
        self.entrada_txt.delete("1.0", "end")
        self.canvas.delete("all")
        self._log("Entrada limpiada.")

    def _leer_numeros(self):
        raw = self.entrada_txt.get("1.0", "end").strip()
        raw = raw.replace(",", " ")
        tokens = raw.split()
        if not tokens:
            raise ValueError("No ingresaste ningún número.")
        nums = []
        for t in tokens:
            try:
                nums.append(int(t))
            except ValueError:
                raise ValueError(f"'{t}' no es un número entero válido.")
        return nums

    def _iniciar_ordenamiento(self):
        if self.animando:
            return
        try:
            nums = self._leer_numeros()
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        metodo = self.metodo_var.get()

        if metodo == "Radix Sort" and any(n < 0 for n in nums):
            messagebox.showwarning("Aviso", "Radix Sort solo admite números no negativos.")
            return

        self._log(f"── {metodo} ──")
        self._log(f"Original: {nums}")

        t0 = time.time()
        if metodo == "Shell Sort":
            resultado, pasos = shell_sort(nums)
        elif metodo == "Quick Sort":
            resultado, pasos = quick_sort(nums)
        elif metodo == "Heap Sort":
            resultado, pasos = heap_sort(nums)
        else:
            resultado, pasos = radix_sort(nums)
        elapsed = time.time() - t0

        self._log(f"Ordenado: {resultado}")
        self._log(f"Pasos de animación: {len(pasos)} | Tiempo: {elapsed*1000:.2f} ms")

        # Mostrar estado inicial
        self._dibujar(nums)

        self.pasos_anim  = pasos
        self.paso_actual = 0
        self.animando    = True
        self._animar()

    def _animar(self):
        if not self.animando:
            return
        if self.paso_actual < len(self.pasos_anim):
            estado = self.pasos_anim[self.paso_actual]
            self._dibujar(estado)
            info = f"Paso {self.paso_actual + 1}/{len(self.pasos_anim)}"
            self.lbl_paso.config(text=info)
            self.paso_actual += 1
            delay = self.velocidad.get()
            self._job = self.after(delay, self._animar)
        else:
            # Mostrar resultado final en verde
            if self.pasos_anim:
                self._dibujar(self.pasos_anim[-1], ordenado=True)
            self.animando = False
            self.lbl_paso.config(text="✓ Completado")

    def _detener(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.animando = False
        self.lbl_paso.config(text="⏹ Detenido")

    def _reiniciar(self):
        self._detener()
        self.canvas.delete("all")
        self.lbl_paso.config(text="")
        self.pasos_anim  = []
        self.paso_actual = 0
        self._log("── Reiniciado ──")

    def _log(self, texto):
        self.log_txt.config(state="normal")
        self.log_txt.insert("end", texto + "\n")
        self.log_txt.see("end")
        self.log_txt.config(state="disabled")


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = VisualizadorOrdenamiento()
    app.mainloop()