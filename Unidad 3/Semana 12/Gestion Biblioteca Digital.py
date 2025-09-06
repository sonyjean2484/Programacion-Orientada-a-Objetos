
# --- Clases Principales ---

class Libro:
    """
    Representa un libro con sus atributos esenciales.
    Utiliza una tupla para el autor y el título, garantizando su inmutabilidad.
    """
    def __init__(self, titulo, autor, categoria, isbn):
        # La tupla (autor, titulo) asegura que estos valores no se modifiquen
        self.identificador = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"Título: {self.identificador[0]}, Autor: {self.identificador[1]}, ISBN: {self.isbn}, Categoría: {self.categoria}"


class Usuario:
    """
    Representa a un usuario de la biblioteca.
    El ID de usuario se debe ingresar al crear el objeto.
    """
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        # El ID de usuario ahora se recibe como parámetro
        self.id_usuario = id_usuario
        # La lista de libros prestados almacena los objetos Libro
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre}, ID: {self.id_usuario}"


class Biblioteca:
    """
    Gestiona la colección de libros, usuarios y el historial de préstamos.
    """
    def __init__(self):
        # El diccionario 'libros_disponibles' usa el ISBN como clave para una búsqueda eficiente O(1)
        self.libros_disponibles = {}
        # El conjunto 'usuarios_registrados' asegura que los IDs de usuarios sean únicos
        self.usuarios_registrados = set()
        # El diccionario 'historial_prestamos' almacena los préstamos por ID de usuario
        self.historial_prestamos = {}

    # --- Funcionalidades de Libros ---

    def anadir_libro(self, libro):
        """Añade un libro al catálogo de la biblioteca si el ISBN es único."""
        if libro.isbn in self.libros_disponibles:
            print(f"Error: El libro con ISBN {libro.isbn} ya existe en la biblioteca.")
        else:
            self.libros_disponibles[libro.isbn] = libro
            print(f"Libro '{libro.identificador[0]}' añadido exitosamente.")

    def quitar_libro(self, isbn):
        """Quita un libro del catálogo usando su ISBN."""
        if isbn in self.libros_disponibles:
            libro_eliminado = self.libros_disponibles.pop(isbn)
            print(f"Libro '{libro_eliminado.identificador[0]}' eliminado exitosamente.")
        else:
            print(f"Error: No se encontró un libro con ISBN {isbn}.")

    def buscar_libro(self, criterio, valor):
        """
        Busca libros por título, autor o categoría.
        Retorna una lista de libros que coinciden con la búsqueda.
        """
        resultados = []
        criterio = criterio.lower()
        valor = valor.lower()

        if criterio not in ['titulo', 'autor', 'categoria']:
            print("Criterio de búsqueda no válido. Use 'titulo', 'autor' o 'categoria'.")
            return resultados

        for libro in self.libros_disponibles.values():
            if criterio == 'titulo' and valor in libro.identificador[0].lower():
                resultados.append(libro)
            elif criterio == 'autor' and valor in libro.identificador[1].lower():
                resultados.append(libro)
            elif criterio == 'categoria' and valor in libro.categoria.lower():
                resultados.append(libro)

        return resultados

    # --- Funcionalidades de Usuarios ---

    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario en la biblioteca si su ID es único."""
        if usuario.id_usuario in self.usuarios_registrados:
            print(f"Error: El usuario con ID {usuario.id_usuario} ya está registrado.")
        else:
            self.usuarios_registrados.add(usuario.id_usuario)
            self.historial_prestamos[usuario.id_usuario] = usuario
            print(f"Usuario '{usuario.nombre}' registrado exitosamente con ID: {usuario.id_usuario}.")

    def dar_baja_usuario(self, id_usuario):
        """Da de baja a un usuario si no tiene libros prestados."""
        if id_usuario in self.usuarios_registrados:
            usuario = self.historial_prestamos[id_usuario]
            if usuario.libros_prestados:
                print(
                    f"Error: El usuario '{usuario.nombre}' aún tiene libros prestados. Debe devolverlos antes de darse de baja.")
            else:
                self.usuarios_registrados.remove(id_usuario)
                del self.historial_prestamos[id_usuario]
                print(f"Usuario con ID {id_usuario} dado de baja exitosamente.")
        else:
            print(f"Error: No se encontró un usuario con ID {id_usuario}.")

    # --- Funcionalidades de Préstamos ---

    def prestar_libro(self, id_usuario, isbn):
        """Presta un libro a un usuario si está disponible y el usuario está registrado."""
        if id_usuario not in self.usuarios_registrados:
            print(f"Error: El usuario con ID {id_usuario} no está registrado.")
            return

        if isbn not in self.libros_disponibles:
            print(f"Error: El libro con ISBN {isbn} no está disponible.")
            return

        libro_a_prestar = self.libros_disponibles[isbn]
        usuario = self.historial_prestamos[id_usuario]

        # Evitamos prestar el mismo libro si ya lo tiene el usuario
        if libro_a_prestar in usuario.libros_prestados:
            print(
                f"Error: El usuario '{usuario.nombre}' ya tiene prestado el libro '{libro_a_prestar.identificador[0]}'.")
            return

        usuario.libros_prestados.append(libro_a_prestar)
        del self.libros_disponibles[isbn]  # Se quita el libro de la colección de disponibles
        print(f"Libro '{libro_a_prestar.identificador[0]}' prestado a '{usuario.nombre}' exitosamente.")

    def devolver_libro(self, id_usuario, isbn):
        """Permite a un usuario devolver un libro."""
        if id_usuario not in self.usuarios_registrados:
            print(f"Error: El usuario con ID {id_usuario} no está registrado.")
            return

        usuario = self.historial_prestamos[id_usuario]
        libro_a_devolver = None

        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                libro_a_devolver = libro
                break

        if libro_a_devolver:
            usuario.libros_prestados.remove(libro_a_devolver)
            self.anadir_libro(libro_a_devolver)  # Usamos el método existente para volver a añadirlo
            print(f"Libro '{libro_a_devolver.identificador[0]}' devuelto por '{usuario.nombre}' exitosamente.")
        else:
            print(f"Error: El usuario '{usuario.nombre}' no tiene prestado el libro con ISBN {isbn}.")

    def listar_libros_prestados(self, id_usuario):
        """Muestra los libros que un usuario tiene actualmente prestados."""
        if id_usuario not in self.usuarios_registrados:
            print(f"Error: No se encontró un usuario con ID {id_usuario}.")
            return

        usuario = self.historial_prestamos[id_usuario]
        if not usuario.libros_prestados:
            print(f"El usuario '{usuario.nombre}' no tiene libros prestados.")
            return

        print(f"--- Libros prestados por '{usuario.nombre}': ---")
        for libro in usuario.libros_prestados:
            print(f"    - {libro}")


# --- Funcionalidad del Menú ---

def menu_principal():
    """
    Función principal que implementa el menú interactivo para gestionar la biblioteca.
    """
    biblioteca = Biblioteca()

    # Datos de prueba para agilizar las demostraciones
    print("Cargando datos de prueba...")
    biblioteca.anadir_libro(Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "978-84-376-0494-8"))
    biblioteca.anadir_libro(Libro("El principito", "Antoine de Saint-Exupéry", "Infantil", "978-84-7888-999-9"))
    biblioteca.anadir_libro(Libro("1984", "George Orwell", "Ciencia Ficción", "978-0-452-28423-4"))
    biblioteca.anadir_libro(Libro("Orgullo y Prejuicio", "Jane Austen", "Novela", "978-0-452-28423-6"))
    biblioteca.anadir_libro(Libro("El señor de los anillos", "J. R. R. Tolkien", "Ciencia Ficción", "978-0-455-28445-0"))

    # Los usuarios ahora se crean con un ID manual para la demostración
    usuario_ana = Usuario("Ana García", "ana123")
    usuario_luis = Usuario("Luis Pérez", "luis456")
    usuario_sonia = Usuario("Sonia Vasquez", "sonia123")
    usuario_david = Usuario("David Calvache", "david456")
    biblioteca.registrar_usuario(usuario_ana)
    biblioteca.registrar_usuario(usuario_luis)
    biblioteca.registrar_usuario(usuario_sonia)
    biblioteca.registrar_usuario(usuario_david)
    print("-" * 30)

    while True:
        print("\n--- Sistema de Gestión de Biblioteca ---")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados de un usuario")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.anadir_libro(libro)

        elif opcion == '2':
            isbn = input("Ingrese el ISBN del libro a quitar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == '3':
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID de usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)

        elif opcion == '4':
            id_usuario = input("Ingrese el ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == '5':
            id_usuario = input("ID del usuario: ")
            isbn = input("ISBN del libro a prestar: ")
            biblioteca.prestar_libro(id_usuario, isbn)

        elif opcion == '6':
            id_usuario = input("ID del usuario: ")
            isbn = input("ISBN del libro a devolver: ")
            biblioteca.devolver_libro(id_usuario, isbn)

        elif opcion == '7':
            criterio = input("Criterio de búsqueda (titulo, autor, categoria): ")
            valor = input("Valor a buscar: ")
            resultados = biblioteca.buscar_libro(criterio, valor)
            if resultados:
                print("\nResultados de la búsqueda:")
                for libro in resultados:
                    print(libro)
            else:
                print("No se encontraron resultados.")

        elif opcion == '8':
            id_usuario = input("ID del usuario: ")
            biblioteca.listar_libros_prestados(id_usuario)

        elif opcion == '9':
            print("Saliendo del sistema. ¡Vuelva pronto!")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")


# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal()