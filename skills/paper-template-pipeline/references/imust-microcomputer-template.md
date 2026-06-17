# 内蒙古科技大学微型计算机实训模版

## 标识

- **TeXPage ID**: `d2016614-0b7b-48ea-b4ed-47a8d2f3933a`
- **TeXPage URL**: https://www.texpage.com/template/d2016614-0b7b-48ea-b4ed-47a8d2f3933a
- **目标仓库**: `iftaken/imust-microcomputer`
- **描述**: 内蒙古科技大学自动化与电气工程学院建电专业微型计算机实训模版

## 来源确认

**方式 B — 无 GitHub 源仓库，需浏览器提取。**

已穷举所有远程途径，无一成功：

| 途径 | 命令/URL | 结果 |
|------|----------|------|
| GitHub 搜索 (`gh search repos "imust"`) | — | 无匹配 |
| GitHub 搜索 ("微型计算机 实训 latex") | — | 无匹配 |
| GitHub 搜索 ("内蒙古科技大学 latex") | — | 无匹配 |
| TeXPage curl | `curl texpage.com/template/...` | ESA 403 |
| TeXPage API template/get | `api/template/get?templateId=...` | `code:1003` 需登录 |
| TeXPage API download | `api/template/download?templateId=...` | `code:1003` 需登录 |
| TeXPage OSS 静态资源 | `latex-static.texpage.com/template/.../main.tex` | NoSuchKey |
| TeXPage OSS upload | `upload.texpage.com/template/...` | ESA 403 |
| TeXPage git | `git clone git.texpage.com/...` | 需认证 |
| DuckDuckGo 网页搜索 | 中英文关键词 | 无 GitHub URL |
| CTAN 搜索 | `ctan.org/search?phrase=imust` | 无匹配 |
| Overleaf 搜索 | `overleaf.com/latex/templates?q=imust` | 无匹配 |

## 页面 meta 信息

```html
<meta name="description" content="内蒙古科技大学自动化与电气工程学院建电专业微型计算机实训模版 | ...">
```

页面无 GitHub URL，无作者名，纯 JS 渲染。

## 当前状态

- ✅ 仓库 `iftaken/imust-microcomputer` 已创建（private）
- ✅ AGENTS.md、.gitignore、init.sh（占位）已写入
- ✅ main.tex、references.bib（占位）已写入
- ✅ 浏览器成功进入 TeXPage 项目编辑器，文件树已识别
- ✅ report.tex 部分提取（~150行/9029字符，scroll-read 方法已验证可行）
- ⏳ **待提取完整源文件**：IMUSTBachelor.cls、report.tex（全量）、gb7714-2015.bbx、gb7714-2015.cbx、BIBbase/ 和 figures/ 目录内容
- ⏳ **待分析字体依赖并补全 init.sh**
- ⏳ **待 Docker 编译验证**

## 项目文件结构（已确认）

```
项目（TeXPage）：
├── BIBbase/                         # 目录 — 含 Test-bibtex.bib
├── figures/                         # 目录 — 待探索
├── FZHTK.TTF                        # 方正黑体（字体）
├── FZSSK.TTF                        # 方正书宋（字体）
├── IMUSTBachelor.cls                # 核心文档类（基于 WHU 硕士模板修改）
├── SourceHanSerifCN-Bold.otf        # 思源宋体 Bold
├── SourceHanSerifCN-Regular.otf     # 思源宋体 Regular
├── SourceHanSerifCN-SemiBold.otf    # 思源宋体 SemiBold
├── gb7714-2015.bbx                  # biblatex 参考文献样式
├── gb7714-2015.cbx                  # biblatex 引用样式
├── report.bbl                       # 编译输出（可跳过）
└── report.tex                       # 主文档（→ 需重命名为 main.tex）
```

## 模板元信息（已确认）

- **文档类**: `IMUSTBachelor`，选项 `forprint` / `forlib`
- **编译引擎**: XeLaTeX（`% !Mode:: "TeX:UTF-8"`，`%% 请使用 XeLaTeX 编译本文`）
- **基座**: 武汉大学硕士学位论文模板（http://aff.whu.edu.cn/huangzh/）
- **参考文献**: biblatex + gb7714-2015 样式
- **字体**: 方正书宋/黑体 + 思源宋体（全部为项目内嵌字体，不进 TeX Live 系统路径）

## 适配要点（预判）

- report.tex → main.tex（心河Paper 硬要求）
- FZHTK.TTF / FZSSK.TTF → COS 上是否已有？待确认后更新 init.sh
- SourceHanSerifCN-*.otf → 思源宋体，COS 上大概率有，确认文件名后加入 init.sh
- 字体均为项目内嵌（文件名直放根目录），需确认 .cls 中 `Path=` 声明方式
- gb7714-2015.bbx/.cbx → 需保留，biblatex 样式文件
- Test-bibtex.bib → 需重命名为 references.bib（心河Paper 硬要求）

## 已知相关仓库

- `AyanamiU/IMUST-Paper` — 内蒙古科技大学毕业论文模板骨架（非本模板）
- `Crystalmomo/imuthesis` — 内蒙古大学（非内蒙古科技大学）
