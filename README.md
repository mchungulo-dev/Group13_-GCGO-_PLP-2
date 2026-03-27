 GreenFinger Inventory Manager
       Group 13 - PLP 2 Project

Group Members: Memory Chungulo · Precious Azubuike · China Viola · Shaun Muhizi · Niteka Morel · Orion Seruvumba

---

## Project Overview

GreenFinger Inventory Manager is a set of Python scripts used to manage and track seed stock and distribution for community garden projects. It automates the process of logging seed batches, recording distributions to members, and generating inventory reports to ensure resources are used efficiently and distributed fairly.

**Core Features**

1. Stock Intake (`seed_intake.py`)
   - Interactive menu prompts the user to enter a seed variety, category, and quantity in grams.
   - Validates all input before saving to the database.
   - Confirms successful logging with a success message.

2. Distribution Tracker (`distribution.py`)
   - Displays all available seed varieties with current stock levels.
   - Records how much was given to each community member.
   - Prevents over-distribution using real-time stock validation and FIFO deduction.

3. Inventory Report (`reports.py`)
   - Queries the database and displays a formatted table of all seed varieties and quantities.
   - Highlights varieties with low stock (below 200 g) as warnings.
   - Saves a full distribution log for accountability and auditing.



## How to Use the System

Step 1: Start the application

```bash
python3 main.py


 Step 2: Log a new seed batch

```bash
 Select option 1 from the main menu
 Enter the seed variety, category, and quantity when prompted
```

Step 3: Distribute seeds to a member

```bash
# Select option 2 from the main menu
# Choose the seed variety and enter the recipient name and quantity
```

Step 4: View the inventory report

```bash
# Select option 3 from the main menu
```

---

## Repository Structure

```
/greenfinger-inventory/
├── main.py            — Entry point, runs the main menu loop
├── database.py        — Handles all SQLite database operations
├── seed_intake.py     — Feature 1: Log new seed batches
├── distribution.py    — Feature 2: Distribute seeds to members
├── reports.py         — Features 3 & 4: Inventory report + low-stock alerts
├── ui.py              — Welcome screen and menu formatting
├── greenfinger.db     — Auto-generated local database (do not commit)
└── README.md
```



## Tools and Technologies Used

| Task | Tools |
|---|---|
| Programming language | Python 3 |
| Database | SQLite3 (`sqlite3` module) |
| Version control | Git & GitHub |
| IDE | Visual Studio Code |
| Data operations | SQL — `INSERT`, `SELECT`, `UPDATE`, `SUM`, `GROUP BY` |



## Conclusion

This project represents an end-to-end seed inventory and distribution management system built for real-world community agriculture use. It is focused on data persistence, input validation, and transparency in resource sharing — ensuring that every seed batch is tracked from intake to distribution.