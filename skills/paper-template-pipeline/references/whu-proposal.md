# 武汉大学开题报告模板 (whu-proposal)

## 模板来源

| 项目 | 值 |
|------|-----|
| 源仓库 | https://github.com/whutug/whu-proposal |
| 版本 | v0.9 (2024-12-04) |
| 文档类 | whu-proposal.cls |
| 底层 | ctexart (默认 fontset，不设 fontset=none) |
| 论文类型 | bachelor / master / doctor |
| TeXPage UUID | 15c655db-e4d1-41d9-a595-c9969314e798 (v0.7) |
| 目标仓库 | iftaken/whu-proposal |
| 作者 | Kangwei Xia (武汉大学数学与统计学院) |

## 与 whu-thesis 的区别

whu-thesis 是武汉大学**学位论文**模板（ctexbook + fontset=none + explicit Fandol handler），whu-proposal 是**开题报告登记表**模板（ctexart + 默认 fontset auto-detect）。两个模板来自同一组织 `whutug` 但是**独立仓库、独立文档类**，互不依赖。

## 架构特点

基于 ctexart，macros 层使用 expl3 + l3keys2e。通过 `\ProposalSetup{...}` 配置元数据。

### 字体配置

ctexart 在 Linux/Docker 上 auto-detect 到 **fandol** fontset。cls 仅针对 mac/windows 的 sans 字体做微调（苹方→华文黑体，微软雅黑→中易黑体），不覆盖 song/hei/kai/fang 主字体。

西文字体：`\setmainfont{Times New Roman}`（Docker 系统字体，可用）。

**零外部字体依赖**。init.sh 的 `FONT_FILES=()` 设为空数组。

### 参考文献

使用 biblatex + gb7714-2015 样式 + biber 后端。tectonic-biber 在 Docker 镜像中可用，自动检测并调用。

### 资源文件

- `figures/whu-logo.png` — 武大校徽（必须保留，`.gitignore` 需例外）
- `figures/proposal_master_doctor-comment1.pdf` — 评审意见页（硕士/博士）
- `figures/proposal_master_doctor-comment2.pdf` — 评审意见页（硕士/博士）

## TL2023 兼容性

完全兼容，无任何阻断项：

- 无 `:en` / `:e` expl3 变体
- 无 `\ProcessKeyOptions`（使用 `\ProcessKeysOptions` + `l3keys2e`，TL2023 兼容）
- 无 `\NewTemplateType` / `\DeclareTemplate`
- 无 `fixdif.sty`
- 无 `circledtext`
- 无 `gbrefcompress`

## 适配要点

**零修改即可编译**。唯一需做的结构化调整：

1. `whu-proposal-main.tex` → `main.tex`（重命名）
2. `whu-proposal.bib` → `references.bib`（重命名）
3. `\addbibresource{whu-proposal.bib}` → `\addbibresource{references.bib}`
4. `.gitignore` 需添加 `!figures/*.pdf` 例外（评审意见页 PDF）

无需修改 cls 中的任何代码。

## 编译结果

```
tectonic -X compile main.tex → 返回 0
main.pdf: 392 KB (3 次 re-run：biber + aux + run.xml)
警告: Times New Roman 绝对路径（无害）、0.26pt overfull hbox（可忽略）、PDF 版本不匹配（1.7 in 1.5）
无致命错误
```

## 关键选项速查

| 选项 | 值 | 说明 |
|------|-----|------|
| type | bachelor / master / doctor | 学位类型 |
| title | 论文题目 | `\ProposalSetup` 中配置 |
| department | 培养单位 | `\ProposalSetup` 中配置 |
| supervisor | 导师姓名 | 仅硕/博需要 |
| major | 专业 | 仅硕/博需要 |
| research_area | 研究方向 | 仅硕/博需要 |

## 发现路径

TeXPpage 页面描述中提到 `github.com/whutug/whu-thesis`（学位论文模板），但本模板是独立仓库 `whutug/whu-proposal`。当 TeXPage HTML 中只出现关联仓库而非目标仓库时，`gh search repos "<模板类名>"` 可直接找到——比 `gh api search/repositories` 更简洁。
