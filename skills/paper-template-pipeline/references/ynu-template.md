# 云南大学本科毕业设计 LaTeX 模板

## 来源

| 属性 | 值 |
|------|-----|
| TeXPage ID | `e584259d-9e84-4ce1-a973-15e38c6ea18f` |
| 作者 | 赵苡积 (Dr. Zhao Yiji) / Dengke Wang |
| GitHub 源 | `yijizhao/YNU-Thesis-Latex` |
| 许可证 | Creative Commons CC BY 4.0 |
| 目标仓库 | `iftaken/ynu-thesis` |
| 适配日期 | 2026-06-08 |

## 模板特征

- 基础文档类：`ctexbook`（`\LoadClass`，非 `\documentclass`）
- 选项解析：`kvoptions`（非 expl3 l3keys）
- 支持三种学位：Bachelor / Master / Doctor
- 字体声明：英文字体用 `Path=style/fonts/` + 文件名，中文字体用 `\setCJKmainfont`/`\setCJKfamilyfont` + `Path=style/fonts/`
- 中文家族：zhsong, zhhei, zhfs, zhkai, zhxingkai（行楷，仅研究生封面用）
- 参考文献：natbib + gbt7714-numerical.bst
- 编译引擎：XeLaTeX

## 适配要点

### 1. ctexbook fontset=none

cls 通过 `\LoadClass[...]{ctexbook}` 加载底层类（非 main.tex 的 `\documentclass`）。在 `\ProvidesClass` 后、`\LoadClass` 前插入：

```latex
\PassOptionsToPackage{quiet}{fontspec}  % 避免与 ctexbook 内部 fontspec 冲突
\LoadClass[...,fontset=none]{ctexbook}
```

**注意**：必须同时移除 cls 中的 `\RequirePackage{fontspec}`（第 82 行），否则会报 Option clash。

### 2. 英文字体适配

原始声明（使用 Path= + local ttf 文件）：

```latex
\setmainfont{TimesNewRoman}[Path=style/fonts/, Extension=.ttf, UprightFont=*-Regular, ...]
\setsansfont{Helvetica}[Path=style/fonts/, Extension=.ttf, UprightFont=*-Regular, ...]
\setmonofont{CourierNew}[Path=style/fonts/, Extension=.ttf, UprightFont=*-Regular, ...]
```

改为 Docker 系统字体：

```latex
\setmainfont{Times New Roman}
\setsansfont{Liberation Sans}
\setmonofont{Liberation Mono}
```

### 3. 中文字体适配

原始使用 `Path=style/fonts/` + 文件名（如 `SimSun.ttf`）。适配策略：

| 原始声明 | Docker 是否可用 | 适配方案 |
|----------|:---------:|----------|
| `\setCJKmainfont{SimSun.ttf}[Path=style/fonts/]` | ✅ 系统字体 | `\setCJKmainfont{SimSun}[AutoFakeBold=true]` |
| `\setCJKsansfont{SimHei.ttf}[Path=style/fonts/]` | ✅ 系统字体 | `\setCJKsansfont{SimHei}[AutoFakeBold=true]` |
| `\setCJKmonofont{SimFang.ttf}[Path=style/fonts/]` | ❌ 需下载 | `\setCJKmonofont{simfang.ttf}[Path=font/, AutoFakeBold=true]` |
| `\setCJKfamilyfont{zhsong}{SimSun.ttf}[...]` | ✅ 系统字体 | `\setCJKfamilyfont{zhsong}{SimSun}[AutoFakeBold=true]` |
| `\setCJKfamilyfont{zhhei}{SimHei.ttf}[...]` | ✅ 系统字体 | `\setCJKfamilyfont{zhhei}{SimHei}[AutoFakeBold=true]` |
| `\setCJKfamilyfont{zhfs}{SimFang.ttf}[...]` | ❌ 需下载 | `\setCJKfamilyfont{zhfs}{simfang.ttf}[Path=font/, AutoFakeBold=true]` |
| `\setCJKfamilyfont{zhkai}{SimKai.ttf}[...]` | ❌ 需下载 | `\setCJKfamilyfont{zhkai}{simkai.ttf}[Path=font/, AutoFakeBold=true]` |
| `\setCJKfamilyfont{zhxingkai}{STXingKai.ttf}[...]` | ❌ 需下载 | `\setCJKfamilyfont{zhxingkai}{STXINGKA.TTF}[Path=font/, AutoFakeBold=true]` |

**关键 pitfall**：原始 `\setCJKmainfont` 有 `ItalicFont=SimKai.ttf` 选项（将 CJK 斜体映射到楷体）。Docker 中 SimSun 作为系统字体加载时，`ItalicFont=KaiTi` 不可用（KaiTi 不在 Docker 中）。**丢弃此选项** — zhkai 家族已单独定义，模板中 CJK 斜体使用极少，功能损失可忽略。

**STXINGKA.TTF**：COS 中是大写文件名，Linux 区分大小写，init.sh 和 cls 声明需保持一致使用大写。

### 4. fontset=none 后手动定义 CJK 切换命令

```latex
\NewDocumentCommand\songti{}{\CJKfamily{zhsong}}
\NewDocumentCommand\heiti{}{\CJKfamily{zhhei}}
\NewDocumentCommand\kaishu{}{\CJKfamily{zhkai}}
\NewDocumentCommand\fangsong{}{\CJKfamily{zhfs}}
```

`\xingkai` 已在原始 cls 中定义为 `\CJKfamily{zhxingkai}`，无需修改。

### 5. main.tex 修改

- `\documentclass[type=Bachelor, print=twoside]{style/YNU-thesis}` → `{ynu-thesis}`
- 所有 `\include{chapters/...}` → `\input{chapters/...}`
- `\bibliography{ref}` → `\bibliography{references}`
- `ref.bib` → `references.bib`（文件重命名）

### 6. 资源文件

- **Logo 图片**：`style/本科毕设-校徽logo.png`, `style/本科毕设-云南大学logo.png`, `style/研究生-云南大学logo.png` — 保留在 style/ 目录，不进 font/
- **gbt7714-numerical.bst**：保留在 style/，tectonic 缓存中也可能有此文件（可 cp 到项目根目录）
- **旧字体目录 `style/fonts/`**：全部删除，替换为项目根 `font/`（由 init.sh 管理，不进 git）
- **figures/ch2/figure1.pdf**：示例图片，不在 .gitignore 排除范围

### 7. init.sh 字体列表

```bash
FONT_FILES=(
    "simkai.ttf"
    "simfang.ttf"
    "STXINGKA.TTF"
)
```

SimSun/SimHei 在 Docker 中作为系统字体可用，无需下载。

## 编译结果

- tectonic 编译成功，生成 809KB PDF
- 仅有已知安全警告（algorthm2e.sty / anyfontsize.sty 的 Invalid UTF-8 byte，系统字体绝对路径 warning，xdivpdfmx 的 PDF name object 警告）
- 3 次 TeX re-run（BibTeX + aux 变化）
