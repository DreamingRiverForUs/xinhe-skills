# 内蒙古科技大学本科生毕业设计（论文）开题报告模板(2025)

## 标识

- **TeXPage ID**: `a5ef683b-0b47-4433-aa0c-fea19c38ffb6`
- **TeXPage URL**: https://www.texpage.com/template/a5ef683b-0b47-4433-aa0c-fea19c38ffb6
- **目标仓库**: `iftaken/imust-proposal-template`
- **描述**: 内蒙古科技大学本科生毕业设计（论文）开题报告 Beamer 幻灯片模板(2025)
- **来源**: TeXPage-only，从通用模板 `iftaken/thesis-proposal-template` 适配

## 来源确认

**方式 C — 从通用提案模板复用（捷径）**

| 途径 | 命令/URL | 结果 |
|------|----------|------|
| TeXPage HTML 抓取 | `curl texpage.com/template/...` | 无 GitHub URL |
| GitHub 搜索 | `gh search repos "imust proposal"` | 仅目标仓库 |
| 通用模板复用 | `iftaken/thesis-proposal-template` | ✅ 直接作为基座 |

## 适配方式

直接复制 `iftaken/thesis-proposal-template`（andy123t/Thesis-Slides Beamer 模板）作为基座，仅修改：

1. `\header{}`: 改为 "内蒙古科技大学本科毕业设计（论文）\\开题报告"
2. `\institute{}`: 改为 "内蒙古科技大学"
3. 标题页字段：学生姓名、专业、指导教师、研究方向（开题报告场景）
4. 内容章节：选题背景与意义 → 国内外研究现状 → 研究内容与方法 → 预期成果与进度安排
5. 日期：2025年

## 模板元信息

- **类型**: Beamer 幻灯片模板
- **主题**: Madrid + rose
- **编译引擎**: XeLaTeX（Tectonic）
- **中文字体**: ctex 默认字体方案（Docker 中自动检测 SimSun/SimHei）
- **参考文献**: Beamer 内建 `thebibliography` 环境
- **字体依赖**: 零（ctex 默认方案）
- **init.sh**: FONT_FILES=() 空数组

## 编译结果

- ✅ Docker tectonic 编译通过（main.pdf 122.7 KB）
- ✅ 零字体下载
- ✅ 所有质检门通过
- ✅ 已推送至 GitHub

## 与其他模板的关系

- **基座模板**: `iftaken/thesis-proposal-template` — 通用 Beamer 开题/答辩模板
- **同一学校**: `iftaken/imust-bachelor-thesis` — 本科毕业设计全文模板（TeXPage-only，待提取）
- **同一学校**: `iftaken/imust-master-thesis` — 硕士学位论文模板
- **同一学校**: `iftaken/imust-microcomputer-training` — 微型计算机实训模板

### 同名多条目：两版 TeXPage 开题报告模板

内蒙古科技大学「本科生毕业设计（论文）开题报告模板」在 TeXPage 上有**两个条目**，内容相同（均为 Beamer Madrid+rose），仅 TeXPage UUID 不同：

| 仓库 | TeXPage UUID | 飞书记录 | 状态 |
|------|-------------|---------|------|
| `iftaken/imust-proposal-template` | `a5ef683b-0b47-4433-aa0c-fea19c38ffb6` | — | 已上线 |
| `iftaken/imust-bachelor-proposal` | `f2fe6041-4809-472b-ac65-ebb9ea51a8aa` | recvlPjTMYAEk7 | 已上线 |

**适配方式**：`imust-bachelor-proposal` 直接从 `imust-proposal-template` 复制全部文件（main.tex / references.bib / init.sh / .gitignore / README.md / figures / AGENTS.md），仅更新 AGENTS.md 中的 TeXPage UUID 和仓库名。Docker 编译一次通过（零修改）。

**识别信号**：当遇到同一学校同名模板的不同 TeXPage UUID 时，先检查学校是否已有适配仓库 — 已有则直接复制，无需重新适配。
