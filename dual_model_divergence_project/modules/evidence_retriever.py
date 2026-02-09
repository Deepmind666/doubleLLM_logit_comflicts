import json
import os
from pathlib import Path
from typing import Dict, List


TIER_RANK = {"L1": 3, "L2": 2, "L3": 1}


def _normalize_subject(s: str) -> str:
    return s.strip().lower().replace("技术", "").replace(" ", "")


def _catalog_path() -> Path:
    env = os.getenv("EVIDENCE_CATALOG_PATH")
    if env:
        return Path(env)
    return Path("data") / "evidence_catalog.json"


def _load_catalog() -> List[Dict]:
    path = _catalog_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def _select_verdict(conflict: Dict, evidences: List[Dict]) -> Dict:
    years_a = set(conflict.get("model_a_years", []))
    years_b = set(conflict.get("model_b_years", []))
    if not years_a and not years_b:
        return {
            "verdict": "unknown",
            "evidence_text": "No candidate years in conflict payload.",
            "source": "",
            "source_tier": "",
            "auto_applied": False,
            "confidence": 0.0,
        }

    # Highest available tier first
    evidences = sorted(evidences, key=lambda x: TIER_RANK.get(x.get("tier", "L3"), 1), reverse=True)
    by_tier: Dict[str, List[Dict]] = {"L1": [], "L2": [], "L3": []}
    for e in evidences:
        t = e.get("tier", "L3")
        by_tier.setdefault(t, []).append(e)

    selected_year = None
    selected_tier = ""
    auto_applied = False

    # Gate 1: any L1 can auto-apply.
    if by_tier.get("L1"):
        selected_year = by_tier["L1"][0].get("year")
        selected_tier = "L1"
        auto_applied = True
    else:
        # Gate 2: at least two independent L2 with same year can auto-apply.
        l2 = by_tier.get("L2", [])
        year_counts: Dict[str, int] = {}
        sources_per_year: Dict[str, set] = {}
        for e in l2:
            y = str(e.get("year", ""))
            if not y:
                continue
            year_counts[y] = year_counts.get(y, 0) + 1
            sources_per_year.setdefault(y, set()).add(str(e.get("source", "")))
        for y, cnt in year_counts.items():
            if cnt >= 2 and len(sources_per_year.get(y, set())) >= 2:
                selected_year = y
                selected_tier = "L2"
                auto_applied = True
                break

    if not selected_year:
        # Low-tier only or insufficient evidence -> keep unresolved
        return {
            "verdict": "unknown",
            "evidence_text": "Only low-tier or insufficient independent evidence; keep unresolved.",
            "source": "; ".join([str(e.get("source", "")) for e in evidences if e.get("source")])[:500],
            "source_tier": "L3_or_insufficient",
            "auto_applied": False,
            "confidence": 0.35 if evidences else 0.0,
        }

    verdict = "unknown"
    if selected_year in years_a and selected_year not in years_b:
        verdict = "A"
    elif selected_year in years_b and selected_year not in years_a:
        verdict = "B"
    elif selected_year in years_a and selected_year in years_b:
        verdict = "unknown"

    confidence = 0.92 if selected_tier == "L1" else 0.78
    return {
        "verdict": verdict,
        "evidence_text": f"Selected year={selected_year} via {selected_tier} gate.",
        "source": "; ".join([str(e.get("source", "")) for e in evidences if e.get("source")])[:500],
        "source_tier": selected_tier,
        "auto_applied": auto_applied and verdict in {"A", "B"},
        "confidence": confidence,
    }


def fetch_evidence(conflicts: List[Dict]) -> Dict[str, Dict]:
    """
    Stage-2 evidence resolver with tiered gating.
    Auto-adjudication is allowed only when:
    - any L1 evidence exists, or
    - at least two independent L2 evidences agree.
    Otherwise keep unresolved.
    """
    catalog = _load_catalog()
    norm_index: Dict[str, List[Dict]] = {}
    for item in catalog:
        subject = _normalize_subject(str(item.get("subject", "")))
        if subject:
            norm_index.setdefault(subject, []).append(item)

    result: Dict[str, Dict] = {}
    for c in conflicts:
        cid = str(c.get("conflict_id", "unknown_conflict"))
        ctype = c.get("type")
        if ctype != "numeric_difference":
            result[cid] = {
                "verdict": "unknown",
                "evidence_text": "Unsupported conflict type for evidence adjudication.",
                "source": "",
                "source_tier": "",
                "auto_applied": False,
                "confidence": 0.0,
            }
            continue

        subject = _normalize_subject(str(c.get("subject", "")))
        evidences = norm_index.get(subject, [])
        result[cid] = _select_verdict(c, evidences)
    return result

