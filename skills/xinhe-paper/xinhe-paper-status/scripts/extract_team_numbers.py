#!/usr/bin/env python3
"""
扫描特定模板的写作空间，提取参赛队号。

数据源: 五一杯_paperIDs.csv (paperID, title, createdAt)
扫描路径: /mnt/nas/xinhe_paper/{paperID}/workspace/workspace/main.tex
提取模式: \baominghao{xxx}

输出: 五一杯_team_numbers.csv (paperID, title, team_number, source_file, status)

用法:
    cd /Users/ming/project/cli_xinhe_status
    python3 scripts/extract_team_numbers.py
"""

import csv
import re
import sys
import time
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
CSV_INPUT = Path(__file__).resolve().parent.parent / "五一杯_paperIDs.csv"
CSV_OUTPUT = Path(__file__).resolve().parent.parent / "五一杯_team_numbers.csv"
NAS_BASE = Path("/mnt/nas/xinhe_paper")
TARGET_FILE = "workspace/workspace/main.tex"

# 正则：匹配 \baominghao{...}，花括号内容即为队号
# 排除注释行（% 开头）、模板占位符（xxxx）
RE_BAOMINGHAO = re.compile(
    r'(?<!\s*%[^\n]*)\\baominghao\s*\{([^}]*)\}'
)


def extract_team_number(filepath: Path) -> tuple[str | None, str | None]:
    """从 main.tex 中提取参赛队号。

    Returns:
        (team_number, source_file) — team_number 为 None 表示未找到
    """
    candidates = [
        filepath,
        filepath.parent / "chapters" / "chapter1.tex",
    ]

    for fp in candidates:
        if not fp.exists():
            continue
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue

        match = RE_BAOMINGHAO.search(content)
        if match:
            team_number = match.group(1).strip()
            if team_number and team_number not in ("xxxx", "xxxxxxxxxxxx"):
                return team_number, str(fp.relative_to(NAS_BASE))
    
    return None, None


def main():
    if not CSV_INPUT.exists():
        print(f"错误: 找不到 {CSV_INPUT}", file=sys.stderr)
        print("请先运行查询生成该文件。", file=sys.stderr)
        sys.exit(1)

    if not NAS_BASE.exists():
        print(f"错误: NAS 挂载点 {NAS_BASE} 不可访问", file=sys.stderr)
        print("请确认 NAS 已挂载。", file=sys.stderr)
        sys.exit(1)

    papers = []
    with open(CSV_INPUT, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)

    total = len(papers)
    print(f"共 {total} 个 paperID 待扫描")

    results = []
    found_count = 0
    missing_count = 0

    t0 = time.time()

    for i, paper in enumerate(papers):
        paper_id = paper["paperID"]
        title = paper.get("title", "")
        main_tex = NAS_BASE / paper_id / TARGET_FILE

        if (i + 1) % 50 == 0 or i == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"  进度: {i+1}/{total} ({rate:.1f} 个/秒)  已找到: {found_count}")

        team_number = None
        source_file = None
        status = ""

        if not main_tex.exists():
            status = "文件不存在"
            missing_count += 1
        else:
            team_number, source_file = extract_team_number(main_tex)
            if team_number:
                status = "成功"
                found_count += 1
            else:
                status = "未填写"
                missing_count += 1

        results.append({
            "paperID": paper_id,
            "title": title,
            "team_number": team_number or "",
            "source_file": source_file or "",
            "status": status,
        })

    elapsed = time.time() - t0

    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["paperID", "title", "team_number", "source_file", "status"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"扫描完成 (耗时 {elapsed:.1f} 秒)")
    print(f"  总数:       {total}")
    print(f"  成功提取:   {found_count}")
    print(f"  未填写/缺:  {missing_count}")
    print(f"  结果文件:   {CSV_OUTPUT}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
