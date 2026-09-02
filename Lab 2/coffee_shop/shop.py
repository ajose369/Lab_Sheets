from .menu import MENU


class CoffeeShop:

    def __init__(self):
        self.menu = MENU

    def display_menu(self):
        print("\n========== MENU ==========")
        print("1. Coffee")
        print("2. Juices")
        print("3. Starters")
        print("4. Soups")

    def display_category(self, category):

        if category == "coffee":
            print("\n--- COFFEE ---")

            for item, price in self.menu["coffee"].items():
                print(f"{item.title()} - ₹{price}")

        elif category == "juices":
            print("\n--- JUICES ---")

            for item, price in self.menu["juices"].items():
                print(f"{item.title()} - ₹{price}")

        elif category == "starters":
            print("\n--- STARTERS ---")

            for item, price in self.menu["starters"].items():
                print(f"{item.title()} - ₹{price}")

        elif category == "soups":
            print("\n--- SOUPS ---")

            for item, price in self.menu["soups"].items():
                print(f"{item.title()} - ₹{price}")

        else:
            print("Invalid category!")

    def order(self, category, item, quantity):

        if category in self.menu:

            if item in self.menu[category]:
                price = self.menu[category][item]
                return price * quantity

            else:
                print("Item not available!")

        else:
            print("Category not available!")

        return None