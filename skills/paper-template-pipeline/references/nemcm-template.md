# 东北三省数学建模联赛（NEMCM）LaTeX 模板

## 模板来源

| 属性 | 值 |
|------|-----|
| GitHub 源 | JohnsonLo00/nemcmthesis |
| cls 版本 | v2.0.0 (2025/05/01) |
| TeXPage | `b08d1300-533d-4f5c-be3a-eef2a2c70fa5` |
| 飞书 | recvlPjTMXYfqi |
| 目标仓库 | iftaken/nemcm-thesis |
| 分类 | 数模竞赛 |

## 源仓库结构

```
nemcmthesis/
├── main.tex                 # 论文入口（\documentclass{nemcmthesis}）
├── nemcmthesis.cls          # 文档类（411行）
├── refs.bib                 # 参考文献（示例 4 条）
├── guidebook_of_nemcmthesis.pdf  # 使用手册
├── mainbody/                # 章节目录（原始名）
│   ├── abstract.tex
│   ├── ch1.tex ~ ch8.tex
│   └── appendices.tex
├── codes/                   # 示例代码（被 \lstinputlisting 引用）
│   ├── funfactorial.cpp
│   ├── funfactorial.java
│   ├── funfactorial.m
│   └── funfactorial.py
└── figures/signature/       # 签名图片（用户自备）
```

## 适配要点

### 文件重命名

| 原文件名 | 新文件名 | 原因 |
|----------|----------|------|
| `nemcmthesis.cls` | `main.cls` | 心河Paper 约定 |
| `mainbody/` | `chapters/` | 心河Paper 约定 |
| `ch1.tex` ~ `ch8.tex` | `chapter1.tex` ~ `chapter8.tex` | 更清晰的命名 |
| `refs.bib` | `references.bib` | 心河Paper 系统要求 |
| `\bibliography{refs}` | `\bibliography{references}` | 对应文件名变更 |

### main.tex 适配

只需修改三处：
1. `\documentclass{nemcmthesis}` → `\documentclass{main}`
2. 所有 `\input{mainbody/xxx}` → `\input{chapters/xxx}`
3. `\bibliography{refs}` → `\bibliography{references}`

### 字体适配

**无需额外下载字体**。cls 内置三级 fallback：

| 优先级 | 条件 | Docker 结果 |
|--------|------|-------------|
| 1 | `\IfFontExistsTF{Times New Roman}` | ✓ 通过（`/usr/local/share/fonts/custom/TIMES.TTF`） |
| 2 | `\IfFontExistsTF{./misc/times.ttf}` | ✗ 无 misc/ 目录 |
| 3 | `\setmainfont{TeX Gyre Termes}` | 不会被触发 |

CJK 使用 ctex 默认字体（SimSun/SimHei），Docker 系统字体，ctex 自动检测。

### 依赖总结

| 依赖类型 | 内容 | 处理 |
|----------|------|------|
| 字体（西文） | Times New Roman | Docker 可用，无需处理 |
| 字体（CJK） | ctex 默认（SimSun/SimHei） | 系统字体，无需处理 |
| 参考文献样式 | `gbt7714-numerical.bst` | 从 tectonic 缓存或已上线模板复制 |
| 参考文献宏包 | `natbib` + `gbt7714` | tectonic 自动下载 |
| 代码文件 | `codes/funfactorial.*` | 从上游整体复制 |
| 其他宏包 | `algorithm2e`, `matlab-prettifier`, `listings`, `subcaption` 等 | tectonic 自动下载 |

### 特有注意事项

- **`\lstinputlisting` 引用 codes/**：appendix.tex 中 4 处 `\lstinputlisting` 引用 `codes/funfactorial.*`，需将 codes/ 目录整体复制
- **`matlab-prettifier`**：提供 `style=Matlab-editor` 选项，tectonic 可自动下载
- **封面页**：通过 `\makecoverpage` 命令生成，含队员信息表（姓名、电话、指导教师）
- **无 `\ProcessKeyOptions` / `:en` 变体**：cls 使用标准 LaTeX2e 语法，兼容 tectonic (TL2023)
- **`algorithm2e` UTF-8 警告**：编译日志有 3 处 `Invalid UTF-8 byte` 警告（宏包内部注释编码），不影响输出
- **Times New Roman 绝对路径警告**：编译日志 `accessing absolute path /usr/local/share/fonts/custom/TIMES*.TTF`，无害

## init.sh

```bash
#!/usr/bin/env bash
# 无需下载额外字体，仅创建 font/ 目录占位
set -euo pipefail
FONT_DIR="font"
mkdir -p "${FONT_DIR}"
echo "==> 初始化完成（无需下载额外字体）"
```

## 编译结果

- tectonic 编译：通过（3 次 re-run，含 BibTeX）
- main.pdf：~395KB
- 警告（全部无害）：
  - `algorithm2e.sty` UTF-8 invalid byte（3 处）
  - Times New Roman absolute path（4 处）
  - Overfull hbox 21.5pt（封面表格）
  - Object @page.1 already defined（rerun 副作用）
- 无 Error

## .gitignore 例外

本模板无校徽 PDF 资源，无需额外例外。标准模板的 `!main.pdf` 已足够。
