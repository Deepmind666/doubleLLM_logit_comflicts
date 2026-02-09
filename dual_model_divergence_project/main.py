import argparse
import json
from pathlib import Path

from modules.database import DatabaseManager
from modules.decoupler import restructure
from modules.divergence_detector import compare_answers
from modules.evidence_retriever import fetch_evidence
from modules.fusion_generator import generate_fused_answer
from modules.model_invoker import get_answers


def run_pipeline(
    question: str,
    db_path: str,
    mock_mode: bool = False,
    use_cache: bool = True,
    enable_evidence: bool = False,
    allow_mock_fallback: bool = False,
) -> str:
    question = (question or "").strip()
    if not question:
        raise ValueError("question must not be empty.")
    if len(question) > 5000:
        raise ValueError("question is too long; max length is 5000 characters.")

    db = DatabaseManager(db_path)
    db.init_db()

    query_id = db.save_query(question)

    answers = get_answers(
        question=question,
        db=db,
        query_id=query_id,
        use_cache=use_cache,
        mock_mode=mock_mode,
        allow_mock_fallback=allow_mock_fallback,
    )

    gpt_answer = answers["GPT"]
    claude_answer = answers["Claude"]

    diff_result = compare_answers(gpt_answer, claude_answer)
    db.save_divergence(
        query_id=query_id,
        diff_summary=diff_result["summary"],
        diff_detail=json.dumps(diff_result, ensure_ascii=False),
    )

    structured = restructure(
        answer_a=gpt_answer,
        answer_b=claude_answer,
        diff_result=diff_result,
    )
    db.save_structure(query_id=query_id, structured_data=json.dumps(structured, ensure_ascii=False))

    evidence = {}
    if enable_evidence:
        evidence = fetch_evidence(diff_result.get("conflicts", []))
        for conflict_id, info in evidence.items():
            db.save_evidence(
                query_id=query_id,
                diff_id=conflict_id,
                evidence_text=info.get("evidence_text", ""),
                source=info.get("source", ""),
                verdict=info.get("verdict", "unknown"),
                source_tier=info.get("source_tier", ""),
                auto_applied=1 if info.get("auto_applied", False) else 0,
                confidence=float(info.get("confidence", 0.0)),
            )

    final_answer = generate_fused_answer(
        answer_a=gpt_answer,
        answer_b=claude_answer,
        diff_result=diff_result,
        structured=structured,
        evidence=evidence,
    )

    db.save_fused_answer(
        query_id=query_id,
        answer_text=final_answer,
        notes="mock_mode=%s, evidence=%s" % (mock_mode, enable_evidence),
    )
    return final_answer


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dual-model divergence detection and fusion demo.")
    parser.add_argument("question", help="User question.")
    parser.add_argument(
        "--db-path",
        default=str(Path("data") / "responses.db"),
        help="SQLite database path.",
    )
    parser.add_argument("--mock", action="store_true", help="Use mock answers instead of API calls.")
    parser.add_argument(
        "--allow-mock-fallback",
        action="store_true",
        help="Allow fallback to mock responses when live API calls fail.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable cache lookup.")
    parser.add_argument("--enable-evidence", action="store_true", help="Enable evidence retrieval module.")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    result = run_pipeline(
        question=args.question,
        db_path=args.db_path,
        mock_mode=args.mock,
        use_cache=not args.no_cache,
        enable_evidence=args.enable_evidence,
        allow_mock_fallback=args.allow_mock_fallback,
    )
    print(result)


if __name__ == "__main__":
    main()
