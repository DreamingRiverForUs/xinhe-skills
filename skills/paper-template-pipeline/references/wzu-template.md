# 温州大学硕士学位论文模板（wzuthesis）

## 模板信息

- **来源**: Quantumcraft616/wzuthesis（基于 thuthesis v7.6.0 改编）
- **TeXPage**: https://www.texpage.com/template/8acbb6a6-ae55-4f1e-a4f9-c71a16faf6f7
- **目标**: iftaken/wzu-thesis
- **编译引擎**: XeLaTeX (Tectonic)
- **文档类**: ctexbook (fontset=none) + wzuthesis.cls

## 适配策略

### 核心问题

这是 thuthesis 派生模板，在 Docker 中面临三个层级的字体问题：

1. **Auto-detection 陷阱**: Docker 有 SimSun → auto-detect 选 `fontset=windows` → CJK handler 直接声明 KaiTi/FangSong → 失败
2. **Ubuntu 路径的 Fandol 依赖**: `fontset=ubuntu` → `cjk-font=noto` 仍用 FandolKai/FandolFang 声明 zhkai/zhfs
3. **英文 sans-serif**: `font=times` 路径声明 Arial → Docker 无此字体

### 最终方案

文档类选项：`fontset=ubuntu,font=times`

三处 cls 补丁：

```latex
% 1. Arial → Liberation Sans（wzu@set@font@times 函数内）
\setsansfont{Liberation Sans}%   原: \setsansfont{Arial}%

% 2. FandolFang → simfang.ttf（wzu@set@cjk@font@noto 函数内）
\setCJKfamilyfont{zhfs}{simfang}[
  Path           = ./font/,
  Extension      = .ttf,
]%

% 3. FandolKai → simkai.ttf（同上）
\setCJKfamilyfont{zhkai}{simkai}[
  Path           = ./font/,
  Extension      = .ttf,
]%
```

### 字体下载

init.sh 只需下载 2 个字体（SimSun/SimHei 在 Docker 中，Noto CJK 也在 Docker 中）：

```
simkai.ttf    (11M)  — 楷体，用于 zhkai
simfang.ttf   (10M)  — 仿宋，用于 zhfs
```

### 其他适配

- 参考文献：`ref/refs.bib` → `references.bib`（系统规范）
- 主文件：`wzuthesis-example.tex` → `main.tex`
- logo PDF：`wzu-text-logo.pdf`、`wzu-fig-logo.pdf` 需在 .gitignore 中加例外

## 编译结果

- Docker 编译成功 (exit 0)
- main.pdf: ~638 KB
- 仅有 UTF-8 警告（algorithm.sty 内注释，安全忽略）
- 仅有 Underfull hbox 警告（标题换行间距，安全忽略）

## 关键学习点

对于所有 thuthesis 派生模板（识别特征：`\LoadClass{ctexbook}[2017/04/01]` + `fontset`/`cjk-font` 选项 + `\wzu@set@cjk@font@noto` 类函数）：

1. **永远不要依赖 auto-detect**，显式声明 `fontset=ubuntu,font=times`
2. **必须检查 noto CJK handler 的 zhkai/zhfs 声明**——大概率用 Fandol，需改为 simkai/simfang + Path=./font/
3. **必须检查 English font handler**——大概率用 Arial，需改为 Liberation Sans
