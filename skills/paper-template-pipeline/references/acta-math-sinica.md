# 数学学报（中文）— Acta Mathematica Sinica (Chinese Series)

## 模板信息

| 项目 | 值 |
|------|-----|
| 期刊 | 数学学报（Acta Mathematica Sinica, Chinese Series） |
| 来源 | TeXPage（无 GitHub 源） |
| TeXPage | https://www.texpage.com/template/f2bc0cb3-7a9d-46d2-8415-e256616620c7 |
| 期刊官网 | https://actamath.cjoe.ac.cn (Magtech 平台) |
| GitHub 仓库 | iftaken/acta-math-sinica |
| 模板分类 | 期刊投稿 |
| 状态 | 占位初始化 — 源文件待从 TeXPage 提取 |

## 来源搜寻记录

### GitHub
- 搜索 "acta-math-sinica"、"acta math sinica latex"、"数学学报 latex"、"amse-new" — 全部无结果

### TeXPage 页面 HTML
- HTML 中无 GitHub 链接、无 `downloadFile` 引用、无 `actamath.cjoe` 域名
- 模板描述中无 "项目地址" 或 "From:" 等指向外部源的文字

### Magtech 直接下载（全部 403）
期刊官网使用 Magtech 系统，模板下载 URL 格式为：
`https://actamath.cjoe.ac.cn/Jwk_sxxb_en/CN/item/downloadFile.do?id=<N>`

尝试了 id 1-15，全部返回 403。Magtech 平台对非浏览器请求有访问控制。

### 结论
TeXPage-only 模板，走「占位先行」策略。

## 处理流程

1. 创建私有仓库 `iftaken/acta-math-sinica`
2. 注入标准结构：AGENTS.md、.gitignore、init.sh（空字体列表）、references.bib
3. 编写占位 `main.tex`（ctexart，含模板源链接和编译命令）
4. Docker 编译通过 → main.pdf (46.6 KiB)
5. Commit + push
6. 标记为「源文件待提取」— 需浏览器端 "Open as Template" 提取 .cls/.tex

## 后续提取步骤

在浏览器环境中：
1. 访问 TeXPage 模板页 → "Open as Template"
2. 提取所有源文件（.cls、.tex、.bst、.sty 等）
3. 识别字体依赖 → 更新 init.sh
4. 替换占位 main.tex → 适配编译 → 推送正式版本
