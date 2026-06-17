# 武汉理工大学硕博学位论文模板 (whutthesis)

- 源: `bohlinz/whutthesis`（Google Code 自动导出，原始作者胡卫谊 2010）
- 格式: DTX + docstrip (WHUTthesis.dtx + WHUTthesis.ins)
- 基于: thuthesis v0.1 早期版本（非现代 v7.x）
- TeXPage: `a121049b-b0b4-4509-b7f8-5a1f86b81209`
- 目标: iftaken/whut-thesis

## DTX 提取

生成三个文件：WHUTthesis.cls（cls guard）、WHUTthesis.cfg（cfg guard）、mythesis.tex（myth guard）。.cfg 文件必须一同提取——cls 通过 `\AtEndOfClass{\input{WHUTthesis.cfg}}` 引用，缺失时编译报 `File not found`。

**提取后的 cls 清理**：原始 .dtx 包含 886 行文档代码（ltxdoc driver），有效的 class 代码从第 887 行开始到 `% \Finale`（约第 1770 行）。只保留这个区间。

## 字体策略

**零外部字体依赖**：ctexbook 在 Docker (Linux) 上默认 auto-detect Fandol fontset。西文字体 Times New Roman / Liberation Sans / DejaVu Sans Mono 均可在 Docker 系统字体中找到。

## 适配要点

### 1. 古老 CJK 字体命令（\youyuan / \lishu）

模板示例正文中使用旧的 thuthesis CJK 字体命令，但现代 ctexbook + Fandol 不支持。在 main.tex 中加 shim：

```latex
\providecommand{\youyuan}{\kaishu}
\providecommand{\lishu}{\songti}
```

### 2. slashbox 宏包

`slashbox.sty` 不在 tectonic bundle 中。移除 cls 和 sty 中的 `\RequirePackage{slashbox}`，正文中将 `\backslashbox{x}{y}` 改为纯文本 `x\,/\,y`。

### 3. GBK 编码的 CJK 转义

WHUTtils.sty 的 listings 配置中使用 `escapebegin=\begin{CJK*}{GBK}{kai},escapeend=\end{CJK*}`——CJK 包的 GBK 模式在 XeTeX/tectonic 中不兼容。改为 ctex 命令：

```latex
escapebegin=\kaishu,escapeend={},
```

### 4. footmisc perpage 选项

TL2023 中 `perpage` 与 hyperref 的 `abspage` 计数器冲突。移除 perpage，仅保留 `[symbol*,stable]`。

### 5. 西文字体替换

原模板使用 Arial 和 Courier New——Docker 中不可用：

- `\setsansfont{Arial}` → `\setsansfont{Liberation Sans}`
- `\setmonofont{Courier New}` → `\setmonofont{DejaVu Sans Mono}`

### 6. txfonts 在 XeTeX 模式

原模板使用 `\RequirePackage{txfonts}`（pdflatex 时代数学字体）。在 XeTeX + tectonic 下，tectonic 自动下载需要的 tx*.tfm/vf/pfb 文件，编译通过。无需移除（与 `newtxtext`/`newtxmath` 不同）。

### 7. 参考文献路径

原模板使用 `\bibliography{reference/refs}`，需改为 `\bibliography{references}`，并将 `reference/refs.bib` 复制为 `references.bib`。

### 8. 章节引用

原模板使用 `\include{body/chap03}` 但 chap03.tex 不在源文件中，且 `\include` 会为每章生成独立 .aux 导致 BibTeX/biber 错误。改为：
- 删除缺失的 `\include{body/chap03}`
- 将所有 `\include{body/xxx}` 改为 `\input{body/xxx}`

## init.sh

```bash
#!/bin/bash
set -e
FONT_DIR="font"
mkdir -p "$FONT_DIR"
echo "WHUT Thesis: 零外部字体依赖，ctexbook Fandol 自动检测"
```

## .gitignore 例外

WHUTlogo.pdf 和 whut.pdf 是模板资源 PDF，需在 .gitignore 中加例外：

```
!figure/WHUTlogo.pdf
!figure/whut.pdf
```

## 编译结果

Docker tectonic 编译通过，main.pdf ≈ 1.4 MiB。仅有少量 Fandol 字体缺失罕见 CJK 字符的警告（如 穉、暠、璘 等），不影响使用。
