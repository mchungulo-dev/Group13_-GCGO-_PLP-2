from datetime import date
from database import database_handler, LOW_STOCK_THRESHOLD


def distribute_seeds_function():
    """Interactive session to record seed distribution to a community member."""

    today_str = date.today().strftime("%Y-%m-%d")
    print(f"\nDISTRIBUTION SESSION: {today_str}")

    varieties = database_handler("get_varieties")
    if not varieties:
        print("\n No seeds in stock yet. Log a batch first (Option 1).")
        return

    print("\n  Current Stock:")
    for i, (v, q) in enumerate(varieties, 1):
        flag = "LOW" if q < LOW_STOCK_THRESHOLD else ""
        print(f"{i}. {v:<25} {q:>10,.0f} g{flag}")

    while True:
        sel = input("\n  >>> Select Variety Number: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(varieties):
            variety, available = varieties[int(sel) - 1]
            break
        print(f"Enter a number between 1 and {len(varieties)}.")

    while True:
        recipient = input("\n  >>> Enter Recipient Name: ").strip().title()
        if recipient:
            break
        print("Recipient name cannot be empty.")

    while True:
        qty_input = input(
            f"\n  >>> Enter Quantity in Grams "
            f"(Available: {available:,.0f} g): "
        ).strip()
        try:
            quantity = float(qty_input)
            if quantity <= 0:
                raise ValueError("Non-positive quantity.")
            if quantity > available:
                print(f"Insufficient stock. Only {available:,.0f} g available.")
                continue   # ask again without breaking the loop
            break
        except ValueError:
            print("Quantity must be a positive number.")

    # Save to Database
    result = database_handler("distribute",
                              (variety, recipient, quantity, today_str))

    if result:
        remaining = available - quantity
        print(f"\nSUCCESS — {quantity:,.0f} g of '{variety}' distributed to "
              f"{recipient}.")
        print(f"Remaining stock: {remaining:,.0f} g")

        # warn if stock is now critically low
        if remaining < LOW_STOCK_THRESHOLD:
            print(f"WARNING: '{variety}' is now below the "
                  f"{LOW_STOCK_THRESHOLD} g threshold. Consider re-stocking.")
    else:
        print("\nERROR — Distribution could not be recorded.")



if __name__ == "__main__":
    database_handler("setup")
    distribute_seeds_function()

