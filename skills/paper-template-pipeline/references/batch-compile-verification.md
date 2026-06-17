# Batch Compile Verification (批量编译验证)

Use when verifying a batch of already-structured official template repos — no adaptation, no PII scrubbing, just clone → compile → push.

## Trigger

"Compile verification for N official journal template repos (batch X)" — the repos already have `main.tex`, `references.bib`, and standard structure. Goal is to verify they still compile and push updated PDF.

## Workflow

Per-repo loop (run in parallel batches of 4 to avoid Docker cache contention):

```bash
# 1. Clone all repos into /tmp
cd /tmp && git clone git@github.com:iftaken/<repo>.git <repo>-work

# 2. Detect .tex filename (not always main.tex)
ls /tmp/<repo>-work/*.tex
# If main.tex absent, check for sample.tex, paper.tex, anor-article.tex etc.
# Use whatever .tex file exists as the compile target

# 3. Docker compile
cd /tmp/<repo>-work
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile <actual-filename>.tex

# 4. Commit + push (use -f if .gitignore blocks PDF)
git add <pdf-name>.pdf || git add -f <pdf-name>.pdf
git commit -m "verify: official template compile test passed"
git push origin main
```

## Pre-flight

```bash
mkdir -p ~/.cache/paper-tectonic
```

## Result classification

| Result | Action |
|--------|--------|
| **PASS** (exit 0, PDF ≥ 10KB) | Commit + push (use `-f` if gitignore blocks) |
| **PASS (alt filename)** (exit 0, e.g. sample.pdf / anor-article.pdf) | Commit + push the actual PDF name |
| **FAIL** (compile error, non-zero exit) | Report, skip push |
| **SKIP** (empty repo, missing .tex) | Report, skip |

## Pitfalls

- **Non-standard .tex filenames**: Some repos use alternative filenames like `sample.tex`, `anor-article.tex`, `paper.tex` instead of `main.tex`. These **DO compile fine** — just use the actual filename for the Docker compile command and the resulting PDF name for `git add`. Example: `tectonic -X compile sample.tex` → `git add sample.pdf`. Don't report these as FAIL; they're still valid compile results.
- **`.gitignore` blocking PDF push**: Many official template repos have `.gitignore` rules like `*.pdf` that block `git add main.pdf`. Use `git add -f main.pdf` to override. Without `-f`, the add silently fails and no commit is created.
- **Empty repos**: Clone succeeds but no files. Report as SKIP.
- **No PII scrubbing for official publisher templates**: When explicitly told "no PII scrubbing", skip the pii-scrubbing step entirely. Official journal templates don't contain personal data.
- **Sequential only**: Don't parallelize Docker compiles — tectonic cache (`~/.cache/paper-tectonic`) doesn't support concurrent writes and will cause non-deterministic failures.
- **All compile warnings are cosmetic**: lineno.sty UTF-8 warnings, overfull/underfull hbox/vbox, font substitution warnings, algorithm.sty encoding warnings, pdffmx object redefinition warnings — all are cosmetic and don't affect PDF output. Exit code 0 + PDF ≥ 10KB = PASS regardless of warnings.

## Summary format

```
[1/14] repo-name: PASS
[2/14] repo-name: PASS
...
[6/14] repo-name: FAIL — reason
...
[14/14] repo-name: SKIP — reason

Totals: N PASS / M FAIL / K SKIP
```
