# SPA 平台数据提取技术手册

记录各平台创作者中心的数据提取方法、已踩过的坑、已验证可用的技术。

## 核心原则

1. **SPA 页面不能用 `body.innerText`** — 抖音/小红书/视频号/知乎创作者中心都是 React 渲染，`body.innerText` 返回空字符串
2. **`querySelectorAll` 拿不到 React Router 链接** — 链接是 `<Link>` 组件渲染的，不是真实 `<a href>`
3. **`window.scrollTo()` 无法触发懒加载** — 虚拟滚动组件监听的是真实滚轮事件，不是 scrollTop 变化
4. **Snapshot 的 accessibility tree 是最可靠的提取源** — 能看到所有已渲染的文本，但需要逐平台定制解析逻辑
5. **绝不编造数据** — URL、播放量、粉丝数必须从浏览器实际提取。如果提取失败，字段留空并标记，不要填假值

## 已测试的无效方法

| 方法 | 结果 | 说明 |
|------|------|------|
| `document.body.innerText` | 空字符串 | React SPA 的 innerText 不包含动态渲染内容 |
| `querySelectorAll('a[href*="/p/"]')` | 空/语法错误 | CSS `*=` 选择器里 `/` 需转义，且 React Router 链接不是标准 `<a>` |
| `window.scrollTo(0, scrollHeight)` | 不触发加载 | 虚拟滚动组件监听滚轮事件，不监听 scrollTop |
| `element.scrollTop = element.scrollHeight` | 同上 | 同上 |
| Python subprocess + WebBridge | 部分可用 | WebBridge 连接正常但 snapshot 解析需定制正则 |

## CSS Module 陷阱（跨平台通用，2026.6.16 发现）

各平台创作者中心大量使用 CSS Modules（hashed class names），导致两个问题：

1. **Snapshot 看不到 hashed div 的值**：`<div class="metric-value-k4R5P_">3061</div>` 中的 "3061" 不出现在 accessibility tree 里，snapshot 提取不到统计数字
2. **但 evaluate 可以查询**：用 `querySelectorAll("[class*=metric-value]")` 做子串匹配可以找到这些元素

**平台对照**：
| 平台 | hashed class 模式 | evaluate 选择器 |
|------|------------------|----------------|
| 抖音 | `metric-container-Rc61p9`, `metric-value-k4R5P_`, `metric-label-AX_5OF` | `[class*=metric-container]`, `[class*=metric-value]`, `[class*=metric-label]` |
| 小红书 | 未验证 | 推测类似模式 |
| B站 | 未验证 | 推测类似模式 |

**修复方案**：遇到 snapshot 缺数字的情况 → 用 evaluate + `[class*=keyword]` 子串选择器直接从 DOM 取值。不要只依赖 snapshot。

## 有效的滚动加载方法

- **抖音内容管理页**：`window.scrollBy(0, 800)` 循环，每次间隔 1-1.5 秒，8-10 次可加载全部
- **判断加载完成**：页面顶部显示「共 N 个作品」，对比已提取的日期数量 vs N
- **视频号/小红书/B站**：`window.scrollBy()` 对虚拟滚动无效，需要 `dispatchEvent(new WheelEvent('wheel', {deltaY: 500}))` 或点击翻页按钮（待验证）

## 各平台提取方法

### 知乎 (zhihu.com/creator)

**URL 提取**: ✅ 可用
```js
// evaluate - 遍历所有 <a> 标签
var links = document.querySelectorAll('a');
for (var i = 0; i < links.length; i++) {
    if (links[i].href.indexOf('zhuanlan.zhihu.com/p/') > -1) {
        // 提取成功
    }
}
```

**单作品数据**: ✅ 首页「最新创作」区域显示阅读/赞同/评论/收藏
- 数据来自 `snapshot` 的 accessibility tree
- 只显示最近一篇，更多在「内容管理」页面（但该页 URL 返回 404）

**翻页**: ❌ 创作者首页只显示最新1条，内容管理页 404

### B站 (member.bilibili.com)

**URL 提取**: ✅ 可用
```js
var links = document.querySelectorAll('a');
// 筛选 href 含 bilibili.com/video/BV 的
// BV 号可直接构建 URL: https://www.bilibili.com/video/BVxxx
```

**单作品数据**: ⚠️ 内容管理页的正文不暴露在 innerText 中
- 首页显示的是频道级聚合数据，不能用作单作品数据
- 通过 snapshot 可提取作品标题和 BV 号，但单条播放量需进入「数据中心」

**翻页**: ❌ 未找到有效的分页机制

### 抖音 (creator.douyin.com)

**URL 提取**: ❌ SPA，无法通过 evaluate 直接获取
- 链接不是 `<a href>` 渲染的
- 需 snapshot → 找到视频卡片 → click → 等详情页加载 → 获取 `window.location.href`

**单作品数据**: ✅ 内容管理页可通过 evaluate 直接提取 per-video stats（2026.6.16 突破）
- **关键发现**：内容管理页的每作品统计数字在 CSS-module-hashed div 里（如 `<div class="metric-value-k4R5P_">3061</div>`），snapshot 的 accessibility tree 看不到这些值！必须用 evaluate 查询 DOM。
- **提取代码**（已验证可用，36/64 条提取成功）：
  ```js
  var containers = document.querySelectorAll("[class*=metric-container]");
  containers.forEach(function(c) {
      var stats = {};
      c.querySelectorAll("[class*=metric-item]").forEach(function(mi) {
          var label = mi.querySelector("[class*=metric-label]");
          var val = mi.querySelector("[class*=metric-value]");
          if (label && val) {
              stats[label.textContent.trim()] = parseInt(val.textContent.replace(/[^0-9]/g, '')) || 0;
          }
      });
      // stats = {播放: 3065, 点赞: 21, 评论: 2, 分享: 2}
  });
  ```
- **为什么是36/64？** 剩余28条是图文（image_text）类型，metrics 结构不同（含「收藏」「文案展开率」「平均浏览图片」而非标准 播放/点赞/评论/分享 四件套）
- **snapshot 补充**：用 snapshot 可提取全部 64 条的标题、发布日期（`2026年06月12日 21:31`）、时长（`01:47`）、状态（已发布/审核中/未通过）

**翻页/滚动**: ✅ `window.scrollBy(0, 800)` 循环可触发懒加载
- 第一屏显示约12条，滚动8次后全部64条加载完毕
- 「共 64 个作品」提示在页面顶部可见

### 小红书 (creator.xiaohongshu.com)

**URL 提取**: ❌ SPA，同抖音
- 笔记链接格式：`https://www.xiaohongshu.com/explore/{note_id}`
- 需 snapshot → click → 获取 URL

**单作品数据**: ⚠️ 笔记管理页内容为空（evaluate 和 innerText 均无数据）
- 首页「最新笔记」区域有单条数据（观看/点赞/收藏/评论）
- 笔记管理页（`/new/manage/notes`）加载了页面框架但列表内容不暴露

**翻页**: ❌ 未找到有效的翻页方法

### 视频号 (channels.weixin.qq.com)

**URL 提取**: ❌ 视频号不提供公网分享链接
- 视频号内容只能在微信生态内查看
- 所有链接都是 `javascript:;`（React Router）

**单作品数据**: ✅ 首页视频列表有完整数据
- 每条视频显示：标题（含 #标签）+ 播放 + 点赞 + 评论 + 分享 + 收藏
- 快照中可通过 regex 提取：日期 → 标题 → 连续5个数字
- 问题：只渲染可见区域的约5条（虚拟滚动），43条中的其余38条不可见

**翻页**: ❌ `scrollTo` 无效，`全部视频` 链接是 `javascript:;`

### CSDN (mp.csdn.net)

**URL 提取**: ✅ 完全可用
- 标准 `<a>` 标签，href 含 `blog.csdn.net` + `article/details`
- 文章列表页直接显示阅读/点赞/评论/收藏

**翻页**: ✅ 文章管理页显示全部已发布文章（当前2篇）

## 已验证的 snapshot 提取模式

```python
import re

# 通用：提取所有文本节点
all_text = re.findall(r"name': '([^']{15,200})'", tree_str)

# 去除转义
clean = text.replace('\\n', ' ').strip()

# 关键词过滤（各平台不同）
keywords = ['数模', '建模', 'Vibe', 'Paper', '心河', '教程', '亚太', '中青']

# 去重（用前50字符做 key）
if clean[:50] not in seen:
    seen.add(clean[:50])
    works.append(clean)

# 提取数字（播放量等）
nums = re.findall(r"name': '(\d[\d,]*)'", context)
```

## 建议的长期方案

1. **定时批量采集**：每天 8:00 cron 自动运行（已创建 job 56c769c9354c）
2. **逐步积累**：每天采集新出现的作品，metrics 每天追加
3. **URL 补全**：对 SPA 平台，分批手动 click → 获取 URL → 回填
4. **翻页突破**：研究各平台的虚拟滚动容器，使用 `dispatchEvent(new WheelEvent(...))` 模拟滚轮事件
