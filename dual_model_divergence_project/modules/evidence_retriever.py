from typing import Dict, List


def fetch_evidence(conflicts: List[Dict]) -> Dict[str, Dict]:
    """
    Minimal evidence resolver used for stage-1/2 scaffolding.
    In production, this should be replaced with authority-tiered retrieval.
    """
    result: Dict[str, Dict] = {}
    for c in conflicts:
        cid = c.get("conflict_id", "unknown_conflict")
        if c.get("type") == "numeric_difference":
            years_a = c.get("model_a_years", [])
            years_b = c.get("model_b_years", [])
            # Demo heuristic: when years differ, keep unresolved by default.
            result[cid] = {
                "verdict": "unknown",
                "evidence_text": f"A years={years_a}, B years={years_b}; no trusted source attached.",
                "source": "local_heuristic",
            }
        else:
            result[cid] = {
                "verdict": "unknown",
                "evidence_text": "No evidence resolver configured for this conflict type.",
                "source": "local_heuristic",
            }
    return result

