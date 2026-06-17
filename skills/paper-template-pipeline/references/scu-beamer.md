# scubeamer 四川大学 Beamer 模版

## 来源

- TeXPage: `5bb222ff-08b3-4e1e-b1bb-b7a652e1ca36`
- 上游 GitHub: `xiaoxiandadada/Scubeamer`
- 目标仓库: `iftaken/scu-beamer`
- 作者: Chen Yang (羊忱), CC BY 4.0

## 适配结论

**零修改编译通过**。ctexbeamer + tectonic bundle 完美兼容。

## 关键适配点

### 英文 sans 字体：BaskervilleF (OTF)

cls 中使用 `\setsansfont[...Extension=.otf,...]{BaskervilleF}`。因为指定了 `Extension=.otf`，fontspec 走 kpathsea 文件名查找，tectonic 自动从 bundle 下载 `BaskervilleF-Regular/Bold/Italic/BoldItalic.otf`，编译无报错。

**关键规则**：`Extension=.otf` / `Extension=.ttf` 触发 kpathsea 查找（能命中 tectonic bundle），裸字体名触发 fontconfig 查找（只能命中系统字体）。此规则同样适用于 FiraSans/FiraMono 等 tectonic bundle 字体。

### CJK 字体：ctexbeamer 自动管理

- cls 中有 `\TryCJKFont{FandolKai-Regular.otf}` 尝试设置 CJK sans 字体，但 `\IfFontExistsTF` 走 fontspec 系统字体查找，在 Docker 中找不到 FandolKai（tectonic bundle 字体不在 fontconfig 中）
- `\scuCJKfontfalse` 保持 false，但**不影响编译**——ctexbeamer 在 Linux 下自动检测 Fandol fontset，通过 TeX Live font map 加载全部四种 CJK 字体（Song/Hei/Kai/Fang）
- 结论：`\setCJKsansfont` 的冗余尝试可以安全忽略

### 资源文件

- `scu-logo.png`：校徽 logo，需保留在仓库中（不被 .gitignore 误杀）
- `references.bib`：标准 BibTeX 格式，`unsrtnat` 样式（tectonic 自动下载 unsrtnat.bst）

### 依赖宏包

| 宏包 | 来源 | 备注 |
|------|------|------|
| ctexbeamer | tectonic bundle | 自动加载 ctex + beamer |
| tikz | tectonic bundle | pgf 基础 |
| pgfplots | tectonic bundle | 数据绘图 |
| algorithm2e | tectonic bundle | 伪代码（有 UTF-8 安全警告，不影响输出） |
| bm | tectonic bundle | 数学粗体 |
| natbib + unsrtnat | tectonic bundle | 参考文献 |

## 编译结果

- Docker 编译: `tectonic -X compile main.tex` → exit 0
- main.pdf: 294KB
- 3 次 re-run（交叉引用 + BibTeX）
- 仅 algorithm2e.sty UTF-8 安全警告（宏包注释中的非 ASCII 字符）
- 零 .cls 修改，零字体下载

## 适用场景

此适配模式适用于所有满足以下条件的 Beamer 模板：
1. 基于 `ctexbeamer`（或 `\LoadClassWithOptions{ctexbeamer}`）
2. 使用 `\setsansfont{...}[Extension=.otf,...]` 加载 tectonic bundle 字体
3. CJK 由 ctex 自动管理（无显式 `\setCJKmainfont` 路径依赖）
4. 无 `\setCJKsansfont{系统字体名}`（Docker 中 fontconfig 找不到）
