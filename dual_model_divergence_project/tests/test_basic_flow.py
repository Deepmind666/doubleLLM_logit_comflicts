import tempfile
import unittest
from pathlib import Path
from unittest import mock

from main import run_pipeline
from modules.database import DatabaseManager
from modules.divergence_detector import _has_negation, compare_answers
from modules.evidence_retriever import _normalize_subject
from modules.knowledge_graph import build_graph_from_text, compare_graphs


class BasicFlowTests(unittest.TestCase):
    def test_divergence_detector_year_conflict(self):
        a = "X技术专利申请于2020年。"
        b = "X技术专利申请于2018年。"
        diff = compare_answers(a, b)
        self.assertTrue(diff["conflicts"], "Expected conflict for year mismatch.")
        self.assertEqual(diff["conflicts"][0]["type"], "numeric_difference")
        self.assertIn("X技术", diff["conflicts"][0]["conflict_id"])

    def test_divergence_detector_fuzzy_consensus(self):
        a = "太阳系中最大的行星是木星。"
        b = "太阳系最大的行星是木星"
        diff = compare_answers(a, b)
        self.assertGreaterEqual(len(diff["consensus"]), 1)
        self.assertEqual(len(diff["model_a_only"]), 0)
        self.assertEqual(len(diff["model_b_only"]), 0)

    def test_divergence_detector_omission_conflict(self):
        a = "Autodesk patent filed in 2025."
        b = "This system verifies language model outputs."
        diff = compare_answers(a, b)
        omission = [c for c in diff["conflicts"] if c.get("type") == "omission"]
        self.assertTrue(omission, "Expected omission conflict when one side misses a subject-year claim.")

    def test_divergence_detector_contradiction_conflict(self):
        a = "该方案可离线执行。"
        b = "该方案不可离线执行。"
        diff = compare_answers(a, b)
        contradiction = [c for c in diff["conflicts"] if c.get("type") == "contradiction"]
        self.assertTrue(contradiction, "Expected contradiction conflict for opposite polarity statements.")

    def test_negation_pattern_should_not_match_non_negative_phrase(self):
        self.assertFalse(_has_negation("该系统在不断进化"))
        self.assertTrue(_has_negation("该系统不能离线执行"))

    def test_graph_extractor_should_capture_negated_relation(self):
        g_a = build_graph_from_text("太阳是恒星。")
        g_b = build_graph_from_text("太阳不是恒星。")
        cmp_result = compare_graphs(g_a, g_b)
        self.assertIn(("太阳", "不是", "恒星"), g_b["edges"])
        self.assertIn(("太阳", "恒星"), cmp_result["contradictions"])

    def test_normalize_subject_should_only_strip_suffix_technology(self):
        self.assertEqual(_normalize_subject("X技术"), "x")
        self.assertEqual(_normalize_subject("生物技术标准"), "生物技术标准")

    def test_pipeline_graph_conflict_should_be_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "responses.db"

            with mock.patch(
                "main.get_answers",
                return_value={"GPT": "太阳是恒星。", "Claude": "太阳不是恒星。"},
            ):
                out = run_pipeline(
                    question="graph contradiction check",
                    db_path=str(db_file),
                    mock_mode=False,
                    use_cache=False,
                    enable_evidence=False,
                    enable_graph=True,
                )

            self.assertIn("待验证区", out)

            db = DatabaseManager(str(db_file))
            with db._connect() as conn:
                row = conn.execute("SELECT diff_detail FROM divergences ORDER BY id DESC LIMIT 1").fetchone()
            self.assertIsNotNone(row)
            diff = row[0]
            self.assertIn("graph_analysis", diff)
            # ensure only one contradiction conflict line appears after graph + detector merge
            self.assertEqual(diff.count("\"type\": \"contradiction\""), 1)

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

    def test_pipeline_rejects_overlong_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "responses.db"
            too_long = "x" * 5001
            with self.assertRaises(ValueError):
                run_pipeline(
                    question=too_long,
                    db_path=str(db_file),
                    mock_mode=True,
                    use_cache=False,
                    enable_evidence=False,
                )


if __name__ == "__main__":
    unittest.main()
