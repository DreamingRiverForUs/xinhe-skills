# ElegantPaper 模板适配记录

## 来源

- **上游**: `ElegantLaTeX/ElegantPaper` v0.12
- **TeXPage ID**: `7f53d606-f215-4f44-a690-e37710c6aeaa`
- **目标仓库**: `iftaken/elegantpaper-template`
- **分类**: 学术论文 / 工作论文模板

## 模板结构

```
elegantpaper.cls      # 自定义文档类（基于 article）
elegantpaper-cn.tex   # 中文示例
elegantpaper-en.tex   # 英文示例
reference.bib         # 参考文献（上游命名，需改为 references.bib）
image/founder.png     # 方正字体安装截图
build.lua             # 构建脚本（不需要）
```

## 字体适配

### 原始声明（elegantpaper.cls lines 110-130）

```latex
\setmainfont{texgyretermes}[
  UprightFont = *-regular,
  BoldFont = *-bold,
  ItalicFont = *-italic,
  BoldItalicFont = *-bolditalic,
  Extension = .otf,
  Scale = 1.0]

\setsansfont{texgyreheros}[
  UprightFont = *-regular,
  BoldFont = *-bold,
  ItalicFont = *-italic,
  BoldItalicFont = *-bolditalic,
  Extension = .otf,
  Scale = 0.9]
```

### 修复后

```latex
\setmainfont{Times New Roman}
\setsansfont{Liberation Sans}[Scale = 0.9]
```

TeX Gyre Termes 和 TeX Gyre Heros 仅在 tectonic 缓存内，非 Docker 系统字体，fontspec 找不到。

### 中文字体

使用 ctex 默认方案（`chinesefont=ctexfont`，类选项默认值）。ctex 自动在 Docker 中找到 SimSun/SimHei，无需任何字体下载或 Path 配置。

```latex
% cls 中的 CJK 配置（无需修改）
\ifdefstring{\ELEGANT@chinesefont}{ctexfont}{
  \RequirePackage[UTF8,scheme=plain]{ctex}}{\relax}
```

## 参考文献适配

上游使用 `\addbibresource[location=local]{reference.bib}`（biblatex 方式），需改为 `references.bib`：

```latex
% main.tex 中
\addbibresource{references.bib}
```

文件名 `reference.bib` → `references.bib`。

## 关键选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `lang` | `en` | `cn` 为中文模式 |
| `chinesefont` | `ctexfont` | 无需字体下载 |
| `math` | `cm` | `newtx` 加载 newtxmath |
| `bibend` | `biber` | tectonic 内置 biber 正常 |
| `bibstyle` | `numeric` | |
| `citestyle` | `numeric-comp` | |

## 宏包依赖（tectonic 自动下载）

- `newtxmath`, `xkeyval`, `centernot`, `esint` — tectonic 首次编译自动拉取
- `ctex` — 中文支持
- `biblatex` + `biber` — 参考文献
- `zhnumber` — `\zhdate` 中文日期

## 编译验证（2026-06-07）

- 退出码 0
- main.pdf 263 KB
- 无错误，中文渲染正常
- biblatex/biber 交叉引用正常
