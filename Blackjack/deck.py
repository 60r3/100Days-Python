import random, sys, time, os
from collections import deque

class Mazo:
    
    def __init__(self):
        """Inicializa un mazo con 8 barajas y las mezcla antes de empezar."""
        self.valores_cartas = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.cartas = deque(self.valores_cartas * 4 * 8)  
        self.cartas_usadas = []  
        self._barajado_inicial()

    def _barajado_inicial(self):
        """Baraja el mazo al inicio del juego."""
        cartas_lista = list(self.cartas)
        random.shuffle(cartas_lista)
        self.cartas = deque(cartas_lista)


    def mezclar(self):
        """Mezcla el mazo solo cuando no quedan cartas, usando los descartes."""
        if not self.cartas:  # Se baraja cuando ya no hay cartas en el mazo
            print("\n🔄 No more cards left, shuffling...\n")
            self.cartas = deque(self.cartas_usadas)  # Convertir descartes en el nuevo mazo
            self.cartas_usadas = []  # Vaciar los descartes

            # Barajar antes de repartir
            cartas_lista = list(self.cartas)
            random.shuffle(cartas_lista)
            self.cartas = deque(cartas_lista)

    def sacar_carta(self):
        """Saca una carta del mazo. Si se agotan, baraja con las descartadas."""
        if not self.cartas:
            self.mezclar()  # Solo se baraja si ya no quedan cartas disponibles
        
        return self.cartas.popleft() if self.cartas else None  # Evitar error si no quedan cartas

    def descartar_cartas(self, cartas):
        """Añade cartas al montón de descartes (se ejecuta al final de la ronda)."""
        self.cartas_usadas.extend(cartas)

    def contar_cartas_restantes(self):
        """Muestra cuántas cartas quedan en el mazo y en los descartes."""
        print(f"🃏 Cards left: {len(self.cartas)} | 🗑 Discarded cards: {len(self.cartas_usadas)}")
