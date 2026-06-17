# 研究生数学建模（GMCM）LaTeX 模板

## 模板来源

GMCM 模板有两个主流 GitHub 源：

| 源 | Stars | cls 版本 | 特点 |
|----|-------|---------|------|
| andy123t/GMCMthesis | ~5 | v2.4 (by latexstudio.net/andy123t) | 多平台字体检测、gmcm.bst 参考文献样式、历年 logo 完整 |
| springli07/GMCM_LaTeX_overleaf | 21 | v2.2 (based on zhanwen/MathModel) | 内置 .ttf 字体文件在根目录、单文件 main.tex、figures/ 含 logo2025.png + title2025.pdf |

**选择 andy123t/GMCMthesis**：功能更完善（多平台字体回退、natbib + gmcm.bst），结构更适合心河Paper 标准。

## 适配要点

### Docker 编译：零字体依赖（关键发现）

在 Docker Linux 环境下，应**显式**设置 `fontset=fandol`（`\documentclass[bwprint,fontset=fandol]{gmcmthesis}`）。Docker 镜像有 SimSun 系统字体，ctexart 可能 auto-detect 为 windows fontset 而非 fandol，而 windows 分支的 KaiTi 在 Docker 中不可用。

gmcmthesis.cls 的 `\ifmcm@fandol` 分支接管全部字体配置：

| 字体层 | Docker 路径 | 来源 |
|--------|------------|------|
| English serif | Times New Roman（或 texgyretermes） | Docker 系统字体 / tectonic bundle |
| English sans | Liberation Sans（或 texgyreheros） | Docker 系统字体 / tectonic bundle |
| English mono | Liberation Mono（或 texgyrecursor） | Docker 系统字体 / tectonic bundle |
| CJK song | FandolSong | ctex fandol fontset ✓ |
| CJK hei | FandolHei | ctex fandol fontset ✓ |
| CJK kai | FandolKai | ctex fandol fontset ✓ |
| CJK fang | FandolFang | ctex fandol fontset ✓ |

**安全策略**：将 fandol 分支的英文字体改为 Docker 系统字体（Times New Roman / Liberation Sans / Liberation Mono），避免 TeX Gyre 字体在 tectonic bundle 中不可用的风险。同时将 `\else` 非 fandol 分支的 Arial/Courier New 也改为 Liberation Sans/Mono 作为兜底。

**结论**：零字体下载。仅需 4 处字体 patch + EPS→PDF 转换。

### 必需适配（4 处 + EPS 转换）

| # | 位置 | 原声明 | 替换 | 原因 |
|---|------|--------|------|------|
| 1 | gmcmthesis.cls:~100 (Matlab listings) | `basicstyle=\small\fontspec{Courier New}` | `basicstyle=\small\ttfamily` | fontspec 按系统字体名查找 Courier New，Docker 无此字体 |
| 2 | gmcmthesis.cls:~224-246 (fandol 分支) | `\setmainfont{texgyretermes}` + `\setsansfont{texgyreheros}` + `\setmonofont{texgyrecursor}` | `\setmainfont{Times New Roman}` + `\setsansfont{Liberation Sans}` + `\setmonofont{Liberation Mono}` | TeX Gyre 在 tectonic bundle 不一定有，改用 Docker 系统字体 |
| 3 | gmcmthesis.cls:~249 (非 fandol 分支) | `\setsansfont{Arial}` | `\setsansfont{Liberation Sans}` | Docker 无 Arial |
| 4 | gmcmthesis.cls:~253 (非 fandol 分支) | `\setmonofont[Scale=MatchLowercase]{Courier New}` | `\setmonofont{Liberation Mono}` | Docker 无 Courier New |
| 5 | main.tex `\documentclass` | `[bwprint]` | `[bwprint,fontset=fandol]` | 显式强制 fandol，避免 Docker 因 SimSun 存在而 auto-detect windows |

### EPS 图片转换

模板 figures/ 含 4 个 `.eps` 示例图片，tectonic 不支持 EPS。用 Ghostscript 转换：

```bash
cd figures && for f in *.eps; do gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="${f%.eps}.pdf" -dEPSCrop "$f"; done
```

### 文件重命名

| 原文件名 | 新文件名 | 原因 |
|----------|----------|------|
| example.tex | main.tex | 心河Paper 系统要求 |
| reference.bib | references.bib | 心河Paper 系统要求 |

### 特有依赖

- `gmcm.bst`：BibTeX 参考文献样式文件，tectonic 自动发现项目根目录下的 .bst
- `natbib`：`\RequirePackage[numbers]{natbib}` + `\bibliographystyle{gmcm}`
- `algorithm` + `algpseudocode`：算法排版（main.tex 中额外加载）
- `mdframed` + TikZ：代码框样式
- `subfig`、`siunitx`、`colortbl`：图表增强

## 编译结果

- tectonic 编译：通过（3次 re-run）
- main.pdf：~940KB
- 警告（无害）：algorithm.sty UTF-8 invalid byte、PDF version mismatch (1.6/1.7→1.5)、Object @page.1 already defined
- 无 Error

## springli07 版本差异（备用参考）

如需切换到 springli07 版本，额外适配工作：
1. 根目录 5 个 .ttf 需移入 font/ 目录并从 git 排除
2. cls 中 `\setCJKmainfont{SimSun.ttf}` 需加 `[Path=./font/]`
3. `\setsansfont{Arial}` → `\setsansfont{Liberation Sans}`
4. `\setmonofont{Courier New}` → `\setmonofont{Liberation Mono}`
5. 无 gmcm.bst，参考文献用 `thebibliography` 环境直接书写
6. figures/ 文件名不同（logo2025.png 替代 logo.pdf）
