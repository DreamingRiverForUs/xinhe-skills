# 华中科技大学研究生学位论文模板（HUST Thesis）

## 基本信息

| 属性 | 值 |
|------|-----|
| 上游仓库 | `hust-latex/hustthesis` |
| TeXPage 链接 | `https://www.texpage.com/template/4d9fefbf-2d5d-4d89-802d-124530cab9cf` |
| 文档类 | `hustthesis`（基于 `ctexbook`） |
| 源格式 | dtx（docstrip） |
| 支持类型 | 硕士（master）、博士（doctor） |
| 参考文献 | biblatex + hustthesis 样式 |

## dtx 提取

| 标签 | 输出文件 |
|------|----------|
| class | `hustthesis.cls` |
| def-m | `hustthesis-m.def`（硕士常量） |
| def-d | `hustthesis-d.def`（博士常量） |
| cbx | `hustthesis.cbx` |
| bbx | `hustthesis.bbx` |
| doc-sty | `hustthesis-doc.sty` |

## 编译适配要点

### 必须修复

1. **`\NeedsTeXFormat{LaTeX2e}[2024-11-01]` → `[2022/06/01]`**
    tectonic TL2023 不支持 2024+ 内核。

2. **`\ProcessKeyOptions [ hust / option ]` → `\ProcessKeysOptions { hust / option }`**
    TL2023 无 `\ProcessKeyOptions`，需添加 `\RequirePackage{l3keys2e}` 并使用旧版命令。

### hustvisual 宏包

v2.1.0 起模板使用 `hustvisual` 宏包（TikZ 绘制校名，替代 PDF 图标）。该包**不在 tectonic TL2023 bundle 中**，需从 CTAN 下载：

```bash
curl -sL 'https://mirrors.ctan.org/macros/latex/contrib/hustvisual.zip' -o /tmp/hv.zip
unzip /tmp/hv.zip -d /tmp/hv
cp /tmp/hv/hustvisual/hustvisual.sty ./
```

### 字体方案

Linux/Docker 自动检测逻辑（`hustthesis.cls` L1141-1163）：
- 非 Windows + 非 macOS → `font_set` = `fandol`
- Latin: TeX Gyre Termes / Heros / Cursor（均在 tectonic bundle 中）
- CJK: FandolSong / FandolHei / FandolFang / FandolKai（均在 tectonic bundle 中）

**零外部字体依赖**。华文中宋（STZHONGS）用于封面标题，缺失时自动回退为宋体（`\cs_set_eq:NN \@@_stzhongs: \rmfamily`）。

不需要 init.sh 下载任何字体文件，只需创建 `font/` 目录占位。

### 不需要修复的问题

- `:en` / `:e` expl3 变体：模板未使用，无需处理
- `fancyhdr` 选项冲突：无 `twoside` 选项，安全
- `fontspec` 重复加载：cls 显式注释"fontspec 包含于 ctex 宏集，无需另行载入"
- `\subcaptionsetup`：未使用
- `\minted`：未使用
- EPS 图片：demo 中使用 PDF（`fig-example.pdf`），无 EPS

## 用户入口

```latex
\documentclass[type=doctor]{hustthesis} % doctor 或 master

\hustsetup {
  info = {
    title = { 中文标题 },
    title* = { English Title },
    degree = { academic },     % academic 或 professional
    author = { 姓名 },
    supervisor = { 指导老师\quad{} 教授 },
    ...
  },
}

\addbibresource{references.bib}  % 系统要求命名为 references.bib
```

**注意**：需将上游 demo 中的 `\addbibresource{ref.bib}` 改为 `\addbibresource{references.bib}`。
