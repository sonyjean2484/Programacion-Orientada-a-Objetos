# Ejemplo para modelar un sistema de vehículos donde se usará Abstracción

from abc import ABC, abstractmethod # Para la abstracción

# Clase principal (abstracta) Vehículo
class Vehiculo(ABC):
    def __init__(self, marca, modelo):
        self.__marca = marca        # Encapsulamiento (atributos privados)
        self.__modelo = modelo

    @abstractmethod
    def arrancar(self):            # Método abstracto
        pass

    def info(self):
        return f"Marca: {self.__marca}, Modelo: {self.__modelo}"

# Subclase Auto que hereda de Vehiculo arrancar
class Auto(Vehiculo):
    def arrancar(self):           # Polimorfismo: redefine el método
        return "El auto arranca con llave."

# Subclase Moto que hereda de Vehículo arrancar
class Moto(Vehiculo):
    def arrancar(self):           # Polimorfismo: redefine el método
        return "La moto arranca con botón."

# Instanciamos los objetos
auto1 = Auto("Mercedez Benz", "Clase-C")
moto1 = Moto("Susuki", "GSX-R1000")

# Uso de métodos
print(auto1.info())              # presenta la información del auto
print(auto1.arrancar())         # El auto arranca con llave

print(moto1.info())              # Presenta la información de la moto
print(moto1.arrancar())         # La moto arranca con botón