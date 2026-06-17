---
name: overleaf-template-pipeline
description: Overleaf 模板 → 心河Paper 上线流水线。WebBridge 打开模板 → Download ZIP → Docker 编译 → GitHub 推送。
category: paper-template-pipeline
---

# Overleaf 模板上线流水线

Overleaf 模板比 TeXPage 简单得多——直接下载完整 ZIP，包含所有源码和二进制文件。

## 流程总览

```
① 预检 → ② 导航 Overleaf → ③ Open as Template → ④ Download as source (.zip) → ⑤ 解压适配 → ⑥ Docker 编译 → ⑦ 推送到 iftaken
```

**预计耗时**：简单模板 2-5 分钟，复杂模板 5-10 分钟（WebBridge 下载 + Docker 编译）。

## 各阶段详细操作

### ① 预检（新增！避免浪费时间）

**先判断模板是否可上线**，避免下载后才发现依赖不可用。

```bash
# 获取模板页面，检查元数据
curl -sL 'https://www.overleaf.com/latex/templates/<slug>/<id>' -H 'User-Agent: Mozilla/5.0' 2>&1 | grep -oE '"mainFile":"[^"]+"|"engine":"[^"]+"|"templateId":[0-9]+|"license":"[^"]*"'
```

**阻断条件（直接跳过）：**
- 模板描述含「internal」「proprietary」「contact ... for」→ 依赖不公开文件
- View Source 预览中引用的 .sty/.cls 在 CTAN/GitHub 搜不到
- 需要 pdflatex 引擎但有商业字体（tectonic 是 XeLaTeX）

**警告条件（需手动处理）：**
- `engine: pdflatex` → 检查是否有 `fontenc`、EPS 图片、`psfrag`
- 中文模板 → 检查是否用 ctex（兼容）还是 CJK 宏包（需适配）
- 含 `minted` → 需注释掉

```bash
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","url":"https://www.overleaf.com/latex/templates/<slug>/<id>"}'
```

等待 3-5 秒页面加载。

### ② 导航 + Dismiss Cookie

```bash
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","url":"https://www.overleaf.com/latex/templates/<slug>/<id>"}'
```

等待 3-5 秒。**必须 dismiss cookie banner**（否则 "Open as Template" 点击无效）：

```bash
# 快照查找 cookie 按钮（通常是 @e47 "Essential cookies only" 或 @e48 "Accept all"）
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"snapshot"}'
# 点击 dismiss
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","selector":"@e47"}'
```

### ③ Open as Template

```bash
# 快照确认按钮
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"snapshot"}'

# 查找 "Open as Template" 的 ref（通常是 @e11）
# 点击
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","selector":"@e11"}'
```

等待 5-8 秒项目编辑器加载。URL 会变为 `https://www.overleaf.com/project/<id>`。

### ④ Download as source (.zip)

```
File 菜单 → Download → Download as source (.zip)
```

具体 ref 序列（已验证稳定）：
- `@e2` — File 菜单
- `@e10` — Download（展开子菜单）
- `@e11` — Download as source (.zip)

文件下载到 `~/Downloads/<template_name>.zip`。

**备选方案 — View Source**：如果 Download 按钮不可用（如 SINTEF 专有模板），
模板页的 "View Source" (@e12) 按钮会展示内嵌源码。可使用 evaluate 提取：

```bash
# 点击 View Source 后
curl ... -d '{"action":"evaluate","code":"document.querySelector(\"code,pre\")?.textContent"}'
```

但此方法**不含二进制文件**（图片/PDF），且 HTML entities 需转义（`&amp;` → `&`）。

### ⑤ 解压与标准结构

```bash
unzip -o ~/Downloads/<name>.zip -d /tmp/overleaf-<name>/
```

**常见适配（参考 paper-template-pipeline skill）：**

| 问题 | 修复 |
|------|------|
| `minted` 宏包 | 注释掉 `\usepackage{minted}` + 所有 `\inputminted` 行（tectonic 不支持 shell-escape） |
| `biblatex style=apa` | 改为 `style=numeric`（TL2023 可能没有 apa） |
| 文件名 `template.tex` | 重命名为 `main.tex`（心河Paper 标准） |
| `\usepackage{fontspec}` 多余 | 注释掉（ctex 已加载） |
| EPS 图片 | `gs` 转 PDF |

**零依赖纯英文模板**（无 ctex/CJK）：无需字体下载，init.sh 为空。

### ⑤ Docker 编译

```bash
cd /tmp/overleaf-<name>/
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

### ⑥ 标准结构 + 推送 → ⑦ PII 清洗

创建 AGENTS.md、.gitignore、init.sh、references.bib（如缺失），编译通过后：

```bash
git init && git remote add origin git@github.com:iftaken/<repo-name>.git
git add -A && git commit -m "init: <template name> - Overleaf → tectonic compile OK"
git push --force origin main
```

**重要**：上线前必须执行 PII 清洗（作者姓名、邮箱、QQ群号、微信二维码、GitHub 个人链接等）。参见 `template-pii-scrubbing` skill。

```bash
git init && git remote add origin git@github.com:iftaken/<repo-name>.git
git add -A && git commit -m "init: <template name> - Overleaf → tectonic compile OK"
git push --force origin main
```

## 批量收集：Overleaf 模板库爬取

从 Overleaf 模板库批量收集模板信息，写入飞书多维表格统一管理。

### 收集策略

Overleaf 模板按分类（tag）组织，每个 tagged 页面显示约 9 个最近模板：

```
https://www.overleaf.com/latex/templates/tagged/<category>
```

12 个主要分类：academic-journal, bibliography, book, calendar, cv, formal-letter, homework, newsletter, poster, presentation, report, thesis

### WebBridge 批量提取

```bash
# 导航到分类页
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","url":"https://www.overleaf.com/latex/templates/tagged/thesis"}'

sleep 4

# 滚动触发懒加载
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","code":"window.scrollTo(0,document.body.scrollHeight)"}'

sleep 2

# 提取所有模板链接（排除 tagged/ 标签链接）
curl -s http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","code":"Array.from(document.querySelectorAll(\"a\")).filter(a=>a.href.includes(\"latex/templates/\")&&!a.href.includes(\"tagged/\")).map(a=>({name:(a.textContent||\"\").trim().slice(0,80),url:a.href})).filter(x=>x.name&&x.url).map(x=>JSON.stringify(x)).join(\"|||\")"}'
```

结果格式：`{"name":"模板名","url":"https://..."}|||{"name":"...","url":"..."}`

### 飞书表格结构

| 字段 | 类型 | 用途 |
|------|------|------|
| 模板名称 | text | slug 转换或页面提取 |
| Overleaf链接 | url | 完整 URL |
| 分类 | select | 12 个分类选项 |
| 状态 | select | 待收集→待适配→适配中→已上线→已下线 |
| GitHub仓库 | url | 上线后填入 |
| 备注 | text | 适配说明 |

批量写入使用 `lark-cli base +record-batch-create`，格式为 `{"fields":[...],"rows":[[...],...]}`，每次最多 50 条。

### curl 不可靠

Overleaf 页面内容是动态加载的（JavaScript 渲染），**直接 curl HTML 结果不一致**（有时 9 个有时 0 个有时 102 个）。必须使用 WebBridge 提取。

## 与 TeXPage 流程对比

| | TeXPage | Overleaf |
|---|---------|----------|
| 获取源码 | 逐文件 evaluate `_texpage_editor.state.doc.toString()` | **一键 Download ZIP** |
| 速度 | 5-10 min | **30 sec** |
| 二进制文件 | 无法提取 | ✅ 全在 ZIP 里 |
| 稳定性 | 依赖 `_texpage_editor` 全局变量 | ✅ 标准浏览器下载 |
| 批量友好度 | 低 | **高** |

## Pitfalls

### 🔴 阻断级（模板不可上线）

- **专有/内部 .sty/.cls 文件**：部分 Overleaf 模板（如 SINTEF Presentation）依赖组织内部的主题文件，不公开分发。ZIP 下载不包含这些文件，GitHub/CTAN 也搜不到。**检测方法**：预检阶段查看模板描述是否含 "internal"、"contact ... for"、"proprietary" 等关键词。**处理**：直接跳过。
- **S3 源文件 403**：Overleaf 模板源文件存储在 `writelatex.s3.amazonaws.com/published_src/<id>/`，未经签名的 URL 返回 403。不能直接 curl 下载，必须走 WebBridge。

### 🟡 需适配（可修复）

- **minted 是高频问题**：Overleaf 支持 shell-escape，tectonic 不支持。所有 minted 引用必须注释。
- **biblatex style**：Overleaf 有完整 TeX Live，tectonic TL2023 缺少部分样式。优先改用 `numeric` 或 `ieee`。
- **HTML entities 污染**：View Source 提取的源码中 `&` 显示为 `&amp;`、`<` 为 `&lt;`。编译前需 `sed 's/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g'`。
- **Cookie banner 阻挡点击**：Overleaf 的 cookie 弹窗会阻止 "Open as Template" 按钮生效。必须先 dismiss（@e47 或 @e48）。
- **gh push 顺序**：`gh repo create --push` 需要已有 commit。先 `git commit`，再 `gh repo create --source . --push`。
- **异体字体**：部分模板使用 LobsterTwo、Raleway、Beuron 等 Google Fonts 字体。tectonic 自动下载 `.tfm`/`.vf`，但初次编译需额外 30-60s。
- **文件名可能不是 main.tex**：Overleaf 主文件常命名为 `template.tex`、`main.tex` 或项目名，需检查后重命名。
- **ZIP 结构**：Overleaf ZIP 解压后通常有一层 `template/` 包裹目录，文件在 `template/` 子目录下。
- **APA biblatex 样式不可用**：tectonic TL2023 中 `biblatex-apa` 不可用，报 `Style 'apa' not found`。改为 `style=numeric`。
- **纯英文模板零 CJK 依赖**：无 ctext、无 xeCJK、无 fontset。init.sh 用 `FONT_FILES=()`。

### 🟢 已验证可行的模板类型

| 类型 | 成功率 | 说明 |
|------|--------|------|
| 简单 CV/简历 | 95% | 单文件，零依赖 |
| 学术期刊（公开 .cls） | 80% | 需检查 biblatex/minted |
| 中文论文（ctex） | 70% | CJK 字体 Fandol 自动处理 |
| Beamer 演示 | 50% | 专有主题风险高 |
| 书籍模板 | 60% | 文件多，编译链复杂 |
- **WebBridge evaluate 响应格式**：返回值在 `data.value` 而非 `data.result`。JSON 解析时注意 proxy warning（`HTTPS_PROXY`）可能混入 stdout，需 strip 或 redirect stderr。
- **GitHub API 不稳定时用 SSH 直推**：`gh repo create` 依赖 REST/GraphQL API，API 不可用时改用 `git init && git remote add origin git@github.com:iftaken/<name>.git && git push --force`。前提是 repo 已存在。
- **飞书批量写入 proxy 干扰**：`lark-cli` 在 stdout 输出 proxy warning，与 JSON 结果混合。解析时先 `grep -v 'lark-cli.*WARN' | grep -v 'HTTPS_PROXY'` 或直接 `2>/dev/null`。

## 文件命名规范

| Overleaf 原始 | 心河Paper 标准 |
|---------------|---------------|
| `template.tex` / `main.tex` | `main.tex` |
| `ref.bib` / 任意名 | `references.bib` |
| `images/` / `figures/` | 保持原名 |
| `code/` | 保持原名 |

## 已验证模板

| 模板 | 仓库 | 分类 | 大小 | 备注 |
|------|------|------|------|------|
| UH ATMO Report | iftaken/uh-atmo-report | 报告 | 1.4MB | minted→注释，apa→numeric |
| Modern Simple CV | iftaken/overleaf-modern-cv | 简历 | 254KB | 异体字体自动下载 |
| 兰州大学本科论文 | iftaken/overleaf-lzu-thesis | 论文 | 501KB | 中文 ctex，Fandol 字体 |
| **SINTEF Presentation** | ❌ 跳过 | 演示 | - | 专有 beamertheme，不可获取 |
