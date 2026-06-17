# NJU Thesis Template (nju-lug/NJUThesis)

TeXPage source: https://www.texpage.com/template/268ecd0e-05a0-4a4a-a217-f63195c2d94d
GitHub source: https://github.com/nju-lug/NJUThesis
Author: NJU-LUG

## Template structure

- **Format**: dtx-based (docstrip). Source file: `source/njuthesis.dtx`
- **Extraction**: use `scripts/extract_dtx.py` to produce:
  - `njuthesis.cls` — main class file
  - `njuthesis-undergraduate.def` — undergraduate definition
  - `njuthesis-graduate.def` — graduate definition
  - `njuthesis-postdoctoral.def` — postdoctoral definition
- **Logo PDFs** (in `source/`): nju-emblem-black.pdf, nju-emblem-purple.pdf, nju-name-black.pdf, nju-name-purple.pdf
- **Sample entry**: `template/njuthesis-sample.tex` + `template/njuthesis-setup.def`

## Font system

Uses ctex with `fontset=win` — all font loading is internal to the class via `\cs_new:Npn \@@_loadfont_cjk_win:N` and `\cs_new:Npn \@@_loadfont_latin:n`.

### fontset=win — font name resolution

The template uses font NAMES (not Path+filename):

Latin (line ~4920):
```
\setmainfont{Times New Roman}    # ✅ Docker system font
\setsansfont{Arial}              # ❌ Not in Docker → Liberation Sans
\setmonofont{Courier New}        # ❌ Not in Docker → Liberation Mono
```

CJK (line ~5031):
```
\setCJKmainfont{SimSun}[AutoFakeBold=2.17,ItalicFont=KaiTi]
\setCJKsansfont{SimHei}          # ✅ Docker system font
\setCJKmonofont{FangSong}        # ❌ needs simfang.ttf + Path=
\setCJKfamilyfont{zhkai}{KaiTi}  # ❌ needs simkai.ttf + Path=
\setCJKfamilyfont{zhfs}{FangSong}# ❌ needs simfang.ttf + Path=
```

### Pre-extraction: fix docstrip installer section

The `.cls` and `.def` files from the GitHub source repo (`source/` or repo root) are NOT directly compilable — they retain a docstrip installer header that produces `Too many }'s` and `Undefined control sequence` errors.

**Required fix** (apply to `njuthesis.cls`, `njuthesis-undergraduate.def`, `njuthesis-graduate.def`, `njuthesis-postdoctoral.def`):

1. **Comment out the installer block** (typically line ~43-71): bare `}`, `\obeyspaces`, `\Msg{...}` lines, and `\endbatchfile`. Prepend `% ` to each line.

2. **Comment out stray description lines** that follow `\NeedsTeXFormat` or precede `\ProvidesExplFile`:
   ```
   OLD:   {Thesis template for Nanjing University}       (cls line ~75)
   NEW: %  {Thesis template for Nanjing University}
   ```
   Same for the `{Undergraduate/Graduate/Postdoctoral definition...}` lines in the `.def` files.

3. **Hardcode `\ExplFileDate` macros**: Replace docstrip-only macros with literal values:
   ```latex
   OLD: \ProvidesExplClass{njuthesis}{\ExplFileDate}{\ExplFileVersion}{\ExplFileDescription}
   NEW: \ProvidesExplClass{njuthesis}{2026/05/30}{1.5.1}{Thesis template for Nanjing University}
   ```
   Same pattern for `\ProvidesExplFile` in all three `.def` files.

> **Note**: The `scripts/extract_dtx.py` script filters by docstrip guard tags but does NOT strip the installer header section — those lines have no guard tag and pass through to all outputs. Manual commenting is required regardless.

**Verification**: After these fixes, `\NeedsTeXFormat{LaTeX2e}` should be the first active line in each file, followed immediately by `\ProvidesExplClass`/`\ProvidesExplFile`.

## Required patches for Docker compilation

**Latin fonts** — change in `\@@_loadfont_latin:n` and `\@@_loadfont_latin_win:`:
```latex
% OLD:
\__fontspec_main_setsansfont:nn { } { Arial }
% NEW:
\__fontspec_main_setsansfont:nn { } { Liberation~Sans }

% OLD:
{ \@@_loadfont_latin:n { Courier~New } }
% NEW:
{ \@@_loadfont_latin:n { Liberation~Mono } }
```

**CJK fonts** — change in `\@@_loadfont_cjk_win:N`:
```latex
% OLD:
\setCJKmainfont { SimSun } [ #1, ItalicFont = KaiTi ]
\setCJKmonofont { FangSong } [#1]
\setCJKfamilyfont { zhfs } { FangSong } [#1]
\setCJKfamilyfont { zhkai } { KaiTi } [#1]
% NEW:
\setCJKmainfont { SimSun } [#1]                          % drop ItalicFont
\setCJKmonofont [ Path = ./font/, #1 ] { simfang.ttf }
\setCJKfamilyfont { zhfs } [ Path = ./font/, #1 ] { simfang.ttf }
\setCJKfamilyfont { zhkai } [ Path = ./font/, #1 ] { simkai.ttf }
```

### init.sh fonts needed
```
simkai.ttf   (楷体)
simfang.ttf  (仿宋)
```

### .gitignore PDF exceptions
```
!nju-emblem-black.pdf
!nju-emblem-purple.pdf
!nju-name-black.pdf
!nju-name-purple.pdf
```
