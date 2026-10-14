# Construction Material and Site Progress Management DBMS

**Student:** A. Sai Surya Teja Goud  
**Roll No.:** 25WU0102012  
**Course:** Database Management Systems  
**Institution:** Woxsen University

## Overview
A starter database application for managing construction projects, sites, contractors, work packages, materials, suppliers, purchase orders, deliveries, site stock, material issues, labour teams, work progress, contractor bills, and payments.

## Technology
- Python 3.9 or later
- SQLite (included with Python)
- SQL DDL, foreign keys, CHECK constraints, and views

## Run
From this directory:

```bash
python app.py
```

The application initializes `construction.db`, creates the schema, inserts demonstration records, and opens a command-line menu.

## Database scripts
- `database/schema.sql`: table definitions, constraints, and reporting views
- `database/sample_data.sql`: demonstration records
- `database/queries.sql`: representative SQL queries
- `database/reports.sql`: reporting queries

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Important submission note
This is a generated starter implementation based on the construction DBMS project description and initial schema in the supplied Review 1 material. Verify it against the final approved ER diagram, your actual implementation, and your faculty's requirements before submission. Do not describe features as implemented unless you have tested them. The CLI currently demonstrates project listing, material balance display, and adding projects; the schema contains additional entities for further application development.

## Suggested ZIP contents
Include this folder, your final report, Review 1/2/3 PDFs if applicable, and your presentation video if required by the faculty. Do not include passwords, API keys, virtual environments, or unnecessary `.git` internals.

## Run the local website

From the `Construction_DBMS_Submission` folder, run:

```bash
python3 web.py
```

Then open `http://127.0.0.1:8000` in your browser. The website uses Python's standard library and the same SQLite database as the CLI. Press `Control+C` in Terminal to stop the server. The web interface currently supports dashboard, project listing, material balance, and adding projects; other database modules are schema-only in this starter version.
