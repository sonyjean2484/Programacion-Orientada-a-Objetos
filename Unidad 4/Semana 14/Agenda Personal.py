
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import json
import os

ARCHIVO = "agenda.json"
FONDO = "imagen agenda3.jpg"

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AGENDA PERSONAL")
        self.root.geometry("800x500")

        # Cargar imagen de fondo
        self._cargar_imagen_fondo()

        # Contenedor principal
        self.container = tk.Frame(root, bg="#FFF0F5", bd=2, relief="groove")
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=760, height=460)

        # Crear layout modular
        self._crear_estructura()

        # Cargar eventos guardados
        self.cargar_eventos()

        # Evento que al seleccionar un ítem en la lista, cargar sus datos en los campos
        self.tree.bind("<<TreeviewSelect>>", self.cargar_datos_evento)

    def _cargar_imagen_fondo(self):
        """Carga y coloca la imagen de fondo si existe."""
        if os.path.exists(FONDO):
            self.bg_image = Image.open(FONDO)
            self.bg_image = self.bg_image.resize((800, 500), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)

    def _crear_estructura(self):
        """Crea la estructura de la interfaz (calendario, botones, campos y lista de eventos)."""
        # Frame para la columna izquierda (calendario y botones)
        frame_izquierda = tk.Frame(self.container, bg="#FFF0F5")
        frame_izquierda.pack(side="left", fill="y", padx=10, pady=10)

        self._crear_calendario(frame_izquierda)
        self._crear_campos_entrada(frame_izquierda)
        self._crear_botones(frame_izquierda)

        # Frame para la columna derecha (lista de eventos)
        frame_derecha = tk.Frame(self.container, bg="#FFF0F5")
        frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self._crear_lista_eventos(frame_derecha)

    def _crear_calendario(self, frame_izquierda):
        """Crea el widget del calendario."""
        self.fecha_entry = DateEntry(frame_izquierda, width=12, background="gray",
                                     foreground="#FFF0F5", borderwidth=2, date_pattern="dd/mm/yyyy")
        self.fecha_entry.pack(pady=5)

    def _crear_campos_entrada(self, frame_izquierda):
        """Crea los campos de entrada (hora y descripción)."""
        tk.Label(frame_izquierda, text="Hora (HH:MM):", font=("Brandon Grotesque Italic", 10), bg="#FFF0F5").pack(
            pady=5)
        self.hora_entry = tk.Entry(frame_izquierda)
        self.hora_entry.pack(pady=5)
        self.hora_entry.config(bg="snow", fg="black")  # Cambiar color de fondo y texto de 'hora_entry'

        tk.Label(frame_izquierda, text="Descripción:", font=("Brandon Grotesque Italic", 10), bg="#FFF0F5").pack(pady=5)
        self.descripcion_entry = tk.Entry(frame_izquierda, width=30)
        self.descripcion_entry.pack(pady=5)
        self.descripcion_entry.config(bg="snow",
                                      fg="black")  # Cambiar color de fondo y texto de 'descripcion_entry'

    def _crear_botones(self, frame_izquierda):
        """Crea los botones (agregar, editar, eliminar, salir)."""
        tk.Button(frame_izquierda, text="Agregar Evento", bg="#E6E6FA", font=("Brandon Grotesque Regular", 10),
                  command=self.agregar_evento).pack(pady=5)
        tk.Button(frame_izquierda, text="Editar Evento", bg="#E6E6FA", font=("Brandon Grotesque Regular", 10),
                  command=self.editar_evento).pack(pady=5)
        tk.Button(frame_izquierda, text="Eliminar Evento", bg="#E6E6FA", font=("Brandon Grotesque Regular", 10),
                  command=self.eliminar_evento).pack(pady=5)
        tk.Button(frame_izquierda, text="Salir", bg="#E6E6FA", font=("Brandon Grotesque Regular", 10),
                  command=self.salir).pack(pady=5)

    def _crear_lista_eventos(self, frame_derecha):
        """Crea el widget Treeview (lista de eventos)."""
        columnas = ("Fecha", "Hora", "Descripción")
        #Crea un objeto de estilo
        styles = ttk.Style()
        #Cambiar el color de fondo y texto del Treeview
        styles.configure("Custom.Treeview", background="snow", fieldbackground="snow", foreground= "black")
        # Cambiar el color de fondo y texto de las filas seleccionadas
        styles.map("Custom.Treeview",
                  background=[("selected", "lightblue")],
                  foreground=[("selected", "black")])

        self.tree = ttk.Treeview(frame_derecha, columns=columnas, show="headings", height=15, style="Custom.Treeview")
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(side="left", fill="both", expand=True)

    def agregar_evento(self):
        """Agrega un evento a la lista."""
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()

        if not hora or not descripcion:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        self.tree.insert("", "end", values=(fecha, hora, descripcion))
        self.limpiar_campos()
        self.guardar_eventos()

    def editar_evento(self):
        """Edita el evento seleccionado."""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un evento para editar.")
            return

        item = seleccionado[0]
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()

        if not hora or not descripcion:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos para editar.")
            return

        self.tree.item(item, values=(fecha, hora, descripcion))
        self.limpiar_campos()
        self.guardar_eventos()

    def eliminar_evento(self):
        """Elimina el evento seleccionado."""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un evento para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el evento seleccionado?")
        if confirmar:
            for item in seleccionado:
                self.tree.delete(item)
            self.guardar_eventos()
        self.limpiar_campos()

    def cargar_datos_evento(self, event):
        """Carga los datos del evento seleccionado en los campos de entrada."""
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado[0])
            fecha, hora, descripcion = item["values"]

            # Cargar valores en los campos
            self.fecha_entry.set_date(fecha)
            self.hora_entry.delete(0, tk.END)
            self.hora_entry.insert(0, hora)
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, descripcion)

    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.hora_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)

    def guardar_eventos(self):
        """Guarda los eventos en el archivo JSON."""
        eventos = []
        for item in self.tree.get_children():
            eventos.append(self.tree.item(item, "values"))

        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(eventos, f, ensure_ascii=False, indent=4)

    def cargar_eventos(self):
        """Carga los eventos guardados desde el archivo JSON."""
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                eventos = json.load(f)
                for evento in eventos:
                    self.tree.insert("", "end", values=evento)

    def salir(self):
        """Guarda los eventos y cierra la aplicación."""
        self.guardar_eventos()
        self.root.quit()

# --- Programa principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()

