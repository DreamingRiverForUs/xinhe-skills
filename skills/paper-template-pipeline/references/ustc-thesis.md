# 中国科学技术大学学位论文模板 (ustcthesis)

- 源: ustctug/ustcthesis
- 格式: .cls 直接在源码中（无 dtx/Release 提取）
- 目标: iftaken/ustc-thesis
- 类型: thuthesis 派生（独立实现，非 thuthesis fork）

## 模板结构

ustcthesis.cls 是自包含的文档类，约 3773 行。核心特点：
- `\LoadClass[UTF8,a4paper,scheme=plain,zihao=-4,fontset=none]{ctexbook}` — 预置 fontset=none，然后自建字体系统
- 四套 CJK 字体处理器：windows、mac、noto、fandol（通过 `\ustc@set@cjk@font@<name>` 函数封装）
- 六套西文字体处理器：times、termes、stix、xits、libertinus、newcm、lm
- 三套数学字体处理器：stix、xits、libertinus
- 通过 key-value 配置系统 (`\ustcsetup`) 驱动所有选择
- 参考文献使用 BibTeX + natbib：`\usepackage[sort]{natbib}` + `\bibliographystyle{ustcthesis-numerical}` + `\bibliography{references}`
- 自定义 .bst 文件（~60KB 每个）：ustcthesis-numerical.bst, ustcthesis-authoryear.bst, ustcthesis-bachelor.bst

## 字体适配策略

### 问题

Docker 有 SimSun → `\IfFontExistsTF{SimSun}` 为 TRUE → auto-detect 进入 windows 分支：
- Windows CJK 分支需要 KaiTi + FangSong（Docker 无）
- font=auto 选 times → `\setsansfont{Arial}`（Docker 无）
- math-font 默认 xits → XITS Math 在 tectonic bundle 中但路径依赖复杂

### 解决

在 `\documentclass` 中显式传入所有字体选项，完全跳过 auto-detect：

```latex
\documentclass[degree=doctor,fontset=ubuntu,font=termes,math-font=stix]{ustcthesis}
```

三件套：
1. **fontset=ubuntu** → 跳过 `\IfFontExistsTF{SimSun}` 检测 → 使用 `\ustc@set@cjk@font@noto`（Noto CJK，Docker 系统字体）
2. **font=termes** → `\ustc@set@font@termes`（TeX Gyre Termes，tectonic bundle 内）
3. **math-font=stix** → `\ustc@set@math@font@stix`（STIX Two Math，tectonic bundle 内）

### ustcthesis.cls Patches（2 处）

**Patch 1**: `\ustc@set@cjk@font@noto` 中 zhfs/zhkai（行 1055-1062）：

原：
```latex
\setCJKfamilyfont{zhfs}{FandolFang}[Extension=.otf, UprightFont=*-Regular]%
\setCJKfamilyfont{zhkai}{FandolKai}[Extension=.otf, UprightFont=*-Regular]%
```

改为：
```latex
\setCJKfamilyfont{zhfs}[Path=font/,AutoFakeBold=3]{simfang.ttf}%
\setCJKfamilyfont{zhkai}[Path=font/,AutoFakeBold=3]{simkai.ttf}%
```

原因：fontspec 系统字体搜索找不到 tectonic bundle 中的 FandolFang/FandolKai。

**Patch 2**: `\setCJKmainfont` 移除 ItalicFont（行 1032-1038）：

原配置中的 `ItalicFont=FandolKai-Regular, ItalicFeatures={Extension=.otf}` 被完全移除。CJK italic 极少使用，不影响输出。

### main.tex 修改

- `\include{chapters/xxx}` → `\input{chapters/xxx}`（避免 BibTeX chapter .aux 孤立）
- `\bibliography{bib/ustc}` → `\bibliography{references}`（心河Paper 系统要求）

### init.sh

字体依赖: simkai.ttf, simfang.ttf（从 COS 下载到 font/）

系统字体（Docker 镜像预装，无需下载）: Noto Serif CJK SC, Noto Sans CJK SC, Noto Sans Mono CJK SC

### 编译结果

- ✅ tectonic 编译一次通过（含 BibTeX + 3 次 re-run）
- ✅ main.pdf ~400KB
- ✅ 仅安全警告（algorithm.sty UTF-8 byte、绝对路径）
- ✅ 非 CJK 的 Fandol 字体（如 fandol 分支的 FandolSong/FandolHei）未被触发使用

## 与 thuthesis 的差异

| 方面 | thuthesis | ustcthesis |
|------|-----------|------------|
| fontset 选项 | 强制 fontset=ubuntu | 同上，但 cls 默认 fontset=none |
| CJK 处理器结构 | `\thu@set@cjk@font@noto` 单一函数 | `\ustc@set@cjk@font@<name>` 四套完整处理器 |
| 西文字体处理器 | 仅 times/termes | times/termes/stix/xits/libertinus/newcm/lm 六套 |
| zhfs/zhkai patch | 在 noto handler 中改 simkai/simfang | 同上，函数名不同 |
| 参考文献 | `\bibliography{ref/refs}` | `\bibliography{bib/ustc}`（都需改成 references） |
| .bst 文件 | thuthesis-numeric.bst 等 | ustcthesis-numerical.bst 等（独立实现，~60KB） |
| 校徽资源 | 无（thuthesis 不含校徽） | figures/ 5个 PDF 文件需在 .gitignore 中加例外 |
