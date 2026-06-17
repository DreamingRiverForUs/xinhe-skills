# Tectonic TL2023 编译错误快速修复表

编译失败时按此表逐项检查，优先修复阻断级错误。

## 阻断级（必须修）

| 错误信息 | 修复 | 命令 |
|----------|------|------|
| `Undefined control sequence: \str_case:enF` | `:en`→`:nn` 加 `\exp_args:Ne` | `sed 's/\\str_case:enF/\\exp_args:Ne \\str_case:nnF/g'` |
| `Undefined control sequence: \ProcessKeyOptions` | 降级为 `\ProcessKeysOptions` | 加 `\RequirePackage{l3keys2e}`，改方括号为花括号 |
| `Option clash for package fontspec` | ctex 已加载，删重复行 | `sed '/RequirePackage.*fontspec/d'` |
| `File 'xxx.cls' not found` | 缺文档类 | 查上游 release zip 或 dtx 提取 |
| `File 'xxx.sty' not found` | 缺宏包 | 见下方"缺失宏包" |
| `Missing \begin{document}` | 语法错误或 Path= 格式不对 | `Path=./font/`→`Path=font/` |
| `Extra alignment tab` | tabular 列数不匹配 | 注释封面表格，先过编译 |
| `Illegal parameter number` | `\newcommand` 内部定义 `#1` | 定义移到 `\newcommand` 外部 |
| `\include → BibTeX chapter aux 错误` | 改 `\input` | `sed 's/\\include{/\\input{/g'` |

## 缺失宏包

| 宏包 | 替代方案 |
|------|----------|
| `circledtext.sty` | TikZ: `\node[circle,draw,inner sep=1pt]{#1}` |
| `minted` | 移除（需 -shell-escape） |
| `unicode-math` | 移除（非重度数学模板） |
| `fontawesome5` | 移除（free() crash） |
| `svg` | 移除（需 inkscape） |
| `glossaries-extra` | 移除（TL2023 参数栈溢出） |
| `hustvisual.sty` | 跳过（CTAN 仅 .dtx） |

## 字体错误

| 错误 | 修复 |
|------|------|
| `The font "Arial" cannot be found` | `\setsansfont{Arial}`→`\setsansfont{Liberation Sans}` |
| `The font "TeX Gyre Termes" cannot be found` | →`\setmainfont{Times New Roman}` |
| `The font "FandolSong-Regular" cannot be found` | →`\setCJKmainfont{SimSun}` |
| `The font "KaiTi" cannot be found` | 下载 simkai.ttf + `Path=font/` |
| `The font "XITS Math" cannot be found` | `\setmathfont{XITS Math}`→`\setmathfont{XITSMath-Regular.otf}[BoldFont=XITSMath-Bold.otf]`（fontspec 通过字体名找不到 bundle 字体，改 filename-based） |
| `\setmainfont[Path=./font/]{times.ttf}` 找不到 | setmainfont 参数必须用字体名不是文件名 |

## 无害警告（不用修）

- `algorithm.sty / algorithm2e.sty Invalid UTF-8 byte` — 宏包内部注释编码问题
- `Object @page.X already defined` — xdvipdfmx 重复对象
- `accessing absolute path` — Docker 系统字体路径

## TL2024 深坑（直接跳过，推送源码占位）

识别特征：`grep "NewTemplateType\\|DeclareTemplateCode\\|DeclareTemplateInterface" *.cls` 有输出。
影响模板：SJTUThesis、sysuthesis（中山大学）、hustthesis（华中科技）、njuthesis（南京大学 TeXPage 版）。

## 缓存竞争（诊断陷阱，不要误判为模板bug）

症状：同一命令两次结果不同，错误行号随机漂移。验证：单独编译一次——如果通过就是缓存问题不是模板bug。
