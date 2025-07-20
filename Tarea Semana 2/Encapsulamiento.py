#Ejercicio que demuestra la técnica de Encapsulammiento en la
#clase Cuenta Bancaria

#Creamos la clase Cuenta bancaria
class CuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.__saldo = saldo_inicial  # atributo privado encapsulado

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto

    def retirar(self, monto):
        if 0 < monto <= self.__saldo:
            self.__saldo -= monto
        else:
            print("Fondos insuficientes")

    def ver_saldo(self):
        return self.__saldo


# Instanciamos un objeto de la clase principal
cuenta = CuentaBancaria("Sonia", 1500)

# Accedemos al saldo solo mediante métodos públicos, si accedemos directamente Error de atributo
cuenta.depositar(800)
cuenta.retirar(300)
print("Saldo actual: $", cuenta.ver_saldo())  # Muestra el Saldo actual: $2000