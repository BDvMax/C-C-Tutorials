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
    "Cyberpunk": {"bg": "#120136", "bg2": "#035AA6", "bg3": "#40BAD5", "accent": "#FCBF49", "text": "#FFFFFF", "bar": "#035AA6", "bar_active": "#FCBF49", "bar_done": "#40BAD5", "borde": "#40BAD5"},
    "Nórdico": {"bg": "#2E3440", "bg2": "#3B4252", "bg3": "#434C5E", "accent": "#88C0D0", "text": "#ECEFF4", "bar": "#5E81AC", "bar_active": "#EBCB8B", "bar_done": "#A3BE8C", "borde": "#434C5E"},
    "Hacker": {"bg": "#0D0D0D", "bg2": "#1A1A1A", "bg3": "#262626", "accent": "#00FF41", "text": "#00FF41", "bar": "#008F11", "bar_active": "#FFFFFF", "bar_done": "#00FF41", "borde": "#262626"},
    "Solarizado": {"bg": "#FDF6E3", "bg2": "#EEE8D5", "bg3": "#93A1A1", "accent": "#268BD2", "text": "#657B83", "bar": "#2AA198", "bar_active": "#CB4B16", "bar_done": "#859900", "borde": "#93A1A1"}
}

FONT_TIT = ("Segoe UI", 16, "bold")
FONT_BTN = ("Segoe UI", 10, "bold")
FONT_SM = ("Segoe UI", 9)

class OrdenamientoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Ordenamiento Dinámico v3.3 - Equipo Integrado")
        self.root.geometry("1200x850")
        
        self.tema_actual = "Cyberpunk"
        self.c = TEMAS[self.tema_actual]
        self.animando = False
        self.datos_actuales = []
        self.metodo_actual = "burbuja"
        self.tipo_metodo = "interno" 
        self.resample_view = False # State for binned view prompt response

        
        self.widgets_tema = [] 
        self._build_ui()
        self._aplicar_tema(self.tema_actual)
        self.root.update_idletasks() # Ensure dimensions are known
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
        
        self.log.delete("1.0", tk.END)
        self._log_msg(f"✅ Datos aleatorios generados ({opcion}).")
        self._sel_metodo(self.metodo_actual, self.tipo_metodo)
        self._dibujar(self.datos_actuales)

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
            return numeros
        elif preferencia == "Solo Texto":
            if not textos: raise ValueError("Seleccionaste 'Solo Texto', pero no se encontraron palabras.")
            return textos
        else:
            if len(numeros) >= len(textos) and numeros: return numeros
            elif textos: return textos
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
            
            self.log.delete("1.0", tk.END)
            self._log_msg(f"📂 Archivo cargado exitosamente: {os.path.basename(ruta)}")
            self._log_msg(f"📊 Total de elementos detectados: {len(self.datos_actuales)}")
            
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
            self._log_msg(f"💾 ¡ÉXITO! Archivo guardado en: {ruta}")
            messagebox.showinfo("Guardado Exitoso", "Tus resultados han sido exportados correctamente.\n¡Buen trabajo!")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{e}")

    # LÓGICA DE DIBUJO CORREGIDA Y MEJORADA
    def _dibujar(self, valores, activos=[], listos=[]):
        self.canvas.delete("all")
        if not valores: return
        W, H = int(self.canvas.winfo_width() or 800), int(self.canvas.winfo_height() or 350)
        n_elem = len(valores)
        
        margin_x = 20
        margin_y_bottom = 30
        margin_y_top = 30
        
        # Estado: si esta es una visualizacion macroscópica (binning)
        is_macroscopic_view = self.resample_view and n_elem > 100
        
        if is_macroscopic_view:
             # Lógica de Visualización Macroscópica (Binning)
             num_bins = 20 # Dibuja un número fijo de barras para la vista macroscópica
             bin_size = n_elem // num_bins
             if bin_size == 0: bin_size = 1 # para casos de borde donde num_bins > n_elem
             
             valores_to_draw = []
             for i in range(num_bins):
                 start = i * bin_size
                 # para el último contenedor, tomar los elementos restantes
                 end = (i + 1) * bin_size if i < num_bins - 1 else n_elem
                 bin_items = valores[start:end]
                 # para el valor, usar el máximo para una buena visualización del rango
                 valores_to_draw.append(max(bin_items) if bin_items else 0)
             
             draw_n = num_bins
             draw_valores = valores_to_draw
             
             # Calculos de ancho y separación para vista macroscópica
             ancho_contenedor = (W - 2 * margin_x) // draw_n
             spacing = max(2, ancho_contenedor // 10) # 10% de separación, mín 2 pixeles
             ancho = ancho_contenedor - spacing
             
        else:
            # Lógica de Ítem Individual
            draw_valores = valores
            draw_n = n_elem
            
            # Ancho mínimo para que las columnas sean visibles
            min_bar_width = 10 
            
            if draw_n > 0:
                ancho_contenedor = (W - 2 * margin_x) // draw_n
                spacing = max(2, ancho_contenedor // 10) # 10% de separación, mín 2 pixeles
                
                # Asegurar un ancho mínimo y ajustar spacing si es necesario
                ancho = max(min_bar_width, ancho_contenedor - spacing)
            else:
                ancho = 0 

        
        if draw_n > 0: # Asegurar cálculos válidos
            valores_unicos = sorted(list(set(draw_valores))) # Valores únicos para escalar
            for i, v in enumerate(draw_valores):
                 # Escalar altura. Rank-based scaling prevents huge variations. Add a small base.
                 rank = valores_unicos.index(v) + 1
                 h_scaled = (rank / len(valores_unicos)) * (H - margin_y_bottom - margin_y_top) if valores_unicos else 5
                 
                 x1, y1 = margin_x + i * (ancho + spacing), H - margin_y_bottom - h_scaled
                 x2, y2 = x1 + ancho, H - margin_y_bottom
                 
                 # visual cues for binned view
                 border_color = "" # No border for individual
                 if is_macroscopic_view:
                      border_color = self.c["borde"] # Add border color for binned bars
                 
                 color = self.c["bar_done"] if (not is_macroscopic_view and i in listos) else (self.c["bar_active"] if (not is_macroscopic_view and i in activos) else self.c["bar"])
                 
                 # Draw rectangle.
                 self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=border_color, width=1)
                 
                 # Solo dibuja el texto si las barras son lo suficientemente anchas y no estamos en macroscópica
                 # Increased threshold. Use is_macroscopic_view to check.
                 if ancho > 25 and not is_macroscopic_view:
                     text_disp = str(v)
                     if len(text_disp) > 8: text_disp = text_disp[:6]+".."
                     # Ángulo corregido a 0 para texto horizontal
                     self.canvas.create_text(x1 + ancho/2, y1 - 15, text=text_disp, fill=self.c["text"], font=("Consolas", 8), angle=0)

        # Draw a baseline line.
        self.canvas.create_line(margin_x, H - margin_y_bottom, W - margin_x, H - margin_y_bottom, fill=self.c["borde"], width=1)

    def _log_msg(self, msg):
        self.log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log.see(tk.END)

    def _anunciar_exito(self, tiempo_real):
        # Mensaje de finalización en el log
        self._log_msg("\n" + "="*50)
        self._log_msg(f"🎉 ¡ORDENAMIENTO COMPLETADO EXITOSAMENTE! 🎉")
        self._log_msg(f"⏱️ Tiempo total transcurrido: {tiempo_real:.2f} segundos.")
        self._log_msg("💡 SUGERENCIA: Ahora puedes ir al menú izquierdo y dar clic en")
        self._log_msg("   '💾 Guardar Resultados' para descargar tu arreglo ordenado.")
        self._log_msg("="*50 + "\n")
        
        # Ventana emergente amigable
        messagebox.showinfo(
            "¡Proceso Terminado!", 
            f"El arreglo de {len(self.datos_actuales)} elementos ha sido ordenado correctamente.\n\n"
            f"Tiempo total: {tiempo_real:.2f} s.\n\n"
            "¡No olvides guardar tus resultados usando el botón 'Guardar Resultados'!"
        )

    def _ejecutar_modo_turbo(self):
        """Ejecuta el ordenamiento de Python nativo sin gráficos para evitar crasheos de RAM"""
        self._log_msg("\n🚀 Iniciando MODO TURBO (Ordenamiento en background)...")
        t_inicio = time.time()
        
        # Ordenamiento nativo
        self.datos_actuales.sort()
        
        t_fin = time.time()
        tiempo_total = t_fin - t_inicio
        
        self.resample_view = False # Asegurar que no dibujamos en binned al final
        self._dibujar(self.datos_actuales, listos=list(range(len(self.datos_actuales))))
        self.animando = False
        self._anunciar_exito(tiempo_total)

    # LÓGICA DE EJECUCIÓN MEJORADA CON MENSAJES
    def _ejecutar(self):
        if self.animando or not self.datos_actuales: return
        
        n_elem = len(self.datos_actuales)
        m = self.metodo_actual
        delay = self.vel_slider.get()
        
        self.log.delete("1.0", tk.END)
        self._log_msg("╔════════════════════════════════════╗")
        self._log_msg(f"║ 📊 OVERVIEW DE LA OPERACIÓN")
        self._log_msg(f"║ Algoritmo: {m.upper()}")
        self._log_msg(f"║ Elementos a ordenar: {n_elem}")
        self._log_msg("╚════════════════════════════════════╝\n")

        # PROTECCIÓN DE MEMORIA Y ARREGLO DE DIBUJO PARA GRANDES DATOS
        if n_elem > 150:
             # Nueva lógica de respuesta de prompt para Modo Turbo o Visualización Macroscópica
             prompt_msg = f"Has cargado {n_elem} elementos.\n\nIntentar crear y visualizar gráficamente cada paso individual para miles de datos congelará la interfaz y agotará la memoria RAM.\n\nElige una opción:"
             
             # Ventana de diálogo personalizada de 3 opciones (Turbo, Macroscópica, Individual-Insegura)
             def custom_prompt():
                 d = tk.Toplevel(self.root)
                 d.title("Opción de Ejecución")
                 d.geometry("400x250")
                 tk.Label(d, text=prompt_msg, wraplength=380, pady=10).pack()
                 
                 choice = tk.StringVar()
                 
                 def set_choice(c):
                     choice.set(c)
                     d.destroy()
                     
                 # Botones de opción
                 btn_turbo = tk.Button(d, text="Modo Turbo (Saltar gráficos)", command=lambda: set_choice("turbo"), width=30)
                 btn_turbo.config(bg=self.c["bar_active"], fg=self.c["bg"])
                 btn_turbo.pack(pady=5)
                 
                 btn_macro = tk.Button(d, text="Visualización Macroscópica (Segura)", command=lambda: set_choice("macro"), width=30)
                 btn_macro.config(bg=self.c["bar"], fg=self.c["bg"])
                 btn_macro.pack(pady=5)
                 
                 btn_force = tk.Button(d, text="Visualización Individual (Insegura)", command=lambda: set_choice("force"), width=30)
                 btn_force.config(bg=self.c["borde"], fg=self.c["text"])
                 btn_force.pack(pady=5)
                 
                 d.transient(self.root)
                 d.grab_set()
                 self.root.wait_window(d)
                 return choice.get()

             user_choice = custom_prompt()

             if user_choice == "turbo":
                 self._ejecutar_modo_turbo()
                 return
             elif user_choice == "macro":
                 self.resample_view = True
                 self._log_msg("👁️ Activando Visualización Macroscópica para la animación (seguro).")
             else: # force
                 self.resample_view = False
                 self._log_msg("⚠️ PRECAUCIÓN: Has forzado la animación individual. La app podría congelarse...")
        else:
             # Por defecto para pocos datos es individual
             self.resample_view = False


        self.animando = True
        t_start_proceso = time.time()
        
        try:
            # EJECUCIÓN MÉTODOS INTERNOS
            if self.tipo_metodo == "interno":
                dic_internos = {
                    "burbuja": burbuja, "insercion": insercion, "seleccion": seleccion,
                    "shell": shell_sort, "quick": quick_sort, "heap": heap_sort, "radix": radix_sort
                }
                
                if m == "radix" and type(self.datos_actuales[0]) == str:
                    self._log_msg("❌ Radix Sort no soporta texto en esta implementación.")
                    self.animando = False
                    return
                else:
                    self._log_msg(f"🧠 Calculando pasos en memoria...")
                    res, pasos = dic_internos[m](self.datos_actuales)
                    
                    # Cálculo de ETA (Estimated Time of Arrival)
                    eta_segundos = len(pasos) * delay
                    self._log_msg(f"📈 Pasos lógicos generados: {len(pasos)}")
                    self._log_msg(f"⏳ Tiempo estimado de animación (ETA): {eta_segundos:.2f} segundos.")
                    self._log_msg(f"▶️ Reproduciendo animación...\n")
                    
                    for p in pasos:
                        self._dibujar(p)
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

            # EJECUCIÓN MÉTODOS EXTERNOS
            elif self.tipo_metodo == "externo":
                self._log_msg(f"🧠 Inicializando lógica de arreglos externos...")
                if m == "intercalacion":
                    mitad = len(self.datos_actuales) // 2
                    a, b = self.datos_actuales[:mitad], self.datos_actuales[mitad:]
                    res, pasos = intercalacion_pasos(a, b)
                    eta_segundos = len(pasos) * delay
                    self._log_msg(f"⏳ ETA de Animación: {eta_segundos:.2f} segundos.")
                    for p in pasos:
                        self._dibujar(a + b, activos=[p[2], len(a)+p[3]])
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res
                
                elif m == "directa":
                    res, pasos = mezcla_directa_pasos(self.datos_actuales)
                    eta_segundos = len(pasos) * delay
                    self._log_msg(f"⏳ ETA de Animación: {eta_segundos:.2f} segundos.")
                    for p in pasos:
                        self._dibujar(p)
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

                elif m == "equilibrada":
                    k_val = int(self.spin_k.get())
                    res, pasos = mezcla_equilibrada_pasos(self.datos_actuales, k=k_val)
                    eta_segundos = len(pasos) * delay
                    self._log_msg(f"⏳ ETA de Animación: {eta_segundos:.2f} segundos.")
                    for p in pasos:
                        self._dibujar(p[1])
                        self.root.update(); time.sleep(delay)
                    self.datos_actuales = res

            # PINTADO FINAL Y ANUNCIO
            # Asegurar visualización final individual y completa (verde)
            self.resample_view = False 
            self._dibujar(self.datos_actuales, listos=list(range(len(self.datos_actuales))))
            
            tiempo_total = time.time() - t_start_proceso
            self._anunciar_exito(tiempo_total)
            
        except Exception as e:
            self._log_msg(f"❌ Error crítico durante la ejecución: {e}")
        finally:
            self.animando = False

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoApp(root)
    root.mainloop()