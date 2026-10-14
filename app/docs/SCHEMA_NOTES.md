# Schema Notes

The SQL implementation contains the following core relations:
PROJECTS, SITES, CONTRACTORS, WORK_PACKAGES, MATERIALS, SUPPLIERS, PURCHASE_ORDERS, PO_ITEMS, DELIVERIES, DELIVERY_ITEMS, SITE_STOCK, MATERIAL_ISSUES, ISSUE_ITEMS, LABOUR_TEAMS, PROGRESS_ENTRIES, CONTRACTOR_BILLS, and PAYMENTS.

Primary keys use integer identifiers. Foreign keys enforce references between related records. CHECK constraints restrict negative quantities and invalid progress percentages. Reporting views summarize site material balances and contractor bill payment balances.

This is an initial implementation; review normalization, functional dependencies, naming consistency, and final ERD alignment before treating it as the approved academic schema.
