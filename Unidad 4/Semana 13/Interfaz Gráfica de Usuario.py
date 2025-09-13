
import tkinter as tk
from tkinter import messagebox

# Función para agregar datos a la lista
def agregar_tarea():
    dato = entry_dato.get()  # Obtiene el dato del campo de texto
    if dato != "":  # Verifica que el campo no esté vacío
        listbox.insert(tk.END, dato)  # Agrega el dato a la lista
        entry_dato.delete(0, tk.END)  # Limpia el campo de texto
    else:
        messagebox.showwarning("Advertencia", "El campo no puede estar vacío.")

# Función para limpiar la lista o un elemento seleccionado
def limpiar_tareas():
    if listbox.curselection():
        # Elimina solo un elemento seleccionado
        listbox.delete(listbox.curselection())
    else:
        # Elimina toda la lista
        messagebox.showwarning("Advertencia", "La lista será eliminada completamente")
        listbox.delete(0, tk.END)

# Crea la ventana principal
ventana = tk.Tk()
ventana.title("GESTOR BÁSICO DE TAREAS")
ventana.geometry("550x400")
ventana.configure(background="#ECE8EB")

# Etiqueta para el campo de texto
label_dato = tk.Label(ventana, text="Ingrese una tarea:", fg="#333333", bg="#ECE8EB", font=("Congenial", 11))
label_dato.pack(pady=10)

# Campo de texto donde el usuario ingresará tareas
entry_dato = tk.Entry(ventana, width=40, font= ("Congenial", 11))
entry_dato.pack(pady=10)

#Marco para los botones
frame_botones = tk.Frame(ventana, background= "#ECE8EB")
frame_botones.pack(pady=5)

# Botón para agregar una tarea a la lista
boton_agregar = tk.Button(frame_botones, text="Agregar", relief= "groove", borderwidth= 5, bg="#FF4081", fg="#FFFFFF", font= ("Congenial", 11), command=agregar_tarea)
boton_agregar.pack(side="left" , padx=5)

# Botón para limpiar la lista o una tarea seleccionada
boton_limpiar = tk.Button(frame_botones, text="Limpiar", relief= "groove", borderwidth= 5, bg="#00BCD4", fg="#FFFFFF", font= ("Congenial", 11), command=limpiar_tareas)
boton_limpiar.pack(side="left" , padx=5)

# Lista para mostrar las tareas agregadas
listbox = tk.Listbox(ventana, width=50, height=10, font= ("Congenial", 11))
listbox.pack(pady=10)

# Inicia la aplicación o la actualiza
ventana.mainloop()
