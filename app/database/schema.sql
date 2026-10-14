PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL UNIQUE,
    start_date TEXT,
    end_date TEXT,
    budget REAL NOT NULL DEFAULT 0 CHECK (budget >= 0),
    status TEXT NOT NULL DEFAULT 'Planned'
        CHECK (status IN ('Planned','Active','On Hold','Completed','Cancelled'))
);

CREATE TABLE IF NOT EXISTS sites (
    site_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    site_name TEXT NOT NULL,
    location TEXT,
    UNIQUE(project_id, site_name),
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS contractors (
    contractor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS work_packages (
    work_package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER NOT NULL,
    contractor_id INTEGER,
    package_name TEXT NOT NULL,
    contract_value REAL NOT NULL DEFAULT 0 CHECK (contract_value >= 0),
    status TEXT NOT NULL DEFAULT 'Pending'
        CHECK (status IN ('Pending','In Progress','Completed','On Hold')),
    FOREIGN KEY (site_id) REFERENCES sites(site_id) ON DELETE RESTRICT,
    FOREIGN KEY (contractor_id) REFERENCES contractors(contractor_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL,
    reorder_level REAL NOT NULL DEFAULT 0 CHECK (reorder_level >= 0)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL UNIQUE,
    contact TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    po_date TEXT NOT NULL DEFAULT (date('now')),
    status TEXT NOT NULL DEFAULT 'Placed'
        CHECK (status IN ('Placed','Partially Delivered','Delivered','Cancelled')),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE RESTRICT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS po_items (
    po_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(material_id) ON DELETE RESTRICT,
    UNIQUE(po_id, material_id)
);

CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id INTEGER NOT NULL,
    delivery_date TEXT NOT NULL DEFAULT (date('now')),
    status TEXT NOT NULL DEFAULT 'Received'
        CHECK (status IN ('Received','Partial','Rejected')),
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS delivery_items (
    delivery_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(material_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS site_stock (
    stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE(site_id, material_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id) ON DELETE RESTRICT,
    FOREIGN KEY (material_id) REFERENCES materials(material_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS material_issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL DEFAULT (date('now')),
    issued_to TEXT,
    notes TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS issue_items (
    issue_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (issue_id) REFERENCES material_issues(issue_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(material_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS labour_teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    supervisor TEXT
);

CREATE TABLE IF NOT EXISTS progress_entries (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_package_id INTEGER NOT NULL,
    team_id INTEGER,
    progress_percent REAL NOT NULL CHECK (progress_percent BETWEEN 0 AND 100),
    verified_status TEXT NOT NULL DEFAULT 'Pending'
        CHECK (verified_status IN ('Pending','Verified','Rejected')),
    entry_date TEXT NOT NULL DEFAULT (date('now')),
    notes TEXT,
    FOREIGN KEY (work_package_id) REFERENCES work_packages(work_package_id) ON DELETE RESTRICT,
    FOREIGN KEY (team_id) REFERENCES labour_teams(team_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS contractor_bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_package_id INTEGER NOT NULL,
    bill_date TEXT NOT NULL DEFAULT (date('now')),
    amount REAL NOT NULL CHECK (amount >= 0),
    status TEXT NOT NULL DEFAULT 'Submitted'
        CHECK (status IN ('Submitted','Verified','Rejected','Partially Paid','Paid')),
    FOREIGN KEY (work_package_id) REFERENCES work_packages(work_package_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL DEFAULT (date('now')),
    amount REAL NOT NULL CHECK (amount > 0),
    reference TEXT,
    FOREIGN KEY (bill_id) REFERENCES contractor_bills(bill_id) ON DELETE RESTRICT
);

CREATE VIEW IF NOT EXISTS v_material_balance AS
SELECT s.site_id, si.site_name, m.material_id, m.material_name, m.unit,
       s.quantity, m.reorder_level,
       CASE WHEN s.quantity <= m.reorder_level THEN 'REORDER' ELSE 'OK' END AS stock_status
FROM site_stock s
JOIN sites si ON si.site_id = s.site_id
JOIN materials m ON m.material_id = s.material_id;

CREATE VIEW IF NOT EXISTS v_bill_payment_balance AS
SELECT b.bill_id, b.work_package_id, b.bill_date, b.amount, b.status,
       COALESCE(SUM(p.amount), 0) AS paid_amount,
       b.amount - COALESCE(SUM(p.amount), 0) AS outstanding_amount
FROM contractor_bills b
LEFT JOIN payments p ON p.bill_id = b.bill_id
GROUP BY b.bill_id, b.work_package_id, b.bill_date, b.amount, b.status;
