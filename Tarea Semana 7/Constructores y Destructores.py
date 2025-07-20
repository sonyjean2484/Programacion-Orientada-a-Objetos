# ------------------------Sistema de ingreso a clases virtuales--------------------------------
# Este programa simula la conexión y desconexión de los estudiantes a clases.
# utilizando el método constructor __init__ para inicializar el objeto estudiante.
# El método destructor __del__es empleado para indicar la salida de cada estudiante de la clase.
# Además, se emplea los métodos conectar y desconectar para almacenar en un archivo "registro_conexiones.txt"
# la entrada y salida de los alumnos. El método participar indica la actividad en clase.

import time
from datetime import datetime

class EstudianteConexion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tiempo_conexion = datetime.now()

    #método para almacenar en un archivo el registro de ingreso de estudaintes
    def conectar(self):
        print(f" {self.nombre} se ha conectado a las {self.tiempo_conexion.strftime('%H:%M:%S')}")
        with open("registro_conexiones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f" {self.nombre} se conectó a las {self.tiempo_conexion.strftime('%H:%M:%S')}\n")

    def participar(self):
        print(f" {self.nombre} está participando en clase.")

    #método que almacena en el archivo la hora de salida de cada estudiante
    def desconectar(self):
        tiempo_desconexion = datetime.now()
        with open("registro_conexiones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f" {self.nombre} se desconectó a las {tiempo_desconexion.strftime('%H:%M:%S')} \n")

    def __del__(self):
        print(f" {self.nombre} ha salido de la clase ")

# ----------------- Simulación de clase -----------------

estudiantes = []
print("-----------INGRESO A CLASES VIRTUALES----------")
# Conexión simulada
nombres = ["Ana Torres", "Luis Pérez", "Carla Gómez"]
for nombre in nombres:
    estudiante = EstudianteConexion(nombre) #instancia de la clase
    estudiantes.append(estudiante)
    estudiante.conectar()
    time.sleep(2)  # Diferencia de tiempo entre conexiones

# Participación en la clase
print("-------------------------------------------")
for estudiante in estudiantes:
    estudiante.participar()
    time.sleep(2)

# Desconexión de los estudiantes.
print("-------------------------------------------")
time.sleep(2)
for estudiante in estudiantes:
    estudiante.desconectar()
    time.sleep(2)

# Al finalizar el programa se llama automáticamente
#al destructor para indicar que cada estudiante ha salido de la clase virtual.

