import difflib
import re
from typing import Dict, List, Set, Tuple


MATCH_W1 = 0.7  # semantic similarity
MATCH_W2 = 0.2  # rule similarity
MATCH_W3 = 0.1  # relative position
MATCH_THRESHOLD = 0.72

NEGATION_PATTERNS = [
    r"\bnot\b",
    r"\bno\b",
    r"\bnever\b",
    r"\bcannot\b",
    r"\bcan't\b",
    r"\bisn't\b",
    r"\baren't\b",
    r"\bwon't\b",
    r"不是",
    r"并非",
    r"不(?:是|会|能|可|应|要|对|好|行|利|宜)",
    r"不可",
    r"不能",
    r"无",
    r"未",
    r"没有",
]


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？!?;\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _extract_years(text: str) -> List[str]:
    return re.findall(r"(19\d{2}|20\d{2})", text)


def _normalize_sentence(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"[\s\t\r\n]+", "", t)
    t = re.sub(r"[，,。.!！？?；;:：\(\)\[\]\"'`~\-_/\\]+", "", t)
    return t


def _char_ngrams(text: str, n: int = 2) -> Set[str]:
    t = _normalize_sentence(text)
    if not t:
        return set()
    if len(t) <= n:
        return {t}
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def _semantic_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=_normalize_sentence(a), b=_normalize_sentence(b)).ratio()


def _rule_similarity(a: str, b: str) -> float:
    years_a = set(_extract_years(a))
    years_b = set(_extract_years(b))
    if years_a and years_b:
        year_score = 1.0 if (years_a & years_b) else 0.0
    else:
        year_score = 0.5

    ngram_score = _jaccard(_char_ngrams(a, n=2), _char_ngrams(b, n=2))
    return 0.6 * ngram_score + 0.4 * year_score


def _position_score(i: int, j: int, len_a: int, len_b: int) -> float:
    if len_a <= 1 and len_b <= 1:
        return 1.0
    ai = i / max(1, len_a - 1)
    bj = j / max(1, len_b - 1)
    return max(0.0, 1.0 - abs(ai - bj))


def _has_negation(text: str) -> bool:
    t = text.lower()
    return any(re.search(pat, t) for pat in NEGATION_PATTERNS)


def _strip_negation(text: str) -> str:
    t = text.lower()
    for pat in NEGATION_PATTERNS:
        t = re.sub(pat, "", t)
    return _normalize_sentence(t)


def _is_negation_contradiction(a: str, b: str) -> bool:
    a_neg = _has_negation(a)
    b_neg = _has_negation(b)
    if a_neg == b_neg:
        return False

    a_core = _strip_negation(a)
    b_core = _strip_negation(b)
    if not a_core or not b_core:
        return False
    score = difflib.SequenceMatcher(a=a_core, b=b_core).ratio()
    return score >= 0.82


def _extract_subject_hint(text: str) -> str:
    m_pred = re.search(r"([A-Za-z0-9\u4e00-\u9fff_-]{1,40}?)(?:不是|是|拥有|用于|专利)", text)
    if m_pred:
        return m_pred.group(1)
    m = re.search(r"([A-Za-z0-9\u4e00-\u9fff_-]{2,40})", text)
    return m.group(1) if m else "UNKNOWN"


def _normalize_subject_name(subject: str) -> str:
    s = (subject or "").strip().strip("，,。.!！？?；;:：")
    s = re.sub(r"(公司|集团|股份有限公司)$", "", s)
    s = re.sub(r"的.*$", "", s)
    s = re.sub(r"'s$", "", s, flags=re.I)
    return s or subject


def _extract_year_claims(sentences: List[str]) -> List[Dict]:
    claims: List[Dict] = []
    for idx, s in enumerate(sentences):
        m_cn = re.search(
            r"(?P<subject>[A-Za-z0-9\u4e00-\u9fff_-]{1,40})专利(?:申请)?于(?P<year>19\d{2}|20\d{2})年",
            s,
        )
        if m_cn:
            claims.append(
                {
                    "subject": _normalize_subject_name(m_cn.group("subject")),
                    "year": m_cn.group("year"),
                    "sentence": s,
                    "sentence_index": idx,
                }
            )
            continue

        m_cn_alt1 = re.search(
            r"(?P<subject>[A-Za-z0-9\u4e00-\u9fff_-]{1,40})(?:公司)?在(?P<year>19\d{2}|20\d{2})年(?:向[\u4e00-\u9fffA-Za-z0-9_-]{1,40})?(?:提交|递交|提出)(?:了)?(?:[\u4e00-\u9fffA-Za-z0-9_-]{0,20})专利(?:申请)?",
            s,
        )
        if m_cn_alt1:
            claims.append(
                {
                    "subject": _normalize_subject_name(m_cn_alt1.group("subject")),
                    "year": m_cn_alt1.group("year"),
                    "sentence": s,
                    "sentence_index": idx,
                }
            )
            continue

        m_cn_alt2 = re.search(
            r"(?P<subject>[A-Za-z0-9\u4e00-\u9fff_-]{1,40})(?:公司)?(?:的)?(?:[\u4e00-\u9fffA-Za-z0-9_-]{0,20})专利(?:是|为)?(?P<year>19\d{2}|20\d{2})年(?:申请|提交|公开)(?:的)?",
            s,
        )
        if m_cn_alt2:
            claims.append(
                {
                    "subject": _normalize_subject_name(m_cn_alt2.group("subject")),
                    "year": m_cn_alt2.group("year"),
                    "sentence": s,
                    "sentence_index": idx,
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
                    "subject": _normalize_subject_name(m_en.group("subject")),
                    "year": m_en.group("year"),
                    "sentence": s,
                    "sentence_index": idx,
                }
            )
    return claims


def _first_sentence_with_year(sentences: List[str]) -> str:
    for s in sentences:
        if _extract_years(s):
            return s
    return ""


def _match_sentences(a_sents: List[str], b_sents: List[str]) -> List[Dict]:
    candidates: List[Tuple[float, float, int, int, float, float, float]] = []
    for i, sa in enumerate(a_sents):
        for j, sb in enumerate(b_sents):
            # Keep contradiction candidates out of consensus matching.
            if _is_negation_contradiction(sa, sb):
                continue
            semantic = _semantic_similarity(sa, sb)
            rule = _rule_similarity(sa, sb)
            pos = _position_score(i, j, len(a_sents), len(b_sents))
            score = MATCH_W1 * semantic + MATCH_W2 * rule + MATCH_W3 * pos
            if score >= MATCH_THRESHOLD:
                candidates.append((score, semantic, i, j, rule, pos, score))

    candidates.sort(reverse=True, key=lambda x: (x[0], x[1]))
    used_a: Set[int] = set()
    used_b: Set[int] = set()
    matches: List[Dict] = []
    for _, semantic, i, j, rule, pos, score in candidates:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        matches.append(
            {
                "a_index": i,
                "b_index": j,
                "a_text": a_sents[i],
                "b_text": b_sents[j],
                "semantic_score": round(float(semantic), 4),
                "rule_score": round(float(rule), 4),
                "position_score": round(float(pos), 4),
                "match_score": round(float(score), 4),
            }
        )
    return matches


def _detect_contradictions(
    a_only_indices: List[int],
    b_only_indices: List[int],
    a_sents: List[str],
    b_sents: List[str],
) -> List[Dict]:
    candidates: List[Tuple[float, int, int]] = []
    for i in a_only_indices:
        for j in b_only_indices:
            sa = a_sents[i]
            sb = b_sents[j]
            if not _is_negation_contradiction(sa, sb):
                continue
            base_score = difflib.SequenceMatcher(a=_strip_negation(sa), b=_strip_negation(sb)).ratio()
            candidates.append((base_score, i, j))

    candidates.sort(reverse=True, key=lambda x: x[0])
    used_a: Set[int] = set()
    used_b: Set[int] = set()
    contradictions: List[Dict] = []
    for score, i, j in candidates:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        sa = a_sents[i]
        sb = b_sents[j]
        subject = _extract_subject_hint(sa)
        contradictions.append(
            {
                "conflict_id": f"contradiction_conflict_{subject}_{len(contradictions)+1}",
                "type": "contradiction",
                "subject": subject,
                "model_a_claim": sa,
                "model_b_claim": sb,
                "description": "Semantically similar statements with opposite polarity detected.",
                "confidence_hint": round(float(score), 4),
            }
        )
    return contradictions


def compare_answers(answer_a: str, answer_b: str) -> Dict:
    a_sents = _split_sentences(answer_a)
    b_sents = _split_sentences(answer_b)

    matches = _match_sentences(a_sents, b_sents)
    matched_a = {m["a_index"] for m in matches}
    matched_b = {m["b_index"] for m in matches}

    a_only_indices = [i for i in range(len(a_sents)) if i not in matched_a]
    b_only_indices = [j for j in range(len(b_sents)) if j not in matched_b]

    a_only = [a_sents[i] for i in a_only_indices]
    b_only = [b_sents[j] for j in b_only_indices]
    consensus = [m["a_text"] if len(m["a_text"]) <= len(m["b_text"]) else m["b_text"] for m in matches]

    conflicts: List[Dict] = []

    claims_a = _extract_year_claims(a_sents)
    claims_b = _extract_year_claims(b_sents)
    map_a = {c["subject"]: c for c in claims_a}
    map_b = {c["subject"]: c for c in claims_b}

    # Type 1: numeric_difference
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

    # Type 2: omission (claim appears in one side only)
    for subject in sorted(set(map_a) - set(map_b)):
        conflicts.append(
            {
                "conflict_id": f"omission_conflict_{subject}_missing_in_B",
                "type": "omission",
                "subject": subject,
                "missing_in": "B",
                "model_a_claim": map_a[subject]["sentence"],
                "model_b_claim": "",
                "description": "Subject claim appears in model A but missing in model B.",
            }
        )
    for subject in sorted(set(map_b) - set(map_a)):
        conflicts.append(
            {
                "conflict_id": f"omission_conflict_{subject}_missing_in_A",
                "type": "omission",
                "subject": subject,
                "missing_in": "A",
                "model_a_claim": "",
                "model_b_claim": map_b[subject]["sentence"],
                "description": "Subject claim appears in model B but missing in model A.",
            }
        )

    # Type 3: contradiction (opposite polarity on similar statements)
    contradictions = _detect_contradictions(a_only_indices, b_only_indices, a_sents, b_sents)
    conflicts.extend(contradictions)

    years_a = _extract_years(answer_a)
    years_b = _extract_years(answer_b)
    numeric_conflicts = [c for c in conflicts if c.get("type") == "numeric_difference"]
    if years_a and years_b and set(years_a) != set(years_b) and not numeric_conflicts:
        conflicts.append(
            {
                "conflict_id": "year_conflict_generic",
                "type": "numeric_difference",
                "subject": "GENERIC",
                "model_a_years": years_a,
                "model_b_years": years_b,
                "model_a_claim": _first_sentence_with_year(a_sents),
                "model_b_claim": _first_sentence_with_year(b_sents),
                "description": "Potential year inconsistency detected.",
            }
        )

    similarity = difflib.SequenceMatcher(a=answer_a, b=answer_b).ratio()

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
        "model_a_sentences": a_sents,
        "model_b_sentences": b_sents,
        "model_a_only_indices": a_only_indices,
        "model_b_only_indices": b_only_indices,
        "sentence_matches": matches,
        "conflicts": conflicts,
    }
