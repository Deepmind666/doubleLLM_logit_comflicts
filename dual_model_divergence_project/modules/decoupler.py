from typing import Dict


def restructure(answer_a: str, answer_b: str, diff_result: Dict) -> Dict:
    """Build a simple structured representation for downstream fusion."""
    return {
        "consensus_units": [
            {"unit_id": f"C{i+1}", "text": s} for i, s in enumerate(diff_result.get("consensus", []))
        ],
        "model_a_units": [
            {"unit_id": f"A{i+1}", "text": s} for i, s in enumerate(diff_result.get("model_a_only", []))
        ],
        "model_b_units": [
            {"unit_id": f"B{i+1}", "text": s} for i, s in enumerate(diff_result.get("model_b_only", []))
        ],
        "conflict_units": diff_result.get("conflicts", []),
        "raw_answer_a": answer_a,
        "raw_answer_b": answer_b,
    }

