"""
╔══════════════════════════════════════════════════════════════╗
║   GreenFinger Inventory Manager  v1.0                        ║
║   MEMBER 3 — Log Seeds Function (Feature 1: Stock Intake)    ║
║   Responsible for: Capturing & validating new seed batches   ║
╚══════════════════════════════════════════════════════════════╝

YOUR JOB:
  - Write log_seeds_function() which prompts the manager to
    enter a seed variety, category, and quantity
  - Validate ALL three inputs in while-True loops before saving
  - Call database_handler("log_seed", ...) to persist the data
  - Print a clear success or error message

VALIDATION RULES:
  • Variety   → must not be empty; auto title-cased
  • Category  → must be a valid number from the printed list
  • Quantity  → must be a positive number (floats allowed)

HOW TO TEST YOUR PART ALONE:
  First run Member 1 to set up the DB:  python member1_database.py
  Then run:  python member3_log_seeds.py
  Try entering bad values to confirm validation works.
"""

from datetime import date

# Import shared dependencies from other members
from database import database_handler, CATEGORIES


# ══════════════════════════════════════════════
#  LOG SEEDS FUNCTION  —  Feature 1: Stock Intake
#  Prompts the user for seed details, validates each input,
#  then saves the batch to the database via database_handler.
# ══════════════════════════════════════════════
def log_seeds_function():
    """Interactive session to log a new seed batch into the database."""

    today_str = date.today().strftime("%Y-%m-%d")
    print(f"\n  ╔══ 📥 STOCK INTAKE SESSION: {today_str} ══╗")

    # ── Step 1: Seed Variety ──────────────────────────────────
    # Keep asking until the user provides a non-empty name
    while True:
        variety = input("\n  >>> Enter Seed Variety (e.g., Maize): ").strip().title()
        if variety:
            break
        print("  ⚠  Variety name cannot be empty. Please try again.")

    # ── Step 2: Category ──────────────────────────────────────
    # Display the numbered list and validate the selection
    print("\n  Available Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")

    while True:
        cat_input = input("\n  >>> Select Category Number: ").strip()
        if cat_input.isdigit() and 1 <= int(cat_input) <= len(CATEGORIES):
            category = CATEGORIES[int(cat_input) - 1]
            break
        print(f"  ⚠  Please enter a number between 1 and {len(CATEGORIES)}.")

    # ── Step 3: Quantity in Grams ─────────────────────────────
    # Must be a positive number; float() lets users enter decimals
    while True:
        qty_input = input("\n  >>> Enter Quantity in Grams (e.g., 2500): ").strip()
        try:
            quantity = float(qty_input)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            break
        except ValueError:
            print("  ⚠  Quantity must be a positive number. Please try again.")

    # ── Step 4: Save to Database ──────────────────────────────
    result = database_handler("log_seed", (variety, category, quantity, today_str))

    if result:
        print(f"\n  ✅  SUCCESS — {quantity:,.0f} g of '{variety}' ({category}) "
              f"logged on {today_str}.")
    else:
        print("\n  ❌  ERROR — Could not save record. Please try again.")


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    from database import database_handler
    database_handler("setup")   # ensure tables exist
    log_seeds_function()

