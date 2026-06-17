---
name: agent-browser-profile
description: "Configure agent-browser to reuse Chrome Profile for bypassing social media anti-scraping. Use when Hermes browser tools are blocked by login walls or anti-bot pages."
version: "1.0"
---

# agent-browser Chrome Profile 复用

## 问题

Hermes 的 browser 工具（browser_navigate / browser_snapshot 等）底层由 agent-browser 驱动，默认跑无头 Chromium，无登录态。访问知乎、小红书、微博等社媒时会被反爬墙拦截（opacity:0.1 遮罩、要求登录）。

## 解决方案

让 agent-browser 复用你的真实 Chrome Profile，注入登录 cookie。

## 配置步骤

### 1. 确认 Chrome Profile 存在

```bash
ls ~/Library/Application\ Support/Google/Chrome/Default/Cookies
# 或
ls ~/Library/Application\ Support/Google/Chrome/Profile\ 1/Cookies
```

### 2. 设置环境变量

在 `~/.hermes/.env` 中添加：

```bash
AGENT_BROWSER_PROFILE=Default
```

如需使用其他 Profile（如 Profile 1），改 `Default` 为对应目录名。

### 3. 重启 Hermes

环境变量在进程启动时读取，必须重启。当前 session 无法热加载。

```bash
# 退出当前 session
/exit
# 重新启动
hermes
```

### 4. 验证

```bash
# 直接测试 agent-browser（不进 Hermes）
export AGENT_BROWSER_PROFILE=Default
npx agent-browser --profile Default open https://www.zhihu.com/hot
npx agent-browser snapshot -i
npx agent-browser close --all
```

看到登录态信息（私信数、通知数等）即成功。

## 原理

agent-browser 的 `--profile` 把 Chrome Profile 目录复制到临时目录（只读副本），浏览器启动时继承所有 cookie、localStorage、session。社媒平台看到的是已登录用户。

Hermes 不直接传 `--profile`，但 `browser_tool.py` 第 1855 行 `browser_env = {**os.environ}` 会把所有环境变量透传给 agent-browser CLI。

## 限制

1. **Profile 是只读副本** — 不回写真实 Chrome，操作不污染
2. **Chrome 运行时可能锁文件** — macOS 通常无问题，极端情况下先关 Chrome
3. **navigator.webdriver 仍为 true** — 对极端严格的反爬（金融网站等）可能不够
4. **需要重启 Hermes** — 环境变量在进程启动时读取，`/reset` 不会重载

## 相关

- agent-browser 官方文档: https://agent-browser.dev
- GitHub: vercel-labs/agent-browser
- Hermes browser 实现: `tools/browser_tool.py`
