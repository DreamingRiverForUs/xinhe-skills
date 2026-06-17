# 清华大学学位论文模板 (thuthesis)

- 源: tuna/thuthesis v7.7.1
- 格式: DTX (thuthesis.dtx + thuthesis.ins)
- Release zip 包含预编译 thuthesis.cls，无需本地 latex 解包
- 目标: iftaken/thu-thesis

## 字体适配策略

### 问题

Docker 中有 SimSun → auto-detect 进入 windows 分支 → 需要 KaiTi/FangSong（Docker 中不存在）+ Arial（不存在）。

### 解决

1. 强制 `fontset=ubuntu`（Noto CJK 字体在 Docker 中可用）
2. 强制 `font=termes`（TeX Gyre Termes/Heros/Cursor 在 tectonic bundle 中）
3. Patch `\thu@set@cjk@font@noto` 中的 zhkai/zhfs：FandolKai/FandolFang → simkai/simfang，Path=font/
4. 同时修改 `\setCJKmainfont` 的 ItalicFont：FandolKai-Regular → simkai

patch 位置：thuthesis.cls 的 `\thu@set@cjk@font@noto` 函数（约第 1097-1130 行）

## 关联模板

- 武汉理工大学硕博论文 (whutthesis, 2010 年) — 基于 thuthesis v0.1 早期版本。细节见 `references/whut-thesis.md`。

示例数据文件（chap03.tex、denotation.tex、appendix.tex）大量使用 unicode-math 命令：
- `\increment`, `\symup`, `\symbf`, `\uppi`, `\symbfsf`, `\mathscr`

`math-font=none` 不加载 unicode-math → 这些命令全部报 Undefined control sequence。

**解决**: `math-font=stix`。STIX Two Math 在 tectonic bundle 中可用，且不依赖系统字体。

### 其他修复

- `data/appendix.tex`: 注释 `\printbibliography`（BibTeX/natbib 模式不需要）
- `data/denotation.tex`: `\increment` → `\Delta`（作为备用，math-font=stix 时回退可用）

### init.sh

需要字体: simkai.ttf, simfang.ttf（从 COS 下载到 font/）
