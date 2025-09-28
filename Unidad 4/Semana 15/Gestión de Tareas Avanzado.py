
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

FONDO = "imagen tareas.webp"  # imagen de fondo

class ListaTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GESTOR DE TAREAS")

        # Tamaño inicial de la ventana
        self.ANCHO_INICIAL = 650
        self.ALTO_INICIAL = 450
        self.centrar_ventana(self.ANCHO_INICIAL, self.ALTO_INICIAL)

        # Imagen de fondo con Label
        self._configurar_fondo()

        # Frame principal
        self.marco_contenido = tk.Frame(self.root, bg="#fff1e3", highlightthickness=0)
        self.marco_contenido.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        # Configuración de la interfaz
        self._configurar_interfaz()

        # Bindings
        self.entry.bind("<Return>", self.agregar_tarea)
        self.tree.bind("<Button-3>", self.mostrar_menu)  # clic derecho
        self.tree.bind("<Button-1>", self.click_opciones)  # clic en opciones
        self.tree.bind("<Double-1>", self.doble_clic_tarea)

        # Menú contextual
        self.menu = tk.Menu(root, tearoff=0)

    #Centra la ventana en la pantallla
    def centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _configurar_fondo(self):
        if os.path.exists(FONDO):
            try:
                self.bg_image_original = Image.open(FONDO)
                imagen_inicial = self.bg_image_original.resize(
                    (self.ANCHO_INICIAL, self.ALTO_INICIAL),
                    Image.Resampling.LANCZOS
                )
                self.bg_photo = ImageTk.PhotoImage(imagen_inicial)

                self.label_bg = tk.Label(self.root, image=self.bg_photo)
                self.label_bg.place(x=0, y=0, relwidth=1, relheight=1)

                self.root.bind("<Configure>", self._al_redimensionar)

            except Exception as e:
                messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen de fondo: {e}")
                self.root.configure(bg="#87CEEB")
        else:
            print("Fondo no encontrado. Usando color sólido.")
            self.root.configure(bg="#f0f0f0")

    def _al_redimensionar(self, event):
        if hasattr(self, "bg_image_original"):
            try:
                imagen_redimensionada = self.bg_image_original.resize(
                    (event.width, event.height),
                    Image.Resampling.LANCZOS
                )
                self.bg_photo = ImageTk.PhotoImage(imagen_redimensionada)
                self.label_bg.config(image=self.bg_photo)
            except Exception as e:
                print(f"Error redimensionando fondo: {e}")

    def _configurar_interfaz(self):
        style = ttk.Style()
        style.configure("Color.TLabelframe", background="#fff1e3")
        style.configure("Color.TLabelframe.Label", background="#fff1e3")

        # ----- Frame entradas -------
        frame_inputs = ttk.LabelFrame(self.marco_contenido, text="Nueva Tarea", padding=(15, 10), style="Color.TLabelframe")
        frame_inputs.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.entry = tk.Entry(frame_inputs, font=("Comic Sans MS", 10))
        self.entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")

        #Botón de selección - Prioridad
        self.combo_prioridad = ttk.Combobox(
            frame_inputs,
            values=["Alta", "Media", "Baja"],
            state="readonly",
            width=12,
            font=("Comic Sans MS", 10)
        )
        self.combo_prioridad.current(1)
        self.combo_prioridad.grid(row=0, column=1, padx=(0, 12), pady=5)

        self.btn_add = tk.Button(
            frame_inputs,
            text="Añadir Tarea",
            command=self.agregar_tarea,
            font=("Comic Sans MS", 10),
            bg="#F7DCD5",
            width=15
        )
        self.btn_add.grid(row=0, column=2, padx=5, pady=5)

        frame_inputs.columnconfigure(0, weight=1)
        self.marco_contenido.columnconfigure(0, weight=1)

        # ------- Treeview --------
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"))
        style.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25)

        self.tree = ttk.Treeview(
            self.marco_contenido,
            columns=("Tarea", "Prioridad", "Terminada", "Opciones"),
            show="headings",
            height=15
        )
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.heading("Terminada", text="Terminada")
        self.tree.heading("Opciones", text="")

        self.tree.column("Tarea", width=320, anchor="w")
        self.tree.column("Prioridad", width=120, anchor="center")
        self.tree.column("Terminada", width=100, anchor="center")
        self.tree.column("Opciones", width=50, anchor="center")

        self.tree.grid(row=1, column=0, padx=15, pady=(0, 5), sticky="nsew")
        self.marco_contenido.rowconfigure(1, weight=1)

        # ---------- Botones debajo del Treeview ----------
        frame_botones = tk.Frame(self.marco_contenido, bg="#fff1e3")
        frame_botones.grid(row=2, column=0, pady=10)

        self.btn_complete = tk.Button(
            frame_botones,
            text="Marcar como terminada",
            command=self._accion_marcar,
            font=("Comic Sans MS", 10),
            bg="#F7DCD5",
            width=18
        )
        self.btn_complete.pack(side=tk.LEFT, padx=10)

        self.btn_delete = tk.Button(
            frame_botones,
            text="Eliminar Tarea",
            command=self._accion_eliminar,
            font=("Comic Sans MS", 10),
            bg="#F7DCD5",
            width=18
        )
        self.btn_delete.pack(side=tk.LEFT, padx=10)

    # --- Lógica de tareas ---
    def agregar_tarea(self, event=None):
        tarea = self.entry.get().strip()
        prioridad = self.combo_prioridad.get()
        if tarea:
            self.tree.insert("", tk.END, values=(tarea, prioridad, "NO", "⋮"))
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")

    def mostrar_menu(self, event, item=None):
        if not item:
            item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            valores = list(self.tree.item(item, "values"))
            self.menu.delete(0, tk.END)

            if valores[2] == "NO":
                self.menu.add_command(label="Marcar como terminada", font=("Comic Sans MS", 9),
                                      command=lambda: self.marcar_completada(item))
            else:
                self.menu.add_command(label="Quitar terminada", font=("Comic Sans MS", 9),
                                      command=lambda: self.quitar_completada(item))

            self.menu.add_separator()
            self.menu.add_command(label="Eliminar", font=("Comic Sans MS", 9),
                                  command=lambda: self.eliminar_tarea(item))
            self.menu.tk_popup(event.x_root, event.y_root)

    def doble_clic_tarea(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            valores = list(self.tree.item(item, "values"))
            if valores[2] == "NO":
                self.marcar_completada(item)
            else:
                self.quitar_completada(item)

    def click_opciones(self, event):
        col = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        if col == "#4" and item:
            self.mostrar_menu(event, item)

    def _accion_marcar(self):
        item = self._get_selected()
        if item:
            valores = list(self.tree.item(item, "values"))
            if valores[2] == "NO":
                self.marcar_completada(item)
            else:
                self.quitar_completada(item)

    def _accion_eliminar(self):
        item = self._get_selected()
        if item:
            self.eliminar_tarea(item)

    def _get_selected(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debes seleccionar una tarea primero.")
            return None
        return seleccion[0]

    def marcar_completada(self, item):
        valores = list(self.tree.item(item, "values"))
        valores[2] = "SÍ"
        self.tree.item(item, values=valores, tags=("terminada",))
        self.tree.tag_configure("terminada", foreground="gray", font=("Comic Sans MS", 10))

    def quitar_completada(self, item):
        valores = list(self.tree.item(item, "values"))
        valores[2] = "NO"
        self.tree.item(item, values=valores, tags=("normal",))
        self.tree.tag_configure("normal", foreground="black", font=("Comic Sans MS", 10))

    def eliminar_tarea(self, item):
        self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()
