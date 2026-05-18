import tkinter as tk
from tkinter import ttk, messagebox
import random
from busqueda.tablahash import TablaHash

class AppInventarioDidactico:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Didáctico de Tabla Hash - Inventario")
        self.root.geometry("1000x700")
        self.root.config(padx=10, pady=10)

        # Usamos una capacidad pequeña (11) para forzar colisiones y poder verlas en la GUI
        self.capacidad_tabla = 11
        self.inventario = TablaHash(capacidad=self.capacidad_tabla)

        self.crear_interfaz()
        self.actualizar_vista_tabla()

    def crear_interfaz(self):
        # --- PANEL IZQUIERDO: Controles ---
        frame_controles = tk.LabelFrame(self.root, text="Panel de Control", padx=10, pady=10)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        tk.Label(frame_controles, text="SKU (Ej: SKU01):").pack(anchor=tk.W)
        self.entry_sku = tk.Entry(frame_controles, width=25)
        self.entry_sku.pack(pady=(0, 10))

        tk.Label(frame_controles, text="Nombre:").pack(anchor=tk.W)
        self.entry_nombre = tk.Entry(frame_controles, width=25)
        self.entry_nombre.pack(pady=(0, 10))

        tk.Button(frame_controles, text="1. Insertar / Actualizar", command=self.insertar_producto, bg="#d9ead3").pack(fill=tk.X, pady=5)
        tk.Button(frame_controles, text="2. Buscar de forma Didáctica", command=self.buscar_producto, bg="#c9daf8", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=5)
        tk.Button(frame_controles, text="3. Generar 5 Aleatorios", command=self.generar_masivos, bg="#fce5cd").pack(fill=tk.X, pady=25)

        # --- PANEL DERECHO: Visualización de la Tabla ---
        frame_tabla = tk.LabelFrame(self.root, text="Estado de la Memoria (Tabla Hash)", padx=10, pady=10)
        frame_tabla.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Usamos un Text widget para dibujar la tabla
        self.texto_tabla = tk.Text(frame_tabla, height=20, width=50, state=tk.DISABLED, font=("Courier", 11), bg="#2b2b2b", fg="#a9b7c6")
        self.texto_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_tabla, command=self.texto_tabla.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_tabla.config(yscrollcommand=scrollbar.set)

        # --- PANEL INFERIOR: Consola Didáctica ---
        frame_consola = tk.LabelFrame(self.root, text="Consola Didáctica (Paso a paso de la búsqueda)", padx=10, pady=10)
        frame_consola.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=(10, 0))

        self.texto_consola = tk.Text(frame_consola, height=10, state=tk.DISABLED, font=("Arial", 11), bg="#f4f4f4")
        self.texto_consola.pack(fill=tk.BOTH, expand=True)

    def log_consola(self, mensaje, color="black", limpiar=False):
        """Escribe mensajes en la consola didáctica de abajo."""
        self.texto_consola.config(state=tk.NORMAL)
        if limpiar:
            self.texto_consola.delete(1.0, tk.END)
        
        # Configurar colores
        self.texto_consola.tag_config(color, foreground=color)
        self.texto_consola.insert(tk.END, mensaje + "\n", color)
        
        self.texto_consola.see(tk.END)
        self.texto_consola.config(state=tk.DISABLED)

    def actualizar_vista_tabla(self, indice_resaltado=None):
        """Dibuja la tabla hash actual en el panel derecho."""
        self.texto_tabla.config(state=tk.NORMAL)
        self.texto_tabla.delete(1.0, tk.END)
        self.texto_tabla.tag_config("resaltado", background="#4a6b46", foreground="white")

        for i in range(self.capacidad_tabla):
            linea_texto = f"Índice [{i:02d}]: "
            actual = self.inventario.tabla[i]
            
            if not actual:
                linea_texto += "Vacío"
            else:
                nodos = []
                while actual:
                    nodos.append(f"[{actual.clave}]")
                    actual = actual.siguiente
                linea_texto += " -> ".join(nodos)
            
            # Insertar línea por línea para poder resaltar el índice buscado
            if indice_resaltado == i:
                self.texto_tabla.insert(tk.END, linea_texto + "\n", "resaltado")
            else:
                self.texto_tabla.insert(tk.END, linea_texto + "\n")

        self.texto_tabla.config(state=tk.DISABLED)

    def insertar_producto(self):
        sku = self.entry_sku.get().upper().strip()
        nombre = self.entry_nombre.get().strip()
        
        if not sku or not nombre:
            messagebox.showwarning("Advertencia", "Llena SKU y Nombre.")
            return
            
        precio = round(random.uniform(10, 100), 2) # Precio autogenerado
        stock = random.randint(1, 50)              # Stock autogenerado

        self.inventario.insertar(sku, {"nombre": nombre, "precio": precio, "stock": stock})
        self.actualizar_vista_tabla()
        
        self.entry_sku.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.log_consola(f"✅ Se insertó {sku} ({nombre}) en la tabla.", "blue", limpiar=True)

    def generar_masivos(self):
        for _ in range(5):
            sku = f"SKU{random.randint(10, 99)}"
            nombre = f"Producto_{random.randint(100, 999)}"
            self.inventario.insertar(sku, {"nombre": nombre, "precio": 0, "stock": 0})
        
        self.actualizar_vista_tabla()
        self.log_consola("🎲 Se generaron e insertaron 5 productos aleatorios.", "blue", limpiar=True)

    def buscar_producto(self):
        """Esta es la función estrella: Simula paso a paso la búsqueda para que el usuario aprenda."""
        sku = self.entry_sku.get().upper().strip()
        if not sku:
            messagebox.showwarning("Advertencia", "Ingresa un SKU para buscar.")
            return

        self.log_consola(f"--- INICIANDO BÚSQUEDA DE '{sku}' ---", "black", limpiar=True)

        # PASO 1: Calcular la función Hash
        indice = self.inventario._funcion_hash_modulo(sku)
        self.log_consola(f"PASO 1: Aplicando función Hash a '{sku}'...", "black")
        self.log_consola(f"        Sumando valores ASCII y calculando módulo {self.capacidad_tabla}.", "black")
        self.log_consola(f"        Resultado matemático -> El elemento debe estar en el Índice [{indice}].", "blue")

        # PASO 2: Resaltar en la GUI el salto directo en memoria O(1)
        self.actualizar_vista_tabla(indice_resaltado=indice)
        self.log_consola(f"\nPASO 2: Saltando directamente a la posición [{indice}] de la memoria... (¡Tiempo O(1)!)", "black")

        # PASO 3: Recorrer la lista enlazada (Manejo de colisiones)
        actual = self.inventario.tabla[indice]
        pasos = 1

        if actual is None:
             self.log_consola(f"PASO 3: El Índice [{indice}] está vacío. \n❌ CONCLUSIÓN: El producto '{sku}' NO existe en el sistema.", "red")
             return

        self.log_consola(f"PASO 3: Hay elementos en el Índice [{indice}]. Iniciando recorrido de la lista enlazada:", "black")
        
        while actual:
            self.log_consola(f"   -> Verificando Nodo {pasos}: ¿'{actual.clave}' es igual a '{sku}'?", "black")
            
            if actual.clave == sku:
                self.log_consola(f"      ¡SÍ COINCIDEN! 🎉", "green")
                self.log_consola(f"\n✅ RESULTADO FINAL: Producto encontrado -> Nombre: {actual.valor['nombre']}", "green")
                return
            else:
                self.log_consola(f"      No coinciden. (Esto es una colisión superada). Pasando al siguiente nodo...", "orange")
            
            actual = actual.siguiente
            pasos += 1

        self.log_consola(f"\n❌ CONCLUSIÓN: Llegamos al final de la lista en el Índice [{indice}]. El producto '{sku}' NO existe.", "red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInventarioDidactico(root)
    root.mainloop()