#     Sistema para compra de productos en línea
#Implemetación de un sistema sencillo que simula la compra
#de productos en línea, presenta el carrito de compras del ususario
# con la especificación de cada producto y el total a pagar.

# Clase padre: Producto
class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre           # Encapsulamiento (uso de atributos privados)
        self._precio = precio
    #presenta información del producto
    def mostrar_info(self):
        return f"{self._nombre}: ${self._precio:.2f}"

    def get_precio(self):
        return self._precio

# Herencia: clase hija ProductoFisico hereda de Producto
class ProductoFisico(Producto):
    def __init__(self, nombre, precio, peso):
        super().__init__(nombre, precio)
        self._peso = peso

    # Polimorfismo: redefinimos mostrar_info para ProductoFisico
    def mostrar_info(self):
        return f"{self._nombre} (físico) - ${self._precio:.2f}, {self._peso}kg"

# Otro tipo de producto (producto digital),también clase hija
class ProductoDigital(Producto):
    def __init__(self, nombre, precio, licencia):
        super().__init__(nombre, precio)
        self._licencia = licencia

    def mostrar_info(self):
        return f"{self._nombre} (digital) - ${self._precio:.2f}, Licencia: {self._licencia}"

# Clase Cliente
class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.carrito = []
    #agrega productos al carrito de compras
    def agregar_al_carrito(self, producto):
        self.carrito.append(producto)
        print(f"\n✔ {producto.mostrar_info()} agregado al carrito.")
    #presenta los productos del carrito
    def ver_carrito(self):
        print(f"\n🛒 Carrito de {self.nombre}:")
        total = 0
        for producto in self.carrito:
            print(" -", producto.mostrar_info())
            total += producto.get_precio()
        print(f"Total a pagar: ${total:.2f}")

# Simulación del sistema
if __name__ == "__main__":
    # Ejemplo de Productos disponibles
    libro = ProductoFisico("Libro Python", 25.99, 0.5)
    curso = ProductoDigital("Curso Online POO", 49.99, "IL2025")

    # Cliente
    cliente1 = Cliente("María")

    # Agregando productos al carrito de compras
    cliente1.agregar_al_carrito(libro)
    cliente1.agregar_al_carrito(curso)

    # Ver el contenido del carrito
    cliente1.ver_carrito()