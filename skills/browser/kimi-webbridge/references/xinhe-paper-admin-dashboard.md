# 心河Paper Admin Dashboard

> URL: `http://192.168.31.32:6796/` (local Vite dev server, React SPA)
> Access: WebBridge `navigate` with `newTab:true` → `snapshot` for data extraction
> Data model: accessibility-tree-based extraction. Charts are SVG with StaticText axis labels — no inline data values. Tables are standard `<table>` with row/column text content.

## Page Map

| 侧栏菜单 | @e ref | 内容 |
|----------|--------|------|
| 数据看板 | @e1 | Dashboard homepage — top-level metrics, charts, conversion funnel, template rankings |
| 用户管理 | @e2 | User list |
| 会员管理 | @e3 | Subscription management |
| 额度管理 | @e4 | Credit management |
| 订单管理 | @e5 | Menu — expands to sub-items |
| ├ 订单列表(旧版) | @e6 | Old order list |
| └ 订单列表(新版) | @e7 | New order list — total orders, paid/unpaid breakdown, per-order detail |
| 配置管理 | @e8 | Pricing config |
| 数据统计 | @e9 | Menu — expands to sub-items |
| ├ 转化报表 | @e10 | Payment conversion report — free→subscriber by day/week/month |
| └ 收入报表 | @e11 | Revenue report — daily breakdown by plan type |
| 客服二维码 | @e12 | CS QR code |
| AI 配置 | @e13 | AI model config |
| ECI 容器管理 | @e14 | Container management |
| GitHub 配置 | @e15 | GitHub integration |
| API Key 管理 | @e16 | API keys |
| 模板审核 | @e17 | Template review |
| 检索词管理 | @e18 | Search terms |
| 教程管理 | @e19 | Tutorial management |

Note: @e refs are relative to dashboard SPA and may shift between deploys. Always use `snapshot` to get current refs before clicking.

## Key Pages for Data Extraction

### 1. 数据看板 (Dashboard)

**Top metrics (summary cards):**
- 今日注册用户, 注册总人数, 今日订单数, 今日收入

**Charts (SVG-based, extract axis labels + table below):**
- 用户注册趋势 (radio: 近7天/近30天/近90天)
- 订单趋势 (radio: same)
- 收入趋势 (radio: same)

**Conversion funnel (section below charts):**
- 统计口径: 用户数（去重）
- 用户行为分布 pie chart + legend
- 总注册用户 / 活跃用户数 / 使用率
- 模板子漏斗: 使用模板 → 产生对话 → 转化率
- 降重子漏斗: 使用降重
- 用户行为明细: 仅模板/仅降重/两者都用/未使用功能

**Daily detail table (below funnel):**
Columns: 日期, 新增注册, 仅模板, 仅降重, 两者, 未使用, 使用(模板), 对话(模板), 转化(模板), 使用(降重)

**Template rankings (below table):**
- 总使用次数排名
- 最近7天使用次数排名
- 当日使用量排名

### 2. 转化报表 (/reports/conversion)

Date range picker (default: last 7 days), radio: 按日/按周/按月

Summary: 总用户数, 免费用户, 订阅用户, 转化率

Table: 日期, 免费用户, 订阅用户, 转化率, Basic转化, Pro转化, Pro Max转化, 升级数, 续费率

### 3. 收入报表 (/reports/income)

Date range picker, radio: 按日/按周/按月

Summary: 总收入, 总退款, 净收入

Table: 日期, 总收入, 单篇收入, 会员收入, 额度包收入, 降重收入, 退款金额

### 4. 订单管理（新版）

Summary cards: 总订单数, 已支付订单, 实际收入, 待支付订单

已支付订单分类: 会员订阅(单数+金额), 降重包, 额度包

Order table: 订单号, 用户, 类型, 金额, 状态(已支付/待支付), 支付时间, 创建时间

## Extraction Pattern

Charts don't expose data values in the accessibility tree — only axis labels. To get chart data, extract the detail table below each chart instead. The table always contains the same data rendered in the chart.

```bash
# Navigate
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"http://192.168.31.32:6796/","newTab":true},"session":"hermes"}'

# Snapshot + extract all text in one pass
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"snapshot","args":{},"session":"hermes"}' | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
tree = data['data']['tree']
def find_texts(node):
    results = []
    if isinstance(node, dict):
        if node.get('role') in ('StaticText','InlineTextBox') and node.get('name'):
            results.append(node['name'])
        if 'children' in node:
            for c in node['children']: results.extend(find_texts(c))
    elif isinstance(node, list):
        for c in node: results.extend(find_texts(c))
    return results
for t in find_texts(tree): print(t)
"
```

To switch time ranges: click the radio button @e refs (e.g., @e18 for 近30天 on user registration chart). All three chart radio groups must be clicked separately if you want all charts in 30-day view.
