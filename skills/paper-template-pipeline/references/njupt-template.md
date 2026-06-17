# 南京邮电大学本科毕业设计论文模板 (NJUPT)

## 来源

- **GitHub 源仓库**: `musnows/NJUPT-Bachelor`（fork 自 `dhiyu/NJUPT-Bachelor`）
- **TeXPage 模板 ID**: `a3b8fd7d-3d1c-419b-b2dc-1b1102f004ec`
- **许可证**: CC BY 4.0
- **心河Paper 仓库**: `iftaken/njupt-thesis`

## 模板特征

| 项目 | 详情 |
|------|------|
| 文档类 | `njupthesis.cls`（基于 book，自定义 cls） |
| 编译器 | XeLaTeX |
| CJK 方案 | `xeCJK`（非 ctex） |
| 参考文献 | natbib + gbt7714（`gbt7714-numerical` 样式，DOI 已关闭） |
| 字体管理 | `ifplatform` 检测 OS，三个分支（Windows / macOS / Linux） |
| 英文字体 | `mathspec` 包 `\setallmainfonts{Times New Roman}` |
| 中文字体 | SimSun（宋体）、SimHei（黑体）、KaiTi（楷体） |
| 图片路径 | `\graphicspath{{./pic/}}`（cls 中配置） |

## 适配要点

### 字体切换（Linux/Docker 分支）

模板使用 `ifplatform` 包检测操作系统，在 Linux 下走 else 分支。Docker 镜像预装 SimSun、SimHei 但**不含楷体**。

**修改前**（行 48）：
```latex
\newCJKfontfamily{\kaiti}{KaiTi}
```

**修改后**：
```latex
\newCJKfontfamily{\kaiti}[Path=./font/]{simkai.ttf}
```

楷体通过 `init.sh` 从 COS 下载 `simkai.ttf` 到 `font/` 目录。

### 参考文献路径

模板 cls 中 `\bibliography{reference}` 需改为 `\bibliography{references}`（行 640），同时源文件 `reference.bib` 重命名为 `references.bib`。

### mathspec 兼容性

模板使用 `mathspec` 包的 `\setallmainfonts` 统一设置英文/数学字体。此命令在 tectonic (TeX Live 2023) 中工作正常。Linux 分支显式声明 BoldFont/ItalicFont/BoldItalicFont，Docker 中 Times New Roman 四个变体均可通过 fontconfig 找到。

### 编译结果

- tectonic 编译通过（exit 0），BibTeX 自动 rerun
- 警告级：algorithm2e.sty UTF-8 字节（安全）、everypage 过时、绝对路径访问
- main.pdf 约 1.2 MB

## 依赖扫描

| 类别 | 内容 | 状态 |
|------|------|------|
| 字体 | Times New Roman, SimSun, SimHei, simkai.ttf | Docker 系统字体 + COS 下载 |
| 宏包 | mathspec, xeCJK, natbib, gbt7714, listings, subfigure, tocloft, algorithm2e, fancyhdr, ifplatform | tectonic 自动下载 |
| 参考文献样式 | gbt7714.sty, gbt7714-numerical.bst | 源仓库自带 |
| 图片 | pic/ 目录（jpg + png） | 源仓库自带 |
| 输入文件 | 无 | 单文件 main.tex |
