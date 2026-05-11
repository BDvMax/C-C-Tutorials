import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import random
import os
import json
import pandas as pd

# Importar nuestras librerías modulares
from interno.ordenacion_interna import (burbuja, insercion, seleccion, 
                                        shell_sort, quick_sort, heap_sort, radix_sort)
from externo.ordenacion_externa import (intercalacion_pasos, mezcla_directa_pasos, 
                                        mezcla_equilibrada_pasos)

# --- TEMAS CONFIGURABLES ---
TEMAS = {
    "Cyberpunk": {"bg": "#120136", "bg2": "#035AA6", "bg3": "#40BAD5", "accent": "#FCBF49", "text": "#FFFFFF", "bar": "#035AA6", "bar_active": "#FCBF49", "bar_done": "#40BAD5"},
    "Nórdico": {"bg": "#2E3440", "bg2": "#3B4252", "bg3": "#434C5E", "accent": "#88C0D0", "text": "#ECEFF4", "bar": "#5E81AC", "bar_active": "#EBCB8B", "bar_done": "#A3BE8C"},
    "Hacker": {"bg": "#0D0D0D", "bg2": "#1A1A1A", "bg3": "#262626", "accent": "#00FF41", "text": "#00FF41", "bar": "#008F11", "bar_active": "#FFFFFF", "bar_done": "#00FF41"},
    "Solarizado": {"bg": "#FDF6E3", "bg2": "#EEE8D5", "bg3": "#93A1A1", "accent": "#268BD2", "text": "#657B83", "bar": "#2AA198", "bar_active": "#CB4B16", "bar_done": "#859900"}
}

FONT_TIT = ("Segoe UI", 16, "bold")
FONT_BTN = ("Segoe UI", 10, "bold")
FONT_SM = ("Segoe UI", 9)

class OrdenamientoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Ordenamiento Dinámico v3.1 - Equipo Integrado")
        self.root.geometry("1200x850")
        
        self.tema_actual = "Cyberpunk"
        self.c = TEMAS[self.tema_actual]
        self.animando = False
        self.datos_actuales = []
        self.metodo_actual = "burbuja"
        self.tipo_metodo = "interno" 
        
        self.widgets_tema = [] 
        self._build_ui()
        self._aplicar_tema(self.tema_actual)
        self._generar_aleatorios()

    def _reg_w(self, widget, t_bg="bg", t_fg="text"):
        self.widgets_tema.append((widget, t_bg, t_fg))
        return widget

    def _build_ui(self):
        # --- HEADER ---
        self.hdr = self._reg_w(tk.Frame(self.root, pady=10))
        self.hdr.pack(fill="x")
        self.lbl_main = self._reg_w(tk.Label(self.hdr, text="⬡ ORDENAMIENTO ULTRA ⬡", font=FONT_TIT), "bg", "accent")
        self.lbl_main.pack()

        body = self._reg_w(tk.Frame(self.root))
        body.pack(fill="both", expand=True, padx=15, pady=10)

        # --- SIDEBAR IZQUIERDA ---
        side = self._reg_w(tk.Frame(body, width=320), "bg2")
        side.pack(side="left", fill="y", padx=(0, 10))
        side.pack_propagate(False)

        # CONFIGURACIÓN
        self._reg_w(tk.Label(side, text="⚙️ CONFIGURACIÓN", font=FONT_SM)).pack(pady=(10,5))
        frame_configs = self._reg_w(tk.Frame(side), "bg2")
        frame_configs.pack(fill="x", padx=10)
        
        self._reg_w(tk.Label(frame_configs, text="Tema:", font=FONT_SM)).grid(row=0, column=0, sticky="w")
        self.combo_tema = ttk.Combobox(frame_configs, values=list(TEMAS.keys()), state="readonly", width=14)
        self.combo_tema.set(self.tema_actual)
        self.combo_tema.bind("<<ComboboxSelected>>", lambda e: self._aplicar_tema(self.combo_tema.get()))
        self.combo_tema.grid(row=0, column=1, pady=2)

        self._reg_w(tk.Label(frame_configs, text="Vías (K):", font=FONT_SM)).grid(row=1, column=0, sticky="w")
        self.spin_k = tk.Spinbox(frame_configs, from_=2, to=10, width=5)
        self.spin_k.delete(0, "end"); self.spin_k.insert(0, "3")
        self.spin_k.grid(row=1, column=1, sticky="w", pady=2)

        self._reg_w(tk.Label(frame_configs, text="Extraer:", font=FONT_SM)).grid(row=2, column=0, sticky="w")
        self.combo_tipo_dato = ttk.Combobox(frame_configs, values=["Automático", "Solo Números", "Solo Texto"], state="readonly", width=14)
        self.combo_tipo_dato.set("Automático")
        self.combo_tipo_dato.grid(row=2, column=1, pady=2)

        # MÉTODOS
        self.btn_metodos = {}
        
        # Internos
        self._reg_w(tk.Label(side, text="MÉTODOS INTERNOS", font=FONT_SM)).pack(pady=(15,5))
        frame_int = self._reg_w(tk.Frame(side), "bg2")
        frame_int.pack(fill="x", padx=10)
        
        metodos_internos = [
            ("Burbuja", "burbuja"), ("Inserción", "insercion"), ("Selección", "seleccion"), 
            ("Shell", "shell"), ("Quick", "quick"), ("Heap", "heap"), ("Radix", "radix")
        ]
        
        for i, (label, key) in enumerate(metodos_internos):
            btn = tk.Button(frame_int, text=label, font=FONT_SM, bd=0, cursor="hand2", command=lambda k=key, t="interno": self._sel_metodo(k, t))
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=2, pady=2)
            frame_int.grid_columnconfigure(i%2, weight=1)
            self.widgets_tema.append((btn, "bg3", "text"))
            self.btn_metodos[key] = btn

        # Externos
        self._reg_w(tk.Label(side, text="MÉTODOS EXTERNOS", font=FONT_SM)).pack(pady=(10,5))
        metodos_externos = [
            ("Intercalación", "intercalacion"), ("Mezcla Directa", "directa"), ("Mezcla Equilibrada", "equilibrada")
        ]
        for label, key in metodos_externos:
            btn = tk.Button(side, text=label, font=FONT_SM, bd=0, cursor="hand2", command=lambda k=key, t="externo": self._sel_metodo(k, t))
            btn.pack(fill="x", padx=10, pady=2)
            self.widgets_tema.append((btn, "bg3", "text"))
            self.btn_metodos[key] = btn

        # CONTROLES INFERIORES Y ARCHIVOS
        self._reg_w(tk.Label(side, text="DATOS Y ARCHIVOS", font=FONT_SM)).pack(pady=(10,5))
        
        btn_rand = tk.Button(side, text="🎲 Generar Aleatorios", font=FONT_SM, bd=0, cursor="hand2", command=self._generar_aleatorios)
        btn_rand.pack(fill="x", padx=10, pady=2)
        self.widgets_tema.append((btn_rand, "bg3", "text"))

        btn_load = tk.Button(side, text="📂 Cargar Archivo", font=FONT_SM, bd=0, cursor="hand2", command=self._cargar_archivo)
        btn_load.pack(fill="x", padx=10, pady=2)
        self.widgets_tema.append((btn_load, "bg3", "text"))

        btn_save = tk.Button(side, text="💾 Guardar Resultados", font=FONT_SM, bd=0, cursor="hand2", command=self._guardar_archivo)
        btn_save.pack(fill="x", padx=10, pady=2)
        self.widgets_tema.append((btn_save, "bg3", "text"))

        self.vel_slider = tk.Scale(side, from_=0.01, to=1.0, resolution=0.05, orient="horizontal", bd=0, highlightthickness=0)
        self.vel_slider.set(0.1)
        self.vel_slider.pack(fill="x", padx=10, pady=(10,5))
        self.widgets_tema.append((self.vel_slider, "bg2", "text"))

        self.btn_run = tk.Button(side, text="▶️ INICIAR ORDENAMIENTO", font=FONT_BTN, bd=0, pady=10, cursor="hand2", command=self._ejecutar)
        self.btn_run.pack(fill="x", padx=10, pady=(10, 15))
        self.widgets_tema.append((self.btn_run, "accent", "bg")) 

        # --- AREA PRINCIPAL ---
        main = self._reg_w(tk.Frame(body))
        main.pack(side="left", fill="both", expand=True)
        
        self.lbl_titulo = self._reg_w(tk.Label(main, text="Esperando datos...", font=("Consolas", 12, "bold"), anchor="w"), "bg", "accent")
        self.lbl_titulo.pack(fill="x")

        self.canvas = tk.Canvas(main, height=350, highlightthickness=0)
        self.canvas.pack(fill="x", pady=5)

        self.log = tk.Text(main, font=("Consolas", 10), bd=0, padx=10, pady=10)
        self.log.pack(fill="both", expand=True)
        self.widgets_tema.append((self.log, "bg2", "text"))

    def _aplicar_tema(self, nombre_tema):
        self.tema_actual = nombre_tema
        self.c = TEMAS[nombre_tema]
        self.root.configure(bg=self.c["bg"])
        self.canvas.configure(bg=self.c["bg2"])
        
        for widget, t_bg, t_fg in self.widgets_tema:
            try:
                widget.configure(bg=self.c[t_bg], fg=self.c[t_fg])
                if isinstance(widget, tk.Scale): widget.configure(troughcolor=self.c["bg3"])
            except: pass
        self._sel_metodo(self.metodo_actual, self.tipo_metodo) 
        self._dibujar(self.datos_actuales)

    def _sel_metodo(self, metodo, tipo):
        self.metodo_actual = metodo
        self.tipo_metodo = tipo
        for k, b in self.btn_metodos.items():
            b.configure(bg=self.c["accent"] if k == metodo else self.c["bg3"], 
                        fg=self.c["bg"] if k == metodo else self.c["text"])
        
        tipo_dato = type(self.datos_actuales[0]).__name__ if self.datos_actuales else "Desconocido"
        self.lbl_titulo.config(text=f"MODO: {self.metodo_actual.upper()} ({tipo.upper()}) | Datos: {tipo_dato} | Elementos: {len(self.datos_actuales)}")

    def _generar_aleatorios(self):
        preferencia = self.combo_tipo_dato.get()
        opcion = "numeros" if preferencia == "Solo Números" else ("texto" if preferencia == "Solo Texto" else random.choice(["numeros", "texto"]))

        if opcion == "numeros":
            self.datos_actuales = [random.randint(1, 100) for _ in range(20)]
        else:
            palabras = ["Python", "Java", "C++", "Ruby", "Rust", "Go", "Perl", "Lua", "Swift", "PHP", "Dart", "Kotlin", "Scala", "R"]
            self.datos_actuales = [random.choice(palabras) for _ in range(15)]
        
        self._log_msg(f"Datos aleatorios generados ({opcion}).")
        self._sel_metodo(self.metodo_actual, self.tipo_metodo)
        self._dibujar(self.datos_actuales)

    # LÓGICA DE ARCHIVOS REINCORPORADA
    def _procesar_y_filtrar_datos(self, raw_data):
        numeros, textos = [], []
        for item in raw_data:
            if pd.isna(item) or item == "": continue
            try: 
                numeros.append(float(item) if '.' in str(item) else int(item))
            except ValueError: 
                textos.append(str(item).strip())
        
        preferencia = self.combo_tipo_dato.get()

        if preferencia == "Solo Números":
            if not numeros: raise ValueError("Seleccionaste 'Solo Números', pero no se encontró ninguno en el archivo.")
            self._log_msg(f"Filtro: Extrayendo solo los {len(numeros)} números.")
            return numeros
        elif preferencia == "Solo Texto":
            if not textos: raise ValueError("Seleccionaste 'Solo Texto', pero no se encontraron palabras.")
            self._log_msg(f"Filtro: Extrayendo solo las {len(textos)} palabras.")
            return textos
        else:
            if len(numeros) >= len(textos) and numeros:
                self._log_msg(f"Detección Auto: NÚMEROS ({len(numeros)}).")
                return numeros
            elif textos:
                self._log_msg(f"Detección Auto: TEXTO ({len(textos)}).")
                return textos
            return []

    def _cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Soportados", "*.txt *.xlsx *.xls *.json")])
        if not ruta: return
        try:
            raw = []
            ext = os.path.splitext(ruta)[1].lower()
            if ext in ['.xlsx', '.xls']:
                df = pd.read_excel(ruta, header=None)
                raw = df.values.flatten().tolist()
            elif ext == '.json':
                with open(ruta, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    raw = data if isinstance(data, list) else list(data.values())
            elif ext == '.txt':
                with open(ruta, 'r', encoding='utf-8') as f:
                    for line in f: raw.extend(line.replace(',', ' ').split())

            datos_limpios = self._procesar_y_filtrar_datos(raw)
            if not datos_limpios: raise ValueError("El archivo está vacío o sin datos válidos.")
            
            self.datos_actuales = datos_limpios
            self._sel_metodo(self.metodo_actual, self.tipo_metodo)
            self._dibujar(self.datos_actuales)
            messagebox.showinfo("Éxito", f"Datos cargados desde {os.path.basename(ruta)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar archivo:\n{e}")
            self._log_msg(f"❌ Error al cargar archivo: {e}")

    def _guardar_archivo(self):
        if not self.datos_actuales:
            messagebox.showwarning("Atención", "No hay datos para guardar.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt"), ("Excel", "*.xlsx"), ("JSON", "*.json")])
        if not ruta: return
        
        try:
            ext = os.path.splitext(ruta)[1].lower()
            if ext == '.json':
                with open(ruta, 'w', encoding='utf-8') as f: json.dump(self.datos_actuales, f)
            elif ext == '.xlsx':
                pd.DataFrame(self.datos_actuales).to_excel(ruta, index=False, header=False)
            else:
                with open(ruta, 'w', encoding='utf-8') as f: f.write(", ".join(map(str, self.datos_actuales)))
            self._log_msg(f"Archivo guardado en: {ruta}")
            messagebox.showinfo("Guardado", "Resultados exportados con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{e}")

    def _dibujar(self, valores, activos=[], listos=[]):
        self.canvas.delete("all")
        if not valores: return
        W, H = int(self.canvas.winfo_width() or 800), int(self.canvas.winfo_height() or 350)
        n = len(valores)
        ancho = min((W - 40) / n, 80) 
        valores_unicos = sorted(list(set(valores)))
        
        for i, v in enumerate(valores):
            rank = valores_unicos.index(v) + 1
            h = (rank / len(valores_unicos)) * (H - 60) if valores_unicos else 100
            x1, y1 = 20 + i * ancho, H - 30 - h
            x2, y2 = x1 + ancho - 2, H - 30
            
            color = self.c["bar_done"] if i in listos else (self.c["bar_active"] if i in activos else self.c["bar"])
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            
            text_disp = str(v)
            if len(text_disp) > 8: text_disp = text_disp[:6]+".."
            self.canvas.create_text(x1 + ancho/2, y1 - 15, text=text_disp, fill=self.c["text"], font=("Consolas", 8), angle=0 if type(v) != str else 45)

    def _log_msg(self, msg):
        self.log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log.see(tk.END)

    def _ejecutar(self):
        if self.animando or not self.datos_actuales: return
        self.animando = True
        delay = self.vel_slider.get()
        m = self.metodo_actual
        self.log.delete("1.0", tk.END)
        
        try:
            # Ejecución de MÉTODOS INTERNOS
            if self.tipo_metodo == "interno":
                dic_internos = {
                    "burbuja": burbuja, "insercion": insercion, "seleccion": seleccion,
                    "shell": shell_sort, "quick": quick_sort, "heap": heap_sort, "radix": radix_sort
                }
                
                if m == "radix" and type(self.datos_actuales[0]) == str:
                    self._log_msg("❌ Radix Sort no soporta strings directamente en esta implementación.")
                else:
                    self._log_msg(f"Iniciando {m.capitalize()} Sort...")
                    res, pasos = dic_internos[m](self.datos_actuales)
                    for p in pasos:
                        self._dibujar(p)
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

            # Ejecución de MÉTODOS EXTERNOS
            elif self.tipo_metodo == "externo":
                if m == "intercalacion":
                    mitad = len(self.datos_actuales) // 2
                    a, b = self.datos_actuales[:mitad], self.datos_actuales[mitad:]
                    self._log_msg(f"Intercalando 2 sublistas (tamaños {len(a)} y {len(b)})...")
                    res, pasos = intercalacion_pasos(a, b)
                    for p in pasos:
                        self._dibujar(a + b, activos=[p[2], len(a)+p[3]])
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res
                
                elif m == "directa":
                    self._log_msg("Iniciando Mezcla Directa...")
                    res, pasos = mezcla_directa_pasos(self.datos_actuales)
                    for p in pasos:
                        self._dibujar(p)
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

                elif m == "equilibrada":
                    k_val = int(self.spin_k.get())
                    self._log_msg(f"Iniciando Mezcla Equilibrada (K={k_val})...")
                    res, pasos = mezcla_equilibrada_pasos(self.datos_actuales, k=k_val)
                    for p in pasos:
                        self._dibujar(p[1])
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

            self._dibujar(self.datos_actuales, listos=list(range(len(self.datos_actuales))))
            self._log_msg("✅ ¡Ordenamiento finalizado!")
            
        except Exception as e:
            self._log_msg(f"❌ Error durante ejecución: {e}")
        finally:
            self.animando = False

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoApp(root)
    root.mainloop()