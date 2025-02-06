class Crupier:
    def __init__(self):
        """Inicializa al crupier con una mano vacía."""
        self.mano = []

    def recibir_carta(self, carta):
        """Añade una carta a la mano del crupier."""
        self.mano.append(carta)

    def calcular_valor_mano(self):
        """Calcula el valor total de la mano del crupier, ajustando los Ases."""
        total = sum(self.mano)
        ases = self.mano.count(11)  # Contar cuántos Ases hay

        # Ajustar Ases de 11 a 1 si el total supera 21
        while total > 21 and ases:
            total -= 10
            ases -= 1

        return total

    def jugar_turno(self, mazo):
        """El crupier sigue sacando cartas hasta alcanzar al menos 17."""
        while self.calcular_valor_mano() < 17:
            self.recibir_carta(mazo.cartas.popleft())  # Toma una carta del mazo

    def resetear_mano(self):
        """Vacía la mano del crupier para una nueva ronda."""
        self.mano = []

    def mostrar_mano(self, ocultar_primera=True):
        """Muestra la mano del crupier. Oculta la primera carta si aún es el turno del jugador."""
        if ocultar_primera:
            print(f"Crupier shows: [{self.mano[1]}, ?]")  # Muestra solo la segunda carta
        else:
            print(f"Crupier has: {self.mano} (Value: {self.calcular_valor_mano()})")
