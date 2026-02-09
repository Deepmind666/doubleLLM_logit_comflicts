from pathlib import Path


ABSTRACT_MD = Path("patent_cn/04_spec/abstract.md")
REPORT_MD = Path("patent_cn/06_packaging/abstract_len_check.md")
MAX_LEN = 300


def extract_abstract_text(md: str) -> str:
    lines = []
    for line in md.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        lines.append(s)
    return "".join(lines)


def main():
    text = ABSTRACT_MD.read_text(encoding="utf-8")
    content = extract_abstract_text(text)
    count = len(content)
    passed = count <= MAX_LEN

    report = [
        "# 摘要字数检查",
        "",
        f"- 文件：`{ABSTRACT_MD}`",
        f"- 字数（含标点，不含Markdown标题）：`{count}`",
        f"- 阈值：`<= {MAX_LEN}`",
        f"- 结果：`{'PASS' if passed else 'FAIL'}`",
    ]
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

