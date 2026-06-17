# 江苏第二师范学院毕业论文模板 (JSSNU Thesis)

- **TeXPage ID**: `a1e49583-d1f4-4611-a83a-ed96c2c1d4d5`
- **GitHub 源**: `XurongLiu/HNIE-Thesis-LaTeX-Template`
- **目标仓库**: `iftaken/jssnu-thesis`
- **文档类**: `ctexbook` + `fontset=none`
- **参考文献引擎**: BibTeX（gbt7714-numerical.bst）
- **License**: 无

## 模板结构

```
├── main.tex              # 入口文件
├── jssnu-thesis.cls      # 文档类（从 hnie-thesis.cls 改名）
├── references.bib        # 参考文献
├── gbt7714-numerical.bst # 参考文献样式（从 tectonic 缓存复制）
├── chapters/
│   └── chapter1.tex      # 示例章节（\input 引入）
├── figures/
│   └── school/
│       ├── school-image-1.png  # 校徽
│       └── school-image-2.png  # 校名
├── init.sh
├── .gitignore
└── AGENTS.md
```

## 适配要点

### 1. 学校名称
cls 内 `\makehnieinstructions` 命令中硬编码了 "湖南工程学院"，改为 "江苏第二师范学院"。

### 2. 字体两路分支
cls 使用 `\IfFileExists{fonts/simsun.ttc}` 检测本地字体目录：
- **有 fonts/ 目录**：使用 `Path=fonts/` 加载本地上传字体（times/simsun/simhei/simkai/simfang）
- **无 fonts/ 目录**（Docker 编译路径）：回退到系统字体

**Docker 回退分支的原始问题**：原版使用 `\setmainfont{TeX Gyre Termes}` + Fandol CJK 字体，但 Docker 中 TeX Gyre Termes 不是系统字体。

**修复**（三个替换）：
```latex
\else
  \setmainfont{Times New Roman}           % 原: TeX Gyre Termes
  \setsansfont{Times New Roman}           % 原: TeX Gyre Termes
  \setCJKmainfont[AutoFakeBold=2.5,AutoFakeSlant=0.2]{SimSun}          % 原: FandolSong
  \setCJKfamilyfont{song}[AutoFakeBold=2.5,AutoFakeSlant=0.2]{SimSun}  % 原: FandolSong
  \setCJKfamilyfont{hei}[AutoFakeBold=2.5]{SimHei}                     % 原: FandolHei
  \setCJKfamilyfont{fang}[AutoFakeBold=2.5]{SimSun}                    % 原: FandolFang
  \setCJKfamilyfont{kai}[AutoFakeBold=2.5]{SimSun}                     % 原: FandolKai
\fi
```

SimSun 和 SimHei 是 Docker 镜像 `/usr/local/share/fonts/custom/` 下的系统字体，fontspec 可直接按名称找到。

### 3. include → input
`main.tex` 中 `\include{chapters/chapter1}` 改为 `\input{chapters/chapter1}` 避免 BibTeX 为子文件生成独立 .aux 导致的引用错误。

### 4. gbt7714-numerical.bst
tectonic 自动下载 gbt7714.sty 但不下载 .bst。从 tectonic 缓存手动复制：
```
~/.cache/paper-tectonic/bundles/data/<hash>/gbt7714-numerical.bst
```

## 编译结果
- tectonic 返回 0
- main.pdf = 233KB
- 警告：algorithm.sty UTF-8 字节（安全，宏包内部注释遗留编码）
