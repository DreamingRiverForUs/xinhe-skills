# USTBThesis（北京科技大学）模板

**注意**：此模板是 **研究生学位论文（硕士/博士）**，不是本科毕业论文。本科模板参见 `references/ustb-bachelor-template.md`。

## 模板概况

| 项目 | 值 |
|------|-----|
| 名称 | USTBThesis |
| 来源 | TeXPage → YiFraternity/USTBThesis (作者: 刘宇航) |
| 分类 | 研究生学位论文（硕士/博士） |
| 文档类 | `ustbthesis.cls` (v3.8.9, 2026-03-31) |
| 底层 | 基于 BITThesis（北京理工大学），`\BITSetup` 配置接口 |
| 编译引擎 | xelatex → biber → xelatex → xelatex |
| 参考文献 | biblatex + biber, style=gb7714-2015 |

## 字体适配

原始模板使用 `ctex={fontset=fandol}`，Fandol 字体仅在 tectonic 缓存中（非系统字体），fontspec 找不到。

**修复方案**：`fontset=none` + 手动声明 CJK 字体（SimSun/SimHei，Docker 预装）。

```latex
\documentclass[type=master,twoside=true,ctex={fontset=none}]{ustbthesis}
% Docker 预装：SimSun (宋体), SimHei (黑体), Times New Roman
\setCJKmainfont{SimSun}
\setCJKsansfont{SimHei}
\setCJKmonofont{SimSun}
\setCJKfamilyfont{zhsong}{SimSun}
\setCJKfamilyfont{zhhei}{SimHei}
\NewDocumentCommand\songti{}{\CJKfamily{zhsong}}
\NewDocumentCommand\heiti{}{\CJKfamily{zhhei}}
\NewDocumentCommand\kaishu{}{\CJKfamily{zhsong}}
\NewDocumentCommand\fangsong{}{\CJKfamily{zhsong}}
```

模板仅使用 `\songti` 和 `\heiti`，不需楷体/仿宋。

## 文件结构

```
├── main.tex          # 入口，BITSetup 配置
├── ustbthesis.cls    # 文档类 (3123行, 基于 bithesis)
├── chapters/         # 章节: abstract, chapter1-2
├── misc/             # 前置/后置: symbols, conclusion, reference, appendices,
│                     #   acknowledgements, pub, resume, statement, dataset
├── figures/          # figure1.png
├── images/           # header.pdf (校徽，需 gitignore 例外)
├── reference/        # main.bib + pub.bib (上游 bib 源)
```

## 编译要点

- **模板类型**: `type=master` (默认) 或 `type=doctor`
- **参考文献路径**: 改为 `\addbibresource{references.bib}` (系统要求)
- **封面字体**: `xihei` 使用 `STXihei`（macOS 字体），Docker 中不存在，自动回退 `\heiti`
- **Arial 字体**: 仅本科英文模板 (`type=3`) 使用，硕士模板不成问题
- **编译命令**: `tectonic -X compile main.tex`
- **初编产物**: main.pdf ≈ 371KB

## 调试记录

初次编译报 `Undefined control sequence` at `\MakeTitle`，实际原因是 `\songti` 未定义
（fontset=fandol 失败后 ctex 未注册 CJK 家族）。

**诊断方法**: `tectonic -X compile --keep-logs main.tex`，查看 `main.log` 中
`! Undefined control sequence` 上下文行。
