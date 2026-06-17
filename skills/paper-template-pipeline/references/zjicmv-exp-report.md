# 浙江传媒学院数字电视原理实验报告

## 基本信息

| 字段 | 值 |
|------|-----|
| TeXPage ID | `3d62c7e2-8c94-478d-95b1-82a3fec336c4` |
| TeXPage URL | https://www.texpage.com/template/3d62c7e2-8c94-478d-95b1-82a3fec336c4 |
| 名称 | 浙江传媒学院数字电视原理实验报告 |
| 作者 | Xinyu |
| License | CC BY 4.0 |
| 最后修改 | 2025-11-26 |
| 目标仓库 | iftaken/zjicmv-exp-report |
| 来源类型 | 方式 B（TeXPage-only，无 GitHub 源） |

## 源文件状态

**当前：占位结构已上线，源文件待提取。**

已完成的：
- 仓库创建 + 标准结构（AGENTS.md、.gitignore、init.sh、references.bib）
- 占位 main.tex（ctexart 文档类）
- Docker 编译验证通过（main.pdf 33KB）
- 已推送至 GitHub

待完成：
- 在浏览器环境中 Open as Template → 提取完整 .cls/.tex 源文件
- 覆盖占位 main.tex，补充完整的模板源码
- 根据实际模板结构调整 init.sh 字体依赖
- 重新编译验证

## 搜索过程记录

1. 页面 HTML 抓取 → 无 GitHub URL
2. SSR HTML 提取 → Author: Xinyu，Abstract/License 成功提取
3. GitHub 搜索 "zjicmv" → 无结果
4. GitHub 搜索 "cuz latex" → 无相关模板
5. GitHub 搜索 "数字电视原理" → 无结果
6. TeXPage API (`/api/template/get`) → 被拦截
7. GitHub code search for template ID → 0 结果

8 层检查全部失败 → 确认为方式 B。
