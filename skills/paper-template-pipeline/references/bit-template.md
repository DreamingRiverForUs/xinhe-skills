# BIT (北京理工大学) BIThesis 模板家族

## 概述

BITNP/BIThesis 是北京理工大学的 LaTeX 模板集合，v3.8.12 (2026-05-28)。基于 expl3 + ctex，dtx 格式源码。

**GitHub**: https://github.com/BITNP/BIThesis
**Release 资产列表**: `gh release download v3.8.12 -R BITNP/BIThesis -p 'xxx'`

## 子模板列表

| 子模板 | Release zip | 文档类 |
|--------|-------------|--------|
| 研究生学位论文 (graduate-thesis) | `graduate-thesis.zip` | bithesis.cls (type=master/doctor) |
| 本科毕业论文 (undergraduate-thesis) | `undergraduate-thesis.zip` | bithesis.cls (type=bachelor) |
| 本科全英文 (undergraduate-thesis-en) | `undergraduate-thesis-en.zip` | bithesis.cls (type=bachelor_english) |
| 实验报告 (lab-report) | `lab-report.zip` | bitreport.cls |
| 论文翻译 (paper-translation) | `paper-translation.zip` | — |
| 开题报告 (presentation-slide) | `presentation-slide.zip` | bitbeamer.cls |
| 读书报告 (reading-report) | `reading-report.zip` | — |

## 文档类分析

### bithesis.cls (通用论文类)

- 基于 expl3 + ctexbook（底层）
- 支持 5 种 type: `bachelor`(1), `bachelor_translation`(2), `bachelor_english`(3), `master`(4), `doctor`(5)
- `\__bithesis_if_graduate:TF` 判断 `3 < \g__bithesis_thesis_type_int` → master/doctor 为 graduate

### TL2024 兼容性: ✅ 完全兼容 TL2023

- 无 `\NeedsTeXFormat`（无版本限制）
- 无 `\ProcessKeyOptions`（使用 expl3 key-value 系统，非 LaTeX 内核级）
- 无 `:e`/`:en` expl3 变体（搜索 `:en`/`:e[nNTVF]` 仅命中 `abstract:en` 标签文本）
- 无 `\NewTemplateType`/`\DeclareTemplateInterface` 等 2024 内核命令
- `\cs_generate_variant:Nn \tl_if_empty:nTF {x}` 使用 `x` 展开，非 `e`

### 字体策略

**CJK 字体**: ctex 管理，Docker/Linux 中自动检测到 **Fandol fontset**（tectonic bundle 内置四体齐全：Song/Hei/Kai/Fang）。

**英文主字体**: `\setmainfont{Times New Roman}`（Docker 系统字体，可用）。另有 `betterTimesNewRoman` 选项改用 TeX Gyre Termes。

**Windows 特殊路径**: `\setCJKmainfont{SimSun}[AutoFakeBold,AutoFakeSlant]` 仅在 `windowsSimSunFakeBold=true` 且 `\ifwindows` 时触发，Docker 中不走此分支。

**Arial 字体**: 仅在以下条件触发，graduate thesis (master/doctor) **不触发**:
```
\bool_if:NTF \l__bithesis_arial_as_title_font_bool {
    \newfontfamily\arialfamily{Arial}  % 用户显式开启
} {
    \__bithesis_if_thesis_int_type:nT {3} {
      \newfontfamily\arialfamily{Arial}  % type=3 (bachelor_english) 自动加载
    }
}
```
Arial 用于 originality 声明页英文文本（`\c__bithesis_bachelor_label_originality_clause_tl`），graduate thesis 走 `\__bithesis_graduate_originality:` 路径不使用 Arial。

**数学字体**: 默认 `cm`（Computer Modern），`\__bithesis_load_math_font_cm:` 为空函数（不加载 unicode-math）。其他选项需 unicode-math + 对应 OTF 数学字体。

**细黑体 (xihei)**: `\setCJKfamilyfont{xihei}` 仅在 `\l__bithesis_cover_xihei_font_path_tl` 非空时加载，默认空（不加载），封面不受影响。

### 零外部字体依赖

graduate-thesis (master/doctor) 编译**零外部字体下载**:
- CJK: Fandol (tectonic bundle) ✓
- English: Times New Roman (Docker) ✓
- Math: cm (default) ✓
- Arial: 不触发 ✓
- xihei: 不触发 ✓

`init.sh` 仅创建 `font/` 目录，`FONT_FILES=()` 空数组。

## 编译特性

### biblatex + biber
模板使用 biblatex (backend=biber, style=gb7714-2015)，tectonic 自动调用 tectonic-biber 并 rerun。
- `\addbibresource{reference/main.bib}` — 主要参考文献
- `\addbibresource{reference/pub.bib}` — 成果清单
- 系统要求 `references.bib` 存在：从 `reference/main.bib` 复制内容创建

### 依赖文件
- `images/header.pdf` — 页眉校徽（需保留在 git 中）
- `figures/figure1.png` — 示例插图
- `misc/icon_academic.jpg`, `misc/icon_professional.jpg` — 成果清单图标

### 已知安全警告
- `fmtcount`/`fcprefix`/`fcnumparser`/`fc-english.def` 的 UTF-8 byte 警告：宏包内部注释遗留编码，不影响输出
- xdvipdfmx "Object @page.1 already defined"：交叉引用重定义，无害

## 获取方式

**推荐: GitHub Release（快速，无需克隆大仓库）**
```bash
gh release download v3.8.12 -R BITNP/BIThesis \
  -p 'bithesis.cls' \
  -p 'graduate-thesis.zip'
unzip graduate-thesis.zip -d graduate-thesis
```

**备选: 全量克隆（慢，仓库较大）**
```bash
gh repo clone BITNP/BIThesis --depth 1
```

## 适配流水线（graduate-thesis 已验证）

```
① 从 Release 下载 bithesis.cls + graduate-thesis.zip
② 解压 zip，提取 main.tex + chapters/ + misc/ + reference/ + images/ + figures/
③ 复制 bithesis.cls 到项目根目录
④ 创建 references.bib（从 reference/main.bib 复制内容）
⑤ 编写 init.sh（空字体数组 + mkdir font/）
⑥ Docker tectonic 编译 → 成功（0 errors）
⑦ 推送到 xinhepaper/bit-graduate-thesis
```

编译结果: PDF 573KB, 0 errors, 仅有安全警告。

## 适配流水线（undergraduate-thesis 已验证）

本科模板与研究生模板的关键差异：**封面需要 STXIHEI.TTF（华文细黑）字体**。

```
① 从 Release 下载 undergraduate-thesis.zip
② 解压 zip，提取 main.tex + chapters/ + misc/ + images/ + bithesis.cls + STXIHEI.TTF
③ 复制 bithesis.cls 到项目根目录
④ 创建 references.bib（从 misc/ref.bib 复制内容）
⑤ 编写 .gitignore：排除编译产物，但保留 STXIHEI.TTF + images/*.pdf + images/*.png + misc/*.pdf
⑥ 编写 init.sh：空字体数组（STXIHEI.TTF 已在仓库中，Docker 从当前目录加载）
⑦ Docker tectonic 编译 → tectonic-biber 自动运行 + rerun → 成功
⑧ 推送到 iftaken/bit-undergraduate-thesis
```

编译结果: PDF 557KB, 0 errors。biber 参考文献 + gb7714-2015 样式正常工作。

**关键 pitfall — STXIHEI.TTF**：
- 本科封面通过 `\BITSetup{cover={xiheiFont=STXIHEI.TTF}}` 引用此字体
- 研究生模板不触发 xihei 加载（`\l__bithesis_cover_xihei_font_path_tl` 默认为空）
- 该字体文件已在 Release zip 中，需随模板一起放入仓库
- Docker 编译时从当前工作目录加载（XeTeX 在当前目录查找字体文件）
- `.gitignore` 不能排除此字体文件（它不是下载的外部字体，而是模板资源）
- 不要放入 `font/` 目录（会被 gitignore 排除），放在项目根目录即可
