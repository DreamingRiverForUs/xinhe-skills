# xinhe-paper CLI 完整参考

路径: `/Users/ming/project/cli_xinhe_status/.venv/bin/xinhe-paper`

## 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `overview` | 平台数据概览 | 用户数、模板数、会话数 |
| `top-templates` | 热门模板排行 | `-d 7 -l 10` (7天Top10) |
| `zero-result-searches` | 搜索零结果 | `--days 7 --limit 20` |
| `search-templates` | 模糊搜索模板 | |
| `template-detail` | 模板详情 | `--id <id>` |
| `template-usage` | 模板使用趋势 | `--id <id>` |
| `search-sessions` | 搜索写作会话 | |

## 典型用法

```bash
XINHE="/Users/ming/project/cli_xinhe_status/.venv/bin/xinhe-paper"

# 全景
$XINHE overview

# 本周热门
$XINHE top-templates -d 7 -l 10

# 本月热门
$XINHE top-templates -d 30 -l 15

# 本周需求缺口
$XINHE zero-result-searches --days 7 --limit 20

# 月需求缺口
$XINHE zero-result-searches --days 30 --limit 30
```
