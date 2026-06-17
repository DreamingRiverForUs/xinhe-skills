#!/bin/bash
# ============================================================
# 扫描五一杯/数模写作空间，提取参赛队号
#
# 用法:
#   ./extract_team_numbers.sh
#
# 前置条件:
#   - /mnt/nas/xinhe_paper 已挂载
#   - 五一杯_paperIDs.csv 在同目录下 （格式: paperID,title,createdAt）
#
# 输出: 五一杯_team_numbers.csv (paperID,title,team_number,source_file,status)
#
# 注意: 只扫描 main.tex，不 fallback 到 chapters/chapter1.tex
#       （chapter1.tex 的 tcode 块里有模板示例 \baominghao{4321}，会误报）
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CSV_INPUT="${SCRIPT_DIR}/五一杯_paperIDs.csv"
CSV_OUTPUT="${SCRIPT_DIR}/五一杯_team_numbers.csv"
NAS_BASE="/mnt/nas/xinhe_paper"

# ── 检查前置条件 ──────────────────────────────────────
if [[ ! -f "$CSV_INPUT" ]]; then
    echo "[错误] 找不到 $CSV_INPUT" >&2
    exit 1
fi

if [[ ! -d "$NAS_BASE" ]]; then
    echo "[错误] NAS 挂载点 $NAS_BASE 不可访问" >&2
    exit 1
fi

# ── 提取核心函数 ──────────────────────────────────────
extract_team_number() {
    local file="$1"
    [[ -f "$file" ]] || return 1

    local result
    result=$(grep -v '^[[:space:]]*%' "$file" 2>/dev/null \
        | grep -oP '\\baominghao\{[^}]*\}' \
        | head -1 \
        | sed 's/\\baominghao{//;s/}//' \
        | xargs)

    # 过滤模板占位符（xxxx / xxxxxxxxxxxx / 4321 都是模板示例值）
    if [[ -n "$result" && "$result" != "xxxx" && "$result" != "xxxxxxxxxxxx" && "$result" != "4321" ]]; then
        echo "$result"
        return 0
    fi
    return 1
}

# ── 主流程 ────────────────────────────────────────────
echo "开始扫描..."
echo ""

total=0
found=0
missing=0
start_time=$(date +%s)

echo "paperID,title,team_number,source_file,status" > "$CSV_OUTPUT"

while IFS= read -r line; do
    total=$((total + 1))

    paperid="${line%%,*}"
    rest="${line#*,}"
    created_at="${rest##*,}"
    title="${rest%"${rest##*,}"}"
    title="${title%,}"
    title="${title#\"}"
    title="${title%\"}"

    if (( total % 50 == 0 )) || (( total == 1 )); then
        now=$(date +%s)
        elapsed=$((now - start_time))
        rate=$(awk "BEGIN {printf \"%.1f\", ${total}/${elapsed}}" 2>/dev/null || echo "0")
        echo "  进度: ${total}  已找到: ${found}  速率: ${rate}/秒"
    fi

    main_tex="${NAS_BASE}/${paperid}/workspace/workspace/main.tex"

    team_number=""
    source_file=""
    status=""

    if [[ -f "$main_tex" ]]; then
        team_number=$(extract_team_number "$main_tex" || true)
        if [[ -n "$team_number" ]]; then
            source_file="${paperid}/workspace/workspace/main.tex"
            status="成功"
            found=$((found + 1))
        else
            status="未填写"
            missing=$((missing + 1))
        fi
    else
        status="文件不存在"
        missing=$((missing + 1))
    fi

    echo "${paperid},\"${title}\",${team_number},${source_file},${status}" >> "$CSV_OUTPUT"
done < <(tail -n +2 "$CSV_INPUT")

end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo ""
echo "============================================================"
echo "扫描完成 (耗时 ${elapsed} 秒)"
echo "  总数:       ${total}"
echo "  成功提取:   ${found}"
echo "  未填写/缺:  ${missing}"
echo "  结果文件:   ${CSV_OUTPUT}"
echo "============================================================"
