# AJbook 数学物理书籍模板适配记录

## 模板信息

- **名称**：AJbook — 数学物理书籍 LaTeX 模板
- **TeXPage ID**：`46385f43-c08a-491f-8805-fe8d06e68c7e`
- **上游仓库**：[wenweili/AlJabr-1](https://github.com/wenweili/AlJabr-1)
- **目标仓库**：`iftaken/ajbook-template`
- **许可**：CC BY 4.0
- **适配日期**：2026-06-09

## 模板特征

AJbook 是 book 类模板（非 thesis/paper），有以下特点：

- 基于 XeLaTeX + xeCJK + fontspec（非 ctexbook）
- 自定义文档类 `AJbook.cls`，通过 key=val 选项系统配置（`kvoptions`）
- 字体配置外置在 `font-setup-open.tex`（由 cls 通过 `\input` 引入）
- 章节标题格式外置在 `titles-setup.tex`
- 使用 biblatex + biber 管理参考文献
- 使用 imakeidx + xindy 管理索引
- 丰富的定理环境：theorem, definition, proposition, lemma, corollary, conjecture, hypothesis, remark, example, exercise, definition-theorem, definition-proposition 等

## 适配要点

### 1. 字体替换（核心适配）

原始模板使用三套字体，其中两套在 tectonic bundle 中不可用：

| 原始字体 | 用途 | tectonic 可用性 | 替换为 |
|---------|------|----------------|--------|
| TeX Gyre Heros | 西文无衬线 | ❌ 不在 bundle | FandolHei-Regular.otf |
| Noto Sans CJK SC | CJK 黑体变体（hei2/sectionfont/pffont） | ❌ 不在 Docker | FandolHei-Regular.otf |
| Noto Serif CJK SC Bold | 封面书名 | ❌ 不在 Docker | FandolSong-Regular.otf |
| FandolSong/FandolHei/FandolKai/FandolFang | CJK 正文 | ✅ tectonic bundle 内置 | 保持不变 |

替换方法：直接编辑 `font-setup-open.tex` 和 `coverpage.tex` 中的字体声明。

**关键 pitfall**：AJbook 的字体设置不在 main.tex 中，而是在 `font-setup-open.tex` 中（由 cls 的 `\input` 引入）。搜索字体声明时需同时检查这类外置配置文件。

### 2. 参考文献（biblatex + tectonic-biber）

tectonic Docker 镜像内置 `tectonic-biber`（位于 `/usr/local/bin/tectonic-biber`）。当模板使用 biblatex 时，tectonic 会自动检测并调用它。

所需改动仅一行：
```latex
% 原来
\addbibresource{Al-jabr.bib}
% 改为
\addbibresource{references.bib}
```

`\printbibliography` 无需注释，tectonic-biber 可正常生成参考书目。

### 3. 索引（imakeidx + xindy）

xindy 仍不被 tectonic 支持。需注释掉 `\usepackage[xindy, splitindex]{imakeidx}` 和 `\makeindex{...}`，并提供占位定义：

```latex
\providecommand{\index}[1]{}       % 无 imakeidx 时的占位
\providecommand{\indexprologue}[1]{}
```

同时注释掉 `\printindex` 调用。

### 4. 编译结果

```
tectonic -X compile main.tex  →  返回 0
main.pdf: 966 KB
```

唯一警告：单个罕见字符 `柟` (U+67DF) 在 FandolHei-Bold 中缺失，不影响使用。

## 参考：Fandol-only 字体配置模板

```latex
% 西文无衬线
\setsansfont{FandolHei-Regular.otf}[
    BoldFont=FandolHei-Bold.otf]

% CJK 正文
\setCJKmainfont[
    BoldFont=FandolSong-Bold.otf,
    ItalicFont=FandolKai-Regular.otf
]{FandolSong-Regular.otf}

\setCJKsansfont[
    BoldFont=FandolHei-Bold.otf
]{FandolHei-Regular.otf}

% CJK 字族
\setCJKfamilyfont{kai}[BoldFont=FandolKai-Regular.otf,...]{FandolKai-Regular.otf}
\setCJKfamilyfont{song}[BoldFont=FandolSong-Bold.otf,...]{FandolSong-Regular.otf}
\setCJKfamilyfont{fangsong}[BoldFont=FandolSong-Bold.otf,...]{FandolFang-Regular.otf}
\setCJKfamilyfont{hei}[BoldFont=FandolHei-Bold.otf,...]{FandolHei-Regular.otf}

\newcommand\kaishu{\CJKfamily{kai}}
\newcommand\songti{\CJKfamily{song}}
\newcommand\heiti{\CJKfamily{hei}}
\newcommand\fangsong{\CJKfamily{fangsong}}
```

此配置完全依赖 tectonic bundle 内置字体，零外部下载。
