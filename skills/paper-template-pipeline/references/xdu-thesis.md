# 西安电子科技大学（XDUTS）研究生学位论文模板

## 基本信息

| 项目 | 值 |
|------|-----|
| CTAN | https://www.ctan.org/pkg/xduts |
| GitHub | note286/xduts |
| TeXPage 模板 ID | f6c51773-d683-4b68-8c42-9329623fab6f |
| 目标 repo | iftaken/xdu-graduate-thesis |
| 版本 | v6.2.9.0 (2025/05/04) |
| 格式 | dtx/docstrip（单文件 .dtx，通过 .ins 提取） |

## 提取产物

xduts.ins 的 `\generate` 指令产出 4 个文件：

| 文件 | docstrip 标签 | 行数 | 用途 |
|------|-------------|------|------|
| xdufont.sty | sty, xdufont | 2690 | 字体配置宏包（可独立使用） |
| xduugtp.cls | class, tp, xduugtp | 3771 | 本科开题报告 |
| xduugthesis.cls | class, thesis, xduugthesis | 5034 | 本科毕业论文 |
| xdupgthesis.cls | class, thesis, xdupgthesis | 6785 | 研究生学位论文（目标） |

## 提取方法

不能直接用现成的 `scripts/extract_dtx.py`（硬编码 NJUThesis 标签）。正确做法：写临时 Python 脚本，以 docstrip 标准语义提取 —— 每个输出文件维护一个活跃标签集合（如 xdupgthesis.cls 的活跃标签为 `{class, thesis, xdupgthesis}`），单行 guard `%<tag1|tag2>` 取**交集**匹配。

```python
output_configs = {
    'xdufont.sty': {'sty', 'xdufont'},
    'xduugtp.cls': {'class', 'tp', 'xduugtp'},
    'xduugthesis.cls': {'class', 'thesis', 'xduugthesis'},
    'xdupgthesis.cls': {'class', 'thesis', 'xdupgthesis'},
}
# 匹配逻辑: guard_tags & active_tags 非空 → 输出到该文件
```

**注意**：提取出的 cls/sty 文件开头有 dtx 文档注释（`% \iffalse`、`% \GetFileInfo` 等），但这些是注释，不影响编译，无需清理。

## 架构关键点

### xdupgthesis.cls 是自包含的

**与直觉相反**：xdupgthesis.cls **不加载** xdufont.sty。xdupgthesis.cls 内部**直接嵌入**了全部字体加载代码（`\@@_load_cjk_font_win:`、`\@@_load_cjk_font_fandol:` 等），键值定义也是 cls 自有的。xdufont.sty 是一个可选的独立宏包，供与其他文档类搭配使用。

部署到 iftaken/xdu-graduate-thesis 时，xdufont.sty 仍然打包进去（完整性和独立使用价值），但编译不依赖它。

### 文档类层级

```
xdupgthesis.cls → \LoadClass{ctexbook} → \LoadClass{book}
```

字体加载延迟到 `\ctex_at_end_preamble:n { \@@_load_font: }`（导言区末尾），在各用户包加载之后执行。

## 字体策略：零下载

**默认字体配置**（xdupgthesis.cls 内 `\keys_set:nn { xdu }`）：

```latex
style / cjk-font   = fandol,     % Fandol 家族 → tectonic bundle 内置
style / latin-font = gyre,       % TeX Gyre → tectonic bundle 内置
style / math-font  = cm,         % Computer Modern → LaTeX 默认
style / font-type  = font,       % 使用字体名而非文件名
style / font-path  = fonts       % 不生效（font-type=font 时不读文件）
```

**结论**：在 tectonic Docker 中编译零字体下载，init.sh 仅需创建占位 `font/` 目录。

`cjk-font` 可选值：win / adobe / founder / hanyi / sinotype / fandol / none。除 fandol 外全部需要外部字体文件。

## 编译陷阱

### `\title{}` 必须显式设置

ctexbook 的 `\maketitle` 要求 `\title{...}` 已定义。xdupgthesis 的 `\xdusetup{info / title = {...}}` **不映射**到 `\title`。`main.tex` 必须：

```latex
\title{论文标题}                    % ← 这一行必须有
\xdusetup{
  info / title = {论文标题},       % ← 这里也要
  ...
}
```

缺失时编译报：`LaTeX Error: No \title given.`

### 参考文献模式

xdupgthesis.cls 在 `\AtBeginDocument` 中检测 `bib-resource` 是否非空：
- 非空 → 使用 `biblatex`（`backend=biber`）+ `gb7714-2015` 样式
- 空 → 使用传统 BibTeX + `gbt7714-numerical`

因此 `\xdusetup{info / bib-resource = {references.bib}}` 必须设置，否则走 BibTeX 路径（在 tectonic 中也能工作但路径不同）。

### 编译警告（无需处理）

- underfull/overfull hbox/vbox — 封面排版微调，不影响内容
- `Object @page.X already defined` — xdvipdfmx 正常行为

## 正确的类选项（实测）

```latex
\documentclass[
  graduate-type  = 硕士,          % 硕士 | 博士
  degree-type    = 学术,          % 学术 | 专业（专业学位）
  secret-level   = 公开,          % 公开 | 秘密
  language       = zh,            % zh | en
]{xdupgthesis}
```

**注意**：选项值全部为中文/短代码，不是英文。
- `graduate-type`（研究生层次）≠ `degree-type`（学位类型），两个独立键
- `language` 为 `zh`/`en`，不是 `chinese`/`english`
- `secret-level` 为 `公开`/`秘密`，不是 `none`/`secret`/`confidential`
- 类选项中无 `degree`/`professional`/`academic` 等英文值 — 编译报 `Key 'xdu/style/language' accepts only a fixed set of choices`

信息选项（通过 `\xdusetup`）：

```latex
\xdusetup{
  info / title         = {论文标题},
  info / title*        = {English Title},
  info / department    = {学院},
  info / major         = {专业},
  info / author        = {作者},
  info / author*       = {Author Name},
  info / supervisor    = {导师一, 导师二},
  info / supv-ent      = {企业导师},
  info / student-id    = {学号},
  info / abstract      = {中文摘要...},
  info / abstract*     = {English abstract...},
  info / keywords      = {关键词1, 关键词2},
  info / keywords*     = {keyword1, keyword2},
  info / bib-resource  = {references.bib},
  info / acknowledgements = {致谢内容...},
}
```

## gbt7714-numerical.bst 补充

编译后若模板使用 BibTeX 路径，需从 tectonic 缓存复制 .bst：

```bash
cp ~/.cache/paper-tectonic/bundles/data/<hash>/gbt7714-numerical.bst .
```

但若设置了 `bib-resource`（走 biblatex 路径），则无需此步骤。
