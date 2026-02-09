from typing import Dict, List


def _infer_topic(text: str) -> str:
    t = (text or "").lower()
    if ("专利" in t) or ("patent" in t):
        return "patent_fact"
    if ("年份" in t) or ("year" in t):
        return "time_claim"
    if ("幻觉" in t) or ("hallucination" in t):
        return "hallucination"
    return "general"


def _build_subquestion(conflict: Dict) -> str:
    ctype = conflict.get("type", "")
    subject = str(conflict.get("subject", "")).strip() or "该主题"

    if ctype == "numeric_difference":
        return f"{subject} 的真实年份信息是什么？"
    if ctype == "omission":
        missing_in = conflict.get("missing_in", "unknown")
        return f"{subject} 的关键断言是否应在模型{missing_in}中出现？"
    if ctype == "contradiction":
        return f"{subject} 的相反陈述中哪一个更可信？"
    return f"{subject} 的冲突应如何裁决？"


def _build_evidence_snippets(conflict: Dict) -> List[Dict]:
    snippets: List[Dict] = []
    a_claim = str(conflict.get("model_a_claim", "")).strip()
    b_claim = str(conflict.get("model_b_claim", "")).strip()
    if a_claim:
        snippets.append({"model": "A", "snippet": a_claim})
    if b_claim:
        snippets.append({"model": "B", "snippet": b_claim})
    return snippets


def restructure(answer_a: str, answer_b: str, diff_result: Dict) -> Dict:
    """Build structured representation with unit metadata for downstream fusion."""
    match_map = {
        (m.get("a_index"), m.get("b_index")): m for m in diff_result.get("sentence_matches", []) if isinstance(m, dict)
    }

    consensus_units = []
    for i, text in enumerate(diff_result.get("consensus", []), start=1):
        consensus_units.append(
            {
                "unit_id": f"C{i}",
                "text": text,
                "topic_tag": _infer_topic(text),
            }
        )

    model_a_units = []
    for i, text in enumerate(diff_result.get("model_a_only", []), start=1):
        model_a_units.append(
            {
                "unit_id": f"A{i}",
                "text": text,
                "topic_tag": _infer_topic(text),
                "source_model": "A",
            }
        )

    model_b_units = []
    for i, text in enumerate(diff_result.get("model_b_only", []), start=1):
        model_b_units.append(
            {
                "unit_id": f"B{i}",
                "text": text,
                "topic_tag": _infer_topic(text),
                "source_model": "B",
            }
        )

    conflict_units = []
    for c in diff_result.get("conflicts", []):
        if not isinstance(c, dict):
            continue
        unit = dict(c)
        unit["subquestion"] = _build_subquestion(c)
        unit["evidence_snippets"] = _build_evidence_snippets(c)
        unit["topic_tag"] = _infer_topic(c.get("description", "") + " " + c.get("subject", ""))
        conflict_units.append(unit)

    return {
        "consensus_units": consensus_units,
        "model_a_units": model_a_units,
        "model_b_units": model_b_units,
        "conflict_units": conflict_units,
        "sentence_matches": list(match_map.values()),
        "raw_answer_a": answer_a,
        "raw_answer_b": answer_b,
    }
