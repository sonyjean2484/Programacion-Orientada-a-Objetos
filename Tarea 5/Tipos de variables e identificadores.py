#       Sistema de Registro de Pacientes
#El programa realiza las siguientes funciones:
#   Solicita al usuario los datos de un paciente.
#   Guarda cada registro en un archivo .csv.
#   Usa variables de distintos tipos (str, int, bool, list, dict).
#   Usa funciones para organizar el código.

import csv
import os
#función que calcula el índice de masa corporal
def calcular_imc(peso, estatura):
    return round(peso / (estatura ** 2), 2)

#función para registrar al paciente, utiliza variables de tipo int, float
def registrar_paciente():
    nombre = input("Nombre del paciente: ")
    edad = int(input("Edad: "))
    genero = input("Género (M/F): ")
    estatura = float(input("Estatura en metros (ej. 1.75): "))
    peso = float(input("Peso en kilogramos: "))
    sintomas = input("Síntomas (separados por comas): ").split(",")
    asegurado = input("¿Está asegurado? (s/n): ").lower() == 's'

    imc = calcular_imc(peso, estatura) #índice de masa corporal (imc)

    paciente = {    #creación de un diccionario que almacena los datos del paciente
        "Nombre": nombre,
        "Edad": edad,
        "Género": genero,
        "Estatura": estatura,
        "Peso": peso,
        "IMC": imc,
        "Síntomas": ";".join([s.strip() for s in sintomas]),
        "Asegurado": "Sí" if asegurado else "No"
    }

    return paciente

#función que guarda los datos del paciente en un archivo csv
def guardar_paciente_csv(paciente, archivo="pacientes.csv"):
    existe = os.path.exists(archivo)

    with open(archivo, mode="a", newline="", encoding="utf-8") as file:
        campos = ["Nombre", "Edad", "Género", "Estatura", "Peso", "IMC", "Síntomas", "Asegurado"]
        escritor = csv.DictWriter(file, fieldnames=campos)

        if not existe:
            escritor.writeheader()

        escritor.writerow(paciente)
    print("✅ Paciente guardado correctamente.\n")

#función que permite mostrar el registro de todos los pacientes
def mostrar_todos(archivo="pacientes.csv"):
    if not os.path.exists(archivo):
        print("❌ No hay registros aún.")
        return

    print("\n📋 Lista de pacientes registrados:\n")
    with open(archivo, mode="r", encoding="utf-8") as file:
        lector = csv.DictReader(file)
        for i, fila in enumerate(lector, start=1):
            print(f"{i}. {fila['Nombre']} - Edad: {fila['Edad']} - Género: {fila['Género']} - Asegurado: {fila['Asegurado']}")
            print(f"   Estatura: {fila['Estatura']} m - Peso: {fila['Peso']} kg - IMC: {fila['IMC']}")
            print("   Síntomas:", fila['Síntomas'])
        print()

# Programa principal
while True:
    print("1. Registrar nuevo paciente")
    print("2. Ver todos los pacientes")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        paciente = registrar_paciente()
        guardar_paciente_csv(paciente)
    elif opcion == "2":
        mostrar_todos()
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("❗ Opción no válida, intenta nuevamente.\n")
