# ACL (Association for Computational Linguistics) Paper Template

## Quick Reference

| Field | Value |
|-------|-------|
| TeXPage ID | `98c8b7d2-858c-4ead-b450-436746e12b7a` |
| TeXPage URL | https://www.texpage.com/template/98c8b7d2-858c-4ead-b450-436746e12b7a |
| GitHub source | `acl-org/acl-style-files` |
| Repo pattern | `iftaken/acl-template` |
| Doc class | `article` (11pt) — no custom .cls |
| Style file | `acl.sty` (loaded via `\usepackage{acl}`) |
| Bib style | `acl_natbib.bst` (natbib-based) |
| Classification | 期刊投稿 (Journal) |
| Font dependency | None — uses `\usepackage{times}` (standard Times) |
| Languages | English only |
| Compilation | pdflatex native; XeLaTeX/LuaLaTeX supported via `acl.sty` |

## Source Structure

```
acl-org/acl-style-files/
├── acl.sty           # Style file (core)
├── acl_natbib.bst    # Bibliography style
├── acl_latex.tex     # Example template (pdflatex)
├── acl_lualatex.tex  # Example template (LuaLaTeX/XeLaTeX)
├── custom.bib        # Example bibliography
├── anthology.bib.txt # ACL Anthology bib
├── formatting.md     # Formatting guidelines
└── README.md
```

## XeLaTeX (Tectonic) Adaptations

1. **Remove `\usepackage[T1]{fontenc}`** — not needed in XeTeX; fontspec handles encoding
2. **Remove `\usepackage[utf8]{inputenc}`** — not needed in XeTeX; UTF-8 is native
3. **Keep `\usepackage{times}`** — works fine in XeTeX (maps to Times New Roman via fontspec)
4. **Change `\bibliography{custom}` → `\bibliography{references}`** — system requires `references.bib`
5. **Keep `\usepackage{microtype}`** — works in XeTeX (protusion only, no expansion)
6. **Keep `\usepackage{inconsolata}`**, `\usepackage{graphicx}`, `\usepackage{latexsym}` — all compatible
7. **`lineno.sty:296` UTF-8 byte warning** — cosmetic, comes from comment in lineno.sty, safe to ignore

## Compilation Result

- `tectonic -X compile main.tex` → exit 0
- Output: main.pdf ≈ 110 KB
- Warnings only (underfull hbox, lineno.sty encoding) — no errors
- tectonic auto-downloads: `phvb.tfm`, `inconsolata.sty`, `example-image-golden.pdf` (from mwe package)

## Pipeline Notes

- No .cls file to scan — uses standard `article` class
- No CJK fonts — init.sh is a no-op (just creates empty font/ dir)
- No `\input`/`\include` dependencies to stub
- No resource files (logos, code files) to fetch
- `\bibliography{custom}` → `\bibliography{references}` is the only path change needed
- `\bibliographystyle` is set inside `acl.sty` (no user-level `\bibliographystyle` command)
