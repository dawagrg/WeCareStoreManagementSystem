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

