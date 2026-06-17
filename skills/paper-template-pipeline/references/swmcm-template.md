# 数维杯（SWMCM / ShuWei Cup）数学建模 LaTeX 模板

## 模板特征

数维杯（ShuWei Mathematical Contest in Modeling）模板使用 `swmcmthesis.cls` 文档类，基于标准 `article` 类（非 ctexbook）。原始为 **pdflatex** 设计，纯英文（零 CJK 依赖）。

## 来源与结构

| 属性 | 本会话案例 (2025 v1.6) |
|------|----------------------|
| TeXPage UUID | `906d45e0-818c-4de5-b714-89488971475b` |
| 文档类 | swmcmthesis.cls (v1.6, by latexstudio.net) |
| 基础类 | article（非 ctexbook/ctexrep） |
| 语言 | English-only |
| 上游仓库 | TeXPage-only（无 GitHub 源仓库） |
| 源文件来源 | GitHub fork `Riyer4ever/2025SHUWEICUPAutumn`（通过 `gh search code` 发现） |
| 飞书仓库 | iftaken/shuweibei-2025 |

## 文件清单

| 文件 | 用途 | 说明 |
|------|------|------|
| swmcmthesis.cls | 文档类 | article-based, 514 lines |
| swmcmthesis.cfg | 配置文件 | 标签名/常量（82 lines），`\AtBeginDocument` 加载 |
| main.tex (demo.tex) | 示例论文 | 271 lines，含 thebibliography 参考文献 |
| figures/gongzhonghao-n.jpg | 公众号二维码 | 258×258 JPEG |
| swmcmthesis.cfg | 配置文件 | 标签名/常量 |

## cls 关键特征

### 包依赖（原始 pdflatex）

```
\LoadClass[a4paper,12pt]{article}
\RequirePackage{ifxetex}
\RequirePackage{geometry}
\RequirePackage{amsmath, amsfonts, amssymb, bm}
\RequirePackage{CJKnumb}           ← 需移除（英文模板无用）
\RequirePackage{titletoc}
\RequirePackage[x11names,svgnames,dvipsnames]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{array,lastpage}
\RequirePackage{longtable, booktabs, multirow, bigstrut}
\RequirePackage{cprotect}
\RequirePackage{listings}
\RequirePackage{lipsum, url, mwe}
\RequirePackage{newtxtext}          ← 需移除（pdflatex 字体包）
\RequirePackage{newtxmath}          ← 需移除（pdflatex 字体包）
\RequirePackage{caption, enumitem}
\RequirePackage{ulem, pdfpages, calc}
\RequirePackage[titletoc,title]{appendix}
\RequirePackage{subfigure}          ← 废弃包，但 demo 使用 \subfigure
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{cleveref}
```

### cls 中已注释的 XeTeX 字体分支

原始 cls 中 lines 89-93 有被注释掉的 XeTeX 字体设置：
```latex
% \setmainfont{Times New Roman}
% \setCJKmainfont[AutoFakeBold = {2.15}]{SimSun}
```
这表明作者曾考虑过 XeTeX 支持但未启用。**但这些行不完整**——只设置了 CJK 字体，缺少 `fontspec` 加载。

### 特殊约定

- `\AtBeginDocument{\makeatletter\input{swmcmthesis.cfg}\makeatother}` — cfg 在文档开始时加载
- 使用 `\abstract{...}` 和 `\keywords{...}` 命令（被 redefined 为 token 存储）
- 使用 `\zubie{ABCD}` 和 `\baominghao{...}` 设置选题和报名号
- `\maketitle` 生成封面页（含选题、报名号、摘要、关键词）
- 使用 `thebibliography` 环境而非 BibTeX

## tectonic XeLaTeX 适配步骤

### 步骤 1：移除 pdflatex 字体包

```latex
% 删除:
\RequirePackage{newtxtext}
\RequirePackage{newtxmath}

% 替换为:
\RequirePackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Liberation Sans}
\setmonofont{Liberation Mono}
```

**说明**：`newtxtext`/`newtxmath` 在 XeTeX 下与 fontspec 冲突（见 pipeline pitfall）。Times New Roman / Liberation Sans / Liberation Mono 均为 Docker 系统字体，无需下载。

### 步骤 2：移除 CJKnumb

```latex
% 删除:
\RequirePackage{CJKnumb}
```

**说明**：CJKnumb 提供 `\CJKnumber` 等中文数字命令。此模板为纯英文，不需要。cls 中被注释的 `\ctexset` 块（lines 375-391）也不会被编译。

### 步骤 3：修复 cfg 中的中文字符

`swmcmthesis.cfg` 中 `\newcommand*{\swmcm@cap@appendixname}{附录}` 包含中文字符。无 CJK 支持的 XeTeX 无法渲染。

```latex
% 改为:
\newcommand*{\swmcm@cap@appendixname}{Appendix}
```

### 步骤 4：init.sh

```bash
#!/usr/bin/env bash
set -e
FONT_DIR="font"
FONT_FILES=()   # 空数组 — 纯英文，零 CJK 依赖
# 注意：空数组 + set -u 会触发 unbound variable
# 使用时建议只用 set -e，或先检查数组长度
```

**关键 pitfall**：`set -euo pipefail` 中的 `-u` 会使空数组 `for f in "${FONT_FILES[@]}"` 失败。只使用 `set -e`。

### 步骤 5：references.bib

模板使用 `thebibliography` 环境（非 BibTeX），但心河Paper 系统要求 `references.bib` 存在。创建占位文件即可：

```bibtex
% references.bib - 占位文件
% 模板使用 thebibliography 环境而非 BibTeX
@misc{latexstudio,
  author = {LaTeXStudio},
  title = {LaTeXStudio.net},
  year = {2025},
  url = {https://www.latexstudio.net}
}
```

### 步骤 6：.gitignore 特殊项

模板使用 `gongzhonghao-n.jpg` 图片，不会被 `*.pdf` 规则误杀。但 `lastpage` 包生成 `.dat` 编译产物需排除：

```
*.dat
```

## 编译结果

- tectonic: exit 0
- main.pdf: ~188KB
- 警告（无害）: accessing absolute path（Docker 系统字体路径）、Underfull \hbox
- 零 Error
- 字体下载: 无（init.sh 为空）
- tectonic 首次编译需下载 x11nam.def, mwe.sty 等 bundle 文件

## 与其他数模模板的区别

| 特征 | 数维杯 (swmcmthesis.cls) | CUMCM (cumcmthesis.cls) | GMCM (GMCMthesis.cls) |
|------|-------------------------|------------------------|----------------------|
| 受众 | 本科生/研究生（国际赛） | 本科生（国赛） | 研究生 |
| 基础类 | article | article | ctexbook |
| ctex 方式 | 无（不加载 ctex） | 宏包 `\RequirePackage{ctex}` | 文档类 `\LoadClass{ctexbook}` |
| 语言 | English-only | 中英混合 | 中英混合 |
| 原始引擎 | pdflatex | pdflatex | XeLaTeX |
| 字体适配 | fontspec + 系统字体 | ctex + simkai 下载 | ctex + simkai 下载 |
| 参考文献 | thebibliography | thebibliography | natbib + gmcm.bst |
| CJK 依赖 | 零 | SimSun/SimHei + simkai | SimSun/SimHei + simkai |
| cfg 文件 | swmcmthesis.cfg | 无（内嵌） | gmcm.cfg |
| 特有依赖 | CJKnumb（可移除）、cprotect | annotate-equations、mdframed | algorithm、algpseudocode |
| newtxtext/math | 是（需移除） | 否 | 否 |

## GitHub 源搜索策略

数维杯模板通常 **TeXPage-only**（无官方 GitHub 仓库）。但学生竞赛仓库常附带完整模板副本，通过 `gh search code` 可快速定位：

```bash
# 搜索 cls 文件名
gh search code swmcmthesis.cls --language tex --limit 10

# 搜索关键词
gh search code "数维杯" --language tex --limit 10
```

**本会话案例**：`gh search code` 发现 10+ 个包含 `swmcmthesis.cls` 的仓库（WuhenGSL/2023_ShuWeiCup, Riyer4ever/2025SHUWEICUPAutumn, peitsan/Courseware-Tex-2023 等）。选择年份匹配的仓库（2025）直接提取 cls/cfg/tex/figures。

优于浏览器逐文件提取（每模板 10-20 分钟），仅需 GitHub API 调用（秒级）。

## Pitfalls

- **CJKnumb 在 XeTeX 下的行为**：`\RequirePackage{CJKnumb}` 在无 ctex/CJK 包的 XeTeX 环境下可能静默失败或产生未定义命令。英文模板可直接移除。
- **cfg 中的中文字符**：`swmcmthesis.cfg` 被 `\AtBeginDocument` 加载，其中的 `附录` 等中文字符在无 CJK 支持的 XeTeX 下会报 `Missing character` 错误。应统一为英文。
- **lastpage + hyperref 冲突风险**：cls 同时加载 `lastpage` 和 `hyperref`，理论上可能触发 `\c@abspage` 双重定义（见 pipeline pitfall）。但本会话案例编译通过，未触发。
- **subfigure 废弃包**：cls 加载 `\RequirePackage{subfigure}` 且 demo 使用 `\subfigure{...}`。tectonic 可自动下载 subfigure.sty。若需更新，替换为 `subcaption`。
- **lipsum/mwe 示例依赖**：demo.tex 使用 `\lipsum` 和 `example-image-a/b`。tectonic 自动下载 mwe.sty。正式论文无需这些包。
- **template 年份版本**：数维杯模板每年更新（v1.3.1 2023 → v1.6 2025），TeXPage UUID 对应特定版本。cls 中 `\ProvidesClass{swmcmthesis}[2025/11/05 v1.6]` 标注了版本。
- **init.sh 空数组 + set -u**：占位模式的 init.sh 使用 `FONT_FILES=()`（空数组）。若脚本有 `set -euo pipefail`（含 -u），则 `for f in "${FONT_FILES[@]}"` 触发 `unbound variable`。修复：只用 `set -e` 无 `-u`，或在 for 前检查 `${#FONT_FILES[@]} -eq 0`。
