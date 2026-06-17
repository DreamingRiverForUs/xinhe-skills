# 浏览器分发扩展开发

## 架构

内容分发通过 Plasmo 浏览器扩展实现，位于 `/Users/ming/project/content-distributor`。

```
src/
├── sidepanel.tsx          # 侧边栏 UI（含工厂拉取按钮）
├── background.ts          # Service Worker（分发调度 + 工厂回写）
├── contents/zhihu.ts      # 知乎 content script（Draft.js 注入）
├── platforms/             # 平台注册表（40+平台）
├── lib/factory-client.ts  # 工厂 API 客户端
└── lib/dom-utils.ts       # DOM 注入工具
```

## 开发流程

```bash
cd /Users/ming/project/content-distributor
npm run dev          # plasmo dev — 热更新，改代码自动重编译
npm run build        # 生产构建 → build/chrome-mv3-prod/
```

开发扩展加载路径：`build/chrome-mv3-dev/`（npm run dev 自动生成）

## Chrome 扩展加载

Chrome 不自动重载解压扩展的代码变更。必须：
1. `chrome://extensions` → 找到扩展 → 点 🔄
2. 或重启 Chrome（`--load-extension` 标志可能不生效于已有 profile）
3. 或扩展自身调用 `chrome.runtime.reload()`

## Chrome DevTools Protocol

需要 Chrome 以 `--remote-debugging-port=9222` 启动才能通过 CDP 自动化操作扩展。

## 内容注入：Draft.js 编辑器（知乎）

知乎专栏编辑器使用 Draft.js（React 管理的富文本）。从页面 JS 上下文无法可靠注入——Draft.js 只响应 React state 变化，不响应 DOM 操作。`document.execCommand`、`innerHTML`、`beforeInput` 事件均无效，发布按钮保持 `disabled: true`。

**正确方案**：通过扩展的 content script 注入。Content script 运行在隔离的 JS 世界，可以访问 React fiber 并触发正确的 onChange 事件。`src/contents/zhihu.ts` 已实现此逻辑。

切勿尝试用 WebBridge evaluate 直接操作 Draft.js 编辑器——已验证不可行。

## Content script 与 page context 通信

Content script 运行在隔离世界，无法设置 `window` 属性被页面读到。需通过 `document.createElement("script")` 注入 `<script>` 标签来向页面暴露变量。

页面 → content script 用 `window.postMessage`，content script 在 `window.addEventListener("message")` 中监听。

## 已知限制

- WebBridge 无法访问 `chrome-extension://` URL
- WebBridge evaluate 运行在页面上下文，无法访问 `chrome.runtime.*` API
- Chrome 扩展热更新：plasmo dev 只负责重编译，Chrome 需手动或 CDP 触发重载
