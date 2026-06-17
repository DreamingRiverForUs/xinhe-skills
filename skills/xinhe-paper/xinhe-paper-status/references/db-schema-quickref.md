# Database Schema Quick Reference

For when you need to bypass the CLI and run raw queries via `safe_query` + `db_session`.

## Connection

```python
import asyncio
from xinhe_paper.db import db_session, safe_query

async def main():
    async with db_session():
        result = await safe_query('SELECT ...', limit=50)
        ...
asyncio.run(main())
```

Run with: `.venv/bin/python -c "..."` from `/Users/ming/project/cli_xinhe_status/`.

## Key Tables

### ChatSession

Columns (all camelCase, must be double-quoted in SQL):

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Session ID |
| `userId` | UUID | FK → User |
| `templateId` | UUID | FK → Template |
| `title` | text | Session title |
| `topic` | text | Research topic |
| `step` | text | Current step (COMPLETED is meaningless) |
| `degree` | text | Degree level (often NULL) |
| `major` | text | Major/field |
| `wordCount` | int | Current word count |
| `createdAt` | timestamp | |
| `updatedAt` | timestamp | |

### User

Columns:

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | |
| `nickname` | text | **Privacy-masked**: only first char + `****` (e.g. `h****`) |
| `avatarUrl` | text | WeChat avatar URL |
| `role` | text | e.g. `USER` |
| `isActive` | bool | |
| `webOpenId` | text | NULL for most users |
| `mpOpenId` | text | NULL for most users |
| `lastLogin` | timestamp | |
| `createdAt` | timestamp | |

No `username` or `email` column — use `nickname`.

### PaperTemplate

Columns (all camelCase, must be double-quoted in SQL):

**`remoteConfig` 结构**：jsonb，包含 `url` 字段存储 GitHub 仓库 URL（如 `https://github.com/iftaken/repo-name`）。提取方式：
```python
rc = t.get('remoteConfig') or {}
if isinstance(rc, str): rc = json.loads(rc)
github_url = rc.get('url', '')
```

| Column | Type | Notes |
|--------|------|-------|
| `id` | text | Template UUID |
| `name` | text | Display name |
| `description` | text | |
| `category` | text | e.g. BACHELOR_THESIS |
| `tags` | ARRAY | |
| `configJson` | jsonb | Template configuration |
| `coverFileKey` | text | S3/OSS cover image key |
| `ownerId` | text | |
| `scope` | text | e.g. public |
| `status` | text | draft / published |
| `auditInfo` | jsonb | |
| `usageCount` | integer | |
| `favoriteCount` | integer | |
| `isDefault` | boolean | |
| `sourceType` | text | Always 'github' for imported templates |
| `remoteConfig` | jsonb | **Contains `url` field with GitHub repo URL** |
| `cacheStatus` | text | |
| `cacheKey` | text | |
| `syncError` | text | |
| `commitHash` | text | Git commit pinned to this template version |
| `createdAt` | timestamp | |
| `updatedAt` | timestamp | |
| `lastSyncedAt` | timestamp | |
| `lastCheckedAt` | timestamp | |

Key: Extract GitHub repo from `remoteConfig->>'url'`. Parse `github.com/<owner>/<repo>` from the URL.

## Common Raw Queries

### Sessions for a template (with user info)

```sql
SELECT 
    s.id, s.title, s.topic, s."userId", s.degree, s.step,
    s."createdAt", u.nickname
FROM "ChatSession" s
LEFT JOIN "User" u ON u.id = s."userId"
WHERE s."templateId" = $1
ORDER BY s."createdAt" DESC
LIMIT 30
```

### Unique users for a template

```sql
SELECT DISTINCT s."userId", u.nickname, u."createdAt", u."lastLogin"
FROM "ChatSession" s
LEFT JOIN "User" u ON u.id = s."userId"
WHERE s."templateId" = $1
```

### Query all published templates with GitHub repos

```sql
SELECT id, name, status, "remoteConfig", "sourceType", "commitHash"
FROM "PaperTemplate"
WHERE status = 'published'
ORDER BY name
```

### Count templates by status

```sql
SELECT status, COUNT(*) FROM "PaperTemplate" GROUP BY status
```

```sql
SELECT
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT "userId") AS unique_users,
    COUNT(*) FILTER (WHERE step = 'COMPLETED') AS completed,
    TO_CHAR(DATE("createdAt"), 'YYYY-MM-DD') AS date,
    COUNT(*) AS daily_count
FROM "ChatSession"
WHERE "templateId" = $1
  AND "createdAt" >= NOW() - INTERVAL '30 days'
GROUP BY DATE("createdAt")
ORDER BY date DESC
```

## The `_quote_camel_case` Gotcha

`safe_query()` auto-wraps known camelCase column names in double quotes. This means:
- `templateId` in your SQL → `"templateId"` (correct PostgreSQL syntax)
- Write camelCase columns as-is — don't manually quote them
- But if a column name is NOT in the known-camelCase set, PostgreSQL will lowercase it silently

The known set includes: `templateId`, `userId`, `wordCount`, `usageCount`, `createdAt`, `updatedAt`, `lastLogin`, `webOpenId`, `mpOpenId`, `avatarUrl`, `lastSyncedAt`, `favoriteCount`, `isDefault`, `sourceType`, `cacheStatus`, and many more (see `db.py` lines 56-69 for the full `_CAMEL_CASE_COLUMNS` set).
