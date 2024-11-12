import json
import datetime

# Files to store data
DATA_FILE = 'inventory_data.json'
LOG_FILE = 'transaction_log.json'

# Initial Inventory Data with 5 products
initial_inventory = {
    "1": {"name": "Apple", "price": 0.5, "quantity": 100},
    "2": {"name": "Banana", "price": 0.3, "quantity": 150},
    "3": {"name": "Orange", "price": 0.7, "quantity": 120},
    "4": {"name": "Milk", "price": 1.2, "quantity": 50},
    "5": {"name": "Bread", "price": 1.0, "quantity": 40}
}

# Load data from file or initialize with default data
def load_data(file, default_data):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_data

# Save data to file
def save_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Display the main menu
def display_menu():
    print("\nInventory Management System")
    print("1. Product Management")
    print("2. Inventory Operations")
    print("3. View Transaction Log")
    print("4. Exit")

# Product management functions: add, view, update, delete
def product_management(inventory):
    while True:
        print("\nProduct Management")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_product(inventory)
        elif choice == "2":
            view_products(inventory)
        elif choice == "3":
            update_product(inventory)
        elif choice == "4":
            delete_product(inventory)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

# Add a new product
def add_product(inventory):
    if len(inventory) >= 5:
        print("Limit reached. Only 5 products allowed.")
        return
    
    product_id = input("Enter product ID: ")
    if product_id in inventory:
        print("Product already exists.")
        return
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter initial quantity: "))
    
    inventory[product_id] = {"name": name, "price": price, "quantity": quantity}
    print(f"Product '{name}' added.")

# View all products
def view_products(inventory):
    print("\nCurrent Products:")
    for pid, details in inventory.items():
        print(f"ID: {pid}, Name: {details['name']}, Price: {details['price']}, Quantity: {details['quantity']}")

# Update product details
def update_product(inventory):
    product_id = input("Enter product ID to update: ")
    if product_id not in inventory:
        print("Product not found.")
        return
    
    name = input("Enter new name (leave blank to keep current): ")
    price = input("Enter new price (leave blank to keep current): ")
    quantity = input("Enter new quantity (leave blank to keep current): ")
    
    if name:
        inventory[product_id]['name'] = name
    if price:
        inventory[product_id]['price'] = float(price)
    if quantity:
        inventory[product_id]['quantity'] = int(quantity)
    
    print("Product updated.")

# Delete a product
def delete_product(inventory):
    product_id = input("Enter product ID to delete: ")
    if product_id in inventory:
        del inventory[product_id]
        print("Product deleted.")
    else:
        print("Product not found.")

# Inventory operations: add stock, remove stock, view stock levels
def inventory_operations(inventory, log):
    while True:
        print("\nInventory Operations")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Stock Levels")
        print("4. Back to Main Menu")
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_stock(inventory, log)
        elif choice == "2":
            remove_stock(inventory, log)
        elif choice == "3":
            view_stock_levels(inventory)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

# Add stock to an existing product
def add_stock(inventory, log):
    product_id = input("Enter product ID: ")
    if product_id not in inventory:
        print("Product not found.")
        return
    
    quantity = int(input("Enter quantity to add: "))
    inventory[product_id]['quantity'] += quantity
    log_transaction(log, product_id, quantity, "Add")
    print("Stock added.")

# Remove stock from an existing product
def remove_stock(inventory, log):
    product_id = input("Enter product ID: ")
    if product_id not in inventory:
        print("Product not found.")
        return
    
    quantity = int(input("Enter quantity to remove: "))
    if quantity > inventory[product_id]['quantity']:
        print("Not enough stock available.")
    else:
        inventory[product_id]['quantity'] -= quantity
        log_transaction(log, product_id, quantity, "Remove")
        print("Stock removed.")

# View stock levels of all products
def view_stock_levels(inventory):
    print("\nCurrent Stock Levels:")
    for pid, details in inventory.items():
        print(f"ID: {pid}, Name: {details['name']}, Quantity: {details['quantity']}")

# Log each transaction
def log_transaction(log, product_id, quantity, operation):
    entry = {
        "date": str(datetime.datetime.now()),
        "product_id": product_id,
        "quantity": quantity,
        "operation": operation
    }
    log.append(entry)

# View the transaction log
def view_transaction_log(log):
    print("\nTransaction Log:")
    for entry in log:
        print(f"{entry['date']} - {entry['operation']} {entry['quantity']} of product ID {entry['product_id']}")

# Main program function
def main():
    inventory = load_data(DATA_FILE, initial_inventory)
    log = load_data(LOG_FILE, [])

    while True:
        display_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            product_management(inventory)
        elif choice == "2":
            inventory_operations(inventory, log)
        elif choice == "3":
            view_transaction_log(log)
        elif choice == "4":
            save_data(inventory, DATA_FILE)
            save_data(log, LOG_FILE)
            print("Data saved. Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
