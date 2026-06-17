# CCT (cctart) → ctexart/XeLaTeX 适配指南

适用于使用 `cctart` 文档类的旧中文 LaTeX 模板（2015年前后），转换为 ctexart + XeLaTeX/Tectonic 编译。

## 适配检查清单

### 1. 文档类替换

```latex
% 前
\LoadClass{cctart}
% 后
\LoadClass{ctexart}
```

同时更新所有 `\PassOptionsToClass{...}{cctart}` 和 `\DeclareOption*{\PassOptionsToClass{...}{cctart}}` 中的 `cctart` → `ctexart`。

### 2. 移除 CCT 专属命令

| CCT 命令 | 处理方式 |
|----------|---------|
| `\pushziti` / `\popziti` | 直接删除，ctex 自动管理字体 |
| `\ziju{0.135}` | 删除（ctex 默认间距，或使用 `\ziju` 但命令名相同实现不同） |
| `\ccwd`（当前字号汉字宽度） | 替换为 `em`，`2\ccwd` → `2em` |
| `\input scrload.tex` | 删除（CCT 内部脚本） |
| `\AtBeginDvi{\input{zhwinfonts}}` | 删除（XeTeX 不需要） |
| `\sectionname` 重定义 | 删除（ctexart 不含此命令） |

### 3. 移除 CCT 字体原语

CCT 使用底层 `\newfont`、`\font`、`\newfam` 声明字体，这些在 XeTeX 中不可用：

```latex
% 删除以下全部:
\newfam\cryfam
\newfam\smbfam
\newfont{\htxt}{eufm10 scaled \magstep0}
\font\tenthxt=eufm10 scaled \magstep0
\font\tenBbb=msbm10 scaled \magstep0
\font\tencyr=wncyr10 scaled \magstep0
\font\tenrm=cmr10 scaled \magstep0
\font\tenbf=cmb10 scaled \magstep0
\font\tenBb=msbm7
\font\tenB=msbm10 scaled \magstep3%
```

替换为标准 AMS 命令：

```latex
\providecommand{\Bbb}{\mathbb}   % 黑板粗体
\providecommand{\Bb}{\mathbb}    % 小黑板粗体
\providecommand{\B}{\mathbb}     % 大黑板粗体
\providecommand{\cyr}{\mathrm}   % 西里尔（中文期刊不需要）
\providecommand{\txt}{\mathfrak} % Euler fraktur
```

### 4. 移除过时宏包

从 `\RequirePackage` 中删除：
- `epsfig` — XeTeX 不需要 EPS 导入桥接
- `epstopdf` — XeTeX 原生支持 PDF 图片

### 5. 编码转换

CCT 模板通常使用 **GBK** 编码。必须先转换为 UTF-8：

```bash
iconv -f GBK -t UTF-8 template.cls > template.cls.utf8
iconv -f GBK -t UTF-8 main.tex > main.tex.utf8
```

### 6. 字体方案

ctexart 在 Docker/Tectonic 环境中默认 auto-detect 到 **Fandol** 字体集：
- FandolSong（宋体）→ `\songti`
- FandolHei（黑体）→ `\heiti`
- FandolKai（楷体）→ `\kaishu`
- FandolFang（仿宋）→ `\fangsong`

**无需下载任何外部字体。** `init.sh` 中只创建空 `font/` 目录即可。

## 编译陷阱

### `\heiti` 在 `\makebox[s]` 中展开失败

症状：`! Undefined control sequence. <argument> \heiti系统科学与数学`

原因：`\makebox[s]`（spread 模式）在内部处理参数时过早展开 `\heiti`，而此时字体命令尚未就绪。

修复：在 `\heiti` 外再加一层花括号：

```latex
% 前
\makebox[4.5cm][s]{\heiti系统科学与数学}
% 后
\makebox[4.5cm][s]{{\heiti 系统科学与数学}}
```

### `\refname` 重定义中字体命令在 moving argument 中失效

症状：`! Undefined control sequence. <recently read> \quad献`

原因：`\refname` 被 `\begin{thebibliography}` 用作 section heading，其内容进入 moving argument（写入 .aux / .toc）。`\heiti` 在 moving argument 中展开失败。

修复：将整个 `\refname` 定义体用花括号保护：

```latex
% 前
\renewcommand\refname{\zihao{5}\heiti 参 \quad 考 \quad 文 \quad 献 \vspace*{4mm}}
% 后
\renewcommand\refname{{\zihao{5}\heiti 参 \quad 考 \quad 文 \quad 献}\vspace*{4mm}}
```

### `\sectionname` 未定义

症状：`! LaTeX Error: Command \sectionname undefined.`

原因：`\sectionname` 是 CCT 特有的命令，标准 LaTeX/ctexart 中不存在。

修复：直接删除 `\renewcommand\sectionname{\thesection}` 行。

## 已知适配案例

- **系统科学与数学 (JSSMS)**: muzimuzhi/jssms-template → iftaken/jssm-template。cctart → ctexart，Fandol 字体，零字体下载。
