import os
from datetime import date

# Import shared config from Member 1
from database import LOW_STOCK_THRESHOLD


def intro_function():
    """Clear the terminal and print the professional welcome banner."""

    os.system("cls" if os.name == "nt" else "clear")

    today = date.today().strftime("%A, %d %B %Y")

    # Dynamically insert today's date into the banner
    print(f"║      Today: {today:<49}║")

    print(f"""╠══════════════════════════════════════════════════════════════╣
║  USAGE GUIDELINES                                            ║
║  ─────────────────────────────────────────────────────────   ║
║  • Log every seed batch received from donors or suppliers.   ║
║  • Record all distributions so stock levels stay accurate.   ║
║  • Use the report to plan planting seasons and re-stocking.  ║
║  • Varieties below {LOW_STOCK_THRESHOLD} g are automatically flagged as LOW.   ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    intro_function()
