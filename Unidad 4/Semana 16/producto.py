class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        # Atributos (simulando encapsulamiento)
        self._codigo = int(codigo)
        self._nombre = nombre
        self._cantidad = int(cantidad)
        self._precio = float(precio)

    # Métodos Getters
    def get_codigo(self):
        return self._codigo

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Métodos Setters
    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def set_cantidad(self, nueva_cantidad):
        self._cantidad = int(nueva_cantidad)

    def set_precio(self, nuevo_precio):
        self._precio = float(nuevo_precio)

    # Método para obtener datos para guardar en archivo CSV
    def to_csv_line(self):
        return f"{self._codigo},{self._nombre},{self._cantidad},{self._precio:.2f}"