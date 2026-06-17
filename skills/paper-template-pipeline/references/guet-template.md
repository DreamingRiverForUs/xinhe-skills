# 桂林电子科技大学本硕博毕业论文模板 (GUET Thesis)

## 基本信息

| 项目 | 值 |
|------|----|
| 上游 | YanMing-lxb/GUET_Thesis_LaTeX |
| 版本 | v2.12.4 (2026-04-15) |
| 文档类 | GUET-Thesis.cls (基于 `\LoadClass{book}`) |
| TeXPage | https://www.texpage.com/template/2f15a24f-20f7-4c04-8a4c-d0aacee0c818 |
| CJK 方案 | xeCJK (手动管理，非 ctex) |
| 参考文献 | biblatex + biber, gb7714-2015 |
| 数学/英文 | stix2 + mathspec |

## 学位类型选项

`\documentclass[<type>]{GUET-Thesis}`:
- `bachelor` — 本科
- `master` — 学硕
- `promaster` — 专硕
- `doctor` — 博士
- `ojmaster` — 在职硕士
- `ptmaster` — 非全专硕
- `pversion` — 打印版 (内侧页边距 3cm)
- `bversion` — 盲审版

## 字体方案（三平台）

| 平台 | 宋体 | 黑体 | 楷体 | 英文 |
|------|------|------|------|------|
| Windows | SimSun | SimHei | KaiTi | Times New Roman |
| macOS | Songti SC | STHeiti | KaiTi | Times New Roman |
| Linux (Docker) | FZ-ShuSong.ttf | FZ-HeiTi.ttf | FZ-KaiTi.ttf | STIXTwoText (stix2) |

Linux 字体通过 `init.sh` 从 jsdelivr CDN 下载到 `Fonts/` 目录。STIXTwoText 由 `stix2` LaTeX 宏包内建（tectonic bundle 自动下载），无需 init.sh 处理。

Linux 字体加载方式：自定义 `\SetCJKfont` 宏，使用 `\IfFileExists{./Fonts/#2}` 检查 + `Path=Fonts/` 加载。

## 适配要点

### 1. fancyhdr twoside 选项
```
\RequirePackage[twoside]{fancyhdr}  →  \RequirePackage{fancyhdr}
```
tectonic 的 fancyhdr 不支持 `twoside` 选项。

### 2. gbrefcompress counter
```
\setcounter{gbrefcompress}{3}  →  注释掉
```
tectonic TL2023 的 `biblatex-gb7714-2015` 包未定义此计数器。在任何位置（preamble / `\AtBeginDocument`）调用均报错。

### 3. `\SetCJKfont` 宏空格污染（关键）
原定义：
```latex
\newcommand{ \SetCJKfont } [2] {
    \IfFileExists { ./Fonts/#2 }
        { #1 [ \AutoFakeCJKOptions, Path=./Fonts/ ] { #2 } }
        ...
}
```
问题：`{ #2 }` 中的空格被传给 fontspec，导致字体名变成 `" FZ-ShuSong "`（含空格），无法匹配。

修复：收紧宏定义，用 `%` 注释行尾：
```latex
\newcommand{\SetCJKfont}[2]{%
    \IfFileExists{./Fonts/#2}%
        {#1[\AutoFakeCJKOptions,Path=Fonts/]{#2}}%
        {\ClassError{字体缺失}{请下载 #2 并放置于 ./Fonts/ 目录，或运行脚本下载}}%
}
```

### 4. Path=./Fonts/ vs Path=Fonts/
`.cls` preamble 中 `Path=./Fonts/` 会导致 fontspec 找不到字体。改为 `Path=Fonts/`（去掉 `./` 前缀）。

### 5. references.bib 路径
原 `main.tex` 中 `\ThesisBibResource{./References/References.bib}`，心河标准要求 `references.bib` 在根目录，需改为 `\ThesisBibResource{./references.bib}`。

### 6. microtype
cls 中 `\RequirePackage{microtype}` 在 XeTeX 下可用（未使用 `\DisableLigatures`），无需处理。

## 编译验证结果

- tectonic -X compile main.tex → 返回 0
- main.pdf: 780 KB
- 仅有 Underfull/Overfull hbox 警告（排版问题，非错误）
- `algorithm.sty:11: Invalid UTF-8 byte` 警告可忽略（宏包内部注释中的遗留编码）

## PII 清洗记录

模板所有源文件（.tex, .cls, .md）的注释头中大量使用开发者真实姓名「焱铭」和 GitHub 个人链接 `github.com/YanMing-lxb/`。共涉及 11 个文件：

- **main.tex**: `\Author{焱铭}`, 文件头注释含 GitHub 链接
- **Chapters/*.tex (7 个)**: 文件头注释含开发者姓名和链接
- **Thanks.tex**: 致谢署名「焱铭」
- **GUET-Thesis.cls**: `\ProvidesClass{...--焱铭}`
- **README.md**: 标题、badge 链接、多处引用原文
- **CHANGELOG.md**: 文件头注释

替换方案：
- 焱铭 → 模板维护者（dev credit）/ 张三（示例作者名）
- `github.com/YanMing-lxb/GUET_Thesis_LaTeX` → `github.com/iftaken/guet-thesis`
- 文件头中的 `% Author: 焱铭` 行直接删除

## 文件结构

```
guet-thesis/
├── main.tex              # 主文件
├── GUET-Thesis.cls       # 文档类 (1874 行)
├── main.pdf              # 编译输出
├── references.bib        # 参考文献
├── Accomplishs.bib       # 攻读学位期间成果
├── init.sh               # 字体下载 (jsdelivr CDN)
├── AGENTS.md, .gitignore
├── Chapters/             # 章节 (Abstract, Chapter1-5, Conclusion, Thanks, Symbol, Appendix, 独创性声明)
├── Pictures/             # 图片 (Guet-logo.pdf + chapter images)
├── Data/                 # 示例数据文件
├── Fonts/                # 字体 (不进 git)
├── latexmkrc, README.md, CHANGELOG.md, LICENSE
```
