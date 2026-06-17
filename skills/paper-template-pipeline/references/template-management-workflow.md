# Template Management: Import + Submit-Audit Flow

## Overview

Templates go through: **draft → pending → published** (NOT draft → published directly).

| Status | Scope | Meaning |
|--------|-------|---------|
| draft | private | Created, not yet submitted for review |
| pending | private | Submitted for admin review (shows in admin dashboard 模板审核) |
| published | public | Admin approved, visible in marketplace |

## Import via WebBridge

Script: `scripts/bulk_import_templates.py` in xinhe-paper CLI project.

Key technique: React controlled inputs require native value setter. See `kimi-webbridge/skill:references/react-controlled-input-workaround.md`.

Usage:
```bash
# Single
python3 scripts/bulk_import_templates.py --single --repo "acl-template" --name "ACL 期刊模板" --desc "..." --tags "ACL,期刊" --category "期刊论文"

# Batch
python3 scripts/bulk_import_templates.py /tmp/templates.csv

# Resume
python3 scripts/bulk_import_templates.py /tmp/templates.csv --start-from 50
```

CSV format: `repo_name,display_name,description,tags,category,branch,subdir`

## Submit for Review (submit-audit)

Equivalent to clicking "分享到模板市场" on the website.

Database operation: set `status = 'pending'` and populate `auditInfo`:
```json
{"notes": "", "auditId": "audit_{timestamp}_{id_prefix}", "submittedAt": "ISO timestamp"}
```

Script: `scripts/bulk_submit_audit.py` in xinhe-paper CLI project.
```bash
python3 scripts/bulk_submit_audit.py          # all drafts
python3 scripts/bulk_submit_audit.py --limit 5  # first 5
python3 scripts/bulk_submit_audit.py --dry-run  # preview
```

After submit, templates appear in admin dashboard at `http://192.168.31.32:6796/templates` for admin approval.

## API Endpoint

The web UI calls: `POST https://api.huimengxinhe.com/api/v1/my-templates/{templateId}/submit-audit`

Auth: cookie-based (same-site from paper.huimengxinhe.com). Direct curl from external origins fails due to CORS and cookie isolation. Use the DB script instead.

## Pitfalls

- **Never set status to 'published' directly** — bypasses admin review queue. Always use `status = 'pending'` for submission.
- **WebBridge network monitoring** does not capture SPA API calls made before the page fully loads. For API discovery, inspect database state instead.
- **WebBridge fetch from browser context** may fail with CORS for cross-origin API calls even with `credentials:'include'` if cookies are httpOnly or cross-site.
