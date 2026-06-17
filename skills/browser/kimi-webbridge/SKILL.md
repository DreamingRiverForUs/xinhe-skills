---
name: kimi-webbridge
description: Control the user's real browser (Chrome/Edge) via Kimi WebBridge daemon at localhost:10086. Navigate, click, type, read, screenshot, and interact with any website using the user's actual login sessions. Use when the user asks to open URLs, browse websites, fill forms, take screenshots, scrape web content, or automate any browser task.
version: 1.0.0
author: moonshot (adapted for Hermes)
platforms: [macos, linux, windows]
prerequisites:
  commands: [curl, jq]
metadata:
  hermes:
    tags: [browser, web, automation, webbridge, kimi]
    requires_toolsets: [terminal, vision]
---

# Kimi WebBridge

> **User preference:** Always prefer Kimi WebBridge over Hermes' built-in `browser` toolset.
> WebBridge operates the user's real Chrome browser with their login sessions,
> requires no API key, and is the first-choice tool for all browser tasks.
# Kimi WebBridge

**PRIORITY RULE: Use Kimi WebBridge for ALL browser operations. Never use the built-in Hermes browser toolset. WebBridge preserves the user's real Chrome login sessions and requires no additional API keys.**

Control the user's real browser via a local daemon at `http://127.0.0.1:10086`. All calls use `terminal()` with curl.

## Health Check (always first)

```bash
~/.kimi-webbridge/bin/kimi-webbridge status
```

If `running: true` and `extension_connected: true` → proceed. Otherwise see Troubleshooting section.

## API Reference

All calls use `curl -s -X POST http://127.0.0.1:10086/command -H 'Content-Type: application/json' -d 'JSON_BODY'`.

### navigate — Open a URL

```
-d '{"action":"navigate","args":{"url":"https://example.com","newTab":true},"session":"hermes"}'
```

Always use `newTab:true` on first call. `group_title` sets the tab group label (optional).

### find_tab — Reuse an already-open tab

```
-d '{"action":"find_tab","args":{"url":"https://kimi.com","active":true},"session":"hermes"}'
```

`active:true` picks the tab the user is currently viewing. Without it, returns the leftmost matching tab by domain.
If returns "no open tab found", fall back to `navigate` with `newTab:true`.

### snapshot — Read page content (accessibility tree)

```
-d '{"action":"snapshot","args":{},"session":"hermes"}'
```

Returns `{url, title, tree}` with `@e` refs for interactive elements. Use `@e` refs for click/fill — they survive CSS changes.

### click — Click an element

```
-d '{"action":"click","args":{"selector":"@e123"},"session":"hermes"}'
```

Selector can be `@e` ref (preferred) or CSS selector. Uses `el.click()`.

### fill — Type into input/contenteditable

```
-d '{"action":"fill","args":{"selector":"@e456","value":"hello world"},"session":"hermes"}'
```

Works on `<input>`, `<textarea>`, and `[contenteditable]` (ProseMirror/TipTap/Lexical etc.).
`fill` is **clear-and-insert** — existing content is replaced.

### evaluate — Run JavaScript

```
-d '{"action":"evaluate","args":{"code":"document.title"},"session":"hermes"}'
```

Supports async/await. Use compact `JSON.stringify(data)` — never format with spaces.

### screenshot — Capture page

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"screenshot","args":{},"session":"hermes"}'
```

Returns `{ok: true, data: {format, path, sizeBytes, mimeType}}`. The `path` field is a temp file on disk (e.g. `/var/folders/.../kimi-webbridge-screenshots/screenshot_<timestamp>.png`).

**Extract the path**:
```bash
curl ... | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['path'])"
```

**View** with `vision_analyze(image_url=PATH)`. For non-vision models (deepseek), fall back to `snapshot` — the accessibility tree captures all visible text and data.

**Batch capture** — run `screenshot` calls sequentially per session name. Each call generates a new timestamped file. Collect paths via Python one-liner and analyze in order.

### network — Monitor network requests

```
# Start monitoring
-d '{"action":"network","args":{"cmd":"start"},"session":"hermes"}'

# List requests
-d '{"action":"network","args":{"cmd":"list"},"session":"hermes"}'

# Get request detail
-d '{"action":"network","args":{"cmd":"detail","requestId":"123"},"session":"hermes"}'

# Stop monitoring
-d '{"action":"network","args":{"cmd":"stop"},"session":"hermes"}'
```

### upload — Upload files

```
-d '{"action":"upload","args":{"selector":"@e789","files":["/path/to/file.pdf"]},"session":"hermes"}'
```

### save_as_pdf — Save page as PDF

```
-d '{"action":"save_as_pdf","args":{},"session":"hermes"}'
```

Optional args: `paper_format` (letter/a4/legal), `landscape` (bool), `scale` (0.1-2.0), `print_background` (bool), `file_name`. Saves to `/tmp/kimi-webbridge-pdfs/`.

### list_tabs — List open tabs

```
-d '{"action":"list_tabs","args":{},"session":"hermes"}'
```

### close_tab — Close current tab

```
-d '{"action":"close_tab","args":{},"session":"hermes"}'
```

### close_session — Close all tabs in session

```
-d '{"action":"close_session","args":{},"session":"hermes"}'
```

Always call `close_session` at task end.

## Sessions

Each session maps to a separate browser tab group. Use `"session":"hermes"` as default. For parallel tasks, use distinct names (e.g., `"hermes-github"`, `"hermes-twitter"`).

## Workflow

1. **Health check** — `~/.kimi-webbridge/bin/kimi-webbridge status`
2. **Navigate** — `navigate` with `newTab:true`
3. **Read** — `snapshot` to get page content and `@e` refs
4. **Interact** — `click`, `fill`, `evaluate` using `@e` refs
5. **Screenshot** — use screenshot API, extract path, then `vision_analyze` (or fall back to `snapshot` for non-vision models)
6. **Cleanup** — `close_session` when done

## Best Practices

- **Prefer snapshot over CSS selectors** — `@e` refs survive DOM changes
- **Use screenshot API, extract path** — response gives a temp file path, not inline base64. Use `vision_analyze` on the path, or fall back to `snapshot` for non-vision models.
- **Compact JSON.stringify** — never `null, 2` formatting in evaluate
- **IIFE for evaluate** — wrap in `(() => { ... })()` to avoid redeclaration errors
- **fill replaces content** — to append, read current value, concatenate, then fill

### CRITICAL: Session isolation for parallel tasks

**Every independent browser task MUST use its own session name.** Sessions are separate tab groups — navigating in one session does NOT interfere with another. Without distinct sessions, tabs from different tasks collide and snapshots return the wrong page.

```
# WRONG — both tasks share tabs, chaos ensues
{"action":"navigate","args":{"url":"https://google.com"},"session":"hermes"}
{"action":"navigate","args":{"url":"https://reddit.com"},"session":"hermes"}

# RIGHT — each task has its own tab group
{"action":"navigate","args":{"url":"https://google.com/search?q=AI+discord"},"session":"ai-discord"}
{"action":"navigate","args":{"url":"https://google.com/search?q=AI+reddit"},"session":"ai-reddit"}
```

Use descriptive session names: `ai-discord`, `ai-reddit`, `search-1`, `search-2`. Close them all at the end with `close_session`. Do NOT reuse the default `"hermes"` session for multi-step research — it likely has stale tabs from prior tasks.

### Pitfall: evaluate silently returns empty with wrong parameter name

The `evaluate` API uses `args.code`, NOT `expression` or `script`:

```
# WRONG — silently returns empty result
{"action":"evaluate","expression":"document.title","session":"x"}

# RIGHT
{"action":"evaluate","args":{"code":"document.title"},"session":"x"}
```

Similarly, `navigate` uses `args.url`, not top-level `url`. All WebBridge actions take parameters inside an `args` object.

## Platform-Specific Patterns

See `references/react-controlled-input-workaround.md` for filling React controlled-input forms — required when `fill` and `element.value = x` both fail to update React state.

See `references/feishu.md` for Feishu (飞书/Lark) web client interaction patterns — chat navigation, message sending, and image upload.

See `references/snapshot-data-extraction.md` for Python one-liner recipes to extract tables, charts, and text from `snapshot` accessibility trees — useful for data-heavy admin dashboards when `vision_analyze` is unavailable.

See `references/bilibili-video-extraction.md` for extracting content from B站/Chinese video platforms when subtitles aren't available — multi-source fallback pattern (description → Google summaries → YouTube mirror).

See `references/testing-content-scripts.md` for testing Chrome extension content scripts against real platform pages via WebBridge `evaluate` — probe DOM, test injection, fix selectors before deploying.

See `references/xinhe-paper-admin-dashboard.md` for the 心河Paper local admin dashboard (192.168.31.32:6796) — page map, data schema, and extraction patterns.

See `references/xinhe-paper-bulk-import.md` for automating 心河Paper template imports — React native setter pattern, form submission flow, and database verification.

See `references/cross-platform-competitive-analysis.md` for cross-platform competitive intelligence — search the same keyword across Douyin/XHS/Bilibili/Zhihu simultaneously, compare result relevance/volume/engagement to diagnose platform-level suppression vs. content quality issues.

See `references/spa-pagination-scraping.md` for scraping JS-rendered SPAs that block curl — combined evaluate+click pagination pattern, escaping pitfalls, and tool-call-limit survival.

See `references/job-board-scraping.md` for scraping job listing SPAs (mokahr.com, etc.) where JDs are inlined in `<a>` element `textContent` — `evaluate` + `textContent` extraction beats `snapshot` for speed and avoids truncation.

See `references/browser-research-pattern.md` for researching and compiling information sources (X accounts, subreddits, Discord servers) via browser — Google→Reddit pattern, blog listicle dead-link avoidance, and Disboard Cloudflare workaround.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `command not found` | Run install script |
| `running: false` | `~/.kimi-webbridge/bin/kimi-webbridge start` |
| `extension_connected: false` | Open browser, ensure extension is installed from https://kimi.com/features/webbridge |
| `address already in use` | `~/.kimi-webbridge/bin/kimi-webbridge stop && ~/.kimi-webbridge/bin/kimi-webbridge start` |
| Tool calls timeout | Check logs: `~/.kimi-webbridge/bin/kimi-webbridge logs -n 100` |
| Extension version mismatch | Update extension from https://kimi.com/features/webbridge |
| Extension installed but `extension_connected: false` persistently | Chrome MV3 may have terminated the extension's service worker. Wake it: `osascript -e 'tell application "Google Chrome" to set URL of active tab of front window to "chrome-extension://fldmhceldgbpfpkbgopacenieobmligc/popup.html"'` then recheck status. The extension ID is in the user's `~/Library/Application Support/Google/Chrome/Default/Extensions/` — find the `Kimi WebBridge` manifest to confirm. **After wakeup**: use `navigate` (not `find_tab`) with the full task URL and `newTab:false` to return to your page — the osascript call replaces the active tab, so `find_tab` on the original domain will say \"no open tab found\". |

- **React controlled inputs: direct `.value =` + events is NOT enough** — Many React/Next.js SPAs (shadcn/ui, Ant Design, 心河Paper) use controlled components that track value through React's fiber, not the DOM. (See `references/react-controlled-input-workaround.md` for native setter pattern.)
- **SPA innerText 为空 (PITFALL)** — 部分 SPA 平台（微信视频号助手 channels.weixin.qq.com、抖音创作者中心）的 `document.body.innerText` 返回空字符串。这些平台使用 Shadow DOM 或 React 虚拟滚动，文本内容不暴露在 innerText 中。唯一可靠的读取方式是通过 `snapshot` 读 accessibility tree。不要浪费时间尝试 `evaluate` + `querySelectorAll` 或 `innerText` 遍历——如果 `evaluate: document.body.innerText` 返回空，立即切换到 `snapshot` 方案。
- **React controlled inputs: direct `.value =` + events is NOT enough** — Many React/Next.js SPAs (shadcn/ui, Ant Design, 心河Paper) use controlled components that track value through React's fiber, not the DOM. (See `references/react-controlled-input-workaround.md` for native setter pattern.)
- **SPA innerText 为空 (PITFALL)** — 部分 SPA 平台（微信视频号助手 channels.weixin.qq.com、抖音创作者中心）的 `document.body.innerText` 返回空字符串。这些平台使用 Shadow DOM 或 React 虚拟滚动，文本内容不暴露在 innerText 中。唯一可靠的读取方式是通过 `snapshot` 读 accessibility tree。
- **WebBridge `network` command may not capture fetch/XHR in React SPAs**
  1. **Click the calendar icon** to open the panel, then click date cells in the popup.
  2. **Use the component's built-in shortcuts** (e.g., 近7天/近30天 radio buttons) instead of manually setting dates.
  3. **Try `evaluate` to trigger React internals** — look for `__vueParentComponent` or `__reactFiber` on the input, then call the component's `onChange` handler directly with a dayjs/moment value. This is fragile and version-dependent.
  4. **If the page has pagination, use it** — broader date ranges may not be needed if you can page through results.

- **Custom-rendered list items (SPA chat apps, virtual scroll)** — `snapshot()` may return no `@e` refs for clickable items in frameworks like React/Vue that render `<div>` trees without ARIA roles (e.g. Feishu, Lark, Slack web). Workaround: use `evaluate` with a `TreeWalker` to find text nodes, then click their closest interactive ancestor:
  ```js
  (() => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) { if (n.textContent.includes("target name")) { let el = n.parentElement; while (el && el !== document.body) { if (el.onclick || el.tagName === "A" || el.getAttribute("role") === "button") { el.click(); return "ok"; } el = el.parentElement; } n.parentElement.click(); return "clicked fallback"; } } return "not found"; })()
  ```
