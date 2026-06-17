# TeXPage 平台操作细节

## 模板来源分布

实测统计：约 **60% 的 TeXPage 模板没有 GitHub 源仓库**，仅存在于 TeXPage 平台。
~35% 有 GitHub 源可直接 clone，~60% 需浏览器提取，~5% 需特殊处理（dtx/API故障）。

## 方式 A：有 GitHub 源（优先）

1. 从 TeXPage 模板页描述/作者信息中提取 GitHub URL
2. `gh repo clone <源仓库>` 获取源码
3. 走标准流水线

## 方式 B：无 GitHub 源（浏览器提取）

### B1：CodeMirror 逐文件读取（已验证可靠，但慢）✅

TeXPage 编辑器使用 CodeMirror 6。通过 `_texpage_editor` 全局变量直接读取当前打开文件的完整内容（不受虚拟视口限制）：

```js
// 获取当前编辑器文件内容
window._texpage_editor.state.doc.toString()
```

**逐文件提取工作流**（每模板 6-10 个文件，耗时 10-20 分钟）：

```js
// 1. 点击文件树中的文件（通过 TreeWalker 找文本节点）：
(function(){
  var w = document.createTreeWalker(document.body, 4); // NodeFilter.SHOW_TEXT
  var n;
  while(n = w.nextNode()) {
    if(n.textContent.trim() === 'SGUTthesis.cls') {
      n.parentElement.click();
      return 'clicked';
    }
  }
  return 'not found';
})()

// 2. 等待 CodeMirror 渲染（sleep 2s）
// 3. 读取内容：
window._texpage_editor.state.doc.toString()
```

**关键发现**：`_texpage_editor` 是 TeXPage 内部 CodeMirror 编辑器实例，稳定存在。`state.doc.toString()` 返回完整文档文本，不受虚拟视口限制。

### B2：文件列表 API（需要 versionNo，权限受限）

```js
// /api/project/files?projectKey=... 返回 200 但需要 versionNo 参数
// /api/project/files?projectKey=...&versionNo=0 → 1004 权限不足
// 说明：Template "Open as Template" 创建的项目副本权限受限
fetch('/api/project/files?projectKey=' + projectKey + '&versionNo=0')
```

### B3：ZIP 下载 API（当前不可用）⚠️

```js
// 已验证全部返回 404 的端点（本会话测试 8 个变体）:
// /api/project/download → 404
// /api/project/export → 404
// /api/project/file/zip → 404
// /api/template/download/<id> → 404
// /api/project/<key>/download → 404
// /api/project/<key>/export → 404
// /api/v1/project/download → 404
// /api/v1/project/export → 404
```

TeXPage 可能已下线或重构了 ZIP 下载端点。B1 逐文件读取是当前唯一可靠路径。

## 单文件模板快速提取

部分模板（Beamer 主题、单文件文章模板）仅含一个 `main.tex` 文件，无需逐文件点击。`

1. Open as Template → 等待编辑器加载
2. 一次 evaluate 直接获取：`window._texpage_editor.state.doc.toString()`
3. 文件树的 "Frame" / "Section" 等节点是文档大纲（非实际文件），可忽略

耗时：< 1 分钟（vs 多文件模板 10-20 分钟）。

**已确认单文件模板**：Monograph Beamer Theme（TeXPage f3b03e3e-2fde-4dbb-8abc-fd5879ebee57）。

## 提取失败处理

| 现象 | 原因 | 解决 |
|------|------|------|
| `.cm-line` scroll-read 重复 | 虚拟视口只渲染可见行 | 用 `state.doc.toString()` |
| Chrome MV3 扩展断开 | Service Worker 超时休眠 | `osascript` 唤醒 + navigate 恢复 |
| TeXPage API 403/1003 | ESA WAF / 未登录 | 必须浏览器操作，CLI curl 无效 |
| ZIP 下载超时 | 含字体文件（28MB+） | 超时 ≥ 120s，或跳过字体用 B2 |

## 占位先行策略（浏览器不可用时的降级）

1. 创建 repo + AGENTS.md / .gitignore / init.sh / references.bib
2. 占位 main.tex（`\documentclass{ctexart}` + 提取说明）
3. Docker 编译 → 推送 → 飞书标注"待浏览器提取"
