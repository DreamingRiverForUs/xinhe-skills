# 内蒙古科技大学本科生毕业设计模板

## 标识

- **TeXPage ID**: `8b08f74d-8e6a-4488-915e-f19b6f739d48`
- **TeXPage URL**: https://www.texpage.com/template/8b08f74d-8e6a-4488-915e-f19b6f739d48
- **目标仓库**: `iftaken/imust-bachelor-thesis`
- **描述**: 内蒙古科技大学本科生毕业设计模板
- **作者**: richey (richey@imust.edu.cn，推测，与 imust-master-thesis 同作者)
- **最后更新**: 待确认

## 来源确认

**方式 B — 无 GitHub 源仓库，需浏览器提取。**

| 途径 | 命令/URL | 结果 |
|------|----------|------|
| TeXPage HTML 抓取 | `curl texpage.com/template/...` | 无 GitHub URL |
| TeXPage API get | `api/template/get?templateId=...` | `code:1003` 需登录 |
| TeXPage API download | `api/template/download?templateId=...` | `code:1003` 需登录 |
| GitHub 搜索 (`gh search code "imust" language:tex`) | — | 无匹配（仅 XAUT 模板引用中提到作者邮件） |

## 模板元信息（预判）

- **作者**: 与 imust-master-thesis 同作者 richey@imust.edu.cn
- **编译引擎**: XeLaTeX（推断）
- **基座模板**: 可能与 imust-master-thesis 同源（武汉大学硕士学位论文模板）
- **参考文献**: 可能使用 gb7714-2015
- **文档类**: 可能基于 ctexbook/ctexrep

## 当前状态

- ✅ 仓库 `iftaken/imust-bachelor-thesis` 已创建（private）
- ✅ AGENTS.md、.gitignore、init.sh（占位）已写入
- ✅ main.tex、references.bib（占位）已写入
- ✅ Docker tectonic 编译验证通过（main.pdf 73KB）
- ✅ 已推送至 GitHub
- ⏳ **待从 TeXPage 浏览器提取源文件**
- ⏳ **待分析字体依赖并补全 init.sh**

## 与 imust-master-thesis 的关系

两个模板均为 TeXPage-only，作者均为 richey@imust.edu.cn：
- `imust-bachelor-thesis`: 本科生毕业设计模板
- `imust-master-thesis`: 硕士学位论文模板

两者可能共享部分代码（如字体声明方式、参考文献样式），提取时可互相参考。
