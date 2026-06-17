# Batch H — June 2026 (ustb–xauat)

Repos: ustb-thesis, ustc-thesis, ustc-thesis-template, whu-proposal, whu-thesis, whut-thesis, wzu-thesis, xauat-thesis

## New PII patterns discovered in this batch

### 1. Maintainer lists in .cls headers (whu-thesis)
Three maintainers with personal QQ emails:
```
%% The Current Maintainers of this work are
%%   Siyu Wu <2401336502@qq.com>
%%   Kangwei Xia <kangweixia_xdyy@163.com>
%%   Anbo Tao <398943960@qq.com>
```
→ Replace all with English fake names + `example@example.com`.

### 2. Personal Gitee repos (whu-proposal)
```
% Gitee: https://gitee.com/xkwxdyy/whu-proposal
```
→ Strip entirely. iftaken has no Gitee presence. Already covered by link handling policy.

### 3. QQ group numbers in code comments (whu-proposal)
```
% QQ group: 681965476
```
→ Remove the line. Same treatment as QQ numbers in text.

### 4. .dtx acknowledgment personal names (whu-thesis)
```
% 向fduthesis的作者曾祥东先生表示感谢
```
→ Replace name with fake: `向fduthesis的作者张三先生表示感谢`.

### 5. Copyright with personal name (whu-proposal .cls)
```
% Copyright (c) 2023 Kangwei Xia
```
→ `% Copyright (c) 2023 iftaken`

### 6. demo.tex mirrors main.tex PII (whu-thesis)
`demo.tex` has identical `\whusetup{info={...}}` block with same placeholder names as `main.tex`. Even though both were already placeholders (张三, 李某某), the pattern of mirroring means demo.tex must always be scanned with same rigor.

### 7. AGENTS.md source-author fields (ustb-thesis)
```
- **来源**: YiFraternity/USTBThesis (作者: 刘宇航)
```
→ `作者: 模板维护者`. Common pattern — the author name after the source org.

### 8. Email in LaTeX comments with real name (whu-proposal main.tex)
```
% Author: Kangwei Xia, kangweixia_xdyy@163.com, School of Mathematics and Statistics, Wuhan University
```
→ Strip name+email, keep institutional affiliation: `% Author: 模板维护者, School of Mathematics and Statistics, Wuhan University`

### 9. Large-scale bib Chinese name scrubbing (all repos)
Every repo in this batch contains `.bib` files with dozens of real Chinese author names from published papers. The bib files serve as template examples, not actual paper references. Use the standard bib scrubbing rule: replace all individual Chinese author names with cycling placeholders (张三/李四/王五/赵六), update bib keys to match. Institutional authors (e.g., `中华医学会湖北分会`, `中国图书馆学会`) are preserved.

### 10. LaTeX doc .tex files have separate author/email (ustc-thesis-template)
`ustcthesis-doc.tex` has `\author{Zeping Lee\thanks{zepinglee AT gmail.com}}` — different file, different PII from `main.tex`. Doc files need separate scanning even when they're not the compile target.
