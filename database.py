import sqlite3
import os
from datetime import date, datetime

DB_FILE = "greenfinger.db"
LOW_STOCK_THRESHOLD = 500   # grams – varieties below this are flagged
CATEGORIES = ["Grains", "Vegetables", "Legumes", "Herbs", "Fruits", "Other"]


def database_handler(action: str, params: tuple = ()):
    """
    Central SQLite gateway.
    Actions:
        'setup':          create tables if they don't exist
        'log_seed':       INSERT or UPDATE a seed batch
        'distribute':     subtract stock & record transaction
        'get_inventory':  SELECT all seed rows
        'get_logs':       SELECT all distribution logs
        'get_varieties':  SELECT variety names and quantities only
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        if action == "setup":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seeds (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    variety     TEXT    NOT NULL UNIQUE,
                    category    TEXT    NOT NULL,
                    quantity_g  REAL    NOT NULL DEFAULT 0,
                    date_added  TEXT    NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS distributions (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    seed_variety TEXT    NOT NULL,
                    recipient    TEXT    NOT NULL,
                    quantity_g   REAL    NOT NULL,
                    dist_date    TEXT    NOT NULL
                )
            """)
            conn.commit()

        elif action == "log_seed":
            variety, category, qty, log_date = params
            # If variety already exists, ADD to its stock
            cursor.execute("SELECT id, quantity_g FROM seeds WHERE variety = ?",
                           (variety,))
            row = cursor.fetchone()
            if row:
                new_qty = row[1] + qty
                cursor.execute("UPDATE seeds SET quantity_g = ?, date_added = ? "
                               "WHERE id = ?", (new_qty, log_date, row[0]))
            else:
                cursor.execute("INSERT INTO seeds (variety, category, quantity_g, "
                               "date_added) VALUES (?, ?, ?, ?)",
                               (variety, category, qty, log_date))
            conn.commit()

        elif action == "distribute":
            variety, recipient, qty, dist_date = params
            cursor.execute("UPDATE seeds SET quantity_g = quantity_g - ? "
                           "WHERE variety = ?", (qty, variety))
            cursor.execute("INSERT INTO distributions (seed_variety, recipient, "
                           "quantity_g, dist_date) VALUES (?, ?, ?, ?)",
                           (variety, recipient, qty, dist_date))
            conn.commit()

        elif action == "get_inventory":
            cursor.execute("SELECT variety, category, quantity_g, date_added "
                           "FROM seeds ORDER BY category, variety")
            return cursor.fetchall()

        elif action == "get_logs":
            cursor.execute("SELECT seed_variety, recipient, quantity_g, dist_date "
                           "FROM distributions ORDER BY dist_date DESC LIMIT 20")
            return cursor.fetchall()

        elif action == "get_varieties":
            cursor.execute("SELECT variety, quantity_g FROM seeds ORDER BY variety")
            return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"\n  [DB ERROR] {e}\n")
        return None
    finally:
        conn.close()

    return True


if __name__ == "__main__":
    result = database_handler("setup")
    if result:
        print("Database setup complete. Tables ready.")
        print(f"DB file: {DB_FILE}")
    else:
        print("❌  Database setup failed. Check error above.")