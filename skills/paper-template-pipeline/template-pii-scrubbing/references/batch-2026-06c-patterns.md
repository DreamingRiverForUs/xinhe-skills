# PII Patterns Discovered (June 2026 Batch C — 8 iftaken LaTeX Template Repos)

Third batch: hust-thesis through imust-proposal-template. Mix of English, Chinese, and empty repos.

## Repository: iiser-trivandrum-thesis (IISER Thiruvananthapuram Thesis)

English-language template. Multiple PII vectors: author name, personal GitHub, acknowledgement.

| Pattern | Location | Action |
|---------|----------|--------|
| `% Created by Joel Sleeba, MSc 2021 ...` | main.tex | → `% Created by 模板维护者, MSc 2021 ...` |
| `% Connect with me at joelsleeba.github.io or github.com/joelsleeba` | main.tex | Lines removed |
| `Joel Sleeba` (author name on title page) | 00Intro/01_Title.tex | → `Tom Smith` |
| `Nikhil Alex Verghese, BS-MS'17, IISER Thiruvananthapuram for creating...` | 00Intro/04_Acknowledgement.tex | → `the contributors who created the official IISER Thiruvananthapuram Thesis/Dissertation Format` |
| `github.com/joelsleeba/iisertvm-thesis-template` | 01Chapters/01FourierSeries.tex | → `github.com/iftaken/iisertvm-thesis-template` |
| `\copyright Joel Sleeba` | 01Chapters/01FourierSeries.tex | → `\copyright 模板维护者` |

## Repository: iiser-tvm-thesis

Placeholder-only repo. Author field is "MSc Thesis Submission" — already clean. No PII found.
Compile test passed (79KB).

## Repository: imust-bachelor-proposal (内蒙古科技大学开题报告)

Chinese Beamer template. All author/title/advisor/major/study fields are placeholders:
`学生姓名`, `指导教师姓名~职称`, `专业名称`, `专业方向名称`, `毕业论文题目`.
No real PII. README attribution to andy123t/Thesis-Slides preserved (CC BY 4.0 required).
Compile test passed (122KB).

## Repository: imust-bachelor-thesis (内蒙古科技大学本科毕业设计)

Placeholder repo with PII in AGENTS.md and main.tex metadata.

| Pattern | Location | Action |
|---------|----------|--------|
| `richey (richey@imust.edu.cn，推测)` | main.tex (comment + body) | → `模板维护者 (example@example.com，推测)` |
| `richey (richey@imust.edu.cn，推测)` | AGENTS.md (table + body) | → `模板维护者 (example@example.com，推测)` |
| `richey@imust.edu.cn` | AGENTS.md (relation section) | → `example@example.com` |

**Note:** AGENTS.md is a PII vector — the email scan catches `@imust.edu.cn` but the name+email pair
needs both fields replaced together for consistency.

## Repository: imust-microcomputer

Empty repository. Skip.

## Repository: imust-microcomputer-training (建电专业微型计算机实训)

Placeholder-only repo. All fields are generic. No PII found.
Compile test passed (84KB).

## Repository: imust-proposal-template

Duplicate of imust-bachelor-proposal in content. All placeholders. No PII found.
README attribution to andy123t/Thesis-Slides preserved (CC BY 4.0 required).
Compile test passed (122KB).

## Repository: hust-thesis

Empty repository. Skip.

## False Positives (verified safe)

| Pattern | Reason safe |
|---------|-------------|
| ISBN numbers `9780763714970`, `9780429973772`, `9780070856134`, `9780821847978` | Bibliographic — `isbn = {...}` field in .bib files |
| `Montgomery, Hugh L.`, `Rudin, Walter`, etc. | BibTeX author fields for published textbooks |
| `andy123t/Thesis-Slides` in README.md | CC BY 4.0 attribution required by license |
| `IISER Thiruvananthapuram` | Product-defining university identity |

## Lessons Learned

1. **ISBN false positives:** Phone number regex `[0-9]{11}` matches 13-digit ISBNs. Filter by context (`isbn` keyword) or prefix (978/979).

2. **English templates need English replacements:** Using Chinese text in English-only templates causes "Missing character" font warnings. Prefer "Tom Smith" over "模板维护者" in English templates.

3. **AGENTS.md is a PII vector:** Email+name pairs in AGENTS.md tables/body need scrubbing just like .tex files.

4. **Acknowledgement sections:** Specific individuals thanked by name + credential (e.g., "Nikhil Alex Verghese, BS-MS'17") are PII. Generalize to institutional language.

5. **License-required attribution:** Some GitHub links are CC BY attribution requirements, not personal links. Preserve them.
