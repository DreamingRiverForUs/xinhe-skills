# CVPR / IEEE Conference Template

CVPR, ICCV, and ECCV share a single author kit. This covers the CVPR 2024/2026 template and its siblings.

## Source

- **GitHub upstream**: `cvpr-org/author-kit`
- **TeXPage**: https://www.texpage.com/template/2385deba-7aaf-4157-8815-ee9856b84b32
- **Types**: CVPR (Computer Vision and Pattern Recognition), reusable for ICCV/ECCV

## Template Characteristics

| Attribute | Value |
|-----------|-------|
| Language | English only |
| Document class | `article` (standard LaTeX, NOT ctex) |
| Style file | `cvpr.sty` (loaded via `\usepackage`) |
| CJK fonts | None — zero font dependency |
| Bibliography style | `ieeenat_fullname.bst` (natbib) |
| Build system | Tectonic (XeTeX), single pass + bibtex rerun |

## Standard File Structure

```
.
├── main.tex           # Entry point, \documentclass{article}
├── cvpr.sty           # Style file (508 lines)
├── references.bib     # Renamed from main.bib
├── ieeenat_fullname.bst  # BibTeX style
├── preamble.tex       # Extra packages (cuted, currfile, caption)
├── rebuttal.tex       # Rebuttal template
├── sec/               # Section files
│   ├── 0_abstract.tex
│   ├── 1_intro.tex
│   ├── 2_formatting.tex
│   ├── 3_finalcopy.tex
│   └── X_suppl.tex
└── fig/
    └── teaser.tex
```

## Adaptation Steps

### Mandatory

1. **Rename bibliography**: `main.bib` → `references.bib`, update `\bibliography{main}` → `\bibliography{references}` in main.tex
2. **init.sh**: empty FONT_FILES — no CJK fonts needed, just create `font/` directory

### Nothing else needed

- No font downloads
- No encoding conversion (already UTF-8)
- No `\input` → `\include` changes needed
- No cls patches required

## Compilation

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

Tectonic auto-downloads missing packages (cuted, currfile). Compilation succeeds on first run; a bibtex rerun pass is automatic.

### Safe Warnings

- `lineno.sty:296: Invalid UTF-8 byte` — known, harmless. Comes from lineno.sty internal comments.

## Key Dependencies (all in tectonic bundle)

`times`, `xspace`, `xcolor[dvipsnames]`, `graphicx`, `amsmath`, `amssymb`, `booktabs`, `natbib[numbers,sort&compress]`, `silence`, `etoolbox`, `caption`, `subcaption`, `cuted`, `currfile`, `hyperref`

## Pitfalls

- **None known**. This is one of the cleanest templates — pure English, standard LaTeX, no esoteric packages. If compilation fails, check for Docker image availability or tectonic cache corruption before suspecting the template.
