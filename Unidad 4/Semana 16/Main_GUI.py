import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from inventario import Inventario
from producto import Producto


class MainGUI:
    def __init__(self, master):
        self.master = master
        master.title("Programación Orientada a Objetos UEA")
        master.geometry("800x600")

        # 1. Instancia la clase Inventario (Carga los datos al inicio)
        self.inventario = Inventario()

        # Atajos de Teclado y Confirmación de Salida de la VENTANA PRINCIPAL
        master.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        master.bind('<Escape>', self.cerrar_aplicacion)

        # --- Estilo personalizado para el botón verde ---
        style = ttk.Style()
        style.configure('Green.TButton', background='#50C878', foreground='black', font=('Comic Sans MS', 10, 'bold'))

        # Almacenar referencia a la imagen
        self.fondo_img = None

        # --- Configuración de la Pantalla Principal (Bienvenida) ---
        self.frame_bienvenida = self.crear_frame_bienvenida(master)

        self.ventana_inventario = None
        self.tree = None

        # Menú Principal
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        opciones_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opciones", menu=opciones_menu)
        opciones_menu.add_command(label="Inventario de Productos", command=self.mostrar_gestion_productos)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.cerrar_aplicacion)

    def cerrar_aplicacion(self, event=None):
        """Cierra toda la aplicación."""
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea salir del sistema de Inventario?"):
            self.master.destroy()

    def cerrar_inventario(self):
        """Muestra un cuadro de diálogo para confirmar la salida de la VENTANA DE INVENTARIO y RESTAURA la Principal."""
        if messagebox.askyesno("Confirmar Cierre", "¿Está seguro de cerrar la ventana de Gestión de Inventario?"):
            if self.ventana_inventario:
                self.ventana_inventario.destroy()
                self.ventana_inventario = None
                # ACCIÓN CLAVE: MOSTRAR LA VENTANA PRINCIPAL DE NUEVO
                self.master.deiconify()

    def crear_frame_bienvenida(self, master):
        """Crea la pantalla de bienvenida con imagen de fondo y datos del estudiante."""
        frame = ttk.Frame(master)
        frame.pack(fill='both', expand=True)

        ancho_ventana = 800
        alto_ventana = 600
        master.update_idletasks()
        path_imagen = "fondo_uea.jpeg"
        try:
            img_pil = Image.open(path_imagen)
            img_pil = img_pil.resize((ancho_ventana, alto_ventana))
            self.fondo_img = ImageTk.PhotoImage(img_pil)
        except FileNotFoundError:
            print(f"ADVERTENCIA: Archivo '{path_imagen}' no encontrado.")
            self.fondo_img = None
        except Exception as e:
            print(f"ADVERTENCIA: Error al cargar la imagen con PIL: {e}")
            self.fondo_img = None

        canvas = tk.Canvas(frame, width=ancho_ventana, height=alto_ventana)
        canvas.pack(fill="both", expand=True)
        if self.fondo_img:
            canvas.create_image(ancho_ventana // 2, alto_ventana // 2, image=self.fondo_img, anchor="center")

        color_texto = 'black'
        canvas.create_text(ancho_ventana // 2, 150, text="UNIVERSIDAD ESTATAL AMAZÓNICA", font=('Arial', 24, 'bold'),
                           fill=color_texto)
        canvas.create_text(ancho_ventana // 2, 200, text="INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN",
                           font=('Arial', 18), fill=color_texto)
        canvas.create_text(ancho_ventana // 2, 240, text="Programación Orientada a Objetos", font=('Arial', 16, 'bold'),
                           fill=color_texto)
        y_pos_estudiante = alto_ventana - 250
        canvas.create_text(ancho_ventana // 2, y_pos_estudiante - 20, text="Tema: Sistema de Gestión de Inventario",
                           font=('Calibri', 14), fill=color_texto)
        canvas.create_text(ancho_ventana // 2, y_pos_estudiante + 30, text="Nombre: Sonia Jeanneth Vásquez Pánchez",
                           font=('Calibri', 14), fill=color_texto)
        canvas.create_text(ancho_ventana // 2, y_pos_estudiante + 80, text="Semestre: Segundo - A",
                           font=('Calibri', 14), fill=color_texto)
        return frame

    def mostrar_gestion_productos(self):
        """Crea y muestra la SEGUNDA VENTANA (Toplevel) y OCULTA la principal."""
        if self.ventana_inventario and self.ventana_inventario.winfo_exists():
            self.ventana_inventario.lift()
            return
        self.master.withdraw()

        # 1. Crear la nueva ventana
        self.ventana_inventario = tk.Toplevel(self.master)
        self.ventana_inventario.title("Gestión de Inventario de Productos")
        self.ventana_inventario.geometry("850x550")
        self.ventana_inventario.protocol("WM_DELETE_WINDOW", self.cerrar_inventario)

        main_frame = ttk.Frame(self.ventana_inventario)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        nb = ttk.Notebook(main_frame)
        nb.pack(fill='both', expand=True)
        tab_productos = ttk.Frame(nb)
        nb.add(tab_productos, text="Productos")

        # --- 2. Frame Superior (Búsqueda y Nuevo Producto) ---
        frame_top = ttk.Frame(tab_productos)
        frame_top.pack(fill='x', pady=10)

        # La búsqueda se mantiene arriba para mayor usabilidad
        ttk.Label(frame_top, text="Buscar:").pack(side='left', padx=(0, 5))
        self.entry_buscar = ttk.Entry(frame_top)
        self.entry_buscar.pack(side='left', fill='x', expand=True, padx=(0, 10))
        style = ttk.Style()
        style.configure("Custom.TButton",
                        font=("Comic Sans MS", 10),  # Cambia la fuente y tamaño
                        foreground="black",  # Cambia el color del texto
                        background="#F7DCD5")  # Cambia el color de fono)

        ttk.Button(frame_top, text="Buscar", style="Custom.TButton", command=self.filtrar_productos).pack(side='left', padx=5)
        ttk.Button(frame_top, text="+ Nuevo", command=lambda: self.abrir_ventana_producto(False),
                   style='Green.TButton').pack(side='right', padx=5)

        # --- 3. Treeview (Tabla de Productos) ---
        columnas = ("Código", "Nombre", "Cantidad", "Precio", "Opciones")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"))
        style.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25)
        self.tree = ttk.Treeview(tab_productos, columns=columnas, show='headings')

        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Opciones", text="Opciones")

        self.tree.column("Código", width=80, anchor="center")
        self.tree.column("Nombre", width=280, anchor="w")
        self.tree.column("Cantidad", width=80, anchor="center")
        self.tree.column("Precio", width=80, anchor="center")
        self.tree.column("Opciones", width=150, anchor="center")

        self.tree.pack(fill='both', expand=True, pady=5)
        #Eventos Delete y Doble clic
        self.tree.bind('<Delete>', self.eliminar_producto_seleccionado)
        self.tree.bind('<Double-1>', self.abrir_ventana_editar)
        self.tree.bind('<Button-1>', self.handle_opciones_click)

        # --- 4. Frame Inferior (Botones de Acción) ---
        frame_bottom = ttk.Frame(tab_productos)
        frame_bottom.pack(fill='x', pady=10)

        # Botón Mostrar Todos
        ttk.Button(frame_bottom, text=" Mostrar Productos",style="Custom.TButton",
                   command=self.cargar_datos_treeview).pack(side='left', padx=5)

        # Botón Salir
        ttk.Button(frame_bottom, text=" Salir",style="Custom.TButton",
                   command=self.cerrar_inventario).pack(side='right', padx=5)
        self.cargar_datos_treeview()

    # ------------------------------------------------------------------------
    # Los siguientes métodos operan sobre el Treeview de la ventana_inventario
    # ------------------------------------------------------------------------

    def handle_opciones_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if item and col == '#5':
            messagebox.showinfo("Acción",
                                "Clic en Opciones: Use DOBLE CLIC para EDITAR o la tecla DELETE para ELIMINAR.")

    def cargar_datos_treeview(self):
        if not self.tree:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for producto in self.inventario.get_todos_productos():
            self.tree.insert('', "end", values=(
                producto.get_codigo(),
                producto.get_nombre(),
                producto.get_cantidad(),
                f"{producto.get_precio():.2f}",
                "Editar / Eliminar"
            ))

    def filtrar_productos(self):
        if not self.entry_buscar:
            return
        query = self.entry_buscar.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not query:
            self.cargar_datos_treeview()
            return
        productos_filtrados = []
        productos = self.inventario.get_todos_productos()
        for producto in productos:
            nombre_lower = producto.get_nombre().lower()
            codigo_str = str(producto.get_codigo())

            if query in nombre_lower or query == codigo_str:
                productos_filtrados.append(producto)
        if not productos_filtrados:
            messagebox.showwarning("Búsqueda sin resultados",
                                  f"No se encontró ningún producto que coincida con: '{self.entry_buscar.get()}'")
        else:
            for producto in productos_filtrados:
                self.tree.insert('', "end", values=(
                    producto.get_codigo(),
                    producto.get_nombre(),
                    producto.get_cantidad(),
                    f"{producto.get_precio():.2f}",
                    "Modificar / Eliminar"
                ))
    # --- Lógica CRUD/Ventanas Modales ---
    def abrir_ventana_producto(self, es_edicion, producto_data=None):
        top = tk.Toplevel(self.master)
        top.title(" Productos " if not es_edicion else " Productos ")
        top.geometry("450x300")
        top.transient(self.ventana_inventario if self.ventana_inventario else self.master)
        top.grab_set()

        ttk.Label(top, text="Nuevo Producto" if not es_edicion else "Editar Producto", font=('Comic Sans MS', 12, 'bold')).pack(
            pady=10)
        frame_entradas = ttk.Frame(top)
        frame_entradas.pack(padx=20, pady=10)

        ttk.Label(frame_entradas, text="Código:").grid(row=0, column=0, sticky='w', pady=5)
        codigo_entry = ttk.Entry(frame_entradas)
        codigo_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_entradas, text="Nombre:").grid(row=1, column=0, sticky='w', pady=5)
        nombre_entry = ttk.Entry(frame_entradas)
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame_entradas, text="Cantidad:").grid(row=2, column=0, sticky='w', pady=5)
        cantidad_entry = ttk.Entry(frame_entradas)
        cantidad_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame_entradas, text="Precio:").grid(row=3, column=0, sticky='w', pady=5)
        precio_entry = ttk.Entry(frame_entradas)
        precio_entry.grid(row=3, column=1, padx=10, pady=5)

        if es_edicion and producto_data:
            codigo_entry.insert(0, producto_data[0])
            codigo_entry.config(state='readonly')
            nombre_entry.insert(0, producto_data[1])
            cantidad_entry.insert(0, producto_data[2])
            precio_entry.insert(0, producto_data[3].replace('$', ''))
        guardar_btn = ttk.Button(top, text="✔ Guardar", style='Green.TButton')
        guardar_btn.pack(pady=10)

        if es_edicion:
            guardar_btn.config(
                command=lambda: self.guardar_edicion(top, codigo_entry.get(), nombre_entry.get(), cantidad_entry.get(),
                                                     precio_entry.get()))
        else:
            guardar_btn.config(
                command=lambda: self.guardar_nuevo(top, codigo_entry.get(), nombre_entry.get(), cantidad_entry.get(),
                                                   precio_entry.get()))
        self.master.wait_window(top)

    def guardar_nuevo(self, top, codigo_str, nombre, cantidad_str, precio_str):
        try:
            codigo = int(codigo_str)
            cantidad = int(cantidad_str)
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error de Validación", "Código, Cantidad y Precio deben ser números válidos.")
            return
        if self.inventario.buscar_producto(codigo):
            messagebox.showerror("Error", f"El producto con código {codigo} ya existe.")
            return
        nuevo_producto = Producto(codigo, nombre, cantidad, precio)
        self.inventario.agregar_producto(nuevo_producto)
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        top.destroy()
        self.cargar_datos_treeview()

    def abrir_ventana_editar(self, event=None):
        if not self.tree or not self.tree.focus():
            return
        seleccion = self.tree.focus()
        producto_data = self.tree.item(seleccion, 'values')
        self.abrir_ventana_producto(True, producto_data[:4])

    def guardar_edicion(self, top, codigo_str, nombre, cantidad_str, precio_str):
        try:
            codigo = int(codigo_str)
            cantidad = int(cantidad_str)
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error de Validación", "Cantidad y Precio deben ser números válidos.")
            return
        if self.inventario.modificar_producto(codigo, nombre, cantidad, precio):
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            top.destroy()
            self.cargar_datos_treeview()
        else:
            messagebox.showerror("Error", "No se pudo modificar el producto.")

    def eliminar_producto_seleccionado(self, event=None):
        if not self.tree or not self.tree.focus():
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        seleccion = self.tree.focus()
        producto_data = self.tree.item(seleccion, 'values')
        codigo = int(producto_data[0])
        nombre = producto_data[1]
        if messagebox.askyesno("Confirmar Eliminación",
                               f"¿Está seguro de eliminar el producto '{nombre}' (Código: {codigo})?"):
            if self.inventario.eliminar_producto(codigo):
                self.tree.delete(seleccion)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto del inventario.")


if __name__ == '__main__':
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()