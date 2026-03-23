"""
╔══════════════════════════════════════════════════════════════╗
║   GreenFinger Inventory Manager  v1.0                        ║
║   MEMBER 4 — Distribute Seeds (Feature 2: Distribution)      ║
║   Responsible for: Recording seed hand-outs to members       ║
╚══════════════════════════════════════════════════════════════╝

YOUR JOB:
  - Write distribute_seeds_function() which lets the manager
    select a seed variety from a live numbered list, enter a
    recipient's name, and specify how many grams to give out
  - Ensure the quantity NEVER exceeds available stock
  - Save the transaction via database_handler("distribute", ...)
  - Show remaining stock after the distribution
  - Trigger a 🔴 low-stock warning if stock drops below threshold

VALIDATION RULES:
  • Variety    → must be a valid number from the displayed list
  • Recipient  → must not be empty; auto title-cased
  • Quantity   → positive number AND must be ≤ available stock

HOW TO TEST YOUR PART ALONE:
  1. python member1_database.py   (set up DB)
  2. python member3_log_seeds.py  (add some seed stock first)
  3. python member4_distribute.py (then test distribution)
"""

from datetime import date

# Import shared dependencies from other members
from database import database_handler, LOW_STOCK_THRESHOLD


# ══════════════════════════════════════════════
#  DISTRIBUTE SEEDS FUNCTION  —  Feature 2: Distribution Tracker
#  Shows live stock, captures recipient + quantity,
#  validates the request, then saves the transaction.
# ══════════════════════════════════════════════
def distribute_seeds_function():
    """Interactive session to record seed distribution to a community member."""

    today_str = date.today().strftime("%Y-%m-%d")
    print(f"\n  ╔══ 🚜 DISTRIBUTION SESSION: {today_str} ══╗")

    # ── Step 1: Fetch and display available varieties ─────────
    varieties = database_handler("get_varieties")
    if not varieties:
        print("\n  ⚠  No seeds in stock yet. Log a batch first (Option 1).")
        return

    print("\n  Current Stock:")
    for i, (v, q) in enumerate(varieties, 1):
        flag = " 🔴 LOW" if q < LOW_STOCK_THRESHOLD else ""
        print(f"    {i}. {v:<25} {q:>10,.0f} g{flag}")

    # ── Step 2: Select Variety ────────────────────────────────
    while True:
        sel = input("\n  >>> Select Variety Number: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(varieties):
            variety, available = varieties[int(sel) - 1]
            break
        print(f"  ⚠  Enter a number between 1 and {len(varieties)}.")

    # ── Step 3: Recipient Name ────────────────────────────────
    while True:
        recipient = input("\n  >>> Enter Recipient Name: ").strip().title()
        if recipient:
            break
        print("  ⚠  Recipient name cannot be empty.")

    # ── Step 4: Quantity with stock ceiling check ─────────────
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
                print(f"  ⚠  Insufficient stock. Only {available:,.0f} g available.")
                continue   # ask again without breaking the loop
            break
        except ValueError:
            print("  ⚠  Quantity must be a positive number.")

    # ── Step 5: Save to Database ──────────────────────────────
    result = database_handler("distribute",
                              (variety, recipient, quantity, today_str))

    if result:
        remaining = available - quantity
        print(f"\n  ✅  SUCCESS — {quantity:,.0f} g of '{variety}' distributed to "
              f"{recipient}.")
        print(f"  📊  Remaining stock: {remaining:,.0f} g")

        # Feature 4 hook: warn if stock is now critically low
        if remaining < LOW_STOCK_THRESHOLD:
            print(f"  🔴  WARNING: '{variety}' is now below the "
                  f"{LOW_STOCK_THRESHOLD} g threshold. Consider re-stocking.")
    else:
        print("\n  ❌  ERROR — Distribution could not be recorded.")


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    database_handler("setup")
    distribute_seeds_function()

