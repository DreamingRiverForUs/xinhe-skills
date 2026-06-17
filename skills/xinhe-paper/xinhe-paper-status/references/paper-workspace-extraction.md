# Paper Workspace Batch Extraction

When you need to extract structured data from the paper workspace files on NAS (not from the database), follow this workflow. Use case examples: extract team numbers, author names, school names, or any LaTeX metadata from paper source files.

## NAS Path Convention

```
/mnt/nas/xinhe_paper/{paperID}/workspace/workspace/
├── main.tex              ← primary metadata source
├── main.cls              ← document class (template logic, not data)
├── main.pdf              ← compiled output
├── chapters/
│   ├── abstract.tex
│   ├── chapter1.tex      ← sometimes has metadata (fallback)
│   └── ...
```

The paperID is the ChatSession UUID from the database.

## Workflow Pattern

### Step 1: Identify the template and its source repo

Query the template by name, note its UUID:

```bash
xinhe-paper search-templates -k "关键词" -l 20
```

Clone the template's source repo to understand where metadata is stored:

```bash
gh repo clone iftaken/<repo-name> -- --depth 1
```

Key: Read the SKILL.md-equivalent (often AGENTS.md or README.md) inside the repo to find where team info / metadata fields are defined.

### Step 2: Dump all paperIDs for this template

Use `safe_query` directly (the `search-sessions` CLI is broken):

```python
sessions = await safe_query(
    'SELECT id, title, "createdAt" FROM "ChatSession" WHERE "templateId" = $1 ORDER BY "createdAt" DESC',
    '<template_uuid>', limit=1000
)
```

Save to CSV with columns: `paperID, title, createdAt`.

### Step 3: Write an extraction script

Template for the script:

1. Read CSV of paperIDs
2. For each paperID, locate `{NAS_BASE}/{paperID}/workspace/workspace/main.tex`
3. Apply regex to extract the target field
4. Add a fallback: check `chapters/chapter1.tex` (users sometimes put metadata there)
5. Handle missing files, template placeholders (e.g., `xxxx`), and commented-out lines
6. Output results CSV with status column

Key patterns for the regex:
- Filter out commented lines: use negative lookbehind for `%` before the command
- Filter out template placeholders: match against known defaults (`xxxx`, `xxxxxxxxxxxx`)
- Use `re.DOTALL`-equivalent patterns for multi-line content

### Step 4: Run and verify

The script includes progress reporting (every N records) with throughput rate. Output columns should include `paperID, title, extracted_value, source_file, status` so you can trace every result.

## Known Template → Repo Mappings

| Template UUID | Template Name | GitHub Repo |
|---|---|---|
| `00197479-0954-41c2-855c-bf61c6df2967` | 五一杯数学建模竞赛推荐模板 | `iftaken/51mcm-latex` |

## 五一杯 Specifics

- Team number command: `\baominghao{xxx}` (12-digit number in production)
- Primary location: `main.tex`
- Fallback location: `chapters/chapter1.tex` (in LaTeX `tcode` environment — same regex works)
- Placeholder values to skip: `xxxx`, `xxxxxxxxxxxx`, empty `{}`
- Commented-out commands (`% \baominghao{...}`) are template defaults, not user data

## Pitfalls

- **NAS may not be mounted locally**: check `ls /mnt/nas/xinhe_paper/` first. If the mount point doesn't exist, the script must run on the machine where NAS is mounted.
- **Filesystem scan is I/O-bound**: 400+ directories over NAS can be slow. The script includes progress output so you can gauge throughput.
- **Don't assume `main.tex` exists**: some sessions may have been created but the workspace was never initialized. Handle missing files gracefully with a status column.
- **LaTeX commands may span lines**: simple cases like `\baominghao{xxx}` don't, but if extracting longer content, be aware of line breaks.
