# 心河Paper WebBridge 模板导入流程

通过 Kimi WebBridge 在 paper.huimengxinhe.com 上批量导入模板的完整操作序列。

## 前置条件

- WebBridge 已连接（`kimi-webbridge status` 确认 `extension_connected: true`）
- 用户已在 paper.huimengxinhe.com 登录

## 完整流程

### 1. 导航到写作页面

```
navigate → https://paper.huimengxinhe.com/writing/new
```

### 2. 切换到「我的模板」tab

```js
// evaluate
[...document.querySelectorAll("button")].find(b=>b.textContent.trim()==="我的模板")?.click()
```

### 3. 点击「新增模板」

```js
[...document.querySelectorAll("button")].find(b=>b.textContent.trim()==="新增模板")?.click()
```

### 4. 点击「GitHub/Gitee 导入」

页面会刷新，显示"返回"和导入选项。

```js
[...document.querySelectorAll("button")].find(b=>b.textContent.includes("GitHub"))?.click()
```

### 5. 填写导入表单

表单有 6 个字段（按 DOM 顺序）：

| 索引 | 类型 | placeholder | 含义 |
|------|------|-------------|------|
| 0 | input | `https://github.com/username/thesis-template` | GitHub 仓库 URL |
| 1 | input | `main` | 分支名 |
| 2 | input | `templates/my-template` | 子目录 |
| 3 | input | `例如：心河大学本科毕业论文模板` | 模板名称 |
| 4 | textarea | `描述这个模板的特点、适用范围...` | 描述 |
| 5 | input | `添加标签，按回车确认` | 标签（逗号分隔） |

**填写方法**：

input 字段用 WebBridge `fill` + CSS 选择器（推荐，因为 fill 会触发 React onChange）：

```bash
# GitHub URL
-d '{"action":"fill","args":{"selector":"input[placeholder*=\"github.com/username\"]","value":"https://github.com/iftaken/repo-name"},"session":"hermes"}'
# 分支
-d '{"action":"fill","args":{"selector":"input[placeholder=\"main\"]","value":"main"},"session":"hermes"}'
# 子目录
-d '{"action":"fill","args":{"selector":"input[placeholder*=\"templates/my-template\"]","value":"."},"session":"hermes"}'
# 模板名称
-d '{"action":"fill","args":{"selector":"input[placeholder*=\"心河大学\"]","value":"模板显示名称"},"session":"hermes"}'
# 标签
-d '{"action":"fill","args":{"selector":"input[placeholder*=\"添加标签\"]","value":"标签1,标签2"},"session":"hermes"}'
```

**textarea 字段**必须用 evaluate（fill 对 textarea 失败）：

```js
var ta=document.querySelector("textarea");
ta.value="模板描述文字";
ta.dispatchEvent(new Event("input",{bubbles:true}));
ta.dispatchEvent(new Event("change",{bubbles:true}));
```

### 6. 添加标签

标签填入后需点击「添加」按钮确认（否则表单验证不通过）：

```bash
# 点击「添加」按钮
-d '{"action":"click","args":{"selector":"@eNN"},"session":"hermes"}'
```

先用 snapshot 获取当前 ref。

### 7. 点击「确认导入」

先用 snapshot 获取「确认导入」按钮的最新 ref，然后 click：

```bash
-d '{"action":"click","args":{"selector":"@eNN"},"session":"hermes"}'
```

### 8. 验证是否成功

```js
// evaluate: 检查页面是否出现模板名
document.body.textContent.includes("模板显示名称")
```

成功后模板出现在「我的模板」列表中。

## 后续步骤（需要进一步自动化）

1. **分享到模板市场**：在「我的模板」中找到模板卡片，点击「分享」按钮
2. **管理员审核**：管理员在后台审核通过后，模板出现在「模板市场」

## Pitfalls

- **React 表单状态不同步**：用 JS `inp.value = "xxx"` 设置值后，必须 dispatch `input` 和 `change` 事件，否则 React 组件不感知变化
- **textarea fill 失败**：WebBridge 的 `fill` 对 `<textarea>` 返回 false。回退到 evaluate + dispatchEvent
- **标签必须点「添加」**：填入标签文本后不点添加，表单验证会阻止提交
- **确认导入可能无反馈**：成功/失败都不会弹 toast，通过检查页面内容确认
- **network 监控不到 fetch**：WebBridge network 工具可能不捕获 SPA 的 fetch 调用，不要依赖它来验证 API 调用
- **模板名称唯一性**：重复导入同名模板可能报错，需要先去重检查
