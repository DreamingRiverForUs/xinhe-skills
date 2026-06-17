# Deep-Dive Analysis Patterns

Supplementary analysis workflows beyond the basic queries in SKILL.md.

## Pattern D: Search Log Analysis (Template Gap Discovery)

When user wants to understand what users are searching for but NOT finding — reveals template gaps.

### Step 1: Query zero-result searches

The CLI has no built-in command for this. Use the .venv Python directly:

```bash
cd /Users/ming/project/cli_xinhe_status && .venv/bin/python -c "
import asyncio
from xinhe_paper.db import safe_query, init_pool, close_pool, db_session

async def main():
    await init_pool()
    async with db_session():
        # Zero-result searches
        results = await safe_query(
            '''SELECT keyword, COUNT(*) AS search_count,
               COUNT(DISTINCT source) AS sources
            FROM \"template_search_log\"
            WHERE result_count = 0
            GROUP BY keyword ORDER BY search_count DESC''',
            limit=100
        )
        total = await safe_query('SELECT COUNT(*) as cnt FROM \"template_search_log\"', limit=1)
        total_zero = await safe_query('SELECT COUNT(*) as cnt FROM \"template_search_log\" WHERE result_count = 0', limit=1)
        tc = total[0]['cnt']
        tz = total_zero[0]['cnt']
        print(f'Total searches: {tc}  Zero-result: {tz} ({tz/tc*100:.1f}%)')
        print()
        for i,r in enumerate(results,1):
            print(f'{i:2}. {r[\"keyword\"]:<40} {r[\"search_count\"]:>3} searches  sources:{r[\"sources\"]}')

        # Top successful searches for comparison
        nonzero = await safe_query(
            '''SELECT keyword, COUNT(*) AS search_count, AVG(result_count) AS avg_results
            FROM \"template_search_log\" WHERE result_count > 0
            GROUP BY keyword ORDER BY search_count DESC''', limit=15
        )
        print()
        print('=== Top 15 successful searches ===')
        for i,r in enumerate(nonzero,1):
            print(f'{i:2}. {r[\"keyword\"]:<35} {r[\"search_count\"]:>3} searches  avg{r[\"avg_results\"]:.1f} results')

    await close_pool()

asyncio.run(main())
"
```

### Step 2: Categorize the results

Zero-result searches fall into four categories:

1. **学校名搜索** — users typing university names expecting school-specific templates. Biggest missed opportunity. Sort by search count, prioritize top ones.
2. **学科/方向搜索** — "网络安全", "中药", "物流" etc. Users treating 心河Paper as a general-purpose paper tool.
3. **具体论文题目** — "圈养湖羊的空间利用率", "物流网络集包规则及设备优化". Users searching for templates by topic. Not actionable for templates but useful for content strategy.
4. **Typo/奇怪的** — "电工被"→"电工杯", "数字meiti"→"数字媒体". Search experience bugs.

### Step 3: Cross-reference with successful searches

Compare zero-result keywords (学位论文, university names) vs successful keywords (竞赛 names) to understand the platform's actual vs perceived positioning.

## Domain Knowledge

### COMPLETED status is meaningless

The `step = 'COMPLETED'` field in ChatSession is a legacy architecture artifact. It has no business significance. Do NOT use completed session counts as a metric in analysis. The meaningful metrics are: total sessions, unique users, and session time distribution.

### Payment/revenue fields are stripped

The CLI intentionally hides all payment and revenue data. `paid_sessions`, `total_revenue`, `paymentAmount`, `isPaid` are removed from all tool outputs. Do not attempt to query or report on revenue — the data is not exposed by design.

### Platform is competition-driven

心河Paper's current traffic is almost entirely driven by 数学建模 (math modeling) competitions. Template usage follows competition schedules — sharp spikes during competition windows, rapid decline after. This is the "pulse pattern." University thesis templates (like 华中农业大学) show smoother, more sustained usage curves.
