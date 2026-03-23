# ================================================================
#  GREENFINGER INVENTORY MANAGER
#  Member 6 Responsibility: main.py
#  Task: Feature 3 & 4 — Inventory Report + Low-Stock Alerts
#        PLUS the main_function() that ties everything together.
#
#  This is the file you RUN to start the application:
#        python main.py
# ================================================================
#
#  DEPENDS ON:
#    member1_config.py              (constants)
#    member2_database_handler.py    (SQL gateway)
#    member3_intro_function.py      (welcome screen)
#    member4_log_seeds_function.py  (stock intake)
#    member5_distribute_seeds_function.py (distribution)
#
# ================================================================

from datetime import datetime
from database import LOW_STOCK_THRESHOLD
from database import database_handler
from intro import intro_function
from log_seeds import log_seeds_function
from distribute import distribute_seeds_function


# ── Feature 3 & 4: Inventory Report + Low-Stock Alerts ────────
def display_report_function():
    """
    Queries the database and renders two sections:
      1. Full inventory table — variety, category, stock, status
         (🔴 LOW STOCK or 🟢 OK), and a totals row.
      2. Low-stock alert panel — lists varieties below threshold
         and shows exactly how many grams are still needed.
      3. Recent distributions log — last 20 transactions.
    """
    print("\n  ╔══ 📋 INVENTORY REPORT ══════════════════════════════════╗")
    print(f"  ║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<47}║")
    print("  ╚═════════════════════════════════════════════════════════╝\n")

    inventory = database_handler("get_inventory")

    if not inventory:
        print("  ℹ  No seed records found. Start by logging a batch (Option 1).\n")
        return

    # ── Inventory table ───────────────────────────────────────
    header  = f"  {'VARIETY':<22} {'CATEGORY':<14} {'STOCK (g)':>12}  {'LAST UPDATED':<14}  STATUS"
    divider = "  " + "─" * 75
    print(header)
    print(divider)

    low_stock_varieties = []
    total_g = 0.0

    for variety, category, qty, date_added in inventory:
        status = "🔴 LOW STOCK" if qty < LOW_STOCK_THRESHOLD else "🟢 OK"
        print(f"  {variety:<22} {category:<14} {qty:>12,.0f}  {date_added:<14}  {status}")
        if qty < LOW_STOCK_THRESHOLD:
            low_stock_varieties.append((variety, qty))
        total_g += qty

    print(divider)
    print(f"  {'TOTAL STOCK':<22} {'':<14} {total_g:>12,.0f} g")

    # ── Feature 4: Low-stock alert panel ──────────────────────
    if low_stock_varieties:
        print(f"\n  ┌─ 🔴 LOW STOCK ALERT (below {LOW_STOCK_THRESHOLD} g) ─────────────┐")
        for v, q in low_stock_varieties:
            needed = LOW_STOCK_THRESHOLD - q
            print(f"  │  ⚠  {v:<20} only {q:>7,.0f} g left  "
                  f"(need {needed:,.0f} g more)  │")
        print("  └──────────────────────────────────────────────────────────┘")

    # ── Recent distributions log ───────────────────────────────
    logs = database_handler("get_logs")
    if logs:
        print("\n  ┌─ 📤 RECENT DISTRIBUTIONS (last 20) ─────────────────────┐")
        print(f"  │  {'VARIETY':<20} {'RECIPIENT':<18} {'QTY (g)':>9}  {'DATE':<12}  │")
        print("  │  " + "─" * 64 + "│")
        for seed_v, recip, qty, dist_date in logs:
            print(f"  │  {seed_v:<20} {recip:<18} {qty:>9,.0f}  {dist_date:<12}  │")
        print("  └──────────────────────────────────────────────────────────┘")

    print()


# ── Main Function — Menu Loop ──────────────────────────────────
def main_function():
    """
    Entry point for the entire application.
    1. Initialises the SQLite database (creates tables if needed).
    2. Shows the welcome screen.
    3. Enters the main menu loop — routes choices to each feature.
    4. After every action asks: Return to menu? (Y/N)
    5. Exits cleanly on option 4 or when user enters N.
    """
    # Step 1: ensure database tables exist
    database_handler("setup")

    # Step 2: show welcome screen
    intro_function()

    # Step 3: main menu loop
    while True:
        print("""  ╔══ MAIN MENU ══════════════════════════════════════╗
  ║                                                   ║
  ║   1.  📥  Log New Seed Batch                      ║
  ║   2.  🚜  Distribute Seeds to Member              ║
  ║   3.  📋  View Inventory Report                   ║
  ║   4.  🚪  Exit                                    ║
  ║                                                   ║
  ╚═══════════════════════════════════════════════════╝""")

        choice = input("\n  >>>> Select an option (1-4): ").strip()

        if choice == "1":
            log_seeds_function()
        elif choice == "2":
            distribute_seeds_function()
        elif choice == "3":
            display_report_function()
        elif choice == "4":
            print("\n  👋  Thank you for using GreenFinger. "
                  "Happy planting, and goodbye!\n")
            break
        else:
            print("\n  ⚠  Invalid option. Please enter 1, 2, 3, or 4.\n")
            continue

        # Step 4: return-to-menu prompt (matches flowchart diamond)
        again = input("\n  ↩  Return to Main Menu? (Y/N): ").strip().upper()
        if again != "Y":
            print("\n  👋  Thank you for using GreenFinger. "
                  "Happy planting, and goodbye!\n")
            break
        intro_function()   # refresh screen before re-showing menu


# ── Entry guard ────────────────────────────────────────────────
if __name__ == "__main__":
    main_function()

