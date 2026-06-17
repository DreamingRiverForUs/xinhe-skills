# pkuthss 模板适配指南

本指南适用于基于 `pkuthss` 文档类（CasperVector/pkuthss，北京大学学位论文 LaTeX 模板）的模板适配。

## 触发信号

- `main.tex` 使用 `\documentclass[UTF8]{pkuthss}`
- 项目根目录有 `pkuthss.cls`、`pkuthss.def`、`pkuthss-utf8.def`
- `\pkuthssinfo{...}` 设置文档信息

## 模板结构

pkuthss 基于 `ctexbook`，使用 biblatex + biber 参考文献。

必需文件：
- `pkuthss.cls` — 文档类
- `pkuthss.def` — 通用定义（被 cls 通过 `\input` 加载）
- `pkuthss-utf8.def` — UTF-8 编码支持（被 cls 条件加载）
- `pkulogo.eps` / `pkuword.eps` — 北京大学 logo 矢量图（标题页使用）

## 适配要点

### 1. EPS → PDF 转换（必须）

tectonic 不支持 EPS 图片。将 logo 文件转换为 PDF：

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=pkulogo.pdf -dEPSCrop pkulogo.eps
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=pkuword.pdf -dEPSCrop pkuword.eps
```

`.gitignore` 需加 PDF 例外（`*.pdf` 规则会误杀）：
```
!pkulogo.pdf
!pkuword.pdf
!main.pdf
```

保留原始 `.eps` 文件在仓库中（作为源文件）。

### 2. 摘要环境名

pkuthss 定义三个摘要环境，**不**使用标准 `abstract`：

| 环境 | 用途 | 对应环境名变量 |
|------|------|-------------|
| `cabstract` | 中文摘要 | `\cabstractname`（定义在 `\pkuthssinfo` 中） |
| `eabstract` | 英文摘要（非盲审） | `\eabstractname` |
| `beabstract` | 英文摘要（盲审） | `\eabstractname` |

### 3. `\pkuthssffaq` — 示例专用

`\pkuthssffaq` 命令仅在示例 `thesis.tex` 中定义（导言区），**不在** `pkuthss.cls` 或 `.def` 中。如果从示例复制了章节文件，需要删除所有 `\pkuthssffaq` 调用，或在 `main.tex` 中定义该命令。

### 4. 字体 — 零外部依赖

pkuthss 在 XeTeX 下使用以下字体，**全部在 tectonic bundle 中可用**：

| 用途 | 字体 | tectonic 状态 |
|------|------|--------------|
| 数学字体 | XITSMath-Regular.otf / XITSMath-Bold.otf | bundle 内置，自动下载 |
| 正文罗马 | XITS (Regular/Bold/Italic/BoldItalic) | bundle 内置 |
| 正文无衬线 | TeX Gyre Heros (texgyreheros) | bundle 内置 |
| CJK 字体 | Fandol (Song/Hei/Kai/Fang) | bundle 内置，ctexbook 默认 fontset |

**init.sh 策略**：字体全部由 tectonic bundle 提供，init.sh 仅创建空 `font/` 目录，`FONT_FILES=()`。

### 5. biblatex-caspervector

`\usepackage[backend = biber, style = caspervector, utf8, sorting = ecnyt]{biblatex}` 所需文件自动从 tectonic bundle 下载：
- `caspervector.bbx`
- `caspervector.cbx`
- `blx-caspervector-base.def`
- `blx-caspervector-utf8.def`

tectonic-biber（`/usr/local/bin/tectonic-biber`）在 Docker 镜像中可用，编译自动 rerun。

### 6. 参考文献文件命名

`\addbibresource{references.bib}` — 必须命名为 `references.bib`（心河Paper 系统硬依赖）。

### 7. 文档信息配置

```latex
\pkuthssinfo{
    cthesisname = {博士学位论文},    % 或 {硕士学位论文}、{学士学位论文}
    ethesisname = {Doctor Thesis},
    thesiscover = {博士研究生学位论文},
    school = {工学院},               % 学院名称
    degreetype = {1},               % 1:学术学位，2:专业学位，0:不显示
    ...
}
```

### 8. 可信的编译结果

- 编译产出：~150 KB+（含封面、目录、摘要、三章正文、参考文献、附录、致谢、声明）
- 警告：PDF version 1.7→1.5（EPS 转换后正常现象）、Overfull hbox（页面布局微调）
- 无致命错误

## 完整编译命令

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```
