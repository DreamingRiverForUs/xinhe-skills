# HHU-thesis (河海大学研究生学位论文)

## Template Info

| Field | Value |
|-------|-------|
| Name | HHU-thesis |
| Source | Vitzron/HHU-thesis (GitHub) |
| TeXPage | d9b4c8b7-b479-4ed2-b793-7050a74dbd2b |
| Class | HHU-thesis.cls |
| Base class | ctexbook |
| Engine | XeLaTeX (tectonic) |
| Bib style | gbt7714-2015 (bst/GBT7714-2015.bst) |
| Degree levels | master (学术硕士), doctor (博士) |
| Layout | oneside / twoside |
| xinhepaper repo | iftaken/hhu-thesis |

## Structure

```
.
├── main.tex              # Entry (document.tex renamed)
├── HHU-thesis.cls        # Document class
├── references.bib         # Bibliography (ref.bib renamed)
├── tex/
│   ├── info.tex           # Author/thesis metadata
│   ├── abstract.tex       # CN/EN abstracts
│   ├── preface.tex        # Doctor preface only
│   ├── abbreviations.tex  # Symbol definitions
│   ├── chap_*.tex         # Chapter content
│   ├── bib.tex            # Bibliography config
│   ├── acknowledgement.tex
│   └── appendix.tex
├── figures/
│   ├── hohai_badge.pdf    # Logo (keep in git)
│   └── logo/hohai_logo.png
├── bst/
│   ├── GBT7714-2005.bst
│   └── GBT7714-2015.bst
├── init.sh
├── AGENTS.md
└── .gitignore
```

## Font Strategy

**Zero external font downloads.** This template uses ctexbook without a `fontset` option. On Linux (Docker), ctex auto-detects to the **fandol** fontset, which includes all four CJK fonts:

| Command | Font | Source |
|---------|------|--------|
| \songti | FandolSong | TeX Live bundle |
| \heiti | FandolHei | TeX Live bundle |
| \kaishu | FandolKai | TeX Live bundle |
| \fangsong | FandolFang | TeX Live bundle |

English text uses `newtxtext`/`newtxmath` (Times New Roman clone, also in TeX Live).

No `simfang.ttf` or `simkai.ttf` download needed. `init.sh` creates `font/` directory as a placeholder only.

## Adaptations Made

1. `ref.bib` → `references.bib` (system requirement)
2. `document.tex` → `main.tex` (system requirement)
3. `tex/bib.tex`: `\bibliography{ref}` → `\bibliography{references}`
4. `.gitignore`: `!figures/hohai_badge.pdf` exception added for logo PDF

## Compilation

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

**First compile result**: exit 0, main.pdf 283KB. No .cls modifications needed.

## Pitfalls

- **None encountered.** Template compiled cleanly on first try with zero modifications to the .cls file. The ctexbook + Fandol auto-detection provides all four CJK fonts, so `\fangsong` (used in subsubsection headings at line 201 of HHU-thesis.cls) works without external font downloads.

- **ctexbook default on Linux = Fandol (not windows)**. Even though Docker has SimSun/SimHei system fonts, ctex on Linux auto-detects Fandol (not Windows). This is favorable — Fandol provides Kai/Fang which Windows fontset would lack in Docker.
