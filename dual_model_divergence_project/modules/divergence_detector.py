import difflib
import re
from typing import Dict, List


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？!?;\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _extract_years(text: str) -> List[str]:
    return re.findall(r"(19\d{2}|20\d{2})", text)


def _extract_year_claims(text: str) -> List[Dict]:
    claims: List[Dict] = []
    for s in _split_sentences(text):
        m_cn = re.search(
            r"(?P<subject>[A-Za-z0-9\u4e00-\u9fff_-]{1,40})专利(?:申请)?于(?P<year>19\d{2}|20\d{2})年",
            s,
        )
        if m_cn:
            claims.append(
                {
                    "subject": m_cn.group("subject"),
                    "year": m_cn.group("year"),
                    "sentence": s,
                }
            )
            continue
        m_en = re.search(
            r"(?P<subject>[A-Za-z0-9_-]{1,40})\s+(?:patent|application)\s+(?:was\s+)?filed\s+in\s+(?P<year>19\d{2}|20\d{2})",
            s,
            re.I,
        )
        if m_en:
            claims.append(
                {
                    "subject": m_en.group("subject"),
                    "year": m_en.group("year"),
                    "sentence": s,
                }
            )
    return claims


def compare_answers(answer_a: str, answer_b: str) -> Dict:
    a_sents = _split_sentences(answer_a)
    b_sents = _split_sentences(answer_b)

    a_set = set(a_sents)
    b_set = set(b_sents)

    a_only = sorted(list(a_set - b_set))
    b_only = sorted(list(b_set - a_set))
    consensus = sorted(list(a_set & b_set))

    conflicts = []
    claims_a = _extract_year_claims(answer_a)
    claims_b = _extract_year_claims(answer_b)
    map_a = {c["subject"]: c for c in claims_a}
    map_b = {c["subject"]: c for c in claims_b}
    for subject in sorted(set(map_a) & set(map_b)):
        ya = map_a[subject]["year"]
        yb = map_b[subject]["year"]
        if ya != yb:
            conflicts.append(
                {
                    "conflict_id": f"year_conflict_{subject}",
                    "type": "numeric_difference",
                    "subject": subject,
                    "model_a_years": [ya],
                    "model_b_years": [yb],
                    "model_a_claim": map_a[subject]["sentence"],
                    "model_b_claim": map_b[subject]["sentence"],
                    "description": "Patent year inconsistency on same subject.",
                }
            )

    years_a = _extract_years(answer_a)
    years_b = _extract_years(answer_b)
    if years_a and years_b and set(years_a) != set(years_b) and not conflicts:
        conflicts.append(
            {
                "conflict_id": "year_conflict_generic",
                "type": "numeric_difference",
                "model_a_years": years_a,
                "model_b_years": years_b,
                "description": "Potential year inconsistency detected.",
            }
        )

    matcher = difflib.SequenceMatcher(a=answer_a, b=answer_b)
    similarity = matcher.ratio()

    summary_bits = []
    if consensus:
        summary_bits.append(f"共识句{len(consensus)}条")
    if a_only:
        summary_bits.append(f"模型A独有{len(a_only)}条")
    if b_only:
        summary_bits.append(f"模型B独有{len(b_only)}条")
    if conflicts:
        summary_bits.append(f"冲突{len(conflicts)}项")
    if not summary_bits:
        summary_bits.append("未发现显著分歧")

    return {
        "summary": "，".join(summary_bits),
        "similarity_ratio": round(similarity, 4),
        "consensus": consensus,
        "model_a_only": a_only,
        "model_b_only": b_only,
        "conflicts": conflicts,
    }
