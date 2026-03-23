from datetime import datetime
from database import database_handler, LOW_STOCK_THRESHOLD


def display_report_function():
    """
    Queries the database and renders two sections:
      1. Full inventory table — variety, category, stock, status
         (LOW STOCK or OK), and a totals row.
      2. Low-stock alert panel — lists varieties below threshold
         and shows exactly how many grams are still needed.
      3. Recent distributions log — last 20 transactions.
    """
    print("\nINVENTORY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<47}")
    print("\n")

    inventory = database_handler("get_inventory")

    if not inventory:
        print("No seed records found. Start by logging a batch (Option 1).\n")
        return

    # ── Inventory table ───────────────────────────────────────
    header  = f"  {'VARIETY':<22} {'CATEGORY':<14} {'STOCK (g)':>12}  {'LAST UPDATED':<14}  STATUS"
    divider = "  " + "─" * 75
    print(header)
    print(divider)

    low_stock_varieties = []
    total_g = 0.0

    for variety, category, qty, date_added in inventory:
        status = "LOW STOCK" if qty < LOW_STOCK_THRESHOLD else " OK"
        print(f"  {variety:<22} {category:<14} {qty:>12,.0f}  {date_added:<14}  {status}")
        if qty < LOW_STOCK_THRESHOLD:
            low_stock_varieties.append((variety, qty))
        total_g += qty

    print(divider)
    print(f"  {'TOTAL STOCK':<22} {'':<14} {total_g:>12,.0f} g")

    # Alert if low stock
    if low_stock_varieties:
        print(f"\nLOW STOCK ALERT (below {LOW_STOCK_THRESHOLD} g)")
        for v, q in low_stock_varieties:
            needed = LOW_STOCK_THRESHOLD - q
            print(f"{v:<20} only {q:>7,.0f} g left  "
                  f"(need {needed:,.0f} g more)")

    # ── Recent distributions log 
    logs = database_handler("get_logs")
    if logs:
        print("\nRECENT DISTRIBUTIONS (last 20) ")
        print(f"{'VARIETY':<20} {'RECIPIENT':<18} {'QTY (g)':>9}  {'DATE':<12}")
        print("─" * 64)
        for seed_v, recip, qty, dist_date in logs:
            print(f"{seed_v:<20} {recip:<18} {qty:>9,.0f}  {dist_date:<12}")

    print()


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    database_handler("setup")
    display_report_function()

