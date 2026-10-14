-- 1. Active projects
SELECT project_id, project_name, budget, status
FROM projects WHERE status = 'Active';

-- 2. Site material balance and reorder status
SELECT * FROM v_material_balance ORDER BY site_name, material_name;

-- 3. Contractor bill and outstanding balance
SELECT * FROM v_bill_payment_balance ORDER BY bill_id;

-- 4. Latest progress by work package
SELECT wp.package_name, MAX(pe.progress_percent) AS latest_recorded_progress,
       MAX(pe.entry_date) AS latest_entry_date
FROM work_packages wp
LEFT JOIN progress_entries pe ON pe.work_package_id = wp.work_package_id
GROUP BY wp.work_package_id, wp.package_name;

-- 5. Supplier purchase order totals
SELECT s.supplier_name, SUM(pi.quantity * pi.unit_price) AS order_value
FROM suppliers s
JOIN purchase_orders po ON po.supplier_id = s.supplier_id
JOIN po_items pi ON pi.po_id = po.po_id
GROUP BY s.supplier_id, s.supplier_name;
