# CUG Bachelor Thesis English Template

## Source
- Chinese version: `iftaken/CUG-thesis` (GitHub)
- English version repo: `iftaken/cug-thesis-english`
- TeXPage: https://www.texpage.com/template/ffb844cb-21b8-4557-a90f-79bea9c95e7a

## Template properties
- Pure English, no CJK dependencies
- init.sh: empty (no font downloads needed)
- Base class: article (a4paper, twoside)
- English font: Times New Roman via fontspec
- Bibliography: gbt7714-numerical.bst + natbib
- References file: references.bib

## CJK→English Adaptation Patterns

This template was adapted from a CJK-dependent Chinese thesis template. Key changes:

### main.cls adaptations
1. **Remove CJK packages**: Delete `\RequirePackage[boldfont,slantfont]{xeCJK}` and `\RequirePackage[cs4size,UTF8,heading=true]{ctex}`
2. **Remove CJK font commands**: Delete `\setCJKmainfont`, `\setCJKsansfont`, `\setCJKmonofont`, `\setCJKfamilyfont{song}`, `\setCJKfamilyfont{hei}`, `\newcommand{\song}`, `\newcommand{\hei}`
3. **Remove zhnumber**: Delete `\RequirePackage{zhnumber}`
4. **Replace ctexset with titlesec**: `\ctexset{section={...}}` → `\titleformat{\section}{...}`
5. **Fix tocloft indents**: `\ccwd` (CJK character width) → explicit `em` values (e.g., `2em`, `4em`)
6. **Translate Chinese strings**: All hardcoded Chinese text → English equivalents
7. **Keep fontspec for English**: `\setmainfont{Times New Roman}`, optionally `\setsansfont{Arial}`, `\setmonofont{Courier New}`

### main.tex adaptations
1. Translate cover page, statement of originality, abstract titles, TOC title, section headers
2. `\makeToc` → Contents (not 目录)
3. `\bibliography` addcontentsline: "参考文献" → "References"
4. `\section*{致谢}` → `\section*{Acknowledgements}`
5. Cover page: Chinese labels → English (学号→Student ID, 姓名→Name, etc.)

### Chapter files
1. Translate all Chinese content to English
2. `\section{绪论}` → `\section{Introduction}`, etc.

## Pitfalls

### Chinese abstract with pure English fonts
The `cnabstract` environment in main.cls renders Chinese text. Since the template has no CJK font fallback (no xeCJK/ctex), Chinese characters render as missing glyphs (□□□). This is **acceptable** for a pure English template — the Chinese abstract is sample content, and users who need CJK rendering should add xeCJK/ctex back.

Fix if needed: add `\usepackage{xeCJK}` and CJK font declarations back to the cls.

### Times New Roman Bold can't render CJK
The `\paragraph{\xiaosihao \bfseries 关键词：}` in the `cnabstract` environment uses bold, which switches to Times New Roman Bold — also without CJK coverage. Same acceptable limitation.

### xdvipdfmx warnings about already-defined page objects
`warning: Object @page.N already defined` — known tectonic issue, safe to ignore.
