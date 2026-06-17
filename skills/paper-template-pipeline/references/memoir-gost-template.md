# Memoir-based Non-CJK Templates (GOST / Russian / European Theses)

Applies to templates using `memoir` document class with no CJK dependency — typically Russian GOST theses, European university templates.

## Identification

- Document class: `memoir` (not ctexbook/ctexrep)
- Language: Russian (via `babel`/`polyglossia`), sometimes English
- No `\setCJKmainfont` or CJK font declarations
- Often uses `pdflatex`-specific packages: `fontenc`, `inputenc`, `babel`, `newtxmath`

## pdflatex → XeTeX Adaptation Map

| pdflatex package | XeTeX replacement | Notes |
|-----------------|-------------------|-------|
| `\usepackage[T1,T2A]{fontenc}` | Remove | XeTeX handles encoding natively |
| `\usepackage[utf8]{inputenc}` | Remove | XeTeX is UTF-8 native |
| `\usepackage[english,russian]{babel}` | `\usepackage{polyglossia}` + `\setdefaultlanguage{russian}` + `\setotherlanguage{english}` | polyglossia is the XeTeX language package |
| `\usepackage[bigdelims,vvarbb]{newtxmath}` | Remove | XeTeX incompatible; OpenType math fonts used by default |
| `\usepackage{newtxtext}` | Remove | XeTeX incompatible; use `\setmainfont` instead |
| `\usepackage{pdflscape}` | `\usepackage{lscape}` | lscape provides pdflscape compatibility |
| `\newcommand*{\memfontpack}{tempora}` | Add `\setmainfont{Times New Roman}` etc. | System fonts in Docker |
| `\include{...}` | `\input{...}` | Avoid chapter aux errors in tectonic (standard rule) |

## Standard XeTeX Font Setup for GOST Templates

```latex
% In styles/fonts.tex:
\usepackage{polyglossia}
\setdefaultlanguage{russian}
\setotherlanguage{english}

\setmainfont{Times New Roman}     % Available in Docker
\setsansfont{Liberation Sans}      % Available in Docker
\setmonofont{Liberation Mono}      % Available in Docker
\usepackage{textcomp}
```

## Math Adaptation

Remove `newtxmath` — XeTeX uses OpenType math by default. Keep `amsmath`, `amssymb`, `amsthm`, `mathtools`, `upgreek`. If the template uses `\renewcommand` for Greek letters (Russian tradition — upright Greek), these work fine with the `upgreek` package under XeTeX.

## init.sh

Empty font array — no CJK fonts needed:

```bash
#!/usr/bin/env bash
set -e
FONT_DIR="font"
FONT_FILES=()
if [ ${#FONT_FILES[@]} -eq 0 ]; then
    echo "No fonts to download (non-CJK template)"
    exit 0
fi
mkdir -p "$FONT_DIR"
# ... (download logic if fonts needed later)
```

## Pitfalls

- **`tempora` font package**: Memoir's `\memfontpack{tempora}` uses the Tempora font which may not be available in tectonic/Docker. Override with `\setmainfont` via fontspec instead of relying on memoir's font machinery.
- **`\usepackage{pdfpages}`**: Keep this — it works in XeTeX. Used for inserting external PDF pages into the document.
- **`\usepackage{changepage}`**: Keep this — works in XeTeX for mid-document page layout changes.
- **biblatex-gost + biber**: tectonic-biber handles this automatically. Keep the biblatex setup as-is, just rename `.bib` file to `references.bib` and update `\addbibresource`.
- **Cyrillic in listings**: The pdflatex `literate` hack for Cyrillic in `lstset` (mapping each Cyrillic char to `\charNNN`) is not needed in XeTeX — remove it but keep `extendedchars=true`.

## Restoration Audit (partial repo / TeXPage extraction)

When restoring from a partial file set, cross-reference all `\input`/`\include`/`\addbibresource` commands in `main.tex` and `config.tex` to find missing files:

```bash
# Find all input/include references
grep -n '\\input{\|\\include{\|\\addbibresource' main.tex config.tex
```

Commonly missing files in restored GOST templates:

| Missing file | Where referenced | What to create |
|-------------|-----------------|----------------|
| `styles/title.tex` | main.tex `\input{styles/title}` | GOST title page (see below) |
| `commands.tex` | main.tex `\input{commands}` | Empty user commands file |
| `references.bib` | main.tex `\addbibresource{references.bib}` | Minimal biblatex .bib |
| `mainfiles/*.tex` | config.tex `\Source` command | Chapter stubs with `\section{...}` |

Always cross-reference after extraction — TeXPage file trees can silently omit files that exist only in the compiled view.

## Title Page (GOST style)

GOST title pages use `\MakeUppercase` for university/faculty/department/author names. Key macros come from `config.tex`:

```latex
% In styles/title.tex:
\thispagestyle{empty}
\begin{center}
    \MakeUppercase{\Univer}
    \MakeUppercase{\Faculty}
    \MakeUppercase{\Department}
\end{center}
\vspace{3cm}
\begin{flushright}\Status\end{flushright}
\vspace{1cm}
\begin{center}
    \textbf{\MakeUppercase{\WorkType}}
    \vspace{0.5cm}
    \textbf{\Title}
\end{center}
\vspace{0.5cm}
\noindent Author of the work: \\
\MakeUppercase{\Author}
\vspace{1cm}
\noindent Scientific advisor: \\
\Position, \AcademicDegree \\
\SciAdvisorShort
\vspace{2cm}
\begin{center}\Place\ --- \Year\end{center}
\clearpage
```

The `\Status` macro expands to either `draft` or `final` (set in config.tex) and is placed flushright above the work type. If the template has `\EnableSign`, add a conditional sign-off line using `\ifthenelse`.

## Example: CMC MSU Thesis

TeXPPage template `c6d517c8-2a77-449a-96e4-fd9e2719886e` by Vadim Zizov. Memoir class, Russian GOST, no CJK. No GitHub source — TeXPage-only extraction required.

**Completed restoration (2026-06-09)**: repo iftaken/cmc-msu-thesis. Files after restoration:
```
main.tex  config.tex  commands.tex  references.bib  init.sh  .gitignore  AGENTS.md
styles/{fonts,math,text,page,media,table,algorithms,commands,title}.tex
mainfiles/{0-Introduction,1-Problem-Statement,2-Overview,3-Research,4-Experiments,5-Conclusion}.tex
```
Docker compile: 72KB main.pdf, exit 0. Only safe upstream warnings (misccorr.sty UTF-8, algorithm2e.sty).
