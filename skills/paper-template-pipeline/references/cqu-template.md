# 重庆大学（CQU）Beamer 汇报模板

## 来源

| 属性 | 值 |
|------|-----|
| TeXPage | https://www.texpage.com/template/2e1885e2-b7d6-4f86-b5b9-8c2752fcb371 |
| TeXPage 作者 | wuz |
| GitHub 源 | Will-hxw/CQU-Beamer-LaTeXPPT |
| 目标仓库 | iftaken/cqu-report |
| 模板类型 | Beamer 学术汇报 |
| 许可证 | CC BY 4.0 |
| 原始引擎 | XeLaTeX |

## 模板结构

```
slide.tex          # 主文件 → main.tex
cqu.sty            # CQU Beamer 主题（基于 THU Beamer Theme）
ref.bib            # 参考文献 → references.bib
pic/校徽+中英文校名_蓝色.pdf   # CQU 校徽
LXGWWenKai-Medium.ttf  # 霞鹜文楷字体（已替换）
```

## 适配要点

### 字体替换

原模板使用 LXGW WenKai（霞鹜文楷）作为导航栏和标题字体：

```latex
\newfontfamily\wenkai{LXGWWenKai-Medium}[Scale=MatchLowercase]
\setCJKsansfont{LXGWWenKai-Medium}[Scale=MatchLowercase]
```

**替换为 FandolKai**（tectonic bundle 内置，无需下载）：

```latex
\newfontfamily\wenkai{FandolKai-Regular.otf}[Scale=MatchLowercase,Extension=.otf]
```

`\setCJKsansfont` 行直接移除（beamer 的 CJK sans 字体由 ctex 默认 manage）。

### 移除 pstricks 和 auto-pst-pdf

- `auto-pst-pdf` 需要 shell-escape，tectonic 不支持 → 直接移除
- `pstricks` 宏包在 tectonic bundle 中不可用 → 移除 `\usepackage[pdf]{pstricks}`
- PSTricks 演示帧（"图形与分栏"）依赖 pstricks → 移除整个 frame

### fontspec 显式加载移除

ctex 在 XeLaTeX 模式下自动加载 fontspec，`\usepackage{fontspec}` 显式加载可移除，避免潜在 option clash。

### 参考文献命名

`\bibliography{ref}` → `\bibliography{references}`（心河Paper 系统标准命名）。

## 编译结果

- Docker tectonic 编译通过
- main.pdf 429KB
- 警告：listofitems.tex UTF-8 警告（stackengine 依赖，安全）、nullfont Missing character（beamer 导航符号，安全）
