# CSPC CCS Thesis Template

Template on TeXPage: `dc8b63ce-6699-4a1e-a2f7-fa6a1009da7b`
Repository: `iftaken/cspc-ccs-thesis`

## Template Characteristics

- **Type**: English-only thesis (Camarines Sur Polytechnic Colleges, Philippines)
- **Document class**: `cspcccsthesis` based on `report` (12pt), derived from `gatechthesis`
- **CJK fonts**: None — pure English template
- **Font strategy**: `\usepackage{times}` (psnfss) → Docker system Times New Roman
- **Bibliography**: biblatex + biber backend, `\addbibresource{references.bib}`
- **Glossary**: `glossaries` package with `acronym` option; `\makeglossaries` + `\printacronyms`
- **init.sh**: `FONT_FILES=()` — no font downloads needed

## Key Packages

graphicx, geometry, ragged2e, multicol, setspace, times, titlesec, tocloft,
ifoddpage, rotating, appendix, ulem, url, siunitx, hyperref, bookmark,
caption, subcaption, glossaries, doi, fancyhdr, authblk, lastpage,
biblatex, chngcntr, indentfirst, float

## Structural Commands

| Command | Purpose |
|---------|---------|
| `\makeTitlePage{month}{year}` | Title page |
| `\begin{approvalPage}...\end{approvalPage}` | Approval page (text-based) |
| `\makePanelofExaminers{grade}` | Panel of examiners page |
| `\makeDedication{text}` | Dedication page |
| `\begin{acknowledgments}...\end{acknowledgments}` | Acknowledgments |
| `\makeAbstract` | Abstract page |
| `\makeTOC` | Table of contents |
| `\makeListOfTables` | List of tables |
| `\makeListOfFigures` | List of figures |
| `\makeListOfAcronyms` | List of acronyms |
| `\begin{frontmatter}...\end{frontmatter}` | Front matter wrapper |
| `\begin{thesisbody}...\end{thesisbody}` | Main body wrapper |
| `\makeBibliography` | Bibliography |
| `\begin{vita}...\end{vita}` | Author vita |

## Template Metadata (set in preamble)

```
\title{...}
\authorOne{...}, \authorTwo{...}, \authorThree{...}
\degree{...}          # e.g. "Bachelor of Science in Computer Science"
\approvaldate{...}    # e.g. "January 1, 2020"
\school{...}          # e.g. "Camarines Sur Polytechnic Colleges"
\adviser{...}
\dean{...}
\committeeMemberOne{...}, \committeeMemberTwo{...}, \committeeChair{...}
\department{...}      # e.g. "College of Computer Studies"
\thesisAbstract{...}
\keywords{...}
```

## Adaptations Applied

1. **biblatex style**: `acmnumeric` (ACM-specific, not in TL2023) → `numeric`
2. **Logo images**: Created placeholder 1x8px PNGs for `settings/CSPC-WEBSITEV2_3.png` and `settings/Proposed Logo - College of Computer Studies (CSPC)-07.png`
3. **Appendices**: `theappendices` environment uses `\clear@ppage` (undefined in tectonic's `appendix` package) — used standard `\appendix` instead
4. **Acronyms**: Two demo acronyms (`\newacronym{ai}{AI}{...}`, `\newacronym{ml}{ML}{...}`) defined in main.tex
5. **Unused commands**: `\authorFour`, `\authorFive` not defined in cls; removed from main.tex

## cls Version Selection

Two versions found on GitHub:
- `CSPC-BSCS-3B/Virgo_Thesis`: hardcoded project title on title page line, image-based approval page
- `crispyp0tat0/thesis`: uses `\@title` on title page, text-based approval page (no external image dependency)

**Chose crispyp0tat0 version** — more general (no hardcoded text) and no binary image dependency for approval page.

## .gitignore Exceptions

```
!settings/CSPC-WEBSITEV2_3.png
!settings/Proposed Logo - College of Computer Studies (CSPC)-07.png
```

## Glossary Build Artifacts

Added to .gitignore: `*.ist`, `*.acn`, `*.acr`, `*.glg`
