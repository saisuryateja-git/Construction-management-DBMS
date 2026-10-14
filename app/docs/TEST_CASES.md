# Test Cases

| ID | Test | Expected result |
|---|---|---|
| TC-01 | Initialize database | Tables and views are created |
| TC-02 | Load sample data | Demonstration project and related records exist |
| TC-03 | Insert a negative project budget | Rejected by CHECK constraint |
| TC-04 | Record progress above 100% | Rejected by CHECK constraint |
| TC-05 | Display material balance | Material quantities and reorder status appear |
| TC-06 | Add a valid project through the menu | Project is inserted and confirmation is shown |
| TC-07 | Add a duplicate project name | Unique constraint prevents duplicate |

Run automated checks using `python -m unittest discover -s tests -v`. Record the actual observed output in the final report.
