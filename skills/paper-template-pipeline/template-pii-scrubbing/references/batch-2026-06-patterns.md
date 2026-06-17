# PII Patterns Discovered (June 2026 Batch — 16 LaTeX Template Repos)

Real PII that was found and scrubbed across both batches.

## Batch 1 (first 8 repos)

### Repository: cmc-msu-thesis

| Pattern | Location | Action |
|---------|----------|--------|
| `Vadim Zizov` | AGENTS.md author field | → "Tom Smith" |
| `Ivanov Ivan Ivanovich` | config.tex `\Author` | → "Tom Smith" (was already Russian John Doe) |

### Repository: cqu-report

| Pattern | Location | Action |
|---------|----------|--------|
| `20230537华晓蔚` | main.tex comment | Removed → "Adapted from THU Beamer template" |
| `Will-Hxw` | main.tex acknowledgements slide | → "Tom Smith" |
| `xiaoweihuacqu@gmail.com` | main.tex email | → "example@example.com" |
| `https://github.com/Will-hxw/CQU-Beamer-LaTexPPT` | main.tex repo link | Line removed |
| `Will-hxw/CQU-Beamer-LaTeXPPT` | AGENTS.md GitHub source | → "cqu-beamer-template" |

### Repository: cspc-ccs-thesis

No PII — all names already placeholders ("Author Name 1", "Panel Member 1", etc.)

### Repository: cug-thesis-english

No PII — all names already placeholders (Zhang San/张三, Li Si/李四, stunum 2024123456)

### Repository: cumcm-general

| Pattern | Location | Action |
|---------|----------|--------|
| `KOKO (SYSU)` | main.tex comment, `\author`, body text, AGENTS.md | → "Tom Smith" |
| `sleepyy-dog/Survival-Handbook-by-KOKO` | main.tex GitHub link | → "example/template" |

### Repository: cumcm-paper-template

| Pattern | Location | Action |
|---------|----------|--------|
| `91940767/478023327/640633524` | main.tex QQ group numbers | Removed |
| `关注我们的微信公众号` + QR image | main.tex WeChat reference | Needs removal |

## Batch 2 (second 8 repos — jiajiao-resume through monograph-beamer)

### Repository: jiajiao-resume

Empty repository — skip immediately.

### Repository: jsie-thesis

| Pattern | Location | Action |
|---------|----------|--------|
| `xhz` | AGENTS.md author field, main.tex comment/body | → "张三" (Chinese placeholder) |

### Repository: jssm-template

| Pattern | Location | Action |
|---------|----------|--------|
| `muzimuzhi@gmail.com` | jssms.cls copyright line | → "example@example.com" |
| `muzimuzhi` (maintainer) | jssms.cls maintainer line | → "模板维护者" |

Note: `muzimuzhi/jssms-template` in AGENTS.md source attribution was preserved — it is a public template origin reference, not personal PII.

### Repository: jssnu-thesis

| Pattern | Location | Action |
|---------|----------|--------|
| `XurongLiu` | main.tex acknowledgements, references.bib author, README.md BibTeX author | → "Tom Smith" |
| `https://github.com/XurongLiu/HNIE-Thesis-LaTeX-Template` | references.bib howpublished, README.md | → "https://github.com/example/template" |

### Repository: litebook-template

Empty repository — skip immediately.

### Repository: lnumcmthesis-template

| Pattern | Location | Action |
|---------|----------|--------|
| `Hank Lo` | README.md author line | → "Tom Smith" |
| `yhlaozero2@163.com` | README.md email, lnumcmthesis.cls copyright | → "example@example.com" |
| `JL <yhlaozero2@163.com>` | lnumcmthesis.cls copyright line | → "模板维护者 <example@example.com>" |
| `345749407` (QQ group) | README.md QQ交流群 | Line removed |
| `https://github.com/JohnsonLo00/lnumcmthesis` | README.md GitHub link | → "https://github.com/iftaken/lnumcmthesis-template" |
| `https://gitee.com/jhonson-lo/lnumcmthesis` | README.md Gitee link | Removed (no iftaken Gitee mirror) |
| `https://github.com/JohnsonLo00/lnumcmthesis/releases` | README.md Releases link | Removed |
| `https://gitee.com/jhonson-lo/lnumcmthesis/releases` | README.md Releases link | Removed |
| `https://github.com/JohnsonLo00/lnumcmthesis/issues` | README.md Issues link | Removed |
| `https://gitee.com/jhonson-lo/lnumcmthesis/issues` | README.md Issues link | Removed |
| `作者为 HankLo` | README.md line 44 | Removed |
| `在QQ群中发起提问` | README.md troubleshooting | → "查阅手册" then removed (duplicate) |

Special handling: GitHub source link was repointed to `iftaken/lnumcmthesis-template` (our org).
Gitee links were stripped entirely (no iftaken Gitee mirror exists).

### Repository: math-exam-a4

Clean placeholder — no PII found. PDF regenerated only.

### Repository: monograph-beamer

Clean placeholder — no PII found. PDF regenerated only.

## False Positives (verified safe — do NOT scrub)

| Pattern | Reason safe |
|---------|-------------|
| `Knuth, Donald E.`, `Lamport, Leslie` | Citation authors in .bib, not template creator |
| `刘海洋`, `胡伟`, `王伟`, `李明` | Citation authors in .bib |
| `Lomonosov Moscow State University` | Product-defining university identity |
| `重庆大学计算机学院` | Product-defining university identity |
| `Camarines Sur Polytechnic Colleges` | Product-defining university identity |
| `湖南工程学院` | Product-defining university identity |
| `江苏第二师范学院` | Product-defining university identity |
| `辽宁省大学生数学建模竞赛` | Product-defining competition identity |
| `系统科学与数学 (JSSMS)` | Product-defining journal identity |
| `校徽+中英文校名_蓝色.pdf` | University logo asset |
| `CSPC-WEBSITEV2_3.png` | University logo asset |
| `latexstudio.net` URLs | Public community site, not personal |
| `ctex`, `TeX Live`, `TeX/LaTeX` macros | Technical references |
| `CC BY 4.0` / `LPPL 1.3c` license | Public license declaration |
| `muzimuzhi/jssms-template` (AGENTS.md source) | Public GitHub template origin attribution |
| `何赛飞 and 周玥丹 and 夏重阳` et al. in .bib | Real published citation authors, not template creator PII |

## Lessons for future batches

1. **Always scan .cls files** — copyright/maintainer lines often carry real names and emails (jssm-template, lnumcmthesis-template).
2. **README.md is a PII hotspot** — BibTeX citation examples often include real author names, emails, GitHub profiles, and QQ/WeChat group numbers.
3. **GitHub repo links**: when the template has an iftaken mirror, repoint personal GitHub links to `iftaken/<repo>`. When no mirror exists, use `example/template` or remove the link.
4. **Gitee links**: iftaken has no Gitee presence — strip Gitee links entirely.
5. **QQ group numbers**: always remove. They are personal contact infrastructure, not product-defining.
6. **Placeholder repos**: many repos in the 8-repo set are "source files pending extraction from TeXPage" placeholders. Still compile to regenerate main.pdf and push — even if no PII was found.
7. **Source attributions**: distinguish between personal GitHub repos (PII → scrub) and public template origins like `muzimuzhi/jssms-template` (product-defining → preserve).
