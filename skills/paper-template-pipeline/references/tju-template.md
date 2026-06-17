# 天津大学本科毕业论文模板

## 来源

- **TeXPage**: https://www.texpage.com/template/a2bf0aed-3537-456e-baca-c7a3e568ce9e
- **GitHub 源**: twtstudio/TJUThesisLatexTemplate
- **目标仓库**: iftaken/tju-thesis

## 模板特征

| 属性 | 值 |
|------|-----|
| 文档类 | `ctexbook`（`\documentclass[12pt,openany,oneside]{ctexbook}`） |
| .cls 文件 | 无 — 使用 `setup/package.tex` + `setup/format.tex` 模式 |
| CJK 方案 | ctexbook 默认 Fandol fontset（Docker/Linux 自动检测） |
| 参考文献 | natbib + 自定义 `ref.bst`（原 `references/ref.buk`） |
| 字体依赖 | 无外部依赖 — Fandol 全部在 tectonic bundle 中 |
| EPS 图片 | 3 个（tjuname.eps, tjulogo.eps, p1p2figure.eps）→ 转 PDF |

## 适配要点

### 包清理（pdflatex → XeTeX）

移除的包（ctexbook 在 XeTeX 下替代或冲突）：
- `CJK`, `CJKutf8`, `CJKpunct`, `CJKnumb` — ctexbook 原生处理
- `lmodern`, `T1 fontenc`, `newtxtext` — XeTeX 用 fontspec

### CJKnumb 兼容

`\CJKnumber` 在格式定义和 BST 文件中被使用。ctex 的 `\chinese` 替代：
- 在 format.tex 的 `\chaptername` 中：`\chinese{chapter}`（**计数器名**，非 `\thechapter`）
- 在 main.tex preamble：`\providecommand{\CJKnumber}[1]{\chinese{#1}}`（BST 兼容 shim）

### EPS 转 PDF

```bash
cd figures && for f in *.eps; do gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="${f%.eps}.pdf" -dEPSCrop "$f"; done
```

.gitingore 需加例外：`!tjuname.pdf`, `!tjulogo.pdf`, `!p1p2figure.pdf`

### 参考文献

- `references/reference.bib` → `references.bib`（心河Paper 标准名）
- `references/ref.buk` → `ref.bst`（标准扩展名）
- `\bibliographystyle{references/ref.buk}` → `\bibliographystyle{ref}`
- `\bibliography{references/reference}` → `\bibliography{references}`

### .gitignore 例外

转换后的校徽 PDF 需要 .gitignore 白名单：
```
!tjuname.pdf
!tjulogo.pdf
!p1p2figure.pdf
```

## 编译验证

**状态**: ✅ 通过
- `tectonic -X compile main.tex` 返回 0
- `main.pdf` 553KB
- 零致命错误
- 安全警告：algorithm.sty UTF-8 字节、PDF 版本差异、示例内容带圈数字缺失（lmroman 无 U+2460-2468）
