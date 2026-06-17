# 全国大学生数学建模（CUMCM）LaTeX 模板

## 模板特征

CUMCM 模板使用 `cumcmthesis.cls` 文档类，基于 `article` + `ctex`（作为宏包加载，非文档类）。常见于 TeXPage "数模竞赛"分类。**有两个常见上游变体**，适配策略因版本而异。

## 变体 A：KOKO 增强版（含多种自定义环境）

| 属性 | 值 |
|------|----|
| TeXPage | `4c847050-151c-4c7e-8db7-e2dd71e3d465` |
| 作者 | KOKO (sysu) |
| 上游仓库 | sleepyy-dog/Survival-Handbook-by-KOKO |
| 源文件 | ZIP 包 `2026数学建模国赛通用模板.zip`（在数学建模/子目录） |
| 文档类 | cumcmthesis.cls (基于 article，ctex 作为宏包) |

**关键文件**：
- `cumcmthesis.cls` — 文档类（竞赛格式：承诺书、编号页、标题格式）
- `article.tex` → 重命名为 `main.tex`
- `structure.tex` — 自定义环境和宏（info/warn/guess/question/pictextblock）
- `annotate-equations.sty` — 公式批注宏包（依赖 tikz, tikzmark）
- `gbt7714-numerical.bst` — 参考文献样式
- `ref.bib` → 重命名为 `references.bib`

## 变体 B：LaTeX Studio 官方版（简洁，推荐优先使用）

| 属性 | 值 |
|------|----|
| 上游仓库 | latexstudio/CUMCMThesis |
| 示例 TeXPage | `22457621-f2d4-4ef6-882e-4231f4adf620` |
| 结构 | 单文件 example.tex + cumcmthesis.cls + figures/ |
| 参考文献 | `thebibliography` 手动管理（非 BibTeX） |

**关键文件**：
- `cumcmthesis.cls` — 文档类（与变体 A 相似但更简洁）
- `example.tex` → 重命名为 `main.tex`
- `figures/` — 示例图片（cat.pdf, f1.png, gongzhonghao2.png, smokeblk.pdf）
- 无 `structure.tex`、`annotate-equations.sty`、`gbt7714-numerical.bst`

**变体 B 适配要点**（两处即可）：
1. `\setsansfont{Arial}` → `\setsansfont{Liberation Sans}`
2. `\setCJKfamilyfont{kai}[AutoFakeBold]{simkai.ttf}` → `[AutoFakeBold,Path=font/]{simkai.ttf}`
3. `references.bib` 为占位文件（模板用 thebibliography，不依赖 BibTeX）
4. init.sh 仅需下载 simkai.ttf

## Docker 字体适配

### 变体 A（KOKO 增强版）字体适配

| 原声明 | Docker 适配 | 位置 |
|--------|------------|------|
| `\setsansfont{Arial}` | `\setsansfont{Liberation Sans}` | cls |
| `\setmonofont[Contextuals={Alternate},ItalicFont=Fira Code...]{YaHei.Consolas.1.11b.ttf}` | `\setmonofont[...]{DejaVu Sans Mono}` | cls |
| `\newfontfamily\yaheiconsola{YaHei.Consolas.1.11b.ttf}` | `\newfontfamily\yaheiconsola{DejaVu Sans Mono}` | cls |
| `\setCJKfamilyfont{kai}[AutoFakeBold]{simkai.ttf}` | `[AutoFakeBold,Path=font/]{simkai.ttf}` | 需 Path= 指向 font/ |
| `\setCJKfamilyfont{song}[AutoFakeBold]{SimSun}` | 不变 | Docker 系统字体 ✓ |

### 变体 B（LaTeX Studio 官方版）字体适配（两处即可）

| 原声明 | Docker 适配 | 位置 |
|--------|------------|------|
| `\setsansfont{Arial}` | `\setsansfont{Liberation Sans}` | cls:157 |
| `\setCJKfamilyfont{kai}[AutoFakeBold]{simkai.ttf}` | `[AutoFakeBold,Path=font/]{simkai.ttf}` | cls:158 |
| `\setmainfont{Times New Roman}` | 不变 | Docker 系统字体 ✓ |
| `\setCJKfamilyfont{song}[AutoFakeBold]{SimSun}` | 不变 | Docker 系统字体 ✓ |

**init.sh 只需下载 simkai.ttf**（两变体相同）：
```
https://xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com/font/simkai.ttf
```

### 变体 B 特有：references.bib 为占位文件

变体 B 使用 `thebibliography` 环境手动管理参考文献（非 BibTeX），不依赖 `.bib` 文件。`references.bib` 仅作为心河Paper 系统的必需占位文件存在，内容可以为空（一行注释即可）。

### 变体 A ctex + fontspec 加载关系

cumcmthesis.cls 加载顺序：
1. `\RequirePackage{ctex}` (line 40) — 内部自动加载 fontspec（无选项）
2. `\RequirePackage{fontspec}` (line 104) — 重复加载，无选项冲突（fontspec 已加载，no-op）
3. xcolor 先以 `[dvipsnames]` 加载 (line 50)，后续 `\RequirePackage{xcolor}` (line 70) 为 no-op

**无选项冲突**：因为两次 fontspec 加载都不带选项，不会触发 "Option clash"。

### 变体 B fontspec 加载（更简洁）

变体 B 的 cumcmthesis.cls 仅加载 `\RequirePackage{ctex}`（内部自动 fontspec），无第二次 fontspec 加载，更干净。无 `\RequirePackage{xcolor}` 重复加载问题。

## 编译结果（变体 A vs B）

| 指标 | 变体 A（KOKO 增强版） | 变体 B（LaTeX Studio 官方版） |
|------|----------------------|---------------------------|
| 编译引擎 | tectonic XeLaTeX | tectonic XeLaTeX |
| main.pdf | ~215KB | ~584KB |
| 依赖复杂度 | 中（mdframed+TikZ, annotate-equations） | 低（mdframed+TikZ） |
| 参考文献 | thebibliography + gbt7714-numerical.bst | thebibliography（手动） |
| 适配难度 | 中（5处字体修改 + init.sh） | 低（2处字体修改 + init.sh） |
| references.bib | 含实际内容 | 占位文件 |

**推荐**：优先使用变体 B（latexstudio/CUMCMThesis）——结构更简洁、适配更少、PDF更大（示例内容更多）。变体 A 适用于需要 KOKO 自定义环境（info/warn/guess/question/pictextblock）的场景。

## 与 GMCM 模板的区别

| 特征 | CUMCM (cumcmthesis.cls) | GMCM (GMCMthesis.cls) |
|------|------------------------|----------------------|
| 受众 | 本科生 | 研究生 |
| 基础类 | article | ctexbook |
| ctex 方式 | 宏包 `\RequirePackage{ctex}` | 文档类 `\LoadClass{ctexbook}` |
| 字体检测 | 无 IfFontExistsTF | 多平台 IfFontExistsTF 回退 |
| 参考文献 | thebibliography + gbt7714-numerical.bst | natbib + gmcm.bst |
| 特有依赖 | annotate-equations, mdframed+TikZ | algorithm+algpseudocode |

## TeXPage-only 来源处理

变体 A：本模板有 GitHub 上游，但源文件在 ZIP 包中（非裸 .tex/.cls）。处理流程：
1. 用 GitHub API (`gh api repos/.../contents/...`) 浏览目录树
2. 下载 ZIP 文件（raw.githubusercontent.com）
3. `unzip` 提取到临时目录
4. 复制文件到目标仓库

变体 B：直接 `gh repo clone latexstudio/CUMCMThesis` 即可获取全部源文件（已包含 .cls 和 .tex），无需 ZIP 解包。
