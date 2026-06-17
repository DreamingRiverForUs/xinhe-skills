# 计算机学报 (CJC) 模板参考

## 模板概述

- **期刊名**: 计算机学报 (Chinese Journal of Computers)
- **目标仓库**: `iftaken/cjc-template`
- **来源**: TeXPage `c234b182-5375-41d3-a7d9-1158bd268b57` → 预准备源仓库 `iftaken/cjc_latex_template`
- **分类**: 期刊投稿

## 文档类架构

- `main.cls` — 自定义类，基于 `article` (a4paper, 10.5pt, twocolumn, twoside, journal)
- **非 ctex 体系**！不使用 ctexbook/ctexrep，自定义了 `\zihao` 命令和 `\normalsize` 等级
- CJK 方案：`main.tex` 中显式加载 `xeCJK` + 逐一声明 `\setCJKmainfont`/`\setCJKfamilyfont`
- 兼容层：映射旧的 `CJK`/`CJK*` 环境到 xeCJK 字体族（通过 `\CJKfamily{zhsong}` 等）

## 字体需求

| 字体族 | 文件 | 用途 |
|--------|------|------|
| zhsong | simsun.ttc (Path=./font/) | 正文宋体 |
| zhhei | simhei.ttf (Path=./font/) | 标题黑体 |
| zhkai | simkai.ttf (Path=./font/) | 致谢等（实际使用很少） |
| zhfs | simfang.ttf (Path=./font/) | 作者名、证明 |

**实际编译只需 4 个字体**（simsun/simhei/simkai/simfang）。init.sh 还声明了 simli/simyou 但模板未实际使用。

### Docker 字体回退：SimSun → Fandol

Docker tectonic 镜像不含 SimSun/SimHei 等 Windows 字体，且 init.sh 所需的 `font_url.txt`
不在仓库中（模板打包遗漏），无法通过 init.sh 下载。

**修复**：将 main.tex 中的 xeCJK 字体声明全部改为 Fandol（tectonic bundle 内置，零下载）：

```latex
% 原文（Docker 中不可用）：
\setCJKmainfont{simsun.ttc}[Path=./font/]
\setCJKsansfont{simhei.ttf}[Path=./font/]
\setCJKmonofont{simkai.ttf}[Path=./font/]
\setCJKfamilyfont{zhsong}{simsun.ttc}[Path=./font/]
\setCJKfamilyfont{zhhei}{simhei.ttf}[Path=./font/]
\setCJKfamilyfont{zhfs}{simfang.ttf}[Path=./font/]
\setCJKfamilyfont{zhkai}{simkai.ttf}[Path=./font/]

% 改为 Fandol（tectonic bundle 内置，即改即用）：
\setCJKmainfont{FandolSong-Regular.otf}
\setCJKsansfont{FandolHei-Regular.otf}
\setCJKmonofont{FandolKai-Regular.otf}
\setCJKfamilyfont{zhsong}{FandolSong-Regular.otf}
\setCJKfamilyfont{zhhei}{FandolHei-Regular.otf}
\setCJKfamilyfont{zhfs}{FandolFang-Regular.otf}
\setCJKfamilyfont{zhkai}{FandolKai-Regular.otf}
```

**副作用**：Fandol 字体的罕见汉字覆盖不如 SimSun 完整，个别生僻字（如 柟 U+67DF）会触发
`Missing character` 警告。这仅影响排版外观，不阻断编译。PDF 正常生成（~320KB）。

**适用场景**：此模式适用于所有使用 `\setCJKmainfont{simsun.ttc}[Path=./font/]` 显式声明
且 init.sh 无法工作的模板。Fandol 提供 Song/Hei/Kai/Fang 四体，覆盖绝大多数 CJK 字符。

## 参考文献

使用 `thebibliography` 环境（顺序编码制），非 bibtex/biblatex。
- 仍需要 `references.bib` 占位文件（心河Paper 系统要求）
- 引文格式：期刊/会议/书籍均有详细模板说明（含中英文对照格式）

## 编译特征

- tectonic 编译通过：仅排版警告（overfull/underfull hbox/vbox），无错误
- 主 PDF 约 187KB
- 使用的宏包：flushend, times, stfloats, cuted, captionhack, picins, ccaption, calc 等
- `mtpro2.sty` 在源码中但 main.tex 中已注释掉（数学字体包，非必需）
- `llncs.cls` / `tst.cls` — 遗留文件，非本模板使用
- `zhwinfonts.tex` — 遗留文件，xeCJK 已替代

## 预编译 main.pdf

源仓库 `iftaken/cjc_latex_template` 已包含预编译的 `main.pdf`（192KB 旧版），Docker 重编译后更新为 187KB。上线前必须重新编译确保一致性。

## 特殊文件

- `captionhack.sty` (489B) — 自定义的 caption 补丁，体积很小，模板特定
- `picins.sty` (17KB) — 图片插入宏包
