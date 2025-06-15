#Programación Tradicional
#Ejercicio que realiza el promedio semanal de temperaturas ingresadas por el usuario

# Variables globales
temperaturas = []
semana=["Lunes","Martes","Miercoles","Jueves","Viernes","Sábado","Domingo"]

# Función para ingresar temperaturas diarias
def ingresar_temperaturas():
    global temperaturas
    global semana
    print("\nIngrese la temperatura de cada día de la semana")
    for i in range(len(semana)):
        temp = float(input(f"\tDía {semana[i]}: "))
        temperaturas.append(temp)

# Función para calcular el promedio semanal
def calcular_promedio():
    global temperaturas
    if len(temperaturas) == 0:
        print("No hay temperaturas registradas.")
        return
    promedio = sum(temperaturas) / len(temperaturas)
    print(f"Promedio semanal del clima: {promedio:.2f}°C")

# Programa principal
print("--------TEMPERATURA PROMEDIO SEMANAL--------")
ingresar_temperaturas() #uso de funciones en programación tradicional
calcular_promedio()