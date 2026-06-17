# 浙江传媒学院 thesis 模板（cuzthesis）

## 基本信息

| 字段 | 值 |
|------|-----|
| TeXPage ID | `56ac21df-8e1c-432f-b3ff-3c53e145c6ab` |
| TeXPage URL | https://www.texpage.com/template/56ac21df-8e1c-432f-b3ff-3c53e145c6ab |
| 名称 | 浙江传媒学院本科毕业论文模板 |
| 作者 | Hao XIE (xiehao/cuzthesis) |
| License | GPL v3 |
| 目标仓库 | iftaken/zjicm-thesis |
| GitHub 源 | xiehao/cuzthesis |
| 文档类 | cuzthesis.cls（基于 ctexbook） |

## 模板结构

源仓库包含 5 种文档模式（共享 styles/ 目录）：

| 模式 | .cls | 入口文件 |
|------|------|----------|
| 本科毕业论文 | cuzthesis.cls | cuzthesis-bachelor.tex |
| 硕士毕业论文 | cuzthesis.cls (master 选项) | cuzthesis-master.tex |
| 开题报告 | cuzopening.cls | cuzopening.tex |
| 文献综述 | cuzreview.cls | cuzreview.tex |
| 课程作业 | cuzassignment.cls | cuzassignment.tex |

共享的样式文件（全部需要复制到根目录）：
- `styles/cuzthesis.cls`, `styles/cuzthesis.cfg`, `styles/cuzthesis-master.cfg`
- `styles/cuzcommon.sty`, `styles/artratex.sty`, `styles/artracom.sty`
- `styles/cuzopening.cls`, `styles/cuzreview.cls`, `styles/cuzassignment.cls`

## artratex.sty 适配要点

artratex.sty 是 ucasthesis 派生的通用样式包，在 Docker/tectonic 环境中需做以下修改：

### 1. 移除 newtxmath（XeTeX 分支，line 221）
```latex
% Before:
\RequirePackage[cmintegrals]{newtxmath}% 数学符号字体
% After: remove entirely
```
注意：`newtxtext` (line 205) 在 `\ifpdftex` 分支中，XeTeX 下不会执行，无需处理。

### 2. 等宽字体替换（Linux else 分支，line 272）
```latex
% Before:
\setmonofont{Fira Mono}[Scale=MatchLowercase,]
% After:
\setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase,]
```
Docker 镜像不含 Fira Mono，DejaVu Sans Mono 是可靠的替代。

### 3. 禁用 minted（line 470，需要 shell-escape）
```latex
% Before:
\RequirePackage[newfloat=true]{minted}
% After: comment out
% \RequirePackage[newfloat=true]{minted}% needs -shell-escape, disabled for tectonic
```
同时需注释掉 minted 相关设置：
- `\SetupFloatingEnvironment{listing}{...}`（依赖 minted 的 newfloat 选项定义的 listing 浮动体）
- `\setmintedinline{...}`, `\setminted{...}`
- 所有 `\newminted[...]{...}{...}`, `\newmintinline{...}{}` 声明

### 4. Linux 字体分支（artratex.sty lines 302-338）

Linux 分支使用 Adobe 字体（AdobeSongStd-Light, AdobeHeitiStd-Regular, AdobeKaitiStd-Regular, AdobeFangsongStd-Regular）和特殊中文字体（隶书, 华文新魏, 幼圆），Docker 中均不可用。

由于 cuzthesis.cls 底层是 `ctexbook`（Docker 中自动检测 fandol 字体集），CJK 核心字体（song/hei/kai/fang）由 ctex 管理。artratex.sty 的 Linux 分支覆盖 `\songti`/`\heiti`/`\kaiti` 和 `\setCJKmainfont`/`\setCJKsansfont`/`\setCJKmonofont`，会覆盖 ctex 的 fandol 设置并导致字体找不到。

**待验证的策略**：注释掉 Linux 分支中所有 CJK 字体覆盖（lines 302-338），让 ctexbook 的 fandol 自动检测管理 CJK 字体。`\setmainfont{Times New Roman}`（line 249）保留，Docker 可用。

### 5. 路径扁平化

源仓库使用 `styles/` 和 `src/` 子目录结构。适配时需：
- `.cls` 内部 `\RequirePackage{styles/xxx}` → `\RequirePackage{xxx}`
- `.cls` 内部 `\InputIfFileExists{styles/xxx.cfg}` → `\InputIfFileExists{xxx.cfg}`
- `main.tex` 中 `\documentclass[...]{styles/cuzthesis}` → `\documentclass[...]{cuzthesis}`
- `main.tex` 中 `\usepackage{styles/artratex}` → `\usepackage{artratex}`
- 所有 `\input{src/xxx/yyy}` → `\input{chapters/yyy}`
- `\bibliography{bibliography/references}` → `\bibliography{references}`

### 6. 编译成功的标志

目标：`tectonic -X compile main.tex` 返回 0，生成 `main.pdf` ≥ 10KB。

已知的 Tectonic TL2023 兼容项（安全，无需修复）：
- `lineno.sty:296: Invalid UTF-8 byte` — 宏包内部注释遗留编码，安全
- `algorithm.sty:11: Invalid UTF-8 byte` — 同上
- `accessing absolute path` warnings — tectonic 在 Docker 中访问系统字体的正常行为
