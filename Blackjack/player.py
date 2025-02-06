class Jugador:
    def __init__(self, nombre, saldo=1000):
        """Inicializa al jugador con un nombre, saldo y mano vacía."""
        self.nombre = nombre
        self.saldo = saldo
        self.mano = []
        self.apuesta = 0

    def apostar(self, cantidad):
        """Permite al jugador hacer una apuesta si tiene saldo suficiente."""
        if cantidad > self.saldo:
            print(f"{self.nombre}, you don't have enough chips for this bet:  {cantidad}.")
            return False
        self.apuesta = cantidad
        self.saldo -= cantidad
        return True

    def recibir_carta(self, carta):
        """Añade una carta a la mano del jugador."""
        self.mano.append(carta)

    def calcular_valor_mano(self):
        """Calcula el valor total de la mano considerando el As como 1 o 11."""
        total = sum(self.mano)
        ases = self.mano.count(11)  # Contamos cuántos Ases hay

        # Ajustar el valor de los Ases si el total supera 21
        while total > 21 and ases:
            total -= 10  # Convertimos un As de 11 a 1
            ases -= 1

        return total

    def resetear_mano(self):
        """Vacía la mano del jugador para una nueva ronda."""
        self.mano = []
        self.apuesta = 0

    def mostrar_mano(self):
        """Muestra la mano del jugador y su valor actual."""
        print(f"{self.nombre} hand: {self.mano} (Value: {self.calcular_valor_mano()})")