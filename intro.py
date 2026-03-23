"""
╔══════════════════════════════════════════════════════════════╗
║   GreenFinger Inventory Manager  v1.0                        ║
║   MEMBER 2 — Welcome Screen (intro_function)                 ║
║   Responsible for: The opening banner shown at startup       ║
╚══════════════════════════════════════════════════════════════╝

YOUR JOB:
  - Write the intro_function() that clears the terminal and
    prints the professional welcome banner with today's date
    and usage guidelines
  - This function is called by Member 6 (main_function) at
    startup AND every time the user returns to the main menu

HOW TO TEST YOUR PART ALONE:
  Run:  python member2_intro.py
  Expected output: The full welcome banner printed in terminal
"""

import os
from datetime import date

# Import shared config from Member 1
from database import LOW_STOCK_THRESHOLD


# ══════════════════════════════════════════════
#  INTRO FUNCTION
#  Displays the welcome banner, today's date, and usage rules.
#  Called once at startup and again on every menu return.
# ══════════════════════════════════════════════
def intro_function():
    """Clear the terminal and print the professional welcome banner."""

    # Cross-platform terminal clear (Windows: cls | Mac/Linux: clear)
    os.system("cls" if os.name == "nt" else "clear")

    today = date.today().strftime("%A, %d %B %Y")

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🌱  GreenFinger Inventory Manager  v1.0  🌱           ║
║          Community Seed Stock & Distribution Tracker         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣""")

    # Dynamically insert today's date into the banner
    print(f"║  📅  Today: {today:<49}║")

    print(f"""╠══════════════════════════════════════════════════════════════╣
║  USAGE GUIDELINES                                            ║
║  ─────────────────────────────────────────────────────────  ║
║  • Log every seed batch received from donors or suppliers.   ║
║  • Record all distributions so stock levels stay accurate.   ║
║  • Use the report to plan planting seasons and re-stocking.  ║
║  • Varieties below {LOW_STOCK_THRESHOLD} g are automatically flagged as LOW.   ║
╚══════════════════════════════════════════════════════════════╝
""")


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    intro_function()
