WeCare Store Management System

A Python-based command-line Store Management System designed to manage product inventory, sales, and restocking operations.
This project demonstrates modular programming, file handling, and inventory management concepts using Python.

The system allows store managers to:

View available products
Sell products with invoice generation
Restock inventory
Add new products to the system

All product information is stored in a text file and invoices are automatically generated for transactions.

Project Features
1. Display Products

Shows all available products in a tabular format including:

Product Name
Brand
Quantity
Selling Price
Origin

The selling price is automatically calculated from the cost price.

2. Sell Products

Allows the user to:

Select products to sell
Enter the quantity
Automatically update inventory
Generate a sales invoice

The invoice is saved in the invoices folder.

3. Restock Products

Store managers can:

Add new stock to existing products
Update the quantity
Generate a restocking invoice

4. Add New Products

New products can be added by entering:

Product Name
Brand
Cost Price
Quantity
Origin

The product is then saved to the inventory file.

Project Structure
WeCare Store Management System
│
├── main.py                # Main program with menu interface
├── operation.py           # Core operations (sell, restock, display, add product)
├── read.py                # Reads product data from file
├── write.py               # Writes updated data and generates invoices
├── products.txt           # Product database
│
├── invoices               # Generated invoices are stored here
└── README.md              # Project documentation

How the System Works

1. The program starts from main.py.
2. A menu is displayed to the user.
3. The user selects an operation.
4. The program calls the appropriate function from operation.py.
5. Product data is read from products.txt.
6. After any transaction, the updated data is written back to the file.

Technologies Used

Python
File Handling
Modular Programming
Command Line Interface (CLI)

Invoice System

The system automatically generates invoices for:

Product Sales
Product Restocking
Adding New Products

Invoices are saved inside the invoices folder with timestamps.

Learning Objectives

This project demonstrates:

Modular Python programming
File handling operations
Inventory management logic
Exception handling
Basic CLI application design

Author

Dhawa Tamu Gurung

License 

This project is created for "educational purposes".