# 亚太数学建模（APMCM）LaTeX 模板

## 模板来源

| 源 | 地址 | 说明 |
|----|------|------|
| GitHub | `latexstudio/APMCMThesis` | LaTeX Studio 官方，2019 年发布 |
| TeXPage | `cf703278-5044-4b2c-ab49-8bb144fcd101` | TeXPage 平台镜像 |

## 模板特点

- **文档类**：`apmcmthesis` (基于 `article`，**非 ctexart**)
- **引擎分支**：`\ifxetex` 分支加载 ctex + Times New Roman；`\else` 分支加载 CJK + newtxtext/newtxmath（PDFLaTeX）
- **参考文献**：`thebibliography` 环境（手动，非 BibTeX / .bib）
- **控制页**：`\makecontrolsheet` 命令生成 APMCM Control Sheet
- **定理环境**：definition, theorem, lemma, corollary 等通过 `.cfg` 文件配置英文名称

## Docker 编译：零字体依赖

ctex 在 Docker Linux 上自动检测 Fandol fontset（而非 windows，即使 Docker 有 SimSun/SimHei）。
Fandol 四体（Song/Hei/Kai/Fang）全部在 tectonic bundle 中可用。

| 字体层 | Docker 路径 | 来源 |
|--------|------------|------|
| English serif | Times New Roman | Docker 系统字体 |
| CJK song | FandolSong | ctex Fandol fontset ✓ |
| CJK hei | FandolHei | ctex Fandol fontset ✓ |
| CJK kai | FandolKai | ctex Fandol fontset ✓ |
| CJK fang | FandolFang | ctex Fandol fontset ✓ |

**结论**：零字体下载。init.sh 为空（仅创建 font/ 目录）。

## 必需适配（3 处）

| # | 位置 | 原内容 | 替换 | 原因 |
|---|------|--------|------|------|
| 1 | main.tex | `\CJK{UTF8}{gbsn}{中文文字}` | `中文文字`（纯文本） | PDFLaTeX 专有命令，XeTeX 下 CJK 宏包未加载 → Undefined control sequence |
| 2 | apmcmthesis.cfg | 缺少 `\tzmcm@cap@abstractname` | 添加 `\newcommand*{\tzmcm@cap@abstractname}{Abstract}` | cls line 309 `\renewcommand\abstractname{\tzmcm@cap@abstractname}` 引用了未定义的宏 |
| 3 | main.tex | 原注释块（PDFLaTeX 推荐说明） | 替换为心河Paper 标准注释块 | 信息更新，非功能性 |

### `\CJK{UTF8}{gbsn}{...}` 移除（关键步骤）

这是 LaTeX Studio 老模板的通用模式。在 main.tex 中搜索所有 `\CJK{UTF8}{gbsn}{...}` 出现位置，替换为纯中文文本。方法：

```bash
# 扫描所有 CJK/UTF8 命令
grep -n 'CJK{UTF8}' main.tex
```

在 XeTeX 模式下，`\ifxetex` 分支加载 ctex 而非 CJK，导致 `\CJK` 命令未定义。直接删除 `\CJK{UTF8}{gbsn}{` 前缀和对应的 `}` 闭合括号即可。

## 无需适配项

- **lastpage 包**：模板使用 `\RequirePackage{array,lastpage}` + `\pageref{LastPage}`。只要不同时加载 hyperref（会引入 zref-abspage 定义 `\c@abspage`），lastpage 在 tectonic TL2023 中正常工作。**不需移除**。
- **Times New Roman**：`\setmainfont{Times New Roman}` 在 Docker 中通过系统字体可用（TIMES.TTF 等）
- **newtxtext/newtxmath**：仅在 `\else`（PDFLaTeX）分支加载，XeTeX 路径不执行，安全
- **EPS 图片**：模板仅使用 cat.pdf + gongzhonghao.jpg，无 EPS 依赖

## .gitignore 特别处理

模板资源 `figures/cat.pdf` 会被 `*.pdf` 规则误杀。添加例外：

```
!main.pdf
!figures/cat.pdf
```

## 编译结果

- tectonic 编译：通过（1 次 re-run，aux 变化触发）
- main.pdf：~169KB
- 警告（无害）：accessing absolute path `/usr/local/share/fonts/custom/TIMES*.TTF`
- 无 Error

## 与 GMCM 模板的区别

| 特性 | APMCM (latexstudio/APMCMThesis) | GMCM (andy123t/GMCMthesis) |
|------|------|------|
| 基类 | `article` | `ctexart` |
| CJK 管理 | ctex 宏包（XeTeX 分支） | ctexart 文档类 |
| 参考文献 | thebibliography（手动） | natbib + gmcm.bst（BibTeX） |
| 字体策略 | ctex Fandol auto-detect | fontset=fandol 显式设置 |
| 代码环境 | listings（Matlab/Lingo 示例） | listings + algorithm/algpseudocode |
| `\CJK{UTF8}{gbsn}` | 有（需移除） | 无 |
| EPS 图片 | 无 | 有（4 个，需转换） |
| 控制页 | `\makecontrolsheet` 内置 | 无 |
