-- Material balance report
SELECT site_name, material_name, quantity, unit, reorder_level, stock_status
FROM v_material_balance ORDER BY site_name, material_name;

-- Outstanding payments report
SELECT bill_id, work_package_id, amount, paid_amount, outstanding_amount
FROM v_bill_payment_balance WHERE outstanding_amount > 0;

-- Project and site overview
SELECT p.project_name, p.status AS project_status, s.site_name, s.location
FROM projects p JOIN sites s ON s.project_id = p.project_id
ORDER BY p.project_name, s.site_name;
