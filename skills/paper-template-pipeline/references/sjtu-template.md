# 上海交通大学硕博论文模板 (SJTUThesis)

## 来源

| 项目 | 值 |
|------|-----|
| 官方仓库 | `sjtug/SJTUThesis` |
| TeXPage | https://www.texpage.com/template/542af6f9-f66f-4068-8732-f20fe7bd08ef |
| 心河Paper 仓库 | `iftaken/sjtu-thesis` |
| 版本 | v2.3.1 |
| 文档类 | `sjtuthesis` (CTAN/TeX Live 分发包) |

## 关键特征

- **CTAN 分发包模式**：GitHub 源码仓库**不含 `.cls` 文件**——`sjtuthesis.cls`、`sjtuarticle.cls`、`sjtureport.cls` 及所有 `.def` 文件通过 TeX Live/CTAN 发布。GitHub 仓库仅含用户文件（main.tex、contents/、figures/、scans/、setup.tex、refs.bib）。
- **完整 texmf 树**：Release zip 解压后 `texmf/` 目录含 ~50 个文件（3 个 .cls、35 个 .def、10 个 VI logo PDF）
- **参考文献引擎**：biblatex + biber（gb7714-2015 标准）
- **CJK 字体方案**：ctex 默认字体方案，内部 auto-detect 系统字体
- **VI 资源**：10 个 SJTU 校徽/标志 PDF（`texmf/tex/latex/sjtutex/vi/sjtu-vi-*.pdf`）

## 获取源文件

### 从 GitHub Release 获取完整 texmf（必须）

```bash
# 1. 下载完整 Release zip
curl -sL 'https://github.com/sjtug/SJTUThesis/releases/download/v2.3.1/SJTUThesis-full-2.3.1.zip' -o /tmp/sjtu-full.zip

# 2. 解压 texmf 目录
unzip -o /tmp/sjtu-full.zip "SJTUThesis-full-2.3.1/texmf/*" -d /tmp/sjtu-full-extract/

# 3. 复制到项目
cp -r /tmp/sjtu-full-extract/SJTUThesis-full-2.3.1/texmf /path/to/repo/
```

### 从 GitHub 仓库获取用户文件

```bash
gh repo clone sjtug/SJTUThesis /tmp/sjtu-source -- --depth 1
# 复制 main.tex, setup.tex, refs.bib, contents/, figures/, scans/
```

## 结构调整

### 必须重命名

```
refs.bib → references.bib  （系统要求）
```

### setup.tex 修改

```latex
# 改前
\addbibresource{refs.bib}

# 改后
\addbibresource{references.bib}
```

## .gitignore 注意事项

模板包含两类 PDF 资源文件，需在 `.gitignore` 中加例外：

### scans/ 目录（2 个）
```
!sample-copyright-a.pdf
!sample-copyright-b.pdf
```

### texmf/vi/ 目录（10 个 SJTU VI logo）
```
!sjtu-vi-*.pdf
```

10 个文件列表：
- sjtu-vi-badge-cor-red.pdf
- sjtu-vi-badge-reg-red.pdf
- sjtu-vi-logo-eng-h-cor-red.pdf
- sjtu-vi-logo-eng-h-reg-red.pdf
- sjtu-vi-logo-std-c-cor-red.pdf
- sjtu-vi-logo-std-c-reg-red.pdf
- sjtu-vi-logo-std-h-cor-red.pdf
- sjtu-vi-logo-std-h-reg-red.pdf
- sjtu-vi-logo-std-v-cor-red.pdf
- sjtu-vi-logo-std-v-reg-red.pdf

> 使用 `!sjtu-vi-*.pdf` 通配符一次性匹配全部 10 个文件，位于 `texmf/tex/latex/sjtutex/vi/` 子目录中，但通配符从项目根 `.gitignore` 作用。

## tectonic 编译适配

### 问题 1：TEXINPUTS 不生效

**现象**：设置 `-e TEXINPUTS="./texmf//:"` 后 tectonic 仍报 `File 'sjtuthesis.cls' not found`。

**修复**：将 cls/def 文件直接复制到项目根目录（与 main.tex 同级）。

```bash
cp texmf/tex/latex/sjtutex/sjtuthesis.cls .
cp texmf/tex/latex/sjtutex/font/*.def .
cp texmf/tex/latex/sjtutex/lang/*.def .
cp texmf/tex/latex/sjtutex/preset/*.def .
cp texmf/tex/latex/sjtutex/scheme/*.def .
cp texmf/tex/latex/sjtutex/vi/*.pdf .
```

### 问题 2：sjtu-thesis.cls 需要 LaTeX 2024-06-01（TL2023 不兼容）

`sjtu-thesis.cls` v2.3.1 共 1525 行，使用了多个 LaTeX 2024-06-01 新增特性。需要以下修改：

#### a) 降低格式版本要求（行 22）
```latex
# 改前
\NeedsTeXFormat{LaTeX2e}[2024-06-01]

# 改后
\NeedsTeXFormat{LaTeX2e}[2022-06-01]
```

#### b) 注释掉格式版本检查错误块（行 23-29）
```latex
# 改前
\providecommand\IfFormatAtLeastTF{\@ifl@t@r\fmtversion}
\IfFormatAtLeastTF{2024-06-01}{}
 {\PackageError{sjtutex}
   {Your LaTeX format is outdated!...}{}}

# 改后
\providecommand\IfFormatAtLeastTF{\@ifl@t@r\fmtversion}
% \IfFormatAtLeastTF{2024-06-01}{}
%  {\PackageError{sjtutex}...}
```

#### c) 注释 exp_args_generate:n { Nnv }（行 51）
```latex
# 改前
\exp_args_generate:n { Nnv }

# 改后
% \exp_args_generate:n { Nnv }  % TL2024+, commented for TL2023 compat
```

#### d) ProcessKeyOptions → ProcessKeysOptions + l3keys2e（行 226）
```latex
# 改前
\ProcessKeyOptions [ sjtu / option ]

# 改后
\RequirePackage{l3keys2e}
\ProcessKeysOptions { sjtu / option }
```

### 问题 3：第 251 行 Undefined control sequence（未解决）

修改上述 4 处后，编译仍报 `sjtu-thesis.cls:251: Undefined control sequence`。需要 `--keep-logs` 查看 `main.log` 精确定位未定义宏。

## 字体方案

sjtuthesis 使用 ctex 默认字体方案（内部 auto-detect）：

- Docker 镜像已有 SimSun、SimHei、Times New Roman → ctex 自动检测通过
- **无需下载任何额外字体**，init.sh 可为空操作

```bash
# init.sh 内容
echo "✓ 此模板使用 ctex 默认字体方案"
echo "✓ 系统字体已预装在 Docker 镜像中"
echo "✓ 无需下载额外字体文件"
```

## Docker 编译命令

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

## 待解决

- [ ] sjtu-thesis.cls 行 251 `Undefined control sequence` —— 需 `--keep-logs` 获取完整日志定位
- [ ] 可能存在更多 `:e`/`:en` expl3 变体或额外的 `\exp_args_generate` 调用
- [ ] VI logo PDF 是否在编译路径正确解析（当前已复制到根目录）

## 经验总结

1. **CTAN 分发包模式 ≠ dtx 模式**：不像 NJU/Nankai 需要用 `extract_dtx.py` 提取，SJTU 的 cls 是预构建的，直接从 Release zip 拿。
2. **Release zip 是唯一完整来源**：GitHub 仓库 + 浅克隆拿不到 cls；`gh release download` 的 sample PDF 也不行——必须下载 `SJTUThesis-full-*.zip`。
3. **tectonic 的 TEXINPUTS 不工作**：遇到 cls 不在 tectonic bundle 中的模板，直接复制到根目录是最稳定的方式。
4. **sjtuthesis v2.3.1 是重度 expl3 模板**：从 TL2024 backport 到 TL2023 需要多轮迭代修改。
