#Ejemplo que demuestra la aplicación de la técnica del Polimosfismo

# Creamos la clase principal Empleado
class Empleado:
    def calcular_pago(self):
        return 0

# Creamos la subclase: empleado por hora
class EmpleadoPorHora(Empleado):
    def __init__(self, horas, tarifa):
        self.horas = horas
        self.tarifa = tarifa

    def calcular_pago(self):
        return self.horas * self.tarifa

#Creamos la subclase: empleado asalariado
class EmpleadoAsalariado(Empleado):
    def __init__(self, salario_mensual):
        self.salario_mensual = salario_mensual

    def calcular_pago(self):
        return self.salario_mensual

# Definimos la función que usa polimorfismo
def mostrar_pago(empleado):
    print(f"Pago: ${empleado.calcular_pago()}")

#Instanciamos los objetos
Juan = EmpleadoPorHora(horas=40, tarifa=15)
Ana = EmpleadoAsalariado(salario_mensual=2400)

# Aplicar polimorfismo
mostrar_pago(Juan)  # Pago: $600
mostrar_pago(Ana)   # Pago: $2400
