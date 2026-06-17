# Batch B Stragglers (June 14, 2026)

8 repos from the iftaken backlog — final stragglers needing PII scrubbing, compile, and push.

## Repos processed

| Repo | PII Status | Notes |
|------|-----------|-------|
| oreilly-template | Clean | Already uses iftaken GitHub refs. 136K PDF. |
| overleaf-lzu-thesis | Adapted | No main.tex/references.bib — created symlinks. Added `overleaf` class option for Fandol fonts. 488K PDF. |
| scu-beamer | Scrubbed | AGENTS.md: Chen Yang (羊忱)→张三. main.tex: `\author{羊忱}`→张三. 288K PDF. |
| scu-beamer-slide | Skipped | Empty repo (only .git skeleton). |
| scu-thesis | Scrubbed | 1_Introduction.tex: dahakawang→iftaken, CasperVector@gmail.com→example@example.com, Casper Ti. Vector→Tom Smith, cuiao→iftaken, Legendary L./Leo→Tom Smith. 453K PDF. |
| sh-t-latex | Clean | Already uses example@example.org. 1.0M PDF. |
| shnu-thesis | Scrubbed | chap01.tex: andy123t/shnuthesis→iftaken/shnuthesis. 840K PDF. |
| southwest-forestry-university-thesis | Clean | Placeholder only. 58K PDF. |

## New PII patterns discovered

### Beamer `\author{姓名}` in main.tex

Beamer templates commonly have `\author{}`, `\institute{}`, `\title{}` in the main.tex preamble. Scan for Chinese names in `\author{}` — not just in AGENTS.md or .cls headers.

PII: `\author{羊忱}` → `\author{张三}`

### Upstream GitHub username in attribution text

Some templates cite the original upstream in body text, not just in AGENTS.md metadata. Example:

```
本模板 \href{https://github.com/andy123t/shnuthesis}{\texttt{shnuthesis}} 基于...
```

Scrub: `andy123t` → `iftaken` (when iftaken has the mirror). The attribution link itself is preserved — only the personal username changes.

### Personal GitHub + email in footnote acknowledgments

Multi-vector PII in single sentences:

```
工作以前由~dahakawang\footnote{\url{https://github.com/dahakawang/scu_thesis_template}}~、
~tan\footnote{\url{http://www.codeforge.com/article/382397}}~等人做过。
本模版是在参考~Casper Ti. Vector\footnote{\url{CasperVector@gmail.com}}~~pkuthss~模版
的基础上完成的。
```

Scrub: dahakawang→iftaken (GitHub user), CasperVector@gmail.com→example@example.com (email), Casper Ti. Vector→Tom Smith (name), cuiao→iftaken (GitHub user), Legendary L./Leo→Tom Smith (name).

## Technical fixes applied

### Font adaptation via class option (overleaf-lzu-thesis)

LZUThesis_xb.cls has a conditional `\ifLZU@overleaffonts` block that uses Fandol fonts (available in Docker) instead of SimSun/SimHei/SimFang (requires local fonts/ directory). The `overleaf` class option activates this branch.

```latex
% Before: \documentclass[AutoFakeBold]{LZUThesis_xb}
% After:
\documentclass[overleaf,AutoFakeBold]{LZUThesis_xb}
```

This pattern applies to any cls that has an `overleaf` option for Fandol fonts — check for `\newif\ifLZU@overleaffonts` or similar conditional blocks.

### Missing main.tex/references.bib — symlink adaptation

When a repo has `template.tex` instead of `main.tex` and `bib/template.bib` instead of `references.bib`:

```bash
ln -sf template.tex main.tex
ln -sf bib/template.bib references.bib
```

Symlinks are preferred over copies because changes to the source propagate. Git tracks symlinks correctly.

Note: template.tex `\bibliography{bib/template}` references the bib by path; when accessed through the symlink, the relative path still resolves because symlinks inherit the target's location.
