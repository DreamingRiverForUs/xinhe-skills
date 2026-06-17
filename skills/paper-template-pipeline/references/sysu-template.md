# 中山大学学位论文模板 (sysuthesis)

## 概述

- **来源**：GitHub `irenier/sysuthesis` v1.0.0
- **TeXPage**：https://www.texpage.com/template/88eb11aa-bd5c-4b6b-b654-86517c5148a1
- **类型**：本科/硕士/博士 学位论文
- **引擎**：XeLaTeX / LuaLaTeX
- **格式**：dtx/docstrip 分发包
- **目标仓库**：`iftaken/sysu-thesis`

## 获取方式

```bash
# 从 GitHub Release 下载用户包（含预编译 .cls）
gh release download v1.0.0 -R irenier/sysuthesis --pattern '*user*'
unzip sysuthesis-user-v1.0.0.zip
# 获得：sysuthesis.cls, sysuvisual.sty, sysu-emblem.pdf, sysu-name-cn.pdf,
#       sysuthesis-sample.tex, sysuthesis-sample.bib
```

⚠️ GitHub 源码仓库仅含 `.dtx`（未编译），需从 Release zip 提取 `.cls`/`.sty`。

## 文件清单

| 文件 | 来源 | 说明 |
|------|------|------|
| `sysuthesis.cls` | Release zip | **需 TL2023 兼容性 patch** |
| `sysuvisual.sty` | Release zip | 视觉样式（无版本敏感语法） |
| `sysu-emblem.pdf` | Release zip | 校徽，需 .gitignore 例外 |
| `sysu-name-cn.pdf` | Release zip | 校名中文，需 .gitignore 例外 |
| `sysuthesis-sample.tex` | Release zip | 示例文档，改编为 main.tex |
| `sysuthesis-sample.bib` | Release zip | 示例参考文献，重命名为 references.bib |

## 字体处理

- **CJK**：ctexbook + `fontset=ubuntu`（Docker 中 Noto CJK 系统字体）
  - ⚠️ ubuntu fontset 的 kai/fang 走 FandolKai/FandolFang（.otf），Docker 中可能缺失
  - 模板使用 `\songti`、`\heiti`、`\kaishu` 等 ctex 字体命令
- **拉丁**：非 Windows 分支使用 TeX Gyre Termes/Heros（.otf）+ Inconsolata
  - ⚠️ TeX Gyre 字体可能不在 Docker 系统字体中，需验证
- **数学**：unicode-math + xits（默认），可选 asana/bonum/cambria/dejavu 等

## 模板架构

- **基础类**：ctexbook（`scheme=chinese, fontset=none, zihao=-4`）
- **平台检测**：Windows → fontset=windows，macOS → mac，Linux → ubuntu
- **模板系统**：使用 LaTeX 2024-06-01 内核的 `\NewTemplateType`/`\DeclareTemplateInterface` 等（**与 TL2023 不兼容**）
- **参考文献**：支持 BibTeX (gbt7714-numerical) 和 BibLaTeX (gb7714-2015)
- **封面**：通过模板实例系统渲染，使用 `\songti`/`\heiti`/`\kaishu` 设置格式

## Tectonic TL2023 兼容性修复

### 已应用的 patch：

1. **`\ExplFileDate`/`\ExplFileVersion`/`\ExplFileDescription`** → 字面值 `{2026/02/06}{1.0.0}{...}`
2. **L3 版本检查**（`\__sysu_if_expl_as_least:n {2024/06/01}`）→ 注释掉
3. **`\ProcessKeyOptions [ sysu / option ]`** → `\ProcessKeysOptions { sysu / option }` + `\RequirePackage{l3keys2e}`
4. **`:en` 变体**（`\cs_generate_variant:Nn \__sysu_chapter:nn { en }`）→ 注释掉，`\__sysu_chapter:en` → `\exp_args:Ne \__sysu_chapter:nn`
5. **`\RequirePackage{xtemplate}`** → 添加（旧版 xtemplate 需显式加载）

### 阻塞问题（未解决）：

**2024 内核模板系统**：模板使用 `\NewTemplateType{sysu}{...}`、`\DeclareTemplateInterface{sysu}{element}{...}` 等命令。这些是 LaTeX 2024-06-01 内核新增的 ltcmd 命令，不在 TL2023 中。

已尝试的 `\NewTemplateType` shim（仅设 token list）不够——旧 xtemplate 的 `\DeclareTemplateInterface` 内部会检查类型是否已注册，报 `The object type 'sysu' is unknown`。

**决策**：标记为「需 Docker 镜像升级至 TL2024+」。源码 + AGENTS.md 可照常上线（用户本地 TL2024+ 环境可编译）。

## .gitignore 要点

```gitignore
# 保留校徽 PDF
!sysu-emblem.pdf
!sysu-name-cn.pdf
# 保留编译输出
!main.pdf
```

## main.tex 关键配置

```latex
\documentclass{sysuthesis}
\sysusetup[style]{
  cjk-font  = ubuntu,  % 明确指定，避免 auto-detect 走 windows 分支
}
\sysusetup[bib]{
  backend  = bibtex,
  style    = gbt7714-numerical,
  resource = references  % 重命名为 references.bib
}
```

## 相关参考

- 模板架构参考：`references/tectonic-expl3-compatibility.md` — LaTeX 2024 内核模板系统
- ctex fontset 回退策略：见 SKILL.md "ctex fontset 三层回退策略"
