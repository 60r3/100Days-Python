from config import COINS

class Wallet:
    def __init__(self):
        """Initializes the coin hoppers with values from config.py."""
        self.coins = {coin: data['quantity'] for coin, data in COINS.items()}
        self.last_inserted_coins = {}

    
    def insert_coins(self):
        """Allows the user to insert coins and temporarily stores them."""
        print("Insert coins:")
        print("(To cancel the transaction, enter: 0000)")
        total_inserted = 0
        inserted_coins = {coin: 0 for coin in self.coins}
        
        for coin, data in COINS.items():
            while True:
                user_input = input(f"How many {coin}s would you like to insert? ")
                if user_input == "0000":
                    self.refund(inserted_coins)
                    return 0, {}
                try:
                    quantity = int(user_input)
                    if quantity >= 0:
                        break
                    else:
                        print("Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number or '0000' to cancel.")
            
            total_inserted += quantity * data['value']
            inserted_coins[coin] += quantity
        
        self.last_inserted_coins = inserted_coins.copy()

        return total_inserted, inserted_coins
    
    def verify_payment(self, total_inserted, price):
        """Checks if the inserted money is sufficient."""
        if total_inserted < price * 100:
            print("Insufficient funds. Please insert more coins or enter '0000' to cancel.")
            return False
        return True
    
    def calculate_change(self, total_inserted, price):
        """Calculates and returns change using the fewest number of coins possible."""
        change = total_inserted - int(price * 100)
        change_to_give = {}
        
        for coin, data in sorted(COINS.items(), key=lambda x: -x[1]['value']):
            while change >= data['value'] and self.coins[coin] > 0:
                if coin not in change_to_give:
                    change_to_give[coin] = 0
                change_to_give[coin] += 1
                self.coins[coin] -= 1
                change -= data['value']
        
        if change == 0:
            return change_to_give
        else:
            print("Not enough change in the machine. Please insert the exact amount.")
            return {}
    
    def update_hoppers(self, inserted_coins, change_to_give):
        """Adds inserted coins and deducts coins given as change."""
        for coin, quantity in inserted_coins.items():
            self.coins[coin] += quantity
        
        if change_to_give:
            for coin, quantity in change_to_give.items():
                self.coins[coin] -= quantity
    
    def check_hoppers(self):
        """Checks if any hopper has fewer than 5 coins and issues an alert."""
        for coin, quantity in self.coins.items():
            if quantity < 5:
                print(f"⚠️ Warning: Low level of {coin}s ({quantity} remaining). Please reload soon.")
    
    def reload_coins(self):
        """Allows the operator in maintenance mode to reload the coin hoppers."""
        for coin in self.coins:
            quantity = int(input(f"Enter the amount of {coin}s to reload: "))
            self.coins[coin] += quantity
        print("Coin hoppers successfully reloaded.")
    
    def refund(self, inserted_coins):
        """Refunds the user by returning the inserted coins."""
        print("Transaction canceled. Refunding:")
        for coin, quantity in inserted_coins.items():
            if quantity > 0:
                print(f"{quantity} {coin}(s)")
    
    def show_status(self):
        """Displays the current number of coins in each hopper."""
        print("Current status of coin hoppers:")
        for coin, quantity in self.coins.items():
            print(f"{coin}: {quantity} available")
