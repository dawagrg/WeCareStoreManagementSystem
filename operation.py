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

