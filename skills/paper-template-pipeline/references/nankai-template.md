# 南开大学模板（nkthesis）适配笔记

## 来源

- 上游仓库：`alumik/nkthesis`（v2026.5.0）
- 生成方式：dtx/docstrip → 预编译 `nkthesis.cls`
- 心河Paper 仓库：`iftaken/nankai-thesis-template`

## 模板架构

```
nkthesis.cls              # 文档类（dtx 生成，~1590 行）
├── LoadClass{ctexbook}    # 基于 ctexbook（fontset=none）
├── fontspec 字体检测       # 条件加载：系统字体 → 本地文件
├── 封面页（\titlepage / \anonymoustitlepage）
├── 声明页 / 授权页
├── 章节/图表/页眉页脚样式
└── 作者信息页
```

## 字体策略

nkthesis 使用 `\fontspec_font_if_exist:nTF` 条件模式（移植友好）：

```latex
\fontspec_font_if_exist:nTF { SimSun }
    { \setCJKmainfont { SimSun } }
    { \setCJKmainfont { simsun.ttc } [ Path = fonts/ ] }
```

**已在 Docker 镜像的系统字体**（自动命中，无需下载）：
- SimSun（宋体）
- SimHei（黑体）
- Times New Roman

**需从 COS 下载到 `fonts/` 目录**（init.sh 处理）：
- simfang.ttf（仿宋）
- simkai.ttf（楷体）
- arial.ttf / arialbd.ttf / ariali.ttf / arialbi.ttf

**注意**：目录名是 `fonts/`（有 s），不是 `font/`。init.sh 的 `FONT_DIR` 和 `.gitignore` 必须匹配。

## ctexbook + fontset=none 模式

nkthesis 加载 ctexbook 时使用 `fontset=none`，字体完全由模板 cls 手动管理。这意味着：
- ctex 提供的 `\ziju` 等命令仍然可用（ctexbook 已加载）
- 但 `\songti` / `\heiti` / `\fangsong` / `\kaishu` 等命令由模板 cls 自行定义（映射到 `\CJKfamily` 系列）
- 封面和正文使用 `\songti` / `\heiti` 切换字体，而非 `\zihao`（那是字号命令）

## tectonic 兼容性修复清单

在 tectonic 的 TeX Live 2023 bundle 中编译此模板需要的修复：

| 状态 | 修复项 | 详情 |
|------|--------|------|
| ✅ 已修 | `\\NeedsTeXFormat{LaTeX2e}[2024/11/01]` | 改为 `[2022/06/01]` |
| ✅ 已修 | `\\ProcessKeyOptions` 支持 | 添加 `\\RequirePackage{l3keys2e}` + 改为 `\\ProcessKeysOptions { ... }` |
| ✅ 已修 | `\\tl_if_empty:eTF` (8处) | 改为 `\\exp_args:Ne \\tl_if_empty:nTF` |
| ✅ 已修 | `\\subcaptionsetup` | 改为 `\\captionsetup[subfigure]` |
| ✅ 已修 | `\\str_case:enF` (1处, L1095) | 改为 `\\exp_args:Ne \\str_case:nnF` |
| ✅ 已修 | `\\__nkthesis_checkbox:en` (8处: L1290/1295/1300 + L1490/1494/1498/1502/1506) | 改为 `\\exp_args:Ne \\__nkthesis_checkbox:nn` |

> 注：该模板无 `\\cs_generate_variant:Nn ... { e }` 声明，所有 `:en` 变体直接替换为 `\\exp_args:Ne` 前缀即可。

详见 `references/tectonic-expl3-compatibility.md`。

## 封面结构

模板有多个封面/说明页，均在 `\begin{document}` 后直接调用：
- `\titlepage` — 正式封面（含论文题目、作者、导师等）
- `\anonymoustitlepage` — 匿名封面（隐藏作者信息）
- `\declarationpage` — 原创性声明
- `\authorizationpage` — 学位论文授权书

封面信息通过 `\nktset{ ... }` 在 preamble 中配置，包含约 30 个 key。

## 目录结构

main.tex 使用 `\input`（非 `\include`），章节分布：
- `frontmatter/` — 摘要、前言、符号表
- `mainmatter/` — 内容要求、格式要求、写作要求、排版印刷要求
- `backmatter/` — 附录、致谢、简历
