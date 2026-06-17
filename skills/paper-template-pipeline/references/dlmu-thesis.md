# 大连海事大学论文模板 (dlmuthesis)

## 基本信息

| 项目 | 值 |
|------|-----|
| TeXPage ID | `b32e0cb4-ef09-4ee2-b4ff-ca92b2ed3665` |
| TeXPage 作者 | HankLo |
| GitHub 源 | `JohnsonLo00/dlmuthesis` |
| 目标仓库 | `iftaken/dlmu-thesis` |
| 许可证 | LPPL 1.3c |
| 文档类 | `dlmuthesis.cls` v3.0.0-beta.6 |

## 平台模式

模板 cls 内置 `customization` 平台选项，专为自定义环境设计。在 Docker 中使用 `\documentclass[MA,customization]{dlmuthesis}`（或其他学位类别+customization）。

customization 分支行为：
- CJK 字体：ctex 自动检测 Docker 系统字体 (SimSun/SimHei)
- 英文：默认 Latin Modern 字体
- **无需下载任何外部字体**

## 学位类别选项

- `BAstem`：本科-理工科
- `BAhumanities`：本科-人文社科
- `MA`：硕士
- `MAlaw`：硕士-法学/法律
- `MAmarxism`：硕士-马克思主义理论
- `DOC`：博士
- `DOClaw`：博士-法学/法律
- `DOCmarxism`：博士-马克思主义理论

## 适配要点

- **零 patch 模板**：customization 分支在 Docker 中开箱即用，无需任何代码修改
- 参考文献引擎：BibTeX（`\bibliography{references}`），非 biblatex
- gbt7714 bst 由 cls 内部管理（调用 gbt7714-numerical.bst），tectonic 自动下载
- 签名图片：`\signofstudent`/`\signofmentor` 引用 signatures/ 目录中的 PNG

## 编译结果

- tectonic exit 0，无错误
- 安全警告：algorithm2e.sty UTF-8 字节（宏包内部注释编码，不影响输出）、PDF version 1.7→1.5 降级
- PDF 大小：~1.1 MB（MA 模式，含封面+中英文摘要+目录+四章正文+结论+参考文献+附录+致谢+简历）

## init.sh

```bash
#!/bin/bash
set -euo pipefail
FONT_DIR="font"
mkdir -p "${FONT_DIR}"
echo "Font directory '${FONT_DIR}' created. No external fonts needed for Docker compilation."
```

FONT_FILES 为空数组——customization 模式下无需字体下载。

---

# 大连海事大学本科毕业论文模板 (dlmubachelorthesis v2.0.1)

dlmuthesis v3.0.0 的前驱版本，专为**本科毕业论文**设计（仅学士学位，无硕博选项）。

## 基本信息

| 项目 | 值 |
|------|-----|
| TeXPage ID | `7227497e-7fce-4ed2-8126-92daa6bda5ac` |
| TeXPage 作者 | HankLo |
| GitHub 源 | `JohnsonLo00/dlmubachelorthesis` |
| 目标仓库 | `iftaken/dlmu-bachelor-thesis` |
| 许可证 | LPPL 1.3c |
| 文档类 | `dlmubachelorthesis.cls` v2.0.1 (2024/09/27) |

## 架构差异（vs dlmuthesis v3.0.0）

| 方面 | v2.0.1 (bachelor) | v3.0.0 (dlmuthesis) |
|------|-------------------|---------------------|
| 基础文档类 | `article` | `ctexbook` |
| CJK 管理 | `\RequirePackage{ctex}`（手动字体声明） | ctexbook 内置 fontset |
| 学位覆盖 | 仅本科（bachelors / bachelorh） | 本/硕/博多类别 |
| 平台模式 | 无 customization 选项 | 内置 customization 分支 |
| 参考文献 BST | `thuthesis-bachelor.bst` | gbt7714-numerical.bst |
| 参考文献引擎 | natbib | natbib |

## 适配要点

### 字体修复

cls 使用 `\ifwindows` / `\ifplatform` 做平台检测：

```latex
\ifwindows
\setCJKmainfont[AutoFakeBold=3.0, AutoFakeSlant=0.3]{SimSun}
\else
\setCJKmainfont[AutoFakeBold=3.0, AutoFakeSlant=0.3]{SourceHanSerifSC-Regular.otf}
\fi
```

非 Windows 分支用文件名作为字体名（fontspec 找不到），且仓库中的 `SourceHanSerifSC-Regular.otf`（~20MB）不应进 git。

**修复**：移除平台检测，直接使用 `\setCJKmainfont[AutoFakeBold=3.0]{SimSun}`（Docker 系统字体）。

### changes 包内容清理（高频）

源文件示例内容（ch4.tex、humanities/ch3.tex）大量使用 `changes` 宏包的批注命令：

```latex
\added[id=海哥, comment={少了一句}]{是鸟也，海运则将徙于南冥。}
\deleted[id=海哥, comment={这句话删掉}]{之乎者也。}
\replaced[id=海老, comment={用错词}]{坳堂}{水堂}
\highlight[id=海老]{故夫知效一官...}
\comment[id=海老]{建议把落款补上}
```

`changes` 是开发调试工具，平台不需要。从 main.tex 移除 `\usepackage[]{changes}` 及相关命令后，**必须同时清理所有章节文件中的 changes 命令**，否则编译报 `Undefined control sequence`。

清理规则（sed）：
```bash
sed -i '' -E \
  -e 's/\\replaced\[[^]]*\]\{([^}]*)\}\{[^}]*\}/\1/g' \
  -e 's/\\added\[[^]]*\]\{([^}]*)\}/\1/g' \
  -e 's/\\deleted\[[^]]*\]\{[^}]*\}//g' \
  -e 's/\\highlight\[[^]]*\]\{([^}]*)\}/\1/g' \
  -e 's/\\comment\[[^]]*\]\{[^}]*\}//g' \
  mainbody/STEM/ch4.tex mainbody/humanities/ch3.tex
```

- `\added{text}` → 保留 text
- `\deleted{text}` → 删除整段
- `\replaced{new}{old}` → 保留 new
- `\highlight{text}` → 保留 text
- `\comment{text}` → 删除整段

### main.tex 要点

- 学位选项：`\documentclass[bachelors]{dlmubachelorthesis}`（理工科）或 `[bachelorh]`（文科）
- 移除 `changes` 包：删掉 `\let\comment\undefined`、`\usepackage[]{changes}`、`\definechangesauthor`、`\listofchanges`
- 参考文献路径：`\bibliography{refs/refs_STEM}` → `\bibliography{references}`
- 保留 `refs/` 目录中的原始 bib 文件（供用户参考）

## 编译结果

- tectonic exit 0，BibTeX 自动 rerun ×2，无错误
- 安全警告：algorithm2e.sty UTF-8 字节、simplekv.tex UTF-8 字节、overfull hbox
- PDF 大小：~754 KB（bachelors 模式，含封面+中英文摘要+目录+四章正文+结论+参考文献+致谢+附录）
- 无需外部字体下载（SimSun + Times New Roman 均为 Docker 系统字体）

## init.sh

```bash
#!/bin/bash
set -euo pipefail
FONT_DIR="font"
FONT_FILES=()

mkdir -p "${FONT_DIR}"

if [ ${#FONT_FILES[@]} -eq 0 ]; then
    echo "No external fonts needed. Docker provides SimSun/Times New Roman as system fonts."
    exit 0
fi
```

注意 `set -u` 下空数组的 for 循环保护。
