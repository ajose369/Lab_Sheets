from coffee_shop.shop import CoffeeShop


shop =CoffeeShop()                                                      # How do we initialize an object here?

print("☕ Welcome to Our Coffee Shop! ☕")

shop.display_menu()                                         # Why am i not storing it in a variable here? - There is nothing to return
category = input("\nChoose a category: ").lower()

shop.display_category(category)

item = input("\nChoose an item: ").lower()
quantity = int(input("Enter quantity: "))

total = shop.order(category, item, quantity)

if total is not None:
    print("\n--------------------------")
    print(f"Item     : {item.title()}")
    print(f"Quantity : {quantity}")
    print(f"Total    : ₹{total}")
    print("Thank you for your order! 😊")
