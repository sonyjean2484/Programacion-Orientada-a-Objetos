
#Programa que realiza la compra de tickets para el cine
#------------------------------------------------------
#Se demuestra la aplicación de conceptos de POO como:
# HERENCIA : AdultoTicket, NinoTicket y TerceraEdadTicket se derivan de Ticket.
# ENCAPSULACIÓN : El atributo __precio es privado; se expone con la propiedad precio.
# POLIMORFISMO : Cada subclase sobreescribe calcular_precio().
#                Además, Carrito.agregar_ticket usa *tickets (argumentos variables) y acepta cualquier subclase de Ticket.

from __future__ import annotations

#Clase base para un ticket de cine
class Ticket:

    def __init__(self, pelicula: str, asiento: str, precio_base: float) -> None:
        self.pelicula = pelicula             # atributo público
        self.asiento = asiento               # atributo público
        self.__precio = precio_base          # atributo privado (encapsulado)

    # ---------------- Encapsulación ----------------
    @property #usado cada vez que el programa lee precio
    def precio(self) -> float:
        return self.__precio   #Precio final del ticket (solo lectura pública).

    # Método protegido que permite a las subclases modificar el precio de forma segura.
    def _precio_fijo(self, valor: float) -> None:
        self.__precio = valor

    # ---------------- Polimorfismo (Sobrescritura) ----------------
    def calcular_precio(self) -> None:
        self._precio_fijo(self.precio) #En la clase base no hay cambio (precio base). Asegura que el precio se mantiene igual

    # ---------------- Utilidad ----------------
    def __str__(self) -> str:
        return f"{self.__class__.__name__} | '{self.pelicula}' | Asiento {self.asiento} | ${self.precio:.2f}"

#Ticket de adulto (sin descuento).
class AdultoTicket(Ticket):
    def calcular_precio(self) -> None:  # sobrescribe
        self._precio_fijo(self.precio) # Adulto paga el 100% del precio base

# Ticket de niño (50% de descuento).
class NinosTicket(Ticket):
      def calcular_precio(self) -> None:  # sobrescribe
        self._precio_fijo(self.precio * 0.5)

# Ticket de tercera edad (30% de descuento).
class TerceraEdadTicket(Ticket):
      def calcular_precio(self) -> None:  # sobrescribe
        self._precio_fijo(self.precio * 0.7)

#Carrito para la compra de tickets.
class Carrito:

    def __init__(self) -> None:
        self._tickets: list[Ticket] = []  # lista protegida que almacena objetos de la clase Ticket

    # Polimorfismo adicional: agregar_ticket acepta cualquier cantidad (*tickets) y cualquier
    # subclase de Ticket.
    def agregar_ticket(self, *tickets: Ticket) -> None:
        for t in tickets:
            t.calcular_precio()  # Polimorfismo: se invoca la versión apropiada
            self._tickets.append(t)

    def total(self) -> float:
        return sum(t.precio for t in self._tickets)

    def resumen(self) -> None:
        print("\n--------------- RESUMEN DE COMPRA ----------------\n")
        for t in self._tickets:
            print(t)
        print(f"\nTOTAL A PAGAR: ${self.total():.2f}\n")


# -------------------------- SIMULACIÓN ----------------------------

def simular() -> None:
    carrito = Carrito()  # Crea un carrito y varias instancias (Herencia)
    # Precio base común de $7.60
    carrito.agregar_ticket(
        AdultoTicket("Superman", "B7", 7.60),
        NinosTicket("Superman", "B8", 7.60),
        TerceraEdadTicket("Superman", "B9", 7.60),
    )

    # Muestra un resumen del pedido
    carrito.resumen()

if __name__ == "__main__":
    simular()
