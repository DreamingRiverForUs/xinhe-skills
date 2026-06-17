# 东北大学生命科学与健康学院本科毕业设计（论文）模板

- **上游**：SchrodingerBlume/NEUCLHSBachelorThesis (GitHub)
- **TeXPage**：https://www.texpage.com/template/b420526e-08a9-4ce2-a7ed-9cc1f8d114ed
- **目标**：iftaken/neu-life-science-thesis
- **状态**：已上线 ✅ (2026-06-09)
- **Docker 编译**：通过（零外部字体下载）

## 模板特征

| 项目 | 值 |
|------|-----|
| 文档类 | NEUCLHSBachelorThesis.cls |
| 基类 | ctexbook (fontset=none) |
| CJK 字体 | 手动声明，四级回退（本地→系统→平台→Fandol） |
| 数学字体 | unicode-math + XITSMath |
| 西文字体 | Times New Roman |
| 参考文献 | biblatex + gb7714-2025（作者自定义 bbx/cbx） |
| 特殊宏包 | unicode-math, siunitx, pdfpages, subcaption, tikz, upgreek |

## 字体回退链

模板在 cls 中手工构建了完整回退链，Docker 环境零配置：

| 字体 | 优先级 1 | 优先级 2 | 优先级 3 | Docker 命中 |
|------|----------|----------|----------|------------|
| 宋体 | fonts/SIMSUN.TTC | SimSun | Songti SC → FandolSong | SimSun (系统) |
| 黑体 | fonts/SIMHEI.TTF | SimHei | Heiti SC → FandolHei | SimHei (系统) |
| 楷体 | fonts/SIMKAI.TTF | KaiTi | Kaiti SC → FandolKai | FandolKai (kpathsea) |
| 仿宋 | fonts/SIMFANG.TTF | FangSong | STFangsong → FandolFang | FandolFang (kpathsea) |

Fandol 回退使用 `Extension=.otf, UprightFont=*-Regular` 语法，走 kpathsea 文件搜索（非 fontspec 系统字体搜索），因此 tectonic bundle 内的 Fandol 字体可被正确找到。

## 依赖扫描结果

### 输入文件依赖
- `\InputIfFileExists{settings/printmode}{}{}` — 存在 ✅
- `\input{settings/chapter}` → `\input{data/chap01}`, `\input{data/chap02}` — 存在 ✅
- `\include{DoNotEdit/cover}`, `\include{DoNotEdit/statement}` — 存在 ✅

### 资源文件依赖
- `DoNotEdit/BIGCOVER.pdf` — 蓝色大封面，需 gitignore 例外 ✅
- `DoNotEdit/BIGBACKCOVER.pdf` — 蓝色大封底，需 gitignore 例外 ✅
- `settings/signature.png` — 签名图片，模板资源 ✅
- `figures/mice.png`, `figures/wb.png`, `figures/placeholder.png`, `figures/wb续图.png`, `figures/附录图片.png` — 示例图片 ✅

### 字体依赖
Docker 环境零外部字体下载。见上方字体回退链。

## 编译适配修改

### 1. XITSMath 字体加载（必须）
```latex
% 修复前
\setmathfont{XITS Math}[StylisticSet=8]
% 修复后
\setmathfont{XITSMath-Regular.otf}[StylisticSet=8, BoldFont=XITSMath-Bold.otf]
```
根因：`\setmathfont{字体名}` 走 fontspec 系统 fontconfig 路径，Docker 中 XITS Math 未注册为系统字体。改 filename-based 后走 kpathsea，命中 tectonic bundle。

### 2. 参考文献路径（系统要求）
```latex
% 修复前
\addbibresource{data/references.bib}
% 修复后
\addbibresource{references.bib}
```
心河Paper 系统要求 references.bib 在项目根目录。

## biblatex-gb7714 特殊注意

模板使用作者自行修复的 `gb7714-2025.bbx` 和 `gb7714-2025.cbx`（基于 CTAN gb7714-2015 修改）。这些文件直接随模板分发，不从 CTAN 获取。注意：
- 使用了 `gbpunctwidth=bylan` 选项（2025 版本新功能，中文全角/英文半角）
- `gbnamefmt=lowercase`、`gbnoauthor=false` 等学校定制选项
- `thesistype=false` 是自定义接口，非 gb7714 官方
- tectonic 的 biber 可正常处理此 bbx/cbx

## 其他文件

- `untilchapter.sty`：模板自定义宏包，提供 `\usestyleuntil` 命令
- `settings/timesorheiti.tex`：控制黑体标题中西文使用 Times 或黑体的开关
- `settings/footnotecounter.tex`：每页脚注独立计数的 Macro
