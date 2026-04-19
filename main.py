from operation import display_products, sell_products, restock_products, add_new_product

def main():
    """
    This function  runs the main menu loop foe WeCare Skin Management System
    It doesnot have any arguments
    It doesnot return any value
    """
    while True:
        try:
            print("\n--- WeCare Store Management ---")
            print("1. Display Products")
            print("2. Sell Product")
            print("3. Restock Product")
            print("4. Add New Product")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()
            choice_num = int(choice)
            
            if choice_num == 1:
                display_products()
            elif choice_num == 2:
                sell_products()
            elif choice_num == 3:
                restock_products()
            elif choice_num == 4:
                add_new_product()
            elif choice_num == 5:
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Please enter a valid number.")
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()