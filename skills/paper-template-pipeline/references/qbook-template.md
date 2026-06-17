# Q-book 书籍模板适配笔记

- **名称**: Q-book LaTeX 书籍模板
- **TeXPage ID**: `f987c971-d1c3-4573-8a48-d04bbeb16571`
- **GitHub 源**: `muzimuzhi/Qbook` (archived)
- **目标仓库**: `iftaken/qbook-template`
- **许可**: CC BY-NC 4.0

## 模板特征

- 文档类 `qbook` 基于 `ctexbook` (scheme=chinese, zihao=-4)
- CJK 字体: ctexbook 在 Docker 中自动检测 Fandol fontset — **无需外部字体下载**
- 参考文献: biblatex + biber 后端 (`numeric` 样式)
- 定理环境: tcolorbox 彩色定理盒子（定义、定理、性质、注）
- 双语标题: bicaption 宏包 (`\bicaption{中文}{English}`)
- 代码高亮: listings（带阴影边框）
- 数学: newtxtext + newtxmath（⚠️ 在 XeTeX 中有问题，见下）
- 10 个示例章节 + cover + preface + overview

## 适配要点

### 必须的修改

1. **`\include` → `\input`**: 全部 13 个 `\include{tex/...}` 改为 `\input{tex/...}`。`\include` 生成独立 .aux → biblatex/biber 报错。

2. **参考文献路径**: `\addbibresource{bib/qbook.bib}` → `\addbibresource{references.bib}`，文件本身也复制一份。

3. **EPS 图片**: `figure/by-nc.eps` 和 `figure/example/figep.eps` 需 `gs` 转 PDF。`.gitignore` 加例外（`!figure/by-nc.pdf`, `!figure/example/figep.pdf`）。

4. **EPS 引用**: `\includegraphics{...eps}` → 去扩展名（`.cls` 中 `\DeclareGraphicsExtensions` 会先找 .pdf）。

### 兼容性修复（TL2023 / tectonic）

5. **`lastpage` 冲突**: `\RequirePackage{lastpage}` 与 hyperref 的 zref-abspage 冲突 → `\c@abspage` 双重定义。Q-book 的 fancyhdr 配置未使用 `\lastpage`，直接注释掉。

6. **`footmisc perpage` 冲突**: `\RequirePackage[perpage, bottom]{footmisc}` 的 `perpage` 选项加载 `perpage.sty`，其中定义了 `\c@abspage` → 与 zref-abspage 冲突。改为 `[bottom]`。

7. **`bicaption` ordering**: `\captionsetup[bi-first]{bi-first}` 必须放在 `\DeclareCaptionOption{bi-first}{...}` **之后**，否则 `bi-first` caption family 未注册。

8. **`newtxtext`/`newtxmath` 问题** (⚠️ 未解决):
   - `newtxtext` 在 XeTeX 下设置 `TeXGyreTermesX` 为正文字体
   - `newtxmath` 尝试使用 `OML/TeXGyreTermesX(0)/m/n` → FD 文件缺失 → `Missing endcsname`
   - **建议修复**: 注释掉 `\RequirePackage[defaultsups]{newtxtext}` 和 `\RequirePackage{newtxmath}`，改用 fontspec `\setmainfont{Times New Roman}`（Docker 有系统字体）+ 默认 math

## 编译验证状态

- ❌ 编译未通过 — `newtxmath` 导致的 `Missing endcsname` 在 `tex/chapter2:222` 处阻断
- 已修复的错误: bicaption ordering, zref-abspage 双重定义 (lastpage + footmisc perpage)

## 已通过的修复

| 错误 | 修复 |
|------|------|
| `bi-first undefined in families caption` | 移动 `\captionsetup[bi-first]{bi-first}` 到 `\DeclareCaptionOption` 之后 |
| `\c@abspage already defined` (lastpage) | 注释掉 `\RequirePackage{lastpage}` |
| `\c@abspage already defined` (footmisc perpage) | `[perpage,bottom]` → `[bottom]` |
