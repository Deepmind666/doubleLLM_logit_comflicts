import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from main import run_pipeline
from modules.database import DatabaseManager
from modules.evidence_retriever import fetch_evidence
from modules.model_invoker import get_answers


class Stage2SecurityAndEvidenceTests(unittest.TestCase):
    def test_l1_evidence_auto_applies_model_b(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "case.db"
            out = run_pipeline(
                question="X技术专利申请年份是多少？",
                db_path=str(db_file),
                mock_mode=True,
                use_cache=False,
                enable_evidence=True,
            )
            self.assertIn("采用模型B结论", out)

            db = DatabaseManager(str(db_file))
            with db._connect() as conn:
                row = conn.execute(
                    "SELECT verdict, source_tier, auto_applied FROM evidence ORDER BY id DESC LIMIT 1"
                ).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[0], "B")
            self.assertEqual(row[1], "L1")
            self.assertEqual(row[2], 1)

    def test_l3_only_should_not_auto_apply(self):
        conflicts = [
            {
                "conflict_id": "year_conflict_CommunityCase",
                "type": "numeric_difference",
                "subject": "CommunityCase",
                "model_a_years": ["2020"],
                "model_b_years": ["2022"],
            }
        ]
        result = fetch_evidence(conflicts)
        item = result["year_conflict_CommunityCase"]
        self.assertEqual(item["verdict"], "unknown")
        self.assertFalse(item["auto_applied"])
        self.assertIn("L3", item["source_tier"])

    def test_api_failure_without_fallback_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "api_fail.db"
            db = DatabaseManager(str(db_file))
            db.init_db()
            qid = db.save_query("test question")

            with mock.patch("modules.model_invoker._call_openai", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    get_answers(
                        question="test question",
                        db=db,
                        query_id=qid,
                        use_cache=False,
                        mock_mode=False,
                        allow_mock_fallback=False,
                    )

    def test_l1_integer_year_should_still_adjudicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog_file = Path(tmp) / "catalog.json"
            catalog_file.write_text(
                json.dumps(
                    [
                        {
                            "subject": "X技术",
                            "year": 2018,
                            "source": "CNIPA mock",
                            "tier": "L1",
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            conflicts = [
                {
                    "conflict_id": "year_conflict_X技术",
                    "type": "numeric_difference",
                    "subject": "X技术",
                    "model_a_years": ["2020"],
                    "model_b_years": ["2018"],
                }
            ]
            with mock.patch.dict(os.environ, {"EVIDENCE_CATALOG_PATH": str(catalog_file)}):
                result = fetch_evidence(conflicts)
            item = result["year_conflict_X技术"]
            self.assertEqual(item["verdict"], "B")
            self.assertEqual(item["source_tier"], "L1")
            self.assertTrue(item["auto_applied"])

    def test_cache_isolation_between_mock_and_live(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "cache.db"
            db = DatabaseManager(str(db_file))
            db.init_db()
            question = "Which is the largest planet in the solar system?"

            qid1 = db.save_query(question)
            mock_answers = get_answers(
                question=question,
                db=db,
                query_id=qid1,
                use_cache=False,
                mock_mode=True,
                allow_mock_fallback=False,
            )
            self.assertIn("木星", mock_answers["GPT"])

            qid2 = db.save_query(question)
            with mock.patch("modules.model_invoker._call_openai", return_value="LIVE GPT answer."), mock.patch(
                "modules.model_invoker._call_anthropic", return_value="LIVE Claude answer."
            ):
                live_answers = get_answers(
                    question=question,
                    db=db,
                    query_id=qid2,
                    use_cache=True,
                    mock_mode=False,
                    allow_mock_fallback=False,
                )

            self.assertEqual(live_answers["GPT"], "LIVE GPT answer.")
            self.assertEqual(live_answers["Claude"], "LIVE Claude answer.")

            with db._connect() as conn:
                rows = conn.execute(
                    "SELECT usage_info FROM model_responses ORDER BY id ASC"
                ).fetchall()
            usages = [r[0] for r in rows]
            self.assertIn("mode=mock", usages)
            self.assertIn("mode=live", usages)

    def test_cache_mode_query_should_use_exact_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "cache_exact.db"
            db = DatabaseManager(str(db_file))
            db.init_db()
            qid = db.save_query("Q")
            db.save_response(qid, "GPT", "answer-from-mock-v2", usage_info="mode=mock_v2")

            exact = db.get_cached_response("Q", "GPT", response_mode="mock")
            self.assertIsNone(exact, "mode=mock must not match mode=mock_v2")


if __name__ == "__main__":
    unittest.main()
