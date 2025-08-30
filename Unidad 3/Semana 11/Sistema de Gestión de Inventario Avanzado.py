

import csv
import os

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        """Representación legible del objeto para depuración."""
        return f"Producto(id={self.id_producto}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"

class Inventario:
    def __init__(self, nombre_archivo="inventario.csv"):
        self.productos = {}
        self.nombre_archivo = nombre_archivo
        self.cargar_inventario()

    def agregar_producto(self, producto):
        #Agrega un nuevo producto al inventario.
        if producto.id_producto in self.productos:
            print("Error: Ya existe un producto con este ID.")
        else:
            self.productos[producto.id_producto] = producto
            print(f"Producto '{producto.nombre}' agregado con éxito.")

    def eliminar_producto(self, id_producto):
        #Elimina un producto por su ID.
        if id_producto in self.productos:
            del self.productos[id_producto]
            print(f"Producto con ID {id_producto} eliminado con éxito.")
        else:
            print("Error: No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        #Actualiza la cantidad o el precio de un producto.
        if id_producto in self.productos:
            producto = self.productos[id_producto]
            if nueva_cantidad is not None:
                producto.cantidad = nueva_cantidad
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            print(f"Producto con ID {id_producto} actualizado con éxito.")
        else:
            print("Error: No se encontró un producto con ese ID.")

    def buscar_producto_por_nombre(self, nombre):
        #Busca y muestra productos que coincidan con el nombre.
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            print("Productos encontrados:")
            for p in encontrados:
                print(f"  ID: {p.id_producto}, Nombre: {p.nombre}, Cantidad: {p.cantidad}, Precio: {p.precio}")
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos_los_productos(self):
        #Muestra todos los productos del inventario.
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("--- Inventario ---")
            for producto in self.productos.values():
                print(f"  ID: {producto.id_producto}, Nombre: {producto.nombre}, Cantidad: {producto.cantidad}, Precio: {producto.precio}")
            print("------------------")

    #Serialización de la colección del inventario
    def guardar_inventario(self):
        #Guarda el inventario en un archivo CSV
        with open(self.nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Escribe la cabecera (opcional pero recomendable)
            writer.writerow(['id', 'nombre', 'cantidad', 'precio'])
            # Escribe los datos de cada producto
            for producto in self.productos.values():
                writer.writerow([producto.id_producto, producto.nombre, producto.cantidad, producto.precio])
        print("Inventario guardado en formato CSV con éxito.")

    #Deserialización de la colección del inventario
    def cargar_inventario(self):
        #Carga el inventario desde un archivo CSV si existe.
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Salta la cabecera si existe
                for row in reader:
                    try:
                        id_producto, nombre, cantidad, precio = row
                        producto = Producto(int(id_producto), nombre, int(cantidad), float(precio))
                        self.productos[producto.id_producto] = producto
                    except (ValueError, IndexError):
                        print(f"Advertencia: Fila inválida en el archivo CSV: {row}")
            print("Inventario cargado desde CSV con éxito.")
        else:
            print("Archivo de inventario CSV no encontrado. Se creará uno nuevo.")
def mostrar_menu():
    #Muestra las opciones del menú.
    print("\n--- Sistema de Gestión de Inventario ---")
    print("1. Agregar producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar producto por ID")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Guardar y salir")

def main():
    #Función principal para ejecutar el programa.
    inventario = Inventario()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                id_producto = int(input("Ingrese el ID del producto: "))
                nombre = input("Ingrese el nombre del producto: ")
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo_producto)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese valores correctos.")

        elif opcion == '2':
            try:
                id_eliminar = int(input("Ingrese el ID del producto a eliminar: "))
                inventario.eliminar_producto(id_eliminar)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un ID numérico.")

        elif opcion == '3':
            try:
                id_actualizar = int(input("Ingrese el ID del producto a actualizar: "))
                print("¿Qué desea actualizar? (cantidad/precio)")
                sub_opcion = input().lower()
                if sub_opcion == 'cantidad':
                    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                    inventario.actualizar_producto(id_actualizar, nueva_cantidad=nueva_cantidad)
                elif sub_opcion == 'precio':
                    nuevo_precio = float(input("Ingrese el nuevo precio: "))
                    inventario.actualizar_producto(id_actualizar, nuevo_precio=nuevo_precio)
                else:
                    print("Opción no válida. Por favor, elija 'cantidad' o 'precio'.")
            except ValueError:
                print("Entrada inválida. Asegúrese de ingresar números.")

        elif opcion == '4':
            nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto_por_nombre(nombre_buscar)

        elif opcion == '5':
            inventario.mostrar_todos_los_productos()

        elif opcion == '6':
            inventario.guardar_inventario()
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()