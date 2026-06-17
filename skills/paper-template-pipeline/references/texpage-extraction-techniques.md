# TeXPage 源文件提取技术

约 60% 的 TeXPage 模板没有 GitHub 镜像，必须从 TeXPage 平台提取源文件。

## 核心约束

- **TeXPPage REST API 全部不可用**：测试了 8 个端点（`/api/project/download`、`/api/project/export`、`/api/project/files` 等），全部返回 404 或 1003(Not logged in)。`/api/project/files?projectKey=` 返回 200 但需 `versionNo` 参数且报 1004 权限不足。
- **必须用 WebBridge evaluate**：API 需要浏览器登录态，curl 全部返回 403/1003。
- **单个模板提取耗时 5-15 分钟**：取决于文件数量（3-10 个文件，每个需点击+等待+读取+保存）。

## 提取流程（已验证可行）

### 步骤 1：导航 + Open as Template

```bash
# 导航到模板页
curl ... navigate url=https://www.texpage.com/template/<exact-id> newTab=true

# 点击 Open as Template（用 evaluate 查找链接）
evaluate: (function(){var as=document.querySelectorAll("a");for(var i=0;i<as.length;i++){if(as[i].textContent.includes("Open as Template")){as[i].click();return "clicked"}};return "not found"})()
```

**⚠️ 模板 ID 必须精确**：错误的 ID（如最后一位不同）会静默重定向到 `/template` 列表页，不报错。飞书表格中的 URL 是权威来源。

### 步骤 2：读取当前文件内容

```bash
evaluate: window._texpage_editor.state.doc.toString()
```

- `_texpage_editor` 是 CodeMirror 6 全局变量，包含当前打开文件的完整内容
- 返回纯文本，不受虚拟视口限制
- 检查 `typeof window._texpage_editor !== "undefined"` 确认编辑器已加载

### 步骤 3：发现文件列表

**方法 A — DOM 文本扫描**（推荐，不需要 ARIA roles）：
```js
(function(){
  var all = document.querySelectorAll("*");
  var r = [];
  for(var i=0; i<all.length; i++){
    var t = all[i].textContent.trim();
    if(t.length<40 && t.length>2 && (t.endsWith(".tex")||t.endsWith(".cls")||t.endsWith(".sty")||t.endsWith(".bib")||t.endsWith(".bst")||t.endsWith(".cfg"))){
      r.push(t);
    }
  }
  return JSON.stringify([...new Set(r)]);
})()
```

**方法 B — snapshot 辅助**：`snapshot` 后查看 accessibility tree 中的 listitem/StaticText 节点，文件名常作为文件树的叶子节点出现。

### 步骤 4：切换到其他文件并读取

**⚠️ 关键：文件树节点结构** — TeXPage 文件树中，文件名渲染在 `<div class="file-name">` 内，但 **点击目标必须是最接近 `[class*=tree]` 的祖先 div**（如 `<div class="tree-node">`），直接点击 `file-name` 或其内部的 `<span>` 不会触发文件切换。

**推荐方法 — 通过 DOM 类名查找 file-name 后向上找到 tree-node 点击**（本文档已验证）：
```js
(function(){
  var divs = document.querySelectorAll(".file-name");
  for(var i = 0; i < divs.length; i++){
    if(divs[i].textContent.trim() === "EXACT_FILENAME"){
      // 往上找最近的 tree 容器节点，该节点才有 click handler
      var p = divs[i].closest("[class*=tree]") || divs[i].parentElement.parentElement || divs[i].parentElement;
      p.click();
      return "clicked " + p.tagName + "." + p.className;
    }
  }
  return "not found";
})()
```

**TreeWalker 点击法（不可靠，需配合 closest 回退）**：单纯的 `n.parentElement.click()` 点击的是 `<span>` 而非 `<div class="tree-node">`，**不生效**。必须用 `n.parentElement.closest("[class*=tree]")` 做回退链。

点击后 `sleep 2`，再读 `_texpage_editor.state.doc.toString()` 获取新文件内容。读取前可用 `(function(){var t=document.querySelectorAll("*");for(var i=0;i<t.length;i++){if(t[i].className.indexOf("active")!==-1&&t[i].textContent.length<40)return t[i].textContent.trim()};return"???"})()` 验证当前打开的文件是否已切换。

### 步骤 5：保存、适配、编译

将提取的文件保存到模板仓库，按标准流水线适配：
- 去除 `\usepackage[utf8]{inputenc}`（XeTeX 原生 UTF-8）
- 去除 `\usepackage[TS1,T1]{fontenc}`（XeTeX 不兼容）
- 去除 `\usepackage{newtxtext}`/`\usepackage{newtxmath}`（XeTeX 不兼容）
- 字体替换：Arial→Liberation Sans，Consolas→Liberation Mono，fontset=windows→fontset=fandol
- `\include`→`\input`（避免 BibTeX chapter aux 错误）
- EPS→PDF 转换
- 缺失图片注释掉（`photo.png` 等可选资源）

### Ant Design 文件树变体（ant-tree）

部分 TeXPage 项目使用 Ant Design Tree 组件（`.ant-tree`）渲染文件列表。**与标准 `.file-name` 类不同**：

- 文件名在 `.ant-tree-title` 内，但 **ant-tree-title 中的文本是文档大纲章节名**（如"绪论""标题""结论"），而非文件名
- 实际的文件名节点可能渲染在列表项的不同 DOM 层级
- 定位方法：用 `querySelectorAll('.ant-tree-node-content-wrapper')` 或扫描所有 `*` 元素的 `textContent` 匹配文件名后缀（`.tex`, `.cls`, `.bst`, `.bib`）

**已验证的 ant-tree 文件切换方法**：
```js
(function(){
  var all = document.querySelectorAll('*');
  for(var i=0;i<all.length;i++){
    var t = all[i].textContent.trim();
    if(t === 'thesis-cls-Miya.cls'){  // 精确匹配文件名
      all[i].click();
      return 'clicked';
    }
  }
  return 'not found';
})()
```

`click()` 后等 1-2 秒让编辑器切换，再用 `_texpage_editor.state.doc.toString()` 读取内容。读取前验证当前文件：检查 `state.doc.length`（不同文件应有不同长度）。

**注意**：`.ant-tree-title` 和 `.ant-tree-node-content-wrapper` 都包含**文档大纲**节点（如章节标题），文件名在独立的文件树节点中。直接匹配 `textContent === '完整文件名'` 是最可靠的方式。

### WebBridge evaluate JSON 转义技巧

当 evaluate 代码含特殊字符（引号、换行、正则等）时，curl 的 shell JSON 嵌套极易产生 `invalid JSON: unexpected EOF` 错误。**可靠模式**：

```bash
cat > /tmp/eval.js << 'JSEOF'
(function(){
  // 复杂 JS 代码，无需转义
  return "result";
})()
JSEOF
JSCODE=$(cat /tmp/eval.js | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d "{\"action\":\"evaluate\",\"args\":{\"code\":$JSCODE},\"session\":\"hermes\"}"
```

`python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))"` 将任意 JS 代码转为合法 JSON 字符串，避免手动转义。

## Chrome MV3 Service Worker 唤醒

长时间闲置后 `extension_connected: false`：
```bash
osascript -e 'tell application "Google Chrome" to set URL of active tab of front window to "chrome-extension://<id>/popup.html"'
sleep 2
```
唤醒后重新 `navigate` 回到任务页面（`find_tab` 可能失效，因为 active tab 被替换）。

## Tab 字符陷阱（高频，诊断陷阱）\n\n从 TeXPage 提取的源文件常含 tab 缩进。Tab 字符在 TeX 中有特殊含义：\n\n- **`\\t` 在括号内会触发 `\\csname` 解析**，导致 `Missing \\endcsname inserted` 错误\n- **错误行号指向的位置不一定是 tab 所在位置**——上下游的括号嵌套可能将 tab 影响传播到其他行\n- **诊断**：编译报 `Missing \\endcsname inserted` 但行内容看似正常时，用 `cat -A` 检查 Tab（显示为 `^I`）\n- **修复**：`sed 's/\\t/    /g'` 全局替换 tab 为空格\n\n### 高频子模式：注释含 tab 的行\n\n当需要注释掉一行（如 `\\includegraphics` 引用缺失图片），直接在该行前加 `%` 会导致：\n```\n\\t% \\includegraphics{...}  →  TeX 将 \\t 解释为 \\csname，报 Missing \\endcsname inserted\n```\n**修复**：先替换 tab 为空格，再加 `%`。或直接删除整行。\n\n## 二进制文件（PDF/PNG/JPG）处理\n\nTeXPage 模板中的二进制文件无法通过 `_texpage_editor` 提取。处理策略按文件类型分级：\n\n| 文件类型 | 策略 | 示例 |\n|----------|------|------|\n| 示例图片/图表（optional） | 注释掉 `\\includegraphics` 行，必要时注释整个 figure 环境 | 中学数学试卷的 `20.pdf` 题图、小论文的 `圖片的檔案名稱.png` |\n| 学校 logo/校徽（critical） | 从上游 GitHub 仓库补真实文件 | `images/header.pdf`、`bit_logo.png` |\n| 字体文件（.ttf/.otf） | 改用 COS 字体或 Docker 系统字体 | `STXIHEI.TTF`、`FZHTK.TTF` |\n\n**注释 figure 环境的可靠步骤**：\n1. `grep -n 'includegraphics' main.tex` 找到所有图片引用\n2. 判断是否需要保留（src 不存在 → 注释，src 存在但无法获取 → 注释）\n3. ⚠️ **先替换 tab 为空格**（`sed 's/\\t/    /g'`），再加 `%` 注释。否则 tab 前导的 `%` 触发 `Missing \\endcsname inserted`\n4. 若注释后仍报错（如图片在 enumerate 内部导致上下文断裂），直接删除整个图块\n\n## 文件树点击：`.tree-node` 直选法（推荐）\n\n较 `.file-name` + `closest()` 更简单可靠：\n\n```js\n// 直接匹配 tree-node 的 textContent\nfor(const n of document.querySelectorAll(\".tree-node\")) {\n    if(n.textContent.trim() === \"TARGET_FILENAME\") {\n        n.click();\n        break;\n    }\n}\n```\n\n点击后 `sleep 2`，用 `_texpage_editor.state.doc.toString().length` 验证文件已切换（不同文件应有不同长度）。\n\n## `click` 静默失败处理\n\n`click(\"@e7\")` 返回 `{ok:true, success:true}` 但页面未跳转时，直接重试：\n```bash\nsleep 2 && curl ... click @e7  # 重试，第二次通常成功\n```\n不检查 DOM 状态——直接重试比诊断更高效。\n\n## 商业字体替换映射

| 商业字体 | 系统替代 |
|----------|----------|
| HelveticaNeueLTPro | Liberation Sans |
| ProGB18030 | SimHei |
| Arial | Liberation Sans |
| Arial Black | Noto Sans CJK SC Black |
| Consolas | Liberation Mono |
| Courier New | Liberation Mono |
