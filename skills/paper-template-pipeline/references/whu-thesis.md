# 武汉大学论文模板 (whu-thesis)

## 模板来源

| 项目 | 值 |
|------|-----|
| 源仓库 | https://github.com/whutug/whu-thesis |
| 版本 | v2.4.0 (2025-03-17) |
| 文档类 | whu-thesis.cls |
| 底层 | ctexbook (fontset=none) |
| 论文类型 | bachelor / master / doctor |
| 学位类别 | academic / professional |
| TeXPage UUID | 6cfb97f4-1394-4ca7-8a81-e81db4a2e701 |
| 目标仓库 | iftaken/whu-thesis |

## 架构特点

expl3 架构的现代模板。cls 中通过 `\LoadClass{ctexbook}` 加载 ctexbook 基类，并设置 `fontset=none`，然后自行管理 CJK 字体配置。

### 字体配置

模板通过 `cjk-font` 选项选择 CJK 字体方案：`windows | mac | fandol | sourcehan | founder | none`。

**Docker 编译使用 `cjk-font=fandol`**。Fandol 字体 handler (`\__whu_style_cjk_font_set_fandol:`) 直接使用文件名调用 `\setCJKmainfont`/`\newCJKfontfamily`：
```latex
\setCJKmainfont{FandolSong-Regular.otf}[BoldFont=FandolSong-Bold.otf,...]
\newCJKfontfamily[zhkai]\kaishu{FandolKai-Regular.otf}[...]
```

**关键点**：这些调用使用文件名（含 .otf 扩展名），fontspec 通过 kpathsea 查找，tectonic bundle 中的 Fandol 字体可被正确找到。这与使用字体名（如 `FandolKai`）的路径不同——后者走 fontspec 系统字体搜索（在 Docker 中不可达）。**零外部字体依赖**。

西文字体：`font=termes`（TeX Gyre Termes，tectonic 自动下载）或 `font=times`（Times New Roman，Docker 系统字体）。

### 参考文献

支持 `bib-backend = bibtex | biblatex`。默认 bibtex 后端 + biblatex 前端（`\printbibliography`）。
样式文件在 `data/` 目录：gbt7714-2005-author-year.bst, gbt7714-2005-numerical.bst, gbt7714-2005-whu-numerical.bst。

## 适配要点

### main.tex 改动

从源仓库 `demo.tex` 创建 `main.tex` 需修改：
1. `cjk-font = mac` → `cjk-font = fandol`（Docker/Linux 环境）
2. `\include{...}` → `\input{...}`（避免 bibtex 章节 aux 问题）
3. `bib-resource = {ref/bachelor-refs.bib}` → `bib-resource = {references.bib}`
4. 保留 `demo.tex` 作为原始参考文件

### fixdif.sty 缺失

tectonic TL2023 bundle 不含 `fixdif.sty`。模板在 `whu-thesis.cls:415` 有 `\RequirePackage{fixdif}`，用于提供 `\d` 命令（直立微分算子 d）。

**修复**：注释掉 `\RequirePackage{fixdif}`，添加：
```latex
\providecommand{\d}{\mathop{}\!\mathrm{d}}
```

### 无 TL2023 兼容性阻断

经检查，whu-thesis.cls 不使用以下 TL2023 不兼容特性：
- 无 `:en` / `:e` expl3 变体
- 无 `\ProcessKeyOptions`
- 无 `\NewTemplateType` / `\DeclareTemplate` / `\DeclareInstance`
- 无 `\s__clist_stop`
- 无 `gbrefcompress`

虽有 `\RequirePackage{xtemplate, l3keys2e}` 但实际使用模式与 TL2023 兼容。

## 编译结果

```
tectonic -X compile main.tex → 返回 0
main.pdf: 316 KB
安全警告: algorithm2e.sty Invalid UTF-8 byte, cmmi12 缺字 (0x323 combining dot below)
无致命错误
```

## 关键选项速查

| 选项 | 值 | 说明 |
|------|-----|------|
| type | bachelor / master / doctor | 学位类型 |
| class | academic / professional | 学位类别（仅 master） |
| cjk-font | fandol (Docker) | CJK 字体方案 |
| font | termes / times | 西文字体 |
| math-font | termes / xits | 数学字体 |
| bib-backend | bibtex / biblatex | 参考文献引擎 |
| bib-resource | references.bib | 参考文献文件 |
