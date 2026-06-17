---
name: xinhe-paper-status
version: 1.1.0
description: "Query 心河Paper platform data: template usage stats, user activity, session analytics, template search. Use when user asks about template usage stats, platform overview, user activity, template performance, session data, or any 心河Paper operational metrics."
metadata:
  requires:
    bins: ["/Users/ming/project/cli_xinhe_status/.venv/bin/xinhe-paper"]
---

# 心河Paper Status CLI

Real-time read-only query tool for the 心河Paper PostgreSQL database. Provides pre-built safe queries — no raw SQL exposed. All payment/revenue data has been stripped from output; this tool only shows usage metrics.

**For WRITE operations** (publishing templates, updating status): use `write_query()` from `xinhe_paper.db` — bypasses the read-only check. See §7 Writing to the Database.

**CLI path:** `/Users/ming/project/cli_xinhe_status/.venv/bin/xinhe-paper`

## 1. When to Use

Trigger this skill whenever the user asks about:

- Template usage stats ("华中农业大学的模板使用情况", "which templates are most used")
- Platform overview ("平台数据怎么样", "overview", "最近用户活跃度")
- Session analysis ("最近有哪些写作会话", "search sessions")
- Any question about 心河Paper operational data that the database can answer

The CLI connects to the production PostgreSQL database (read-only, with multi-layer protection).

## 2. Available Commands

### search-templates — Fuzzy search paper templates

```bash
xinhe-paper search-templates -k "<keyword>" [-c <category>] [-s <status>] [--scope <scope>] [-l <limit>]
```

Options:
- `-k, --keyword` (required): Search keyword (matches name, description, tags)
- `-c, --category`: Filter by category (e.g., "BACHELOR_THESIS", "MASTER_THESIS")
- `-s, --status`: Filter by status (e.g., "published")
- `--scope`: Filter by scope (e.g., "public")
- `-l, --limit`: Max results (default 20)

### template-usage — Get usage stats for a template

```bash
xinhe-paper template-usage --id <template_uuid>
```

This is the **core command**. Returns:
- Summary: total sessions, unique users, completed sessions
- Time distribution: daily usage over last 30 days
- Degree distribution: user degree breakdown

Note: payment/revenue fields are hidden by design.

### template-detail — Get template details

```bash
xinhe-paper template-detail --id <template_uuid>
```

### top-templates — Hot template leaderboard

```bash
xinhe-paper top-templates [-c <category>] [-d <days>] [-l <limit>]
```

Options:
- `-c, --category`: Filter by category
- `-d, --days`: Recent N days (omit for all-time)
- `-l, --limit`: Max results (default 10)

### search-sessions — Search writing sessions

```bash
xinhe-paper search-sessions [-k <keyword>] [--template-id <uuid>] [--paid/--unpaid] [--degree <degree>] [-l <limit>]
```

Options:
- `-k, --keyword`: Search in titles and topics
- `--template-id`: Filter by template
- `--paid/--unpaid`: Payment status filter (note: payment amount is NOT shown, only the filter flag)
- `--degree`: Filter by degree
- `-l, --limit`: Max results (default 20)

### zero-result-searches — Find keywords with no matching templates

```bash
xinhe-paper zero-result-searches [-d <days>] [-l <limit>]
```

Returns search keywords that returned zero results, sorted by search count. Shows which searches are "falling through the cracks" — users are searching for things the platform doesn't have.

Options:
- `-d, --days`: Recent N days (default 30)
- `-l, --limit`: Max results (default 50)

### overview — Platform overview dashboard

```bash
xinhe-paper overview
```

Returns: total users, 7d/30d active users, 30d new users, total sessions, completed sessions, 7d/30d sessions, total/published/public templates, total template usage.

No payment or revenue data included.

## 3. Workflow Patterns

### Pattern A: "某学校/某关键词的模板使用情况"

```
1. search-templates -k "<keyword>"     → get template IDs
2. template-usage --id <uuid>          → for each relevant template
3. [optional] raw query via safe_query → dive into sessions (see §5, search-sessions CLI is broken)
```

### Pattern B: "最近平台整体情况"

```
1. overview                            → platform dashboard
2. top-templates -d 7                  → recent hot templates
3. top-templates -d 30                 → monthly hot templates
```

### Pattern C: "最近用户都在搜索什么 / 哪些搜索没结果"

```
1. zero-result-searches -d 30 -l 20   → see what users want but can't find
2. overview                            → get user count and activity
3. top-templates -d 7 -l 10            → see what's trending
```

### Pattern D: "搜索日志分析 / 模板缺口发现"

See `references/deep-dive-analysis.md` for the full workflow including Python scripts.
This pattern reveals what users are searching for but NOT finding — identifies template gaps.

### Pattern E: "生成对外材料（评审/产品介绍/BP等）"

**Before writing ANY external-facing document, MUST load `references/external-doc-guidelines.md`.**

### Pattern G: "GitHub 模板仓库盘点 / 哪些仓库没上线"

See `references/github-template-inventory.md` for full workflow: pull PaperTemplate table → parse `remoteConfig.url` → cross-reference with `gh repo list iftaken`.

### Pattern F: "竞赛获奖匹配 / 哪些用户获奖了"

**Load `references/competition-result-matching.md` for the full workflow.**

Steps: ① 查模板 paperIDs → ② 扫描 NAS 写作空间提取队号 → ③ 解析获奖名单 PDF → ④ JOIN 匹配。 Critical rules:
- Never include operational data (user counts, template usage numbers, rankings)
- Always verify pricing/plans from paper.huimengxinhe.com/profile via Kimi WebBridge
- Output as self-contained HTML (see `templates/external-doc-template.html`), not PDF

### Pattern F: "从写作空间批量提取结构化数据"

When the user wants to extract metadata (team numbers, author names, school names) from paper workspace files on NAS — not from the database. Full workflow documented in `references/paper-workspace-extraction.md`.

```
1. search-templates -k "<关键词>"        → get template UUID
2. gh repo clone iftaken/<repo> --depth 1  → understand file structure
3. safe_query all sessions for template    → dump paperIDs to CSV
4. Write/run extraction script             → scan main.tex on NAS per paperID
```

Key mappings — template UUID → GitHub repo (add new entries here as discovered):

| Template UUID | Template Name | GitHub Repo |
|---|---|---|
| `00197479-0954-41c2-855c-bf61c6df2967` | 五一杯数学建模竞赛推荐模板 | `iftaken/51mcm-latex` |

A reusable extraction script template is at `scripts/extract_team_numbers.py`.

## 4. Data Safety & Domain Knowledge

- All queries are read-only (connection-level + SQL-level + DB-permission-level)
- Sensitive fields (password, apiKey, phone, email, openid, etc.) are auto-filtered at the DB layer
- Payment amounts and revenue are stripped at the tool level — do not attempt to report on revenue
- Max 1000 rows per query, 30s timeout
- **COMPLETED status is meaningless**: the `step = 'COMPLETED'` field is a legacy architecture artifact with no business significance. Do not use completed session counts as a metric
- **Platform is competition-driven**: traffic is almost entirely 数学建模 competition pulse traffic. Template usage spikes during competition windows and drops sharply after. University thesis templates show smoother, sustained curves
- **CALENDAR CONTEXT IS MANDATORY (pitfall)**: never present raw platform data without mapping it to the seasonal calendar first. 心河Paper has extreme seasonality: peak activity May–early June (电工杯 + provincial competitions), vacuum June–September (university summer break, no competitions), October spike (国赛), November–April slow. A 30-day window in mid-June shows inflated numbers from the just-ended competition season. If the user asks for \"6月数据分析\", the first thing to state is where we are on the calendar — not the raw metrics. Failing to anchor analysis in seasonality leads to wrong strategic conclusions (e.g., \"user growth is strong\" when it's just the tail end of competition pulse). Always explicitly answer: what month is it, what's the next competition window, what season are users in right now
- **OPERATIONAL DATA IS INTERNAL — NEVER EXPOSE IN EXTERNAL DOCS**: user counts, session counts, template usage numbers, Top-N rankings, and all quantitative metrics from this tool are core competitive data. Do NOT include these in external-facing documents (review applications, product introductions, marketing materials, pitch decks, funding applications). External docs may describe the platform qualitatively but must not cite specific numbers. If the user asks for external docs, query data for YOUR context only — do not paste numbers into the output
- **Pricing verification**: do not use memory for pricing/feature details in external docs. Memory may contain stale video-script conventions that differ from the live product. Open paper.huimengxinhe.com/profile via Kimi WebBridge, click "升级会员", and read the actual plan names, prices, and feature breakdowns from the page before writing

## 5. Known Issues & Workarounds

### Write Operations (write_query)

The CLI is read-only by default, but `db.py` now has a `write_query` function that bypasses the SQL write blacklist for controlled operations:

```python
from xinhe_paper.db import write_query
await write_query(
    'UPDATE "PaperTemplate" SET status = $1 WHERE id = $2',
    'pending', template_id
)
```

**Use only for:**
- Template status transitions (draft → pending for review)
- Audit info updates
- Scope changes

**Never use for:** destructive operations, bulk deletes, schema changes.

### Template Management Scripts

Located in `scripts/`:
- `bulk_import_templates.py` — WebBridge-based bulk import from GitHub repos
- `bulk_submit_audit.py` — Direct DB submit-audit for templates (draft → pending)

### search-sessions CLI is broken (`is_paid` vs `isPaid`)

The `xinhe-paper search-sessions` command has a parameter naming bug: the CLI passes `is_paid` but the underlying `tools.search_sessions()` function expects `isPaid` (camelCase). Any invocation with `--paid`/`--unpaid` triggers a `TypeError`. Even without those flags, the CLI may fail on other parameter mismatches.

**Workaround**: Bypass the CLI and call the tools module directly through the venv Python:

```bash
cd /Users/ming/project/cli_xinhe_status && .venv/bin/python -c "
import asyncio
from xinhe_paper.db import db_session, safe_query

async def main():
    async with db_session():
        sessions = await safe_query(
            'SELECT * FROM \"ChatSession\" WHERE \"templateId\" = \$1 ORDER BY \"createdAt\" DESC',
            '<template_uuid>', limit=30
        )
        for s in sessions:
            print(s)

asyncio.run(main())
"
```

See `references/db-schema-quickref.md` for table schemas and common query patterns.

### User nicknames are privacy-masked

The `User` table uses `nickname` (not `username`). Nickname values are privacy-masked in the database — only the first character + `****` is stored (e.g., `h****`, `****`). Full names/identities are not queryable through the read-only connection.

## 6. Common Queries

### Check what users are searching for with no results

```bash
xinhe-paper zero-result-searches -d 30 -l 20
```

### Check a specific university's template usage

```bash
xinhe-paper search-templates -k "华中农业大学" -l 20
xinhe-paper template-usage --id <uuid>
```

### See what's hot this week

```bash
xinhe-paper top-templates -d 7 -l 10
```

### Platform pulse check

```bash
xinhe-paper overview
```

### Find sessions for a specific template

```bash
xinhe-paper search-sessions --template-id <uuid> -l 30
```

## 7. Writing to the Database

`write_query()` was added to `xinhe_paper.db` to support template publishing. It bypasses the read-only SQL check.

### Publishing a draft template

```python
import asyncio, json, time
from xinhe_paper.db import db_session, write_query

async def publish(template_id):
    async with db_session():
        audit_info = json.dumps({
            "notes": "", "reason": "", "status": "published",
            "auditId": f"audit_{int(time.time()*1000)}_{template_id[:8]}",
            "reviewedAt": None, "reviewedBy": None
        })
        await write_query(
            'UPDATE "PaperTemplate" SET status = $1, scope = $2, "auditInfo" = $3, "updatedAt" = NOW() WHERE id = $4',
            'published', 'public', audit_info, template_id
        )
```

### Batch publish script

```bash
cd /Users/ming/project/cli_xinhe_status
.venv/bin/python scripts/bulk_publish.py           # publish all drafts
.venv/bin/python scripts/bulk_publish.py --dry-run  # preview only
.venv/bin/python scripts/bulk_publish.py --limit 5  # test 5
```

### Key fields for template publishing

| Field | Draft value | Published value |
|-------|------------|-----------------|
| `status` | `draft` | `published` |
| `scope` | `private` | `public` |
| `auditInfo` | NULL | JSON with `auditId`, `status: "published"` |

### Importing templates (WebBridge)

See `scripts/bulk_import_templates.py` — automates the web form for importing GitHub templates into 心河Paper.

**Pitfall**: React controlled inputs won't pick up direct `.value =` assignment. Must use native setter:

```js
var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(element, newValue);
element.dispatchEvent(new Event('input', {bubbles: true}));
```
