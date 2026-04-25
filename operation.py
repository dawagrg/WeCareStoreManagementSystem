from read import read_products, INVOICE_FOLDER
from write import write_products, generate_invoice
from datetime import datetime

# Display products with selling price
def display_products():
    """
    Displays all products in a tabular format with their details.
    Arguments: None
    Return Value: List of product dictionaries or empty list if none available
    """
    try:
        products = read_products()
        if not products:
            print("No products available.")
            return products
        print("\nAvailable Products:")
        print("+-------------------------+---------------+--------+---------+-------------+")
        print("| Product Name            | Brand         | Qty    | Price   | Origin      |")
        print("+-------------------------+---------------+--------+---------+-------------+")
        for p in products:
            selling_price = p['cost_price'] * 3
            name = p['name'] + " " * (23 - len(p['name']))
            brand = p['brand'] + " " * (13 - len(p['brand']))
            qty = str(p['quantity']) + " " * (6 - len(str(p['quantity'])))
            price = str(int(selling_price)) + " " * (7 - len(str(int(selling_price))))
            origin = p['origin'] + " " * (11 - len(p['origin']))
            print("| " + name + " | " + brand + " | " + qty + " | " + price + " | " + origin + " |")
        print("+-------------------------+---------------+--------+---------+-------------+")
        return products
    except Exception as e:
        print("Error displaying products: " + str(e))
        return []

# Sell products
def sell_products():
    """
    Processes product sales, applies discounts, generates a sales invoice, and returns the invoice content.
    Arguments: None
    Return Value: String containing the sales invoice content or None if no sale is processed
    """
    try:
        products = read_products()
        if not products:
            print("No products available to sell.")
            return None

        customer = input("Enter customer name: ").strip()
        if not customer:
            raise ValueError("Customer name cannot be empty")

        selected_items = []
        subtotal = 0
        vat_rate = 0.13

        while True:
            display_products()
            name = input("Enter product name to buy (or 'done' to finish): ").strip()
            if name == 'done':
                break
            if not name:
                print("Error: Product name cannot be empty")
                continue

            try:
                quantity = int(input("Enter quantity to buy: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                print("Error: Quantity must be a valid positive integer")
                continue

            for p in products:
                if p['name'] == name:
                    free_items = quantity // 3
                    total_items = quantity + free_items

                    if p['quantity'] >= total_items:
                        p['quantity'] -= total_items
                        selling_price = p['cost_price'] * 3
                        amount = quantity * selling_price
                        selected_items.append((p['name'], p['brand'], quantity, free_items, selling_price, amount))
                        subtotal += amount
                        print(str(quantity) + " + " + str(free_items) + " free " + p['name'] + " added to invoice.")
                    else:
                        print("Insufficient stock!")
                    break
            else:
                print("Product not found.")

        if selected_items:
            vat_amount = subtotal * vat_rate
            total = subtotal + vat_amount
            now = datetime.now()
            filename = INVOICE_FOLDER + "/sale_" + customer + "_" + now.strftime('%Y%m%d_%H%M%S') + ".txt"
            content = "Customer Name: " + customer + "\n"
            content += "Date: " + now.strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
            content += "Items Sold:\n"
            content += "+-------------------------+---------------+--------+--------+---------+------------+\n"
            content += "| Product Name            | Brand         | Qty    | Free   | Price   | Amount     |\n"
            content += "+-------------------------+---------------+--------+--------+---------+------------+\n"
            for name, brand, qty, free, price, amt in selected_items:
                name_padded = name + " " * (23 - len(name))
                brand_padded = brand + " " * (13 - len(brand))
                qty_padded = str(qty) + " " * (6 - len(str(qty)))
                free_padded = str(free) + " " * (6 - len(str(free)))
                price_padded = str(int(price)) + " " * (7 - len(str(int(price))))
                amt_padded = str(int(amt)) + " " * (7 - len(str(int(amt))))
                content += "| " + name_padded + " | " + brand_padded + " | " + qty_padded + " | " + free_padded + " | " + price_padded + " | " + amt_padded + " |\n"
            content += "+-------------------------+---------------+--------+--------+---------+------------+\n"
            content += "\nSubtotal: Rs " + str(int(subtotal)) + "\n"
            content += "VAT (13%): Rs " + str(int(vat_amount)) + "\n"
            content += "Total Amount: Rs " + str(int(total)) + "\n"
            try:
                generate_invoice(filename, content)
                print("Invoice generated: " + filename)
                write_products(products)
                return content
            except FileNotFoundError:
                print("Error: Could not write invoice file due to file access issue")
                return content
            except Exception as e:
                print("Unexpected error generating invoice: " + str(e))
                return content
        else:
            return None

    except ValueError as ve:
        print("Error: Invalid input - " + str(ve))
        return None
    except Exception as e:
        print("Unexpected error: " + str(e))
        return None

# Restock products
def restock_products():
    """
    Restocks products, updates inventory, and generates a restock invoice.
    Arguments: None
    Return Value: None
    """
    try:
        products = read_products()
        vendor = input("Enter vendor/supplier name: ").strip()
        if not vendor:
            raise ValueError("Vendor name cannot be empty")

        now = datetime.now()
        filename = INVOICE_FOLDER + "/restock_" + vendor + "_" + now.strftime('%Y%m%d_%H%M%S') + ".txt"
        subtotal = 0
        vat_rate = 0.13
        new_items = []

        while True:
            name = input("Enter product name to restock (or 'done' to finish): ").strip()
            if name == 'done':
                break
            if not name:
                print("Error: Product name cannot be empty")
                continue

            brand = input("Enter brand: ").strip()
            if not brand:
                print("Error: Brand cannot be empty")
                continue

            try:
                quantity = int(input("Enter quantity to add: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                print("Error: Quantity must be a valid positive integer")
                continue

            try:
                cost_price = float(input("Enter cost price: "))
                if cost_price <= 0:
                    raise ValueError("Cost price must be positive")
            except ValueError:
                print("Error: Cost price must be a valid positive number")
                continue

            origin = input("Enter country of origin: ").strip()
            if not origin:
                print("Error: Country of origin cannot be empty")
                continue

            for p in products:
                if p['name'] == name and p['brand'] == brand:
                    p['quantity'] += quantity
                    p['cost_price'] = cost_price
                    break
            else:
                products.append({
                    'name': name,
                    'brand': brand,
                    'quantity': quantity,
                    'cost_price': cost_price,
                    'origin': origin
                })
            subtotal += quantity * cost_price
            new_items.append((name, brand, quantity, cost_price))

        if new_items:
            vat_amount = subtotal * vat_rate
            total = subtotal + vat_amount
            content = "Vendor Name: " + vendor + "\n"
            content += "Date: " + now.strftime('%Y-%m-%d %H:%M:%S') + "\n\n"   
            content += "Items Restocked:\n"
            content += "+-------------------------+---------------+--------+---------+---------+\n"
            content += "| Product Name            | Brand         | Qty    | Price   | Amount  |\n"
            content += "+-------------------------+---------------+--------+---------+---------+\n"
            for name, brand, qty, price in new_items:
                name_padded = name + " " * (23 - len(name))
                brand_padded = brand + " " * (13 - len(brand))
                qty_padded = str(qty) + " " * (6 - len(str(qty)))
                price_padded = str(int(price)) + " " * (7 - len(str(int(price))))
                amount_padded = str(int(qty * price)) + " " * (7 - len(str(int(qty * price))))
                content += "| " + name_padded + " | " + brand_padded + " | " + qty_padded + " | " + price_padded + " | " + amount_padded + " |\n"
            content += "+-------------------------+---------------+--------+---------+---------+\n"
            content += "\nSubtotal: Rs " + str(int(subtotal)) + "\n"
            content += "VAT (13%): Rs " + str(int(vat_amount)) + "\n"
            content += "Total Amount: Rs " + str(int(total)) + "\n"
            try:
                generate_invoice(filename, content)
                print("Restock invoice generated: " + filename)
                write_products(products)
            except FileNotFoundError:
                print("Error: Could not write invoice file due to file access issue")
            except Exception as e:
                print("Unexpected error generating invoice: " + str(e))

    except ValueError as ve:
        print("Error: Invalid input - " + str(ve))
    except Exception as e:
        print("Unexpected error: " + str(e))

# Add a new product
def add_new_product():
    """
    Adds a new product to the inventory and generates an invoice.
    Arguments: None
    Return Value: None
    """
    try:
        products = read_products()

        print("\n--- Add New Product ---")
        name = input("Enter product name: ").strip()
        if not name:
            raise ValueError("Product name cannot be empty")

        brand = input("Enter brand: ").strip()
        if not brand:
            raise ValueError("Brand cannot be empty")

        try:
            quantity = int(input("Enter quantity: "))
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except ValueError as e:
            if str(e) == "Quantity cannot be negative":
                raise
            raise ValueError("Quantity must be a valid integer")

        try:
            cost_price = float(input("Enter cost price: "))
            if cost_price <= 0:
                raise ValueError("Cost price must be positive")
        except ValueError as e:
            if str(e) == "Cost price must be positive":
                raise
            raise ValueError("Cost price must be a valid number")

        origin = input("Enter country of origin: ").strip()
        if not origin:
            raise ValueError("Country of origin cannot be empty")

        # Check if product already exists
        for p in products:
            if p['name'] == name and p['brand'] == brand:
                print("This product already exists. Please restock it instead.")
                return

        # Add the new product
        new_product = {
            'name': name,
            'brand': brand,
            'quantity': quantity,
            'cost_price': cost_price,
            'origin': origin
        }
        products.append(new_product)

        # Generate invoice for the new product
        vendor = input("Enter vendor/supplier name for this product: ").strip()
        if not vendor:
            raise ValueError("Vendor name cannot be empty")

        now = datetime.now()
        filename = INVOICE_FOLDER + "/new_product_" + vendor + "_" + now.strftime('%Y%m%d_%H%M%S') + ".txt"
        subtotal = quantity * cost_price
        vat_rate = 0.13  # 13% VAT
        vat_amount = subtotal * vat_rate
        total = subtotal + vat_amount
        content = "Vendor Name: " + vendor + "\n"
        content += "Date: " + now.strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
        content += "New Product Added:\n"
        content += "+-------------------------+---------------+--------+---------+---------+\n"
        content += "| Product Name            | Brand         | Qty    | Price   | Amount  |\n"
        content += "+-------------------------+---------------+--------+---------+---------+\n"
        name_padded = name + " " * (23 - len(name))
        brand_padded = brand + " " * (13 - len(brand))
        qty_padded = str(quantity) + " " * (6 - len(str(quantity)))
        price_padded = str(int(cost_price)) + " " * (7 - len(str(int(cost_price))))
        subtotal_padded = str(int(subtotal)) + " " * (7 - len(str(int(subtotal))))
        content += "| " + name_padded + " | " + brand_padded + " | " + qty_padded + " | " + price_padded + " | " + subtotal_padded + " |\n"
        content += "+-------------------------+---------------+--------+---------+---------+\n"
        content += "\nSubtotal: Rs " + str(int(subtotal)) + "\n"
        content += "VAT (13%): Rs " + str(int(vat_amount)) + "\n"
        content += "Total Amount: Rs " + str(int(total)) + "\n"

        