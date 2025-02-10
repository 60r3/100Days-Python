from inventario import INVENTORY
from monedero import Wallet
from utils import countdown

class Maintenance:
    def __init__(self, wallet: Wallet):
        """Initializes the maintenance system with access to inventory and wallet."""
        self.inventory = INVENTORY
        self.wallet = wallet
        self.machine_on = True
    
    def show_status(self):
        """Displays the current levels of ingredients and coins."""
        print("\nMachine Status:")
        print("Ingredients:")
        for item, amount in self.inventory.items():
            print(f"- {item}: {amount} remaining")
        
        print("\nCoin Hoppers:")
        self.wallet.show_status()
    
    def refill_ingredients(self):
        """Allows the operator to refill the ingredient reservoirs."""
        print("\nRefill Ingredients")
        for item in self.inventory:
            amount = int(input(f"Enter amount to add for {item}: "))
            self.inventory[item] += amount
        print("Ingredients successfully refilled.")
    
    def refill_coins(self):
        """Allows the operator to refill the coin hoppers."""
        print("\nRefill Coins")
        self.wallet.reload_coins()
    
    def turn_off(self):
        """Simulates turning off the machine."""
        print("Machine is now OFF.")
        self.machine_on = False
    
    def turn_on(self):
        """Simulates turning on the machine."""
        print("Machine is now ON.")
        self.machine_on = True
    
    def reset_machine(self):
        """Resets the machine with a 5-second countdown."""
        print("Resetting machine...")
        countdown(5)
        self.machine_on = True
        print("Machine reset successfully.")
    
    def maintenance_menu(self):
        """Provides an interface for maintenance operations."""
        while True:
            print("\nMaintenance Mode")
            print("1. Show machine status")
            print("2. Refill ingredients")
            print("3. Refill coins")
            print("4. Turn off machine")
            print("5. Turn on machine")
            print("6. Reset machine")
            print("7. Exit maintenance mode")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                self.show_status()
            elif choice == "2":
                self.refill_ingredients()
            elif choice == "3":
                self.refill_coins()
            elif choice == "4":
                self.turn_off()
            elif choice == "5":
                self.turn_on()
            elif choice == "6":
                self.reset_machine()
            elif choice == "7":
                print("Exiting maintenance mode.")
                break
            else:
                print("Invalid option, please try again.")
