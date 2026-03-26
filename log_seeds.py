from datetime import date
from database import database_handler, CATEGORIES


def log_seeds_function():
    """Interactive session to log a new seed batch into the database."""

    today_str = date.today().strftime("%Y-%m-%d")
    print(f"\nSTOCK INTAKE SESSION: {today_str}")

    # Keep asking until the user provides a non-empty name
    while True:
        variety = input("\n  >>> Enter Seed Variety (e.g., Maize): ").strip().title()
        if variety:
            break
        print("Variety name cannot be empty. Please try again.")

    # Display the numbered list and validate the selection
    print("\n Available Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")

    while True:
        cat_input = input("\n  >>> Select Category Number: ").strip()
        if cat_input.isdigit() and 1 <= int(cat_input) <= len(CATEGORIES):
            category = CATEGORIES[int(cat_input) - 1]
            break
        print(f"Please enter a number between 1 and {len(CATEGORIES)}.")

    while True:
        qty_input = input("\n  >>> Enter Quantity in Grams (e.g., 2500): ").strip()
        try:
            quantity = float(qty_input)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            break
        except ValueError:
            print("Quantity must be a positive number. Please try again.")

    result = database_handler("log_seed", (variety, category, quantity, today_str))

    if result:
        print(f"\nSUCCESS — {quantity:,.0f} g of '{variety}' ({category}) "
              f"logged on {today_str}.")
    else:
        print("\nERROR — Could not save record. Please try again.")


if __name__ == "__main__":
    from database import database_handler
    database_handler("setup") 
    log_seeds_function()

