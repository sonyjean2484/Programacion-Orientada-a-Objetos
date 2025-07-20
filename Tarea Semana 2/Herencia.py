#Ejercicio que demuestra como los objetos: perro y gato HEREDAN atributos de la clase principal Animal.

# Clase principal (superclase)
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    print("Superclase : ANIMAL")

    def hacersonido(self):
        return f"{self.nombre} hace un sonido."

# Creamos la subclase Perro - Hereda de Animal
class Perro(Animal):
    def hacersonido(self):
        return f"{self.nombre} dice ¡Guau!"
    print("Subclase : Perro de nombre Coquito")

# Creamos la subclase Gato - Hereda de Animal
class Gato(Animal):
    def hacersonido(self):
        return f"{self.nombre} dice ¡Miau!"
    print("Subclase : Gato de nombre Goku")

# Instanciamos objetos de las subclases Perro y Gato
perro1 = Perro("Coquito")
gato1 = Gato("Goku")

# Probamos los métodos
print(perro1.hacersonido())  # Coquito dice ¡Guau!
print(gato1.hacersonido())   # Goku dice ¡Miau!