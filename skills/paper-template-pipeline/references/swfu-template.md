# 西南林业大学研究生论文模板（SWFU swfuthesism）

## 来源

- **GitHub 源**: wx672/texmf → `tex/latex/swfu/swfuthesism.cls` + `doc/latex/swfu/swfuthesism/`
- **作者**: 孙永科
- **TeXPage**: https://www.texpage.com/template/4ed268dc-4116-4c3b-a851-b9e6eba04326
- **分类**: 硕士学位论文（研究生）
- **目标仓库**: iftaken/swfu-graduate-thesis

## 模板结构

- 文档类: `swfuthesism.cls`，基于 `ctexbook`（`scheme=chinese, zihao=-4`）
- CJK 字体: ctexbook 默认 Fandol fontset（Linux/Docker 自动检测）
- 参考文献: `biblatex` + `gb7714-2015` + tectonic-biber
- 封面: TikZ 排版（含校徽 logo `swfulogo`、中英文标题页、独创性声明）
- 示例章节: ch1-pre（前置准备）、ch2-quick（快速入门）、ch3-adv（进阶）、ch4-thesis（论文写作）、ch5-app-sw（软件）、ch6-spec（规范）

## 适配记录

### cls 修改清单

| 修改项 | 原因 | 方式 |
|--------|------|------|
| `footmisc` 移除 `perpage` | 避免 `\c@abspage` 冲突 | `[bottom,perpage]` → `[bottom]` |
| 移除 `lua-ul` | tectonic bundle 不支持 | 从 `\RequirePackage{tasks,lua-ul}` 中移除 |
| `minted` → `listings` | tectonic 不支持 shell-escape | 完整替换 minted 章节（~35行），用 listings 替代 |
| 注释 `swfulogo` | 校徽图片未包含在源文件中 | 注释 TikZ 封面中的 logo 节点，调整标题节点定位 |
| 缺失的自定义命令 | `\auctex`、`\LKeyTab`、`\Frowny`、`\Ctrl` 未在 cls 中定义 | `\providecommand` 添加（避免与 marvosym/wasysym 冲突） |

### 关键 pitfall: `\Frowny` 已被 marvosym/wasysym 定义

`swfuthesism.cls` 加载了 `\RequirePackage{amsmath,amsfonts,amssymb,marvosym,pifont}`。marvosym 定义了 `\Frowny` 命令。在 cls 末尾添加 shim 定义时必须用 `\providecommand` 而非 `\newcommand`，否则报 `Command \Frowny already defined`。

### 章节文件 minted 转换

ch2-quick.tex 和 ch3-adv.tex 中有 `\begin{minted}` 环境，需转换为 `\begin{lstlisting}`。

### 缺失资源

- `swfulogo`: 西南林业大学校徽图片，不在 wx672/texmf 的 swfuthesism 目录中（可能在 swfubeamer 或其他模板中）。封面暂时跳过 logo
- `screenshot`: `chapters/ch1-pre.tex` 引用的示例截图，需从 `wx672/texmf` 的 `doc/latex/swfu/swfuthesism/figs/` 下载
- 其他 `figs/` 下的 PDF 图片资源同理

### 编译状态

- 封面 ✅
- 中英文摘要 ✅
- 目录 ✅
- ch1-pre 部分 ✅（到 screenshot 图片处中断）
- 待补齐 figs/ 图片后继续

## 无需字体下载

ctexbook 在 Linux/Docker 上自动检测 fandol fontset，FandolSong/Hei/Kai/Fang 四体均在 tectonic bundle 中可用。`init.sh` 只需空数组即可。
