from typing import Dict, List


def _conflict_line(conflict_id: str, verdict: str) -> str:
    if verdict == "A":
        return f"- {conflict_id}: 采用模型A结论。"
    if verdict == "B":
        return f"- {conflict_id}: 采用模型B结论。"
    return f"- {conflict_id}: 暂无充分证据，保留多解。"


def generate_fused_answer(
    answer_a: str,
    answer_b: str,
    diff_result: Dict,
    structured: Dict,
    evidence: Dict,
) -> str:
    consensus = [u.get("text", "") for u in structured.get("consensus_units", []) if u.get("text")]
    a_only = [u.get("text", "") for u in structured.get("model_a_units", []) if u.get("text")]
    b_only = [u.get("text", "") for u in structured.get("model_b_units", []) if u.get("text")]
    conflicts = [c for c in structured.get("conflict_units", []) if isinstance(c, dict)]

    adjudicated_lines: List[str] = []
    pending_lines: List[str] = []
    for c in conflicts:
        cid = str(c.get("conflict_id", "unknown_conflict"))
        info = evidence.get(cid, {})
        verdict = str(info.get("verdict", "unknown"))
        line = _conflict_line(cid, verdict)
        if verdict in {"A", "B"}:
            adjudicated_lines.append(line)
        else:
            pending_lines.append(line)

    lines = []
    lines.append("【融合答案】")

    if consensus:
        lines.append("共识区：")
        for c in consensus:
            lines.append(f"- {c}")

    if a_only or b_only:
        lines.append("补充区：")
        for x in a_only:
            lines.append(f"- 来自模型A：{x}")
        for x in b_only:
            lines.append(f"- 来自模型B：{x}")

    if adjudicated_lines:
        lines.append("裁决区：")
        lines.extend(adjudicated_lines)

    if pending_lines:
        lines.append("待验证区：")
        lines.extend(pending_lines)

    if not lines or len(lines) == 1:
        # fallback for fully empty parse result: keep both raw answers for human review
        lines.append("待验证区：")
        lines.append("- 未提取到稳定结构化结果，保留双模型原始回答。")
        lines.append(f"- 模型A原始回答：{answer_a}")
        lines.append(f"- 模型B原始回答：{answer_b}")

    return "\n".join(lines)
