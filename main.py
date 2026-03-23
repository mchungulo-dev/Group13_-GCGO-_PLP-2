from datetime import datetime
from database import LOW_STOCK_THRESHOLD
from database import database_handler
from intro import intro_function
from log_seeds import log_seeds_function
from distribute import distribute_seeds_function
from report import display_report_function

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
    # ensure database tables exist
    database_handler("setup")

    # show welcome screen
    intro_function()

    # main menu loop
    while True:
        print("""                                          
   1. Enter New Seed Batch                     
   2. Sell seeds to a customer             
   3. View Inventory Report                  
   4. Exit                                                                            
  """)

        choice = input("\n  >>>> Select an option (1-4): ").strip()

        if choice == "1":
            log_seeds_function()
        elif choice == "2":
            distribute_seeds_function()
        elif choice == "3":
            display_report_function()
        elif choice == "4":
            print("\n Thank you for using GreenFinger. "
                  "Happy planting, and goodbye!\n")
            break
        else:
            print("\n  Invalid option. Please enter 1, 2, 3, or 4.\n")
            continue

        # return-to-menu prompt
        again = input("\n Return to Main Menu? (Y/N): ").strip().upper()
        if again != "Y":
            print("\n Thank you for using GreenFinger. "
                  "Happy planting, and goodbye!\n")
            break
        intro_function()   # refresh screen before re-showing menu


# ── Entry guard ────────────────────────────────────────────────
if __name__ == "__main__":
    main_function()

