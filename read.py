PRODUCT_FILE = "products.txt"
INVOICE_FOLDER = "invoices"

try:
    with open(INVOICE_FOLDER, 'r'):
        pass
except FileNotFoundError:
    try:
        with open(INVOICE_FOLDER, 'w'):
            pass
    except Exception as e:
        print(f"Error: Could not create invoice directory - {str(e)}")
except Exception as e:
    print(f"Unexpected error while checking invoice directory: {str(e)}")

# Read products from file
def read_products():
    """
    This function reads product data from the products file and returns a list of product dictionaries.
    It doesnot have any arguments
    It returns the list of dictionaries containing product details
    """
    try:
        products = []
        with open(PRODUCT_FILE, 'r') as file:
            for line in file:
                try:
                    name, brand, qty, cost, origin = line.strip().split(',')
                    quantity = int(qty)
                    cost_price = float(cost)
                    if quantity < 0:
                        raise ValueError(f"Negative quantity in file for product {name}")
                    if cost_price <= 0:
                        raise ValueError(f"Non-positive cost price in file for product {name}")
                    products.append({
                        'name': name,
                        'brand': brand,
                        'quantity': quantity,
                        'cost_price': cost_price,
                        'origin': origin
                    })
                except ValueError as ve:
                    print(f"Error parsing line '{line.strip()}': {str(ve)}")
                    continue
        return products
    except FileNotFoundError:
        print(f"Error: Product file '{PRODUCT_FILE}' not found.")
        return []
    except Exception as e:
        print(f"Unexpected error reading product file: {str(e)}")
        return []