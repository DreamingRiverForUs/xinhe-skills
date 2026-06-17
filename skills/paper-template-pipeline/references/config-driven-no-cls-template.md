# Config-Driven Templates Without Custom .cls

Some templates have **no custom document class** — they use standard LaTeX classes (`report`, `book`, `article`) directly and are structured entirely through `\input{config/*.tex}` files. These are simpler to adapt than cls-based templates.

## Identification

- `main.tex` starts with `\documentclass[12pt]{report}` (or `book`, `article`) — no custom class name
- `find . -name '*.cls'` returns **nothing**
- `find . -name '*.sty'` returns **nothing** (or only standard packages in tectonic cache)
- Config lives in `config/` directory: `packages.tex`, `options.tex`, `colors.tex`, etc.

## Template examples

| Template | Doc Class | Source | Notable |
|----------|-----------|--------|---------|
| HNU Bachelor Thesis | `article` | TrisenYu/hnu_thesis_latex_template | ctex+CJK (pdflatex→XeTeX adapted), biblatex+gb7714 |
| IISER TVM Thesis | `report` | joelsleeba/iisertvm-thesis-template | biblatex+biber, CM fonts, no CJK |

## Adaptation checklist (simplified from full pipeline)

### Skip these full-pipeline steps entirely

- ❌ dtx/docstrip extraction → no .dtx files
- ❌ Font dependency scanning (`\setmainfont`/`\setCJKfamilyfont`) → none exist
- ❌ `font/` directory font downloads → `init.sh` just creates empty `font/` dir
- ❌ `\ProcessKeyOptions` / `:en` / `:e` expl3 compatibility → no expl3 in config files
- ❌ `.bst` file extraction → uses biblatex/biber, no .bst needed

### Do these checks

1. **`\include` → `\input`**: Scan main.tex for `\include{` and convert to `\input{`. Same rationale as cls-based templates — avoids biber/bibtex chapter-level aux errors.
   ```bash
   grep -n '\\include{' main.tex
   ```

2. **Bibliography reference**: For biblatex templates, the reference is `\addbibresource{path}` not `\bibliography{path}`. Update to `\addbibresource{references.bib}`.
   ```bash
   grep -n 'addbibresource\|bibliography{' main.tex
   ```

3. **Package typos**: Scan for common misspellings. `hyperref` is correct (not `hyperref` — two r's).
   ```bash
   grep -n '\\usepackage{' config/packages.tex
   ```

4. **Missing input files**: Check that all `\input{...}` and `\includegraphics{...}` paths resolve.
   ```bash
   grep -oP '\\input\{[^}]+\}' main.tex config/*.tex
   grep -oP '\\includegraphics[^}]*\{[^}]+\}' *.tex **/*.tex
   ```

5. **.gitignore exceptions**: Check for logo/emblem PNGs in `figures/` that shouldn't be excluded. PNGs are NOT excluded by the `.gitignore` template (only `*.pdf` is), so usually no exception needed. But verify. Add `!<logo>.pdf` exceptions for any PDF logos used in `\includegraphics`.

## Chinese ctex templates: pdflatex → XeTeX adaptation

When a config-driven template uses `\usepackage[UTF8]{ctex}` and was designed for pdflatex (with `CJKutf8`, `CJK`, `fontenc`, `inputenc`), it needs systematic cleanup for tectonic (XeTeX). **This is the most common failure mode for Chinese university thesis templates.**

### Package removal checklist (mandatory)

| Package | Reason |
|---------|--------|
| `\usepackage[T1]{fontenc}` | XeTeX uses Unicode fonts natively, not T1 encoding |
| `\usepackage[utf8]{inputenc}` | XeTeX is always UTF-8 |
| `\usepackage{CJKutf8}`, `\usepackage{CJK}` | ctex handles Chinese in XeTeX mode automatically |
| `{txfonts}` | TFM-based math fonts; XeTeX uses OpenType/TTF |
| `{times}` (in amsmath group) | Conflicts with fontspec loaded by ctex |
| `\usepackage{svg}` | Requires Inkscape; tectonic Docker has none |
| `\usepackage{ipaex-type1}` | Japanese font package; unnecessary and may conflict |

### Command-level fixes

| Original | Fix |
|----------|-----|
| `\CJKtilde` | Remove entirely — XeTeX handles CJK spacing natively |
| `\DisableLigatures{encoding = *, family = *}` | Comment out — microtype's ligature disable only works with pdfTeX. Use `fontspec` features instead |
| `\usepackage[..., pdftex, ...]{hyperref}` | Remove `pdftex` option — XeTeX is not pdfTeX |

### Fontspec option clash prevention

**Always** add before `\usepackage[UTF8]{ctex}`:
```latex
\PassOptionsToPackage{quiet}{fontspec}
```
This prevents "Option clash for package fontspec" — ctex loads fontspec first (without options), then any subsequent `\RequirePackage[quiet]{fontspec}` in user code triggers the clash.

### glossaries-extra incompatibility (tectonic TL2023)

`\usepackage[automake,...]{glossaries-extra}` causes **parameter stack overflow** (`TeX capacity exceeded [parameter stack size=10000]`) in tectonic's TL2023 bundle. **Remove glossaries-extra entirely** and use only base `glossaries` package. The `automake`, `acronym`, `postdot` features are non-essential.

### Verify with Docker compile

After all changes, the Docker compile should produce `main.pdf`:
```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  <image> tectonic -X compile main.tex
```


## biblatex/biber specific notes

- tectonic's `tectonic-biber` handles biber execution automatically (no separate `biber main` step needed)
- The `.gitignore` template should include `.bcf` and `.run.xml` (biber auxiliary files)
- `\printbibliography[heading=bibintoc]` is the standard output command
- Citation commands vary: some templates use `\autocite`, some use `\cite`. Both work with biblatex.

## Zero font dependency

When the template uses only standard LaTeX fonts (Computer Modern via OT1/T1 encoding), with no `fontspec` or `xeCJK` packages:
- `init.sh` only needs to create an empty `font/` directory
- No COS font URLs needed
- The ctexfont pitfall from the main pipeline applies here too
