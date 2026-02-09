from pathlib import Path

from modules.database import DatabaseManager
from modules.divergence_detector import compare_answers
from main import run_pipeline


def test_divergence_detector_year_conflict():
    a = "X技术专利申请于2020年。"
    b = "X技术专利申请于2018年。"
    diff = compare_answers(a, b)
    assert diff["conflicts"], "Expected at least one conflict for year mismatch."
    assert diff["conflicts"][0]["type"] == "numeric_difference"
    assert "X技术" in diff["conflicts"][0]["conflict_id"]


def test_pipeline_mock_mode(tmp_path: Path):
    db_file = tmp_path / "responses.db"
    out = run_pipeline(
        question="Which is the largest planet in the solar system?",
        db_path=str(db_file),
        mock_mode=True,
        use_cache=False,
        enable_evidence=True,
    )
    assert "融合答案" in out
    assert db_file.exists()

    db = DatabaseManager(str(db_file))
    with db._connect() as conn:
        q_count = conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
        resp_count = conn.execute("SELECT COUNT(*) FROM model_responses").fetchone()[0]
        fused_count = conn.execute("SELECT COUNT(*) FROM fused_answers").fetchone()[0]
    assert q_count == 1
    assert resp_count == 2
    assert fused_count == 1
