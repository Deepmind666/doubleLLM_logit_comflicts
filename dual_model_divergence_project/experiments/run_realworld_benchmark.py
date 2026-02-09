import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.decoupler import restructure  # noqa: E402
from modules.divergence_detector import compare_answers  # noqa: E402
from modules.evidence_retriever import fetch_evidence  # noqa: E402
from modules.fusion_generator import generate_fused_answer  # noqa: E402


CASES_FILE = Path(__file__).with_name("realworld_cases.json")
CATALOG_FILE = Path(__file__).with_name("realworld_evidence_catalog.json")
REPORT_FILE = Path(__file__).with_name("realworld_benchmark_report.md")


@dataclass
class LayerStats:
    total: int = 0
    passed: int = 0


def _load_cases() -> List[Dict]:
    data = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("realworld_cases.json must contain a list.")
    return data


def _pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "N/A"
    return f"{(numerator / denominator) * 100:.1f}%"


def _evaluate_case(case: Dict) -> Dict:
    answer_a = str(case.get("model_a_answer", "")).strip()
    answer_b = str(case.get("model_b_answer", "")).strip()
    if not answer_a or not answer_b:
        raise ValueError("Each realworld case must provide model_a_answer and model_b_answer.")

    diff_result = compare_answers(answer_a, answer_b)
    structured = restructure(answer_a=answer_a, answer_b=answer_b, diff_result=diff_result)
    evidence = fetch_evidence(diff_result.get("conflicts", []))
    final_answer = generate_fused_answer(
        answer_a=answer_a,
        answer_b=answer_b,
        diff_result=diff_result,
        structured=structured,
        evidence=evidence,
    )

    expect = dict(case.get("expect", {}))
    observed_ids = {str(c.get("conflict_id", "")) for c in diff_result.get("conflicts", []) if c.get("conflict_id")}
    expected_ids = {str(x) for x in list(expect.get("conflict_ids", []))}

    checks: List[Dict] = []

    # Layer-1: conflict detection
    layer1_pass = observed_ids == expected_ids
    checks.append(
        {
            "layer": "L1",
            "type": "conflict_set",
            "passed": layer1_pass,
            "message": f"expected_conflicts={sorted(expected_ids)}, observed_conflicts={sorted(observed_ids)}",
        }
    )

    # Layer-2: evidence adjudication
    layer2_pass = True
    for cid, expected_verdict in dict(expect.get("expected_verdicts", {})).items():
        actual_verdict = evidence.get(cid, {}).get("verdict", "missing")
        passed = actual_verdict == expected_verdict
        layer2_pass = layer2_pass and passed
        checks.append(
            {
                "layer": "L2",
                "type": "verdict",
                "passed": passed,
                "message": f"{cid} verdict expected={expected_verdict}, actual={actual_verdict}",
            }
        )

    for cid, expected_auto in dict(expect.get("expected_auto_applied", {})).items():
        actual_auto = evidence.get(cid, {}).get("auto_applied", "missing")
        passed = actual_auto == bool(expected_auto)
        layer2_pass = layer2_pass and passed
        checks.append(
            {
                "layer": "L2",
                "type": "auto_applied",
                "passed": passed,
                "message": f"{cid} auto_applied expected={bool(expected_auto)}, actual={actual_auto}",
            }
        )

    # Layer-3: fusion output
    layer3_pass = True
    for token in list(expect.get("final_must_contain", [])):
        passed = str(token) in final_answer
        layer3_pass = layer3_pass and passed
        checks.append(
            {
                "layer": "L3",
                "type": "final_contains",
                "passed": passed,
                "message": f"final contains '{token}'",
            }
        )

    return {
        "case_id": str(case.get("id", "unknown_case")),
        "tier_group": str(case.get("tier_group", "UNSPECIFIED")),
        "source_ref": str(case.get("source_ref", "")),
        "checks": checks,
        "layer1_pass": layer1_pass,
        "layer2_pass": layer2_pass,
        "layer3_pass": layer3_pass,
        "case_passed": all(c["passed"] for c in checks),
        "expected_conflicts": expected_ids,
        "observed_conflicts": observed_ids,
    }


def _safe_divide(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _build_aggregate(results: List[Dict]) -> Dict:
    layer_stats = {
        "L1": LayerStats(),
        "L2": LayerStats(),
        "L3": LayerStats(),
    }
    tier_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    total_cases = len(results)
    pass_cases = 0
    total_checks = 0
    pass_checks = 0

    tp = 0
    fp = 0
    fn = 0

    for r in results:
        if r["case_passed"]:
            pass_cases += 1

        layer_stats["L1"].total += 1
        layer_stats["L2"].total += 1
        layer_stats["L3"].total += 1
        if r["layer1_pass"]:
            layer_stats["L1"].passed += 1
        if r["layer2_pass"]:
            layer_stats["L2"].passed += 1
        if r["layer3_pass"]:
            layer_stats["L3"].passed += 1

        tier = r["tier_group"]
        tier_stats[tier]["cases_total"] += 1
        if r["layer1_pass"]:
            tier_stats[tier]["layer1_pass"] += 1
        if r["layer2_pass"]:
            tier_stats[tier]["layer2_pass"] += 1
        if r["layer3_pass"]:
            tier_stats[tier]["layer3_pass"] += 1
        if r["case_passed"]:
            tier_stats[tier]["cases_pass"] += 1

        expected = set(r["expected_conflicts"])
        observed = set(r["observed_conflicts"])
        tp += len(expected & observed)
        fp += len(observed - expected)
        fn += len(expected - observed)

        for c in r["checks"]:
            total_checks += 1
            if c["passed"]:
                pass_checks += 1

    precision = _safe_divide(tp, tp + fp)
    recall = _safe_divide(tp, tp + fn)
    f1 = _safe_divide(2 * precision * recall, precision + recall) if precision + recall > 0 else 0.0

    return {
        "total_cases": total_cases,
        "pass_cases": pass_cases,
        "total_checks": total_checks,
        "pass_checks": pass_checks,
        "layer_stats": layer_stats,
        "tier_stats": tier_stats,
        "conflict_tp": tp,
        "conflict_fp": fp,
        "conflict_fn": fn,
        "conflict_precision": precision,
        "conflict_recall": recall,
        "conflict_f1": f1,
    }


def _fmt_ratio(value: float) -> str:
    return f"{value * 100:.1f}%"


def _write_report(results: List[Dict], agg: Dict):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    lines: List[str] = []
    lines.append("# Realworld Benchmark Report")
    lines.append("")
    lines.append(f"- Timestamp: `{timestamp}`")
    lines.append(f"- Cases passed: `{agg['pass_cases']}/{agg['total_cases']}` ({_pct(agg['pass_cases'], agg['total_cases'])})")
    lines.append(f"- Checks passed: `{agg['pass_checks']}/{agg['total_checks']}` ({_pct(agg['pass_checks'], agg['total_checks'])})")
    lines.append("")
    lines.append("## Layer Metrics")
    lines.append("")
    for layer in ["L1", "L2", "L3"]:
        stat = agg["layer_stats"][layer]
        lines.append(f"- {layer} pass: `{stat.passed}/{stat.total}` ({_pct(stat.passed, stat.total)})")
    lines.append("")
    lines.append("## Conflict Detection Error Analysis")
    lines.append("")
    lines.append(f"- TP: `{agg['conflict_tp']}`")
    lines.append(f"- FP: `{agg['conflict_fp']}`")
    lines.append(f"- FN: `{agg['conflict_fn']}`")
    lines.append(f"- Precision: `{_fmt_ratio(agg['conflict_precision'])}`")
    lines.append(f"- Recall: `{_fmt_ratio(agg['conflict_recall'])}`")
    lines.append(f"- F1: `{_fmt_ratio(agg['conflict_f1'])}`")
    lines.append("")
    lines.append("## Tier Breakdown")
    lines.append("")
    lines.append("| tier_group | cases | case_pass_rate | L1_pass | L2_pass | L3_pass |")
    lines.append("|---|---|---|---|---|---|")
    for tier in sorted(agg["tier_stats"].keys()):
        t = agg["tier_stats"][tier]
        total = int(t["cases_total"])
        lines.append(
            "| {tier} | {cases} | {case_rate} | {l1} | {l2} | {l3} |".format(
                tier=tier,
                cases=total,
                case_rate=_pct(int(t["cases_pass"]), total),
                l1=_pct(int(t["layer1_pass"]), total),
                l2=_pct(int(t["layer2_pass"]), total),
                l3=_pct(int(t["layer3_pass"]), total),
            )
        )
    lines.append("")
    lines.append("## Case Details")
    lines.append("")
    lines.append("| case_id | source_ref | tier_group | result | failed_checks |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        failed = [c["message"] for c in r["checks"] if not c["passed"]]
        failed_text = " ; ".join(failed) if failed else "-"
        lines.append(
            f"| {r['case_id']} | {r['source_ref']} | {r['tier_group']} | {'PASS' if r['case_passed'] else 'FAIL'} | {failed_text} |"
        )

    lines.append("")
    lines.append("## Layered Findings")
    lines.append("")
    l1_fail = [r["case_id"] for r in results if not r["layer1_pass"]]
    l2_fail = [r["case_id"] for r in results if not r["layer2_pass"]]
    l3_fail = [r["case_id"] for r in results if not r["layer3_pass"]]
    lines.append(f"- Layer-1 (conflict detection) failures: `{len(l1_fail)}` -> `{l1_fail}`")
    lines.append(f"- Layer-2 (evidence adjudication) failures: `{len(l2_fail)}` -> `{l2_fail}`")
    lines.append(f"- Layer-3 (fusion output) failures: `{len(l3_fail)}` -> `{l3_fail}`")

    REPORT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    if not CATALOG_FILE.exists():
        raise FileNotFoundError(f"Missing evidence catalog: {CATALOG_FILE}")
    original_catalog = os.environ.get("EVIDENCE_CATALOG_PATH")
    os.environ["EVIDENCE_CATALOG_PATH"] = str(CATALOG_FILE)

    agg = None
    try:
        cases = _load_cases()
        results: List[Dict] = []
        for case in cases:
            results.append(_evaluate_case(case))
        agg = _build_aggregate(results)
        _write_report(results, agg)
    finally:
        if original_catalog is None:
            os.environ.pop("EVIDENCE_CATALOG_PATH", None)
        else:
            os.environ["EVIDENCE_CATALOG_PATH"] = original_catalog

    if agg is None:
        raise RuntimeError("realworld benchmark did not complete successfully.")

    print(f"Realworld benchmark report generated: {REPORT_FILE}")
    print(f"Cases passed: {agg['pass_cases']}/{agg['total_cases']}")

    if agg["pass_cases"] != agg["total_cases"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
