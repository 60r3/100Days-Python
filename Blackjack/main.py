from deck import Mazo
from player import Jugador
from crupier import Crupier

### =============================== ###

# Funciones #

def turno_jugador(jugador, mazo):
    """Permite al jugador elegir su acción (Hit, Stand, Double Down, Split o Surrender cuando sea posible)."""
    primera_jugada = len(jugador.mano) == 2
    puede_dividir = primera_jugada and jugador.mano[0] == jugador.mano[1] and jugador.saldo >= jugador.apuesta
    puede_doblar = primera_jugada and jugador.saldo >= jugador.apuesta
    puede_rendirse = primera_jugada  # Solo en la primera jugada

    while True:
        opciones = ["h = Hit", "s = Stand"]
        if puede_doblar:
            opciones.append("d = Double Down")
        if puede_dividir:
            opciones.append("p = Split")
        if puede_rendirse:
            opciones.append("r = Surrender")

        opcion = input(f"\nWhat do you want to do? ({', '.join(opciones)}): ").strip().lower()

        if opcion == 'h':
            jugador.recibir_carta(mazo.sacar_carta())
            jugador.mostrar_mano()

            if jugador.calcular_valor_mano() > 21:
                print("You're over 21! You lose this round!")

                return False
            
        elif opcion == 's':
            print("You stand! Crupier's turn.")

            return True
        
        elif opcion == 'd' and puede_doblar:
            jugador.saldo -= jugador.apuesta
            jugador.apuesta *= 2

            print(f"Double Down! New bet: {jugador.apuesta}")

            jugador.recibir_carta(mazo.sacar_carta())
            jugador.mostrar_mano()

            if jugador.calcular_valor_mano() > 21:
                print("You're over 21! You lose this round!")

                return False
            
            print("You stand automatically after doubling down.")

            return True
        
        elif opcion == 'p' and puede_dividir:
            return "split"
        
        elif opcion == 'r' and puede_rendirse:
            print(f"{jugador.nombre} surrenders. Half the bet is returned.")

            jugador.saldo += jugador.apuesta // 2

            return False  # Fin de la ronda para el jugador
        
        else:
            print("Not a valid option. Please try again.")




def determinar_ganador(jugador, crupier, seguro=0):
    """Compara las manos del jugador y el crupier para decidir el ganador."""
    puntos_jugador = jugador.calcular_valor_mano()
    puntos_crupier = crupier.calcular_valor_mano()

    print(f"\nFinal result:\n")
    print(f"{jugador.nombre}: {puntos_jugador} points\n")
    print(f"Crupier: {puntos_crupier} points\n")

    # Crupier tiene Blackjack Natural
    if puntos_crupier == 21 and len(crupier.mano) == 2:
        if seguro > 0:
            print("Crupier has Blackjack! Your Insurance bet pays 2:1.")
            jugador.saldo += seguro * 2  # Seguro paga 2:1
        else:
            print("Crupier has Blackjack! You lose.")
        return

    # Jugador tiene Blackjack de mano.
    if puntos_jugador == 21 and len(jugador.mano) == 2:
        print("Winner winner, chicken dinner! You got a Blackjack!\n")
        jugador.saldo += int(jugador.apuesta * 2.5)  # Pago 3:2
        return

    if puntos_jugador > 21:
        print("You're over 21! You lose this round!\n")

    elif puntos_crupier > 21 or puntos_jugador > puntos_crupier:
        print("Congratulations! You win this round!\n")
        jugador.saldo += jugador.apuesta * 2

    elif puntos_jugador < puntos_crupier:
        print("The house wins. Better luck next time.\n")

    else:
        print("Push! Your bet is back to you.\n")
        jugador.saldo += jugador.apuesta



def preguntar_continuar():



    """Pregunta al jugador si quiere jugar otra ronda o salir del juego."""
    while True:
        opcion = input("\nDo you want to keep playing: Yes: y // No: n\n").strip().lower()
        if opcion == 'y':
            return True
        elif opcion == 'n':
            print("\nThanks for playing! See you next time!")
            return False
        else:
            print("Not a valid option. Please try again.")

def apostar(jugador):
    """Pregunta cuántas fichas quiere apostar (mínimo 25)."""
    while True:
        try:
            cantidad = int(input(f"\n{jugador.nombre}, enter your bet (min 25, max {jugador.saldo}): "))
            if 25 <= cantidad <= jugador.saldo:
                return cantidad
            else:
                print("Invalid bet. It must be at least 25 and within your available chips.")
        except ValueError:
            print("Please enter a valid number.")



### =============================== ###

# Lógica de juego.

# Pedir nombre y saldo inicial
nombre_jugador = input("Welcome! Please, enter your name: ").strip()
saldo_inicial = int(input("Enter your starting chips amount: "))

# Crear el mazo y el jugador antes del bucle
mazo = Mazo()
jugador = Jugador(nombre_jugador, saldo=saldo_inicial)

seguir_jugando = True

while seguir_jugando:
    crupier = Crupier()  # Nuevo crupier con mano vacía

    # Reiniciar manos antes de cada ronda
    jugador.resetear_mano()
    crupier.resetear_mano()

    # Mezclar el mazo solo si ya no quedan cartas
    mazo.mezclar()  

    # Mostrar cartas restantes antes de repartir
    mazo.contar_cartas_restantes()

    # Apostar
    cantidad_apuesta = apostar(jugador)
    jugador.apostar(cantidad_apuesta)


    # Repartir cartas
    jugador.recibir_carta(mazo.sacar_carta())
    jugador.recibir_carta(mazo.sacar_carta())

    crupier.recibir_carta(mazo.sacar_carta())  # Primera carta (oculta)
    crupier.recibir_carta(mazo.sacar_carta())  # Segunda carta (visible)

    # Mostrar manos
    jugador.mostrar_mano()
    print(f"Chips left: {jugador.saldo}")
    crupier.mostrar_mano(ocultar_primera=True)

    # Verificar si el crupier muestra un As para ofrecer Seguro
    if crupier.mano[0] == 11:  # El crupier muestra un As
        while True:
            opcion_seguro = input("\nCrupier shows an Ace. Do you want to buy Insurance? (y/n): ").strip().lower()
            if opcion_seguro == 'y' and jugador.saldo >= jugador.apuesta // 2:
                seguro = jugador.apuesta // 2
                jugador.saldo -= seguro
                print(f"Insurance placed: {seguro} chips.")
                break
            elif opcion_seguro == 'n':
                seguro = 0
                break
            else:
                print("Invalid option. Please enter 'y' or 'n'.")


    # Turno del jugador
    resultado = turno_jugador(jugador, mazo)

    # Si el jugador no se pasó de 21, turno del crupier
    if resultado:
        crupier.jugar_turno(mazo)
        crupier.mostrar_mano(ocultar_primera=False)
        determinar_ganador(jugador, crupier)

        # Descartar cartas jugadas
        mazo.descartar_cartas(jugador.mano + crupier.mano)
        mazo.contar_cartas_restantes()

    # Si el jugador tiene menos de 25 fichas, no puede seguir jugando
    if jugador.saldo < 25:
        print("\nYou're out of chips! The game is over.")
        break  # Sale del bucle y finaliza el juego

    # Preguntar si quiere jugar otra ronda
    seguir_jugando = preguntar_continuar()


print("\nGame finished. Your final balance is: ", jugador.saldo)