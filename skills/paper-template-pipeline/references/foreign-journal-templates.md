# 外国期刊/学术模板快速上线参考

纯英文、零 CJK 依赖的模板，上线流程比国内大学模板简单得多。按出版商获取 cls → 创建示例 main.tex → Docker 编译 → 推送。

## 期刊出版商 cls 获取

| 出版商 | 文档类 | 获取方式 | 示例仓库 |
|--------|--------|----------|----------|
| Elsevier | `elsarticle.cls` | CTAN → tectonic 自动下载缓存 | `iftaken/elsevier-article-template` |
| Springer Nature | `sn-jnl.cls` | Springer CDN 直接下载 | `iftaken/springer-nature-template` |
| IEEE | `IEEEtran.cls` | tectonic bundle 自动下载 | `iftaken/ieee-template` |
| ACM | `acmart.cls` | CTAN zip → docstrip 提取 | `iftaken/acm-template` |
| MDPI | `mdpi.cls` | MDPI 官方 GitHub/latex-templates | `iftaken/mdpi-template` |
| AASTeX | `aastex701.cls` | CTAN zip 下载 | `iftaken/aastex-template` |

## 通用学术文章模板

对于无特定出版商 cls 的通用模板，使用 `article` + `natbib` + `biblatex`：

| 模板 | 仓库 |
|------|------|
| Academic Article (Manuscript/Preprint) | `iftaken/academic-article-template` |
| O'Reilly Template | `iftaken/oreilly-template` |

## 关键流程（比国内大学模板快 3-5x）

1. **获取 cls**：CTAN curl 下载 zip → 解压 cls/bst 到项目根目录
2. **创建 main.tex**：写一个技术深度足够（MILP/算法/伪代码/博弈模型）的示例
3. **零 CJK 依赖**：init.sh 空数组，`.gitignore` 排除 `font/` 即可
4. **一行编译**：`tectonic -X compile main.tex`，通常一次通过
5. **推送**：add + commit + push

## Pitfalls

- **CTAN zip 不含预编译 cls**：如 acmart.dtx 需 docstrip 提取 → Python 脚本 `scripts/extract_dtx.py`
- **MDPI 的 `pdftex` 选项**：需移除（XeTeX/tectonic 不兼容 `pdftex` class option）
- **EPS logo**：期刊模板常含 EPS logo（如 MDPI 的 logo-mdpi.eps），需 `gs` 转 PDF
- **thebibliography 手动参考文献**：部分期刊模板使用 `\begin{thebibliography}` 而非 BibTeX，心河Paper 仍要求 `references.bib` 文件存在（创建占位即可）
- **非标准依赖**：巴西 abntex2、印尼/俄文 GOST 等不在 tectonic bundle，此类模板标记「需完整 TeX Live」→ 占位先行
