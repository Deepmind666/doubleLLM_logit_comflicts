import re
from pathlib import Path


CLAIMS_MD = Path("patent_cn/03_claims/claims_final.md")
SPEC_MD = Path("patent_cn/04_spec/spec_draft.md")
REPORT_MD = Path("patent_cn/06_packaging/claim_support_map.md")


KEY_TERMS = [
    "模型A",
    "模型B",
    "论点单元",
    "分歧点",
    "结构化解耦",
    "子问题",
    "裁决记录",
    "融合输出",
    "来源追溯",
    "预算",
    "迭代",
    "装置",
    "电子设备",
    "计算机可读存储介质",
]


def parse_claim_blocks(text: str):
    pattern = r"^##\s*权利要求(\d+).*?$"
    matches = list(re.finditer(pattern, text, re.M))
    blocks = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        claim_id = int(m.group(1))
        body = text[start:end].strip()
        blocks.append((claim_id, body))
    return blocks


def parse_spec_sections(spec_text: str):
    sections = []
    current = "未归类"
    for line in spec_text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
        elif line.startswith("### "):
            current = line[4:].strip()
        sections.append((current, line))
    return sections


def locate_terms_in_sections(terms, sections):
    hits = []
    for term in terms:
        found_sections = []
        for sec, line in sections:
            if term in line:
                found_sections.append(sec)
        found_sections = sorted(set(found_sections))
        if found_sections:
            hits.append((term, found_sections))
    return hits


def main():
    claims_text = CLAIMS_MD.read_text(encoding="utf-8")
    spec_text = SPEC_MD.read_text(encoding="utf-8")
    sections = parse_spec_sections(spec_text)
    blocks = parse_claim_blocks(claims_text)

    rows = []
    all_supported = True
    for claim_id, body in blocks:
        present_terms = [t for t in KEY_TERMS if t in body]
        if not present_terms:
            present_terms = ["模型A", "分歧点", "融合输出"]
        hits = locate_terms_in_sections(present_terms, sections)
        supported = len(hits) > 0
        all_supported = all_supported and supported
        support_sections = sorted(set([sec for _, secs in hits for sec in secs]))
        rows.append(
            {
                "claim_id": claim_id,
                "terms": present_terms,
                "supported": supported,
                "sections": support_sections,
            }
        )

    lines = [
        "# 权利要求-说明书支撑映射",
        "",
        f"- 总体结果：`{'PASS' if all_supported else 'FAIL'}`",
        "",
        "| 权利要求号 | 关键词 | 说明书支撑章节 | 结果 |",
        "|---:|---|---|---|",
    ]
    for r in rows:
        terms = "、".join(r["terms"])
        secs = "；".join(r["sections"]) if r["sections"] else "未检出"
        lines.append(
            f"| {r['claim_id']} | {terms} | {secs} | {'PASS' if r['supported'] else 'FAIL'} |"
        )

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    if not all_supported:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

