from typing import Dict


def generate_fused_answer(
    answer_a: str,
    answer_b: str,
    diff_result: Dict,
    structured: Dict,
    evidence: Dict,
) -> str:
    consensus = [u["text"] for u in structured.get("consensus_units", [])]
    a_only = [u["text"] for u in structured.get("model_a_units", [])]
    b_only = [u["text"] for u in structured.get("model_b_units", [])]
    conflicts = structured.get("conflict_units", [])

    lines = []
    lines.append("【融合答案】")

    if consensus:
        lines.append("共识信息：")
        for c in consensus:
            lines.append(f"- {c}")

    if a_only or b_only:
        lines.append("补充信息：")
        for x in a_only:
            lines.append(f"- 来自模型A：{x}")
        for x in b_only:
            lines.append(f"- 来自模型B：{x}")

    if conflicts:
        lines.append("分歧与处理：")
        for c in conflicts:
            cid = c.get("conflict_id", "unknown_conflict")
            info = evidence.get(cid, {})
            verdict = info.get("verdict", "unknown")
            if verdict == "A":
                lines.append(f"- {cid}: 采用模型A结论。")
            elif verdict == "B":
                lines.append(f"- {cid}: 采用模型B结论。")
            else:
                lines.append(f"- {cid}: 暂无充分证据，保留多解。")

    if not (consensus or a_only or b_only or conflicts):
        # fallback for fully empty parse result
        lines.append(answer_a if len(answer_a) >= len(answer_b) else answer_b)

    return "\n".join(lines)

