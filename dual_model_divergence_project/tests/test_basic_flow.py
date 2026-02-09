import tempfile
import unittest
from pathlib import Path

from main import run_pipeline
from modules.database import DatabaseManager
from modules.divergence_detector import compare_answers


class BasicFlowTests(unittest.TestCase):
    def test_divergence_detector_year_conflict(self):
        a = "X技术专利申请于2020年。"
        b = "X技术专利申请于2018年。"
        diff = compare_answers(a, b)
        self.assertTrue(diff["conflicts"], "Expected conflict for year mismatch.")
        self.assertEqual(diff["conflicts"][0]["type"], "numeric_difference")
        self.assertIn("X技术", diff["conflicts"][0]["conflict_id"])

    def test_pipeline_mock_mode_persists_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "responses.db"
            out = run_pipeline(
                question="Which is the largest planet in the solar system?",
                db_path=str(db_file),
                mock_mode=True,
                use_cache=False,
                enable_evidence=True,
            )
            self.assertIn("融合答案", out)
            self.assertTrue(db_file.exists())

            db = DatabaseManager(str(db_file))
            with db._connect() as conn:
                q_count = conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
                resp_count = conn.execute("SELECT COUNT(*) FROM model_responses").fetchone()[0]
                fused_count = conn.execute("SELECT COUNT(*) FROM fused_answers").fetchone()[0]
            self.assertEqual(q_count, 1)
            self.assertEqual(resp_count, 2)
            self.assertEqual(fused_count, 1)

    def test_pipeline_rejects_empty_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "responses.db"
            with self.assertRaises(ValueError):
                run_pipeline(
                    question="  ",
                    db_path=str(db_file),
                    mock_mode=True,
                    use_cache=False,
                    enable_evidence=False,
                )


if __name__ == "__main__":
    unittest.main()
