# MDPI Journal Template (mdpi.cls v4.0)

## Publisher Info

| 属性 | 值 |
|------|-----|
| 出版商 | MDPI (Multidisciplinary Digital Publishing Institute) |
| 文档类 | `mdpi.cls` v4.0 (20 March 2024) |
| 基础类 | `article` (10pt, a4paper) |
| 官方来源 | https://www.mdpi.com/authors/latex |
| GitHub 镜像 | `xiuliyouran/MDPI_Template_LaTex` |
| 语言 | 纯英文，零 CJK 依赖 |
| 字体 | `mathpazo` (Palatino) + T1 fontenc（pdflatex 风格） |

## 模板结构

```
.
├── main.tex              # 论文入口（需从 template.tex 重命名）
├── Definitions/          # MDPI 类文件目录（关键！）
│   ├── mdpi.cls          # 文档类
│   ├── journalnames.tex  # 期刊名称数据库（~480种期刊）
│   ├── logo-mdpi.eps     # MDPI logo（EPS → 需转 PDF）
│   ├── logo-ccby.eps     # CC-BY logo（EPS → 需转 PDF）
│   ├── logo-updates.eps  # Updates logo（EPS → 需转 PDF）
│   └── logo-orcid.pdf    # ORCID logo（已为 PDF，无需转换）
├── mdpi.bst              # MDPI BibTeX 样式
├── chicago2.bst          # Chicago BibTeX 样式
└── references.bib        # 心河Paper 系统要求（thebibliography 模式也需此占位文件）
```

## 适配要点

### 1. pdftex 选项移除（必须）

`main.tex` 中 `\documentclass` 的默认选项包含 `pdftex`：

```latex
\documentclass[journal,article,submit,pdftex,moreauthors]{Definitions/mdpi}
```

tectonic 使用 XeTeX 引擎，必须移除 `pdftex`：

```latex
\documentclass[journal,article,submit,moreauthors]{Definitions/mdpi}
```

### 2. EPS → PDF 转换（必须）

MDPI 模板使用 3 个 EPS logo 文件，tectonic 不支持 EPS：

```bash
cd Definitions/
for f in *.eps; do
  gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite \
    -sOutputFile="${f%.eps}.pdf" -dEPSCrop "$f"
done
rm *.eps  # 删除 EPS 源文件，避免 tectonic 误用
```

### 3. cls 中硬编码 .eps 路径修正（必须）

`Definitions/mdpi.cls` 中有 6+ 处硬编码 `.eps` 扩展名。转换后需批量替换：

| 原引用 | 替换为 | 触发条件 |
|--------|--------|----------|
| `logo-mdpi.eps` | `logo-mdpi.pdf` | 默认 submit 状态（2处：header + fallback） |
| `logo-ccby.eps` | `logo-ccby.pdf` | 默认 copyright 区块（1处） |
| `logo-updates.eps` | `logo-updates.pdf` | accept 状态（1处，不触发但仍需修正） |
| `logo-ccby-nc-nd.eps` | `logo-ccby.pdf` | ijtpp 期刊专用（1处，不触发） |
| `\@journal-logo.eps` | 保持不动 | 期刊特定 logo（accept 状态，不触发） |
| `logo-mdpi-siuj.eps` | 保持不动 | siuj 期刊专用（不触发） |
| `logo-mdpi-scipharm.eps` | 保持不动 | scipharm 期刊专用（不触发） |

**只替换我们会触发的3个**：`logo-mdpi.eps` → `logo-mdpi.pdf`（replace_all=true），`logo-ccby.eps` → `logo-ccby.pdf`，`logo-updates.eps` → `logo-updates.pdf`。

### 4. init.sh

零 CJK 依赖，空字体列表：

```bash
FONT_FILES=()
# 或直接 echo 提示并 exit 0
```

### 5. references.bib

MDPI 模板使用 `thebibliography` 环境（手动参考文献），不依赖 BibTeX。但心河Paper 系统要求 `references.bib` 必须存在 → 创建占位文件即可。

### 6. 编译验证

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

预期：exit 0，PDF ~65-70KB，仅有 Underfull hbox + smart quote glyph 警告（无害）。

## 警告说明（安全忽略）

| 警告 | 原因 | 影响 |
|------|------|------|
| `Missing character: "“" (0x201c) in font pplr8t` | T1 Palatino 不含 Unicode 弯引号 | 极小——弯引号渲染为空白，段落中不易察觉 |
| `Underfull \hbox` | 行内内容过窄 | 无影响 |
| `Invalid UTF-8 byte` | 部分包文件注释含非 UTF-8 字节 | 无影响 |

## 已上线实例

- `iftaken/mdpi-template` — 2026-06-09 上线，tectonic 编译通过 67KB PDF
