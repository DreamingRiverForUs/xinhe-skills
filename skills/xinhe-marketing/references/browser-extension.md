# 浏览器扩展开发与调试

## 项目结构

```
/Users/ming/project/content-distributor/
├── src/                    # 源代码（Plasmo 框架）
│   ├── sidepanel.tsx       # 侧边栏 UI（含🏭工厂按钮）
│   ├── background.ts       # Service Worker（分发调度+回写工厂）
│   ├── contents/zhihu.ts   # 知乎专栏 Draft.js 注入器
│   ├── lib/factory-client.ts # 工厂 API 客户端
│   └── platforms/          # 平台注册表（40+平台）
├── build/chrome-mv3-dev/   # dev 构建（热更新）
├── build/chrome-mv3-prod/  # prod 构建
├── extension/              # 原始爱贝壳完整版（19平台，备份）
└── extension.bak/          # extension/ 备份
```

## 开发流程

```bash
cd /Users/ming/project/content-distributor

# 开发模式（热更新，加载 build/chrome-mv3-dev/）
npm run dev

# 生产构建
npm run build     # → build/chrome-mv3-prod/
```

在 Chrome 中加载：`chrome://extensions` → 「加载已解压的扩展程序」→ 选 `build/chrome-mv3-dev/`

## 知乎专栏注入原理

知乎编辑器是 React + Draft.js。页面 JavaScript 上下文（WebBridge evaluate）无法可靠注入内容，因为 Draft.js 用 React 内部状态管理，直接设置 innerHTML 不会触发 onChange。

**正确方式**：扩展的 content script（`src/contents/zhihu.ts`）运行在隔离世界中，使用以下事件序列：

1. 标题：native `HTMLTextAreaElement.prototype.value` setter + `input` + `change` events
2. 正文：`.public-DraftEditor-content` 设置 innerHTML + `input` + `change` + `blur` events（500ms延迟触发 blur 让 Draft.js 保存状态）

## 工厂集成架构

```
sidepanel.tsx                    background.ts                  zhihu.ts
┌──────────────┐   message    ┌──────────────┐   new tab    ┌──────────────┐
│ 🏭 工厂按钮   │ ──────────→ │ distribute() │ ───────────→ │ injectZhihu()│
│ 拉文章列表    │              │ injectToPlat │              │ Draft.js注入 │
│ 填编辑区      │              │ recordPub()  │              └──────────────┘
└──────────────┘              └──────────────┘
                                    │
                                    ▼ POST /api/v1/publications
                               ┌──────────────┐
                               │ 心河内容工厂   │
                               └──────────────┘
```

## 当前状态

- ✅ `factory-client.ts` — 拉文章/图文、回写发布记录
- ✅ `sidepanel.tsx` — 🏭工厂按钮 + 文章列表 + 加载填充
- ✅ `background.ts` — 分发后自动回写工厂 `publications`
- ⚠️ 端到端测试 — 需在 Chrome 加载 dev 扩展后验证
- ❌ 自动点发布按钮 — 未实现（需在注入成功后 click 发布按钮）

## Pitfall: Draft.js 注入

**绝对不要在 WebBridge evaluate 中尝试注入 Draft.js/React 富文本编辑器！** 这是已验证的死胡同。以下方法全部失败：
- `el.innerHTML = content` → Draft.js 不感知，发布按钮保持 disabled
- `new ClipboardEvent('paste', {clipboardData: dt})` → event 到达但 React state 不更新
- `new InputEvent('beforeinput', {data: 'x'})` → 同上
- `document.execCommand('insertText', ...)` → 同上
- React fiber `__reactFiber` + `memoizedProps.onChange()` → 需要完整的 Draft.js EditorState 对象

**唯一有效路径**：扩展的 content script（`zhihu.ts`）。它在隔离世界中运行，能正确触发 React 的事件处理。
