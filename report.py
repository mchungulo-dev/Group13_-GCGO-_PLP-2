"""
╔══════════════════════════════════════════════════════════════╗
║   GreenFinger Inventory Manager  v1.0                        ║
║   MEMBER 5 — Report & Low-Stock Alerts (Features 3 & 4)      ║
║   Responsible for: Formatted inventory table + alert panel   ║
╚══════════════════════════════════════════════════════════════╝

YOUR JOB:
  - Write display_report_function() which queries the database
    and renders:
      1. A formatted inventory table with VARIETY, CATEGORY,
         STOCK (g), LAST UPDATED, and a 🟢/🔴 STATUS column
      2. A TOTALS row at the bottom of the table
      3. A 🔴 LOW STOCK ALERT panel listing every variety
         below the threshold and how many grams are needed
      4. A RECENT DISTRIBUTIONS log showing the last 20
         hand-outs (variety, recipient, qty, date)

HOW TO TEST YOUR PART ALONE:
  1. python member1_database.py   (set up DB)
  2. python member3_log_seeds.py  (add stock)
  3. python member4_distribute.py (record some distributions)
  4. python member5_report.py     (view the report)
"""

from datetime import datetime

# Import shared dependencies from other members
from database import database_handler, LOW_STOCK_THRESHOLD


# ══════════════════════════════════════════════
#  DISPLAY REPORT FUNCTION  —  Features 3 & 4
#  Queries both tables and renders a complete, formatted report.
# ══════════════════════════════════════════════
def display_report_function():
    """Query the database and display a formatted inventory report."""

    # ── Report Header ─────────────────────────────────────────
    print("\n  ╔══ 📋 INVENTORY REPORT ══════════════════════════════════╗")
    print(f"  ║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<47}║")
    print("  ╚═════════════════════════════════════════════════════════╝\n")

    inventory = database_handler("get_inventory")

    if not inventory:
        print("  ℹ  No seed records found. Start by logging a batch (Option 1).\n")
        return

    # ── Feature 3: Inventory Table ────────────────────────────
    header  = f"  {'VARIETY':<22} {'CATEGORY':<14} {'STOCK (g)':>12}  {'LAST UPDATED':<14}  STATUS"
    divider = "  " + "─" * 75
    print(header)
    print(divider)

    low_stock_varieties = []   # collect for the alert panel below
    total_g = 0.0

    for variety, category, qty, date_added in inventory:
        status = "🔴 LOW STOCK" if qty < LOW_STOCK_THRESHOLD else "🟢 OK"
        print(f"  {variety:<22} {category:<14} {qty:>12,.0f}  {date_added:<14}  {status}")
        if qty < LOW_STOCK_THRESHOLD:
            low_stock_varieties.append((variety, qty))
        total_g += qty

    print(divider)
    print(f"  {'TOTAL STOCK':<22} {'':<14} {total_g:>12,.0f} g\n")

    # ── Feature 4: Low-Stock Alert Panel ─────────────────────
    if low_stock_varieties:
        print(f"  ┌─ 🔴 LOW STOCK ALERT "
              f"(below {LOW_STOCK_THRESHOLD} g) ─────────────────────┐")
        for v, q in low_stock_varieties:
            needed = LOW_STOCK_THRESHOLD - q
            print(f"  │  ⚠  {v:<20} only {q:>7,.0f} g left  "
                  f"(need {needed:,.0f} g more)  │")
        print("  └──────────────────────────────────────────────────────────┘\n")

    # ── Recent Distributions Log ──────────────────────────────
    logs = database_handler("get_logs")
    if logs:
        print("  ┌─ 📤 RECENT DISTRIBUTIONS (last 20) ─────────────────────┐")
        print(f"  │  {'VARIETY':<20} {'RECIPIENT':<18} {'QTY (g)':>9}  {'DATE':<12}  │")
        print("  │  " + "─" * 64 + "│")
        for seed_v, recip, qty, dist_date in logs:
            print(f"  │  {seed_v:<20} {recip:<18} {qty:>9,.0f}  {dist_date:<12}  │")
        print("  └──────────────────────────────────────────────────────────┘")

    print()


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    database_handler("setup")
    display_report_function()

