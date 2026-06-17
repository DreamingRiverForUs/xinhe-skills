# ustcthesis 派生模板适配模式

适用于基于 ustctug/ustcthesis 的大学论文模板（陕西理工大学、或其他 fork）。

## 模板特征识别

- 文档类：`ustcthesis.cls`（v3.x，基于 ctexbook）
- 核心架构：`\LoadClass[fontset=none]{ctexbook}` → cls 自行管理全部字体
- Key-value 配置：`\ustcsetup{...}` 在 `ustcsetup.tex` 中
- 字体体系：英文 font（times/termes/xits）+ CJK fontset（windows/mac/ubuntu/fandol）+ 数学 math-font（xits/stix/libertinus）
- 参考文献：BibTeX natbib（默认）+ BibLaTeX 可选

## Docker 适配策略（推荐：force windows path）

ustcthesis 的 Linux auto-detect 走 `ubuntu` 或 `fandol` 分支，两者在 Docker 中均有 fontspec 系统字体搜索问题。**最简单的策略是强制 windows fontset + 修补其 CJK 字体声明**。

### 第 1 步：ustcsetup.tex 强制字体方案

```latex
\ustcsetup{
  ...
  fontset = windows,   % 强制使用 Windows 字体方案
  font    = times,     % Times New Roman + Liberation Sans
  math-font = xits,    % XITS Math（tectonic bundle 中有，kpathsea 可达）
}
```

### 第 2 步：修补 ustcthesis.cls 的 windows CJK handler

Docker 系统字体：SimSun ✓ / SimHei ✓ / KaiTi ✗ / FangSong ✗

**原始代码问题**：
- `\setCJKmainfont{SimSun}[ItalicFont=KaiTi]` — KaiTi 在 Docker 中不可用
- `\setCJKmonofont{FangSong}` — FangSong 不可用
- `\setCJKfamilyfont{zhkai}{KaiTi}` — 走 fontspec 系统字体搜索，不可用
- `\setCJKfamilyfont{zhfs}{FangSong}` — 同上

**修补后**：
```latex
\newcommand\ustc@set@cjk@font@windows{%
  \setCJKmainfont{SimSun}[AutoFakeBold = 3]%     ← 移除 ItalicFont=KaiTi
  \setCJKsansfont{SimHei}%
  \setCJKmonofont{SimSun}%                        ← FangSong → SimSun
  \setCJKfamilyfont{zhsong}{SimSun}%
  \setCJKfamilyfont{zhhei}{SimHei}%
  \setCJKfamilyfont{zhkai}[Path=font/,AutoFakeBold]{simkai.ttf}%   ← Path= 本地字体
  \setCJKfamilyfont{zhfs}[Path=font/,AutoFakeBold]{simfang.ttf}%   ← Path= 本地字体
}
```

### 第 3 步：修补 times 英文 handler

Docker 系统字体：Times New Roman ✓ / Liberation Sans ✓ / DejaVu Sans Mono ✓
Docker **不含**：Arial ✗ / Courier New ✗

```latex
\newcommand\ustc@set@font@times{%
  \setmainfont{Times New Roman}%
  \setsansfont{Liberation Sans}%       ← Arial → Liberation Sans
  \ifustc@system@mac
    \setmonofont{Menlo}[Scale = MatchLowercase]%
  \else
    \setmonofont{DejaVu Sans Mono}[Scale = MatchLowercase]%  ← Courier New → DejaVu Sans Mono
  \fi
}
```

### 第 4 步：init.sh 字体下载

```bash
FONT_FILES=(
    "simkai.ttf"
    "simfang.ttf"
)
```

### 第 5 步：.gitignore 资源 PDF 例外

ustcthesis 模板通常附带校徽、校名 PDF：
```
!ustc-badge.pdf
!ustc-name.pdf
!ustc-name-stxingkai.pdf
!ustc-title-page-heading.pdf
```

## XITS Math 数学字体（tectonic 兼容，无需修改）

ustcthesis 的 XITS 数学字体加载使用 `Extension=.otf` + kpathsea 文件名查找：
```latex
\IfFontExistsTF{XITSMath-Regular.otf}{%
  \gdef\ustc@font@name@xits@math{XITSMath-Regular}%
}
\setmathfont{\ustc@font@name@xits@math}[Extension=.otf,StylisticSet=8]
```
tectonic bundle 包含 XITSMath-Regular.otf，kpathsea 可直接找到。**无需任何修改**。

## 为什么不走 ubuntu/fandol 分支

| 分支 | 问题 |
|------|------|
| ubuntu (noto CJK) | zhkai/zhfs 用 `\setCJKfamilyfont{zhkai}{FandolKai}[Extension=.otf]` — 走 fontspec 系统字体搜索，Fandol 不在 Docker 系统字体中 |
| fandol | 所有 `\setCJKmainfont{FandolSong}[Extension=.otf]` 等 — 全部走 fontspec 系统搜索，全部失败 |

强制 windows 分支 + 修补是最少改动的方案（4 行 cls 修改 + 1 行 ustcsetup + 下载 2 个字体）。

## Pitfalls

- **`\IfFontExistsTF` 在 cls preamble 中可用**（与通用说法相反）：ustcthesis 的 cls 在 `\LoadClass[fontset=none]{ctexbook}` 之后才调用 `\IfFontExistsTF`，此时 fontspec 已由 ctexbook 加载，该命令可用。XITS 字体检测和 fontset auto-detect 均正常工作。
- **校徽 PDF 可能缺或与学校不匹配**：ustcthesis 派生模板常保留原 USTC 校徽。需要替换为实际学校 logo，或保留占位（学生自行替换）。
- **`\RequirePackage{subcaption}` 在 ustcthesis.cls:428**：tectonic bundle 有 subcaption.sty，无需修改。
