import re
from pathlib import Path


CLAIMS_MD = Path("patent_cn/03_claims/claims_final.md")
SPEC_MD = Path("patent_cn/04_spec/spec_draft.md")
DRAWINGS_MD = Path("patent_cn/05_drawings/drawings_list.md")
REPORT_MD = Path("patent_cn/06_packaging/cnipa_format_check.md")


def check_claim_numbering(claims_text: str):
    nums = [int(n) for n in re.findall(r"^##\s*权利要求(\d+)", claims_text, re.M)]
    if not nums:
        return False, nums, "未检测到权利要求编号标题。"
    expected = list(range(1, len(nums) + 1))
    ok = nums == expected
    msg = "连续" if ok else f"不连续，检测到{nums}，预期{expected}"
    return ok, nums, msg


def check_fig_references(spec_text: str):
    required_figs = [f"图{i}" for i in range(1, 7)]
    missing = [f for f in required_figs if f not in spec_text]
    return len(missing) == 0, missing


def check_module_marks(spec_text: str, drawings_text: str):
    marks = ["101", "102A", "102B", "103", "104", "105", "106", "107", "108", "109", "110"]
    miss_in_spec = [m for m in marks if m not in spec_text]
    miss_in_drawings = [m for m in marks if m not in drawings_text]
    return len(miss_in_spec) == 0 and len(miss_in_drawings) == 0, miss_in_spec, miss_in_drawings


def check_term_consistency(spec_text: str, claims_text: str):
    terms = ["模型A", "模型B", "论点单元", "分歧点", "结构化解耦", "子问题", "裁决记录"]
    result = []
    for t in terms:
        in_spec = t in spec_text
        in_claims = t in claims_text
        result.append((t, in_spec, in_claims, in_spec and in_claims))
    all_ok = all(r[3] for r in result)
    return all_ok, result


def check_drawings_files(drawings_text: str):
    expected = [
        "fig1_system_architecture.png",
        "fig2_method_flow.png",
        "fig3_disagreement_graph.png",
        "fig4_decoupling_subquestions.png",
        "fig5_iteration_feedback_loop.png",
        "fig6_data_structure.png",
    ]
    missing = [f for f in expected if f not in drawings_text]
    return len(missing) == 0, missing


def main():
    claims_text = CLAIMS_MD.read_text(encoding="utf-8")
    spec_text = SPEC_MD.read_text(encoding="utf-8")
    drawings_text = DRAWINGS_MD.read_text(encoding="utf-8")

    n_ok, nums, n_msg = check_claim_numbering(claims_text)
    f_ok, f_missing = check_fig_references(spec_text)
    m_ok, miss_spec, miss_drawings = check_module_marks(spec_text, drawings_text)
    t_ok, t_rows = check_term_consistency(spec_text, claims_text)
    d_ok, d_missing = check_drawings_files(drawings_text)

    passed = all([n_ok, f_ok, m_ok, t_ok, d_ok])

    lines = [
        "# CNIPA 形式与一致性检查",
        "",
        f"- 总体结果：`{'PASS' if passed else 'FAIL'}`",
        "",
        "## 1) 权利要求编号连续性",
        f"- 检测结果：`{'PASS' if n_ok else 'FAIL'}`",
        f"- 详情：{n_msg}",
        f"- 编号序列：{nums}",
        "",
        "## 2) 说明书附图引用完整性（图1~图6）",
        f"- 检测结果：`{'PASS' if f_ok else 'FAIL'}`",
        f"- 缺失图号：{f_missing if f_missing else '无'}",
        "",
        "## 3) 模块标记一致性（101~110）",
        f"- 检测结果：`{'PASS' if m_ok else 'FAIL'}`",
        f"- 说明书缺失：{miss_spec if miss_spec else '无'}",
        f"- 附图清单缺失：{miss_drawings if miss_drawings else '无'}",
        "",
        "## 4) 术语一致性（说明书 vs 权利要求）",
        f"- 检测结果：`{'PASS' if t_ok else 'FAIL'}`",
        "",
        "| 术语 | 说明书出现 | 权利要求出现 | 结果 |",
        "|---|---|---|---|",
    ]
    for t, s, c, ok in t_rows:
        lines.append(f"| {t} | {s} | {c} | {'PASS' if ok else 'FAIL'} |")

    lines.extend(
        [
            "",
            "## 5) 附图清单文件名完整性",
            f"- 检测结果：`{'PASS' if d_ok else 'FAIL'}`",
            f"- 缺失文件名：{d_missing if d_missing else '无'}",
        ]
    )

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

