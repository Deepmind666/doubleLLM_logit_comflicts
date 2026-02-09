import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import run_pipeline  # noqa: E402
from modules.database import DatabaseManager  # noqa: E402
from modules.evidence_retriever import fetch_evidence  # noqa: E402


CASES_FILE = Path(__file__).with_name("benchmark_cases.json")
REPORT_FILE = Path(__file__).with_name("benchmark_report.md")


def _load_cases() -> List[Dict]:
    data = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("benchmark_cases.json must contain a list.")
    return data


def _collect_pipeline_artifacts(db_file: Path) -> Dict:
    db = DatabaseManager(str(db_file))
    with db._connect() as conn:
        q_row = conn.execute("SELECT id FROM queries ORDER BY id DESC LIMIT 1").fetchone()
        if not q_row:
            return {"conflicts": [], "evidence": {}}
        query_id = int(q_row[0])

        d_row = conn.execute(
            "SELECT diff_detail FROM divergences WHERE query_id=? ORDER BY id DESC LIMIT 1",
            (query_id,),
        ).fetchone()
        conflicts = []
        if d_row and d_row[0]:
            try:
                diff = json.loads(d_row[0])
                conflicts = diff.get("conflicts", []) if isinstance(diff, dict) else []
            except Exception:
                conflicts = []

        evidence_rows = conn.execute(
            """
            SELECT diff_id, verdict, source_tier, auto_applied, confidence
            FROM evidence
            WHERE query_id=?
            """,
            (query_id,),
        ).fetchall()

    evidence: Dict[str, Dict] = {}
    for row in evidence_rows:
        evidence[str(row[0])] = {
            "verdict": str(row[1]) if row[1] is not None else "unknown",
            "source_tier": str(row[2]) if row[2] is not None else "",
            "auto_applied": bool(row[3]),
            "confidence": float(row[4]) if row[4] is not None else 0.0,
        }
    return {"conflicts": conflicts, "evidence": evidence}


def _run_pipeline_case(case: Dict) -> Dict:
    question = str(case.get("question", "")).strip()
    if not question:
        raise ValueError("pipeline case requires non-empty question.")
    with tempfile.TemporaryDirectory() as tmp:
        db_file = Path(tmp) / "benchmark.db"
        final_answer = run_pipeline(
            question=question,
            db_path=str(db_file),
            mock_mode=True,
            use_cache=False,
            enable_evidence=bool(case.get("enable_evidence", False)),
        )
        artifacts = _collect_pipeline_artifacts(db_file)
    return {
        "conflict_count": len(artifacts["conflicts"]),
        "conflicts": artifacts["conflicts"],
        "evidence": artifacts["evidence"],
        "final_answer": final_answer,
    }


def _run_evidence_only_case(case: Dict) -> Dict:
    conflicts = case.get("conflicts", [])
    if not isinstance(conflicts, list):
        raise ValueError("evidence_only case requires list conflicts.")
    evidence = fetch_evidence(conflicts)
    return {
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "evidence": evidence,
        "final_answer": "",
    }


def _evaluate_case(case: Dict, observed: Dict) -> Tuple[bool, List[Dict]]:
    checks: List[Dict] = []
    expect = case.get("expect", {})

    if "conflict_count" in expect:
        expected_count = int(expect["conflict_count"])
        actual_count = int(observed.get("conflict_count", 0))
        passed = actual_count == expected_count
        checks.append(
            {
                "type": "conflict_count",
                "passed": passed,
                "message": f"conflict_count expected={expected_count}, actual={actual_count}",
            }
        )

    for cid, expected_verdict in dict(expect.get("expected_verdicts", {})).items():
        actual_verdict = observed.get("evidence", {}).get(cid, {}).get("verdict", "missing")
        passed = actual_verdict == expected_verdict
        checks.append(
            {
                "type": "verdict",
                "passed": passed,
                "message": f"{cid} verdict expected={expected_verdict}, actual={actual_verdict}",
            }
        )

    for cid, expected_auto in dict(expect.get("expected_auto_applied", {})).items():
        actual_auto = observed.get("evidence", {}).get(cid, {}).get("auto_applied", "missing")
        passed = actual_auto == bool(expected_auto)
        checks.append(
            {
                "type": "auto_applied",
                "passed": passed,
                "message": f"{cid} auto_applied expected={bool(expected_auto)}, actual={actual_auto}",
            }
        )

    for token in list(expect.get("final_must_contain", [])):
        final_answer = str(observed.get("final_answer", ""))
        passed = str(token) in final_answer
        checks.append(
            {
                "type": "final_contains",
                "passed": passed,
                "message": f"final contains '{token}'",
            }
        )

    return all(c["passed"] for c in checks), checks


def _pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "N/A"
    return f"{(numerator / denominator) * 100:.1f}%"


def _build_metrics(results: List[Dict]) -> Dict[str, int]:
    metrics = {
        "cases_total": len(results),
        "cases_pass": 0,
        "checks_total": 0,
        "checks_pass": 0,
        "conflict_checks_total": 0,
        "conflict_checks_pass": 0,
        "verdict_checks_total": 0,
        "verdict_checks_pass": 0,
        "auto_checks_total": 0,
        "auto_checks_pass": 0,
    }
    for r in results:
        if r["case_passed"]:
            metrics["cases_pass"] += 1
        for c in r["checks"]:
            metrics["checks_total"] += 1
            if c["passed"]:
                metrics["checks_pass"] += 1
            if c["type"] == "conflict_count":
                metrics["conflict_checks_total"] += 1
                if c["passed"]:
                    metrics["conflict_checks_pass"] += 1
            elif c["type"] == "verdict":
                metrics["verdict_checks_total"] += 1
                if c["passed"]:
                    metrics["verdict_checks_pass"] += 1
            elif c["type"] == "auto_applied":
                metrics["auto_checks_total"] += 1
                if c["passed"]:
                    metrics["auto_checks_pass"] += 1
    return metrics


def _write_report(results: List[Dict], metrics: Dict[str, int]):
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    lines: List[str] = []
    lines.append("# Benchmark Report")
    lines.append("")
    lines.append(f"- Timestamp: `{now}`")
    lines.append(f"- Cases passed: `{metrics['cases_pass']}/{metrics['cases_total']}` ({_pct(metrics['cases_pass'], metrics['cases_total'])})")
    lines.append(f"- Checks passed: `{metrics['checks_pass']}/{metrics['checks_total']}` ({_pct(metrics['checks_pass'], metrics['checks_total'])})")
    lines.append(
        f"- Conflict detection checks: `{metrics['conflict_checks_pass']}/{metrics['conflict_checks_total']}` ({_pct(metrics['conflict_checks_pass'], metrics['conflict_checks_total'])})"
    )
    lines.append(
        f"- Verdict checks: `{metrics['verdict_checks_pass']}/{metrics['verdict_checks_total']}` ({_pct(metrics['verdict_checks_pass'], metrics['verdict_checks_total'])})"
    )
    lines.append(
        f"- Auto-apply checks: `{metrics['auto_checks_pass']}/{metrics['auto_checks_total']}` ({_pct(metrics['auto_checks_pass'], metrics['auto_checks_total'])})"
    )
    lines.append("")
    lines.append("## Case Summary")
    lines.append("")
    lines.append("| case_id | kind | pass | failed_checks |")
    lines.append("|---|---|---|---|")
    for r in results:
        failed_msgs = [c["message"] for c in r["checks"] if not c["passed"]]
        failed_text = " ; ".join(failed_msgs) if failed_msgs else "-"
        lines.append(
            f"| {r['case_id']} | {r['kind']} | {'PASS' if r['case_passed'] else 'FAIL'} | {failed_text} |"
        )

    lines.append("")
    lines.append("## Check Details")
    lines.append("")
    for r in results:
        lines.append(f"### {r['case_id']}")
        lines.append(f"- Kind: `{r['kind']}`")
        lines.append(f"- Result: `{'PASS' if r['case_passed'] else 'FAIL'}`")
        for c in r["checks"]:
            lines.append(f"- [{'x' if c['passed'] else ' '}] `{c['type']}` {c['message']}")
        lines.append("")

    REPORT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    cases = _load_cases()
    results: List[Dict] = []
    any_fail = False

    for case in cases:
        case_id = str(case.get("id", "unknown_case"))
        kind = str(case.get("kind", "pipeline"))
        try:
            if kind == "pipeline":
                observed = _run_pipeline_case(case)
            elif kind == "evidence_only":
                observed = _run_evidence_only_case(case)
            else:
                raise ValueError(f"Unsupported case kind: {kind}")
            case_passed, checks = _evaluate_case(case, observed)
        except Exception as e:
            case_passed = False
            checks = [{"type": "execution", "passed": False, "message": f"execution error: {e}"}]

        if not case_passed:
            any_fail = True

        results.append(
            {
                "case_id": case_id,
                "kind": kind,
                "case_passed": case_passed,
                "checks": checks,
            }
        )

    metrics = _build_metrics(results)
    _write_report(results, metrics)

    print(f"Benchmark report generated: {REPORT_FILE}")
    print(f"Cases passed: {metrics['cases_pass']}/{metrics['cases_total']}")
    if any_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
