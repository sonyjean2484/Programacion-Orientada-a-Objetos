#Programación Orientada a Objetos
#Ejercicio que realiza el promedio semanal de temperaturas ingresadas por el usuario creando clases
#usando Herencia y encapsulamieto.

class ClimaSemana:
    def __init__(self):
        self._temperaturas = []  # Privado para acceso desde la subclase
        self.semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sábado","Domingo"]

    def ingresar_temperaturas(self):
        print("\nIngrese la temperatura de cada día de la semana")
        for i in range(len(self.semana)):
            temp = float(input(f"\tDía {self.semana[i]}: "))
            self._temperaturas.append(temp)

    def calcular_promedio(self):
        if not self._temperaturas:
            print("No hay temperaturas registradas.")
            return
        promedio = sum(self._temperaturas) / len(self._temperaturas)
        print(f"Promedio semanal del clima: {promedio:.2f}°C")


# Clase hija que hereda de ClimaSemana y amplía un método
class AnalisisClima(ClimaSemana):
    def mostrar_maxima_minima(self):
        if not self._temperaturas:
            print("No hay temperaturas registradas.")
            return
        print(f"Temperatura máxima: {max(self._temperaturas)}°C")
        print(f"Temperatura mínima: {min(self._temperaturas)}°C")


# Programa principal
if __name__ == "__main__":
    print("--------TEMPERATURA PROMEDIO SEMANAL--------")
    clima = AnalisisClima()  #Instancia del objeto de la subclase
    clima.ingresar_temperaturas() #uso de los métodos en POO
    clima.calcular_promedio()
    clima.mostrar_maxima_minima()