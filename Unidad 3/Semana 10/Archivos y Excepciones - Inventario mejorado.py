#------------------------SISTEMA DE GESTIÓN DE INVENTARIO------------------------------
#Este programa es una aplicación de consola desarrollada en Python, cuyo objetivo es
# administrar de manera sencilla los productos de un inventario en una tienda.

# Función principal
# El sistema permite añadir, actualizar, eliminar, buscar y mostrar productos utilizando
# una estructura de datos personalizada basada en clases.
#


import os
import csv

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Métodos Getters
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Métodos Setters
    def set_cantidad(self, nueva_cantidad):
        self._cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio):
        self._precio = nuevo_precio

    def __str__(self):
        return f" {self._id:<5} {self._nombre:<20} {self._cantidad:<10}{self._precio:<10.2f}"

# Clase Inventario
class Inventario:
    def __init__(self, nombre_archivo='inventario.csv'):
        self.productos = []
        self.nombre_archivo = nombre_archivo

    def agregar_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print("ERROR: El ID del producto ya existe.")
            return False
        self.productos.append(producto)
        self.guardar_inventario()
        print(" Producto agregado con éxito.")
        return True

    def eliminar_producto(self, id_producto):
        producto_encontrado = self.buscar_por_id(id_producto)
        if producto_encontrado:
            self.productos.remove(producto_encontrado)
            self.guardar_inventario()
            print(" Producto eliminado con éxito.")
            return True
        else:
            print(" Error: Producto no encontrado.")
            return False

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        producto = self.buscar_por_id(id_producto)
        if producto:
            if nueva_cantidad is not None:
                producto.set_cantidad(nueva_cantidad)
            if nuevo_precio is not None:
                producto.set_precio(nuevo_precio)
            self.guardar_inventario()
            print(" Producto actualizado con éxito.")
            return True
        else:
            print(" Error: Producto no encontrado.")
            return False

    def buscar_por_nombre(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        return resultados

    def buscar_por_id(self, id_producto):
        for producto in self.productos:
            if producto.get_id() == id_producto:
                return producto
        return None

    def mostrar_inventario(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\n--- Inventario Actual ---")
            print("-" * 50)
            print(f"{'ID':<5} {'Nombre':<20} {'Cantidad':<10} {'Precio':<10}")
            print("-" * 50)
            for producto in self.productos:
                print(producto)
            print("-" * 50)

    def guardar_inventario(self):
        try:
            with open(self.nombre_archivo, 'w', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                for producto in self.productos:
                    escritor_csv.writerow([producto.get_id(), producto.get_nombre(), producto.get_cantidad(), producto.get_precio()])
            print(f" Inventario guardado exitosamente en el archivo {self.nombre_archivo}.")
        except PermissionError:
            print(f" Error: No tienes permisos para escribir en el archivo {self.nombre_archivo}.")
        except Exception as e:
            print(f" Ocurrió un error inesperado al guardar el archivo: {e}")

    def cargar_inventario(self):
        try:
            if not os.path.exists(self.nombre_archivo):
                print(f" Archivo '{self.nombre_archivo}' no encontrado. Creando nuevo inventario.")
                return

            with open(self.nombre_archivo, 'r') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                for fila in lector_csv:
                    if len(fila) == 4:
                        try:
                            id_prod = int(fila[0])
                            nombre = fila[1]
                            cantidad = int(fila[2])
                            precio = float(fila[3])
                            producto = Producto(id_prod, nombre, cantidad, precio)
                            self.productos.append(producto)
                        except (ValueError, IndexError):
                            print(f" Advertencia: Línea con formato incorrecto en el archivo: '{fila}'")
            print(f" Inventario cargado exitosamente desde el archivo {self.nombre_archivo}.")

        except FileNotFoundError:
            print(f" Error: No se pudo encontrar el archivo {self.nombre_archivo}.")
        except PermissionError:
            print(f" Error: No tienes permisos para leer el archivo {self.nombre_archivo}.")
        except Exception as e:
            print(f" Ocurrió un error inesperado al cargar el archivo: {e}")

# Menú principal
def mostrar_menu():
    print("\n---------- Sistema de Gestión de Inventario ----------")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Salir")
    return input("Elija una opción: ")

# Función principal
def main():
    inventario = Inventario()
    inventario.cargar_inventario()

    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            try:
                id_prod = int(input("Ingresa el ID del producto: "))
                nombre = input("Ingresa el nombre: ")
                cantidad = int(input("Ingresa la cantidad: "))
                precio = float(input("Ingresa el precio: "))
                nuevo_producto = Producto(id_prod, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo_producto)
            except ValueError:
                print(" Entrada inválida. Asegúrate de usar los tipos de datos correctos.")

        elif opcion == '2':
            try:
                id_prod = int(input("Ingresa el ID del producto a eliminar: "))
                inventario.eliminar_producto(id_prod)
            except ValueError:
                print(" Entrada inválida. El ID debe ser un número.")

        elif opcion == '3':
            try:
                id_prod = int(input("Ingresa el ID del producto a actualizar: "))
                opcion_act = input("¿Deseas actualizar 'cantidad' (c), 'precio' (p) o 'ambos' (a)? ").lower()
                nueva_cantidad = None
                nuevo_precio = None

                if opcion_act in ['c', 'a']:
                    nueva_cantidad = int(input("Ingresa la nueva cantidad: "))
                if opcion_act in ['p', 'a']:
                    nuevo_precio = float(input("Ingresa el nuevo precio: "))

                inventario.actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)
            except ValueError:
                print(" Entrada inválida. Asegúrate de usar los tipos de datos correctos.")

        elif opcion == '4':
            nombre_buscado = input("Ingresa el nombre del producto a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre_buscado)
            if resultados:
                print("\n--- Resultados de Búsqueda ---")
                print("-" * 50)
                print(f"{'ID':<5} {'Nombre':<20} {'Cantidad':<10} {'Precio':<10}")
                print("-" * 50)
                for prod in resultados:
                    print(prod)
                print("-" * 50)
            else:
                print("No se encontraron productos con ese nombre.")

        elif opcion == '5':
            inventario.mostrar_inventario()

        elif opcion == '6':
            print(" Gracias, vuelva pronto.")
            break

        else:
            print(" Opción inválida. Seleccione del 1 al 6.")

if __name__ == "__main__":
    main()