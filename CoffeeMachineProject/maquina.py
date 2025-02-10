from bebidas import BEVERAGES
from inventario import INVENTORY
from monedero import Wallet
from mantenimiento import Maintenance
from utils import countdown

class CoffeeMachine:
    def __init__(self):
        """Initializes the coffee machine with wallet and maintenance system."""
        self.wallet = Wallet()
        self.maintenance = Maintenance(self.wallet)
        self.inventory = INVENTORY
        self.running = True
    
    # def show_menu(self):
    #     """Displays available beverage options."""
    #     print("\nAvailable Beverages:")
    #     for name, details in BEVERAGES.items():
    #         status = "Available" if self.check_ingredients(name) else "Not available"
    #         print(f"- {name} (${details['price']:.2f}): {status}")

    def show_menu(self):
        """Displays available beverage options."""
        print("\nAvailable Beverages:")
        for index, (name, details) in enumerate(BEVERAGES.items(), start=1):
            status = "Available" if self.check_ingredients(name) else "Not available"
            print(f"{index}. {name.capitalize()} (${details['price']:.2f}): {status}")

    
    def check_ingredients(self, beverage):
        """Checks if there are enough ingredients for the selected beverage."""
        for ingredient, amount in BEVERAGES[beverage].items():
            if ingredient != "price" and self.inventory[ingredient] < amount:
                return False
        return True

    def ask_for_sugar(self):
        """Asks the user if they want sugar and how much."""
        while True:
            sugar_choice = input("Would you like sugar? (yes/no): ").strip().lower()
            if sugar_choice == "yes":
                try:
                    sugar_amount = int(input("How much sugar? (1-5): "))
                    if 1 <= sugar_amount <= 5:
                        if self.inventory["sugar"] >= sugar_amount:
                            self.inventory["sugar"] -= sugar_amount
                            print(f"Added {sugar_amount} grams of sugar.")
                        else:
                            print("Not enough sugar available.")
                        break
                    else:
                        print("Please enter a value between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif sugar_choice == "no":
                print("No sugar added.")
                break
            else:
                print("Please enter 'yes' or 'no'.")

    
    def process_payment(self, price):
        """Handles the payment process."""
        print(f"\nThe price of the beverage is ${price:.2f}")
        total_inserted, inserted_coins = self.wallet.insert_coins()
        
        if not self.wallet.verify_payment(total_inserted, price):
            return None
        
        change = self.wallet.calculate_change(total_inserted, price)
        if not isinstance(change, dict):
            return {}
        
        self.wallet.update_hoppers(inserted_coins, change)
        return change, inserted_coins
    
    def deduct_ingredients(self, beverage):
        """Deducts the required ingredients from the inventory."""
        for ingredient, amount in BEVERAGES[beverage].items():
            if ingredient != "price":
                self.inventory[ingredient] -= amount
    
    def prepare_beverage(self, beverage):
        """Simulates beverage preparation."""
        print(f"\nPreparing {beverage}...")
        countdown(10)
        print(f"Your {beverage} is ready! Enjoy! ☕")
    
    def start_machine(self):
        """Starts the coffee machine interaction."""
        while self.running:
            print("\nWelcome to the Coffee Machine!")
            self.show_menu()
            
            choice = input("\nSelect a beverage (enter the number): ").strip()

            # Verificar si es el código secreto de mantenimiento
            if choice == "9999":
                self.maintenance.maintenance_menu()
                continue

            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(BEVERAGES):
                print("Invalid selection. Please try again.")
                continue

            choice = list(BEVERAGES.keys())[int(choice) - 1]  

            if not self.check_ingredients(choice):
                print("Sorry, this beverage is currently unavailable due to ingredient shortages.")
                continue

            result = self.process_payment(BEVERAGES[choice]['price'])
            if result is None:
                print("Transaction canceled. Returning to main menu.")
                
                print("Refunding:")
                for coin, quantity in self.wallet.last_inserted_coins.items():
                    if quantity > 0:
                        print(f"{quantity} x {coin}(s)")
                
                continue

            change, inserted_coins = result  # Solo se desempaqueta si result no es None


            if change is None:
                print("Transaction canceled. Returning to main menu.")
                print("Refunding:")
                for coin, quantity in inserted_coins.items():
                    if quantity > 0:
                        print(f"{quantity} x {coin}(s)")
                continue

            
            self.deduct_ingredients(choice)
            self.ask_for_sugar()
            self.prepare_beverage(choice)

            
            if change:
                print("Change returned:")
                for coin, quantity in change.items():
                    print(f"{quantity} x {coin}(s)")
            
            print("\nThank you for using the Coffee Machine!\n")
