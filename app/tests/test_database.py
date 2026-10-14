import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ConstructionDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = Path(self.tmp.name)
        self.tmp.close()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript((ROOT / "database" / "schema.sql").read_text())
        self.conn.executescript((ROOT / "database" / "sample_data.sql").read_text())

    def tearDown(self):
        self.conn.close()
        self.db_path.unlink(missing_ok=True)

    def test_sample_project_exists(self):
        count = self.conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        self.assertGreaterEqual(count, 1)

    def test_material_balance_view(self):
        rows = self.conn.execute("SELECT * FROM v_material_balance").fetchall()
        self.assertGreaterEqual(len(rows), 1)

    def test_negative_budget_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO projects(project_name, budget) VALUES ('Invalid Budget Project', -1)"
            )

    def test_invalid_progress_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO progress_entries(work_package_id, progress_percent) VALUES (1, 150)"
            )

if __name__ == "__main__":
    unittest.main()
