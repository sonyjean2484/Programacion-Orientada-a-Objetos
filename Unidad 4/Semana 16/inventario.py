from producto import Producto
import os


class Inventario:
    def __init__(self, archivo_datos="inventario_data.csv"):
        # Colección: Diccionario donde la clave es el código del producto
        self.productos = {}
        self.archivo_datos = archivo_datos
        self.cargar_inventario()

    # Métodos de Persistencia (Guardar y Cargar)
    def cargar_inventario(self):
        # Carga los productos desde el archivo CSV
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r') as f:
                for line in f:
                    try:
                        codigo, nombre, cantidad, precio = line.strip().split(',')
                        producto = Producto(codigo, nombre, cantidad, precio)
                        self.productos[int(codigo)] = producto  # Almacena en la colección (diccionario)
                    except ValueError:
                        continue

    def guardar_inventario(self):
        # Guarda el estado actual de la colección en el archivo
        with open(self.archivo_datos, 'w') as f:
            for producto in self.productos.values():
                f.write(producto.to_csv_line() + '\n')

    # Métodos de Gestión
    def agregar_producto(self, producto):
        codigo = producto.get_codigo()
        if codigo not in self.productos:
            self.productos[codigo] = producto
            self.guardar_inventario()
            return True
        return False  # Producto ya existe

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            self.guardar_inventario()
            return True
        return False

    def modificar_producto(self, codigo, nuevo_nombre, nueva_cantidad, nuevo_precio):
        if codigo in self.productos:
            producto = self.productos[codigo]
            producto.set_nombre(nuevo_nombre)
            producto.set_cantidad(nueva_cantidad)
            producto.set_precio(nuevo_precio)
            self.guardar_inventario()
            return True
        return False

    def get_todos_productos(self):
        # Retorna una lista de objetos Producto
        return list(self.productos.values())

    def buscar_producto(self, codigo):
        # Búsqueda eficiente por clave del diccionario (código)
        return self.productos.get(codigo)