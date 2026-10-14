PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO projects(project_id, project_name, start_date, end_date, budget, status)
VALUES (1, 'Green Heights Residential Project', '2026-01-10', '2027-12-31', 12500000, 'Active');

INSERT OR IGNORE INTO sites(site_id, project_id, site_name, location)
VALUES (1, 1, 'North Block Site', 'Hyderabad');

INSERT OR IGNORE INTO contractors(contractor_id, name, contact, address)
VALUES (1, 'BuildRight Contractors', '9000000001', 'Hyderabad');

INSERT OR IGNORE INTO work_packages(work_package_id, site_id, contractor_id, package_name, contract_value, status)
VALUES (1, 1, 1, 'Foundation and Structure', 2500000, 'In Progress');

INSERT OR IGNORE INTO materials(material_id, material_name, unit, reorder_level)
VALUES (1, 'Cement', 'bags', 50), (2, 'Steel Rods', 'kg', 200), (3, 'Bricks', 'units', 500);

INSERT OR IGNORE INTO suppliers(supplier_id, supplier_name, contact, address)
VALUES (1, 'Deccan Building Supplies', '9000000002', 'Secunderabad');

INSERT OR IGNORE INTO purchase_orders(po_id, supplier_id, site_id, po_date, status)
VALUES (1, 1, 1, '2026-10-01', 'Delivered');

INSERT OR IGNORE INTO po_items(po_item_id, po_id, material_id, quantity, unit_price)
VALUES (1, 1, 1, 100, 390);

INSERT OR IGNORE INTO deliveries(delivery_id, po_id, delivery_date, status)
VALUES (1, 1, '2026-10-03', 'Received');

INSERT OR IGNORE INTO delivery_items(delivery_item_id, delivery_id, material_id, quantity)
VALUES (1, 1, 1, 100);

INSERT OR IGNORE INTO site_stock(stock_id, site_id, material_id, quantity)
VALUES (1, 1, 1, 75), (2, 1, 2, 350), (3, 1, 3, 1200);

INSERT OR IGNORE INTO labour_teams(team_id, team_name, supervisor)
VALUES (1, 'Foundation Team A', 'Ramesh Kumar');

INSERT OR IGNORE INTO progress_entries(progress_id, work_package_id, team_id, progress_percent, verified_status, entry_date, notes)
VALUES (1, 1, 1, 35, 'Verified', '2026-10-08', 'Foundation work progress reviewed');

INSERT OR IGNORE INTO contractor_bills(bill_id, work_package_id, bill_date, amount, status)
VALUES (1, 1, '2026-10-09', 250000, 'Verified');

INSERT OR IGNORE INTO payments(payment_id, bill_id, payment_date, amount, reference)
VALUES (1, 1, '2026-10-10', 100000, 'PAY-DEMO-001');
