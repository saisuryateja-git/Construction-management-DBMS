import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "construction.db"
SCHEMA = ROOT / "database" / "schema.sql"
SEED = ROOT / "database" / "sample_data.sql"

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize():
    with connect() as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        conn.executescript(SEED.read_text(encoding="utf-8"))

def show_projects():
    with connect() as conn:
        rows = conn.execute(
            "SELECT project_id, project_name, budget, status FROM projects ORDER BY project_id"
        ).fetchall()
    if not rows:
        print("No projects found.")
        return
    print("\\nPROJECTS")
    print("-" * 76)
    for r in rows:
        print(f"#{r['project_id']} | {r['project_name']} | Budget: {r['budget']:.2f} | {r['status']}")

def show_material_balance():
    with connect() as conn:
        rows = conn.execute(
            "SELECT site_name, material_name, quantity, unit, stock_status FROM v_material_balance "
            "ORDER BY site_name, material_name"
        ).fetchall()
    print("\\nSITE MATERIAL BALANCE")
    print("-" * 76)
    if not rows:
        print("No stock records found.")
    for r in rows:
        print(f"{r['site_name']} | {r['material_name']}: {r['quantity']} {r['unit']} [{r['stock_status']}]")

def add_project():
    name = input("Project name: ").strip()
    if not name:
        print("Project name cannot be empty.")
        return
    try:
        budget = float(input("Budget (number): ").strip())
        if budget < 0:
            print("Budget cannot be negative.")
            return
    except ValueError:
        print("Enter a valid numeric budget.")
        return
    status = input("Status [Planned/Active/On Hold/Completed/Cancelled] (default Planned): ").strip() or "Planned"
    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO projects(project_name, budget, status) VALUES (?, ?, ?)",
                (name, budget, status)
            )
        print("Project added successfully.")
    except sqlite3.IntegrityError as exc:
        print(f"Could not add project: {exc}")

def main():
    initialize()
    while True:
        print("\\nCONSTRUCTION MATERIAL & SITE PROGRESS MANAGEMENT")
        print("1. List projects")
        print("2. Show material balance")
        print("3. Add project")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_projects()
        elif choice == "2":
            show_material_balance()
        elif choice == "3":
            add_project()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1-4.")

if __name__ == "__main__":
    main()
