# 内蒙古科技大学硕士学位论文模板 (2025)

## 标识

- **TeXPage ID**: `59239f8f-78ed-4048-8246-213d6f3b6f03`
- **TeXPage URL**: https://www.texpage.com/template/59239f8f-78ed-4048-8246-213d6f3b6f03
- **目标仓库**: `iftaken/imust-master-thesis`
- **描述**: 内蒙古科技大学硕士学位论文模板 (2025)
- **作者**: richey (richey@imust.edu.cn)
- **许可证**: Creative Commons CC BY 4.0
- **最后更新**: 2024-12-24

## 来源确认

**方式 B — 无 GitHub 源仓库，需浏览器提取。**

已穷举所有远程途径，无一成功：

| 途径 | 命令/URL | 结果 |
|------|----------|------|
| TeXPage HTML 抓取 | `curl texpage.com/template/...` | GitHub URL 不在 HTML 中（纯 JS 渲染） |
| TeXPage API get | `api/template/get?templateId=...` | `code:1003` 需登录 |
| TeXPage API download | `api/template/download?templateId=...` | `code:1003` 需登录 |
| TeXPage OSS 静态资源 | `latex-static.texpage.com/template/.../main.tex` | 404 |
| GitHub 搜索 (`gh search repos "imust thesis"`) | — | 无匹配 |
| GitHub 搜索 (`gh search repos "richey"`) | — | 用户不存在于 GitHub |
| GitHub code search (`gh search code "IMUST" language:tex`) | — | 仅 XAUT 模板引用中提到作者邮件 |

## 页面 meta 信息

```html
<meta name="description" content="内蒙古科技大学硕士学位论文模板 (2025) | Online LaTeX editor...">
```

页面无 GitHub URL，作者名 richey，纯 JS 渲染。

## 模板元信息（预判）

- **基座模板**: 武汉大学硕士学位论文模板 (http://aff.whu.edu.cn/huangzh/)
  - GitHub code search 中 XAUT 模板的注释：`%本模板在武汉大学硕士学位论文模板以及内蒙古科技大学硕士学位论文基础基础上修改，感谢原作者的工作！http://aff.whu.edu.cn/huangzh/ (武汉大学) and richey@imust.edu.cn (内蒙古科技大学)`
- **编译引擎**: XeLaTeX（推断，基座 WHU 模板使用 XeLaTeX）
- **参考文献**: 可能使用 gb7714-2015
- **文档类**: 可能基于 ctexbook/ctexrep

## 飞书记录

- **Record ID**: `recvlPjTMYa3md`
- **Base Token**: `ErlObuSw9aTdOysjjkUce6j1nNh`（模板管理表）
- **Table ID**: `tbl0YkvmiUznuZ8O`
- **模板编号**: 170
- **状态**: 待适配（2026-06-09 更新）
- **GitHub仓库链接**: https://github.com/iftaken/imust-master-thesis

> **TeXPage UUID 核对**：用户在 2026-06-09 任务中提供了 UUID `59239f8f-4c12-4d53-935e-a7a5d36bb47f`，但 curl 该 URL 返回的是通用模板列表页（HNIE Thesis、Monograph Beamer 等），非 IMUST 专属页。飞书记录的原始来源链接确认为 `59239f8f-78ed-4048-8246-213d6f3b6f03`，与本参考文件一致。**诊断信号**：curl TeXPage URL 返回多模板列表 → UUID 错误，应从飞书 `原始来源链接` 字段获取正确 UUID。

## 当前状态

- ✅ 仓库 `iftaken/imust-master-thesis` 已创建（private）
- ✅ AGENTS.md、.gitignore、init.sh（占位）已写入
- ✅ main.tex、references.bib（占位）已写入
- ✅ Docker tectonic 编译验证通过（main.pdf 69KB，2026-06-09 两次验证均通过）
- ✅ 已推送至 GitHub（commit faa447d）
- ✅ 飞书记录已更新（状态→待适配，GitHub链接已写入）
- ⏳ **待从 TeXPage 浏览器提取源文件**
- ⏳ **待分析字体依赖并补全 init.sh**

## 适配要点（预判，待提取后确认）

- 主 tex 文件 → 需重命名为 main.tex
- 参考文献文件 → 需重命名为 references.bib
- 字体可能为项目内嵌 → 需确认 COS 字体库覆盖并更新 init.sh
- 基座为 WHU 模板 → 可能遇到 WHU 模板常见适配问题
- 参考文献样式可能是 gb7714-2015

## 与 imust-microcomputer 的关系

两个模板均为 TeXPage-only，作者均为 richey@imust.edu.cn：
- `imust-microcomputer`: 本科微型计算机实训模版，文档类 IMUSTBachelor（基于 WHU 模板修改）
- `imust-master-thesis`: 硕士学位论文模板，详细信息待提取后确认

两者可能共享部分代码（如字体声明方式、参考文献样式），提取时可互相参考。
