# B站内容采集器

从 `https://member.bilibili.com/platform/upload-manager/article` 采集全部视频作品。

## 核心原理

B站创作中心使用标准翻页（非虚拟滚动），每页10条，`article-card` DOM结构清晰稳定。

## 提取方法

### 步骤1：导航到视频管理页

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://member.bilibili.com/platform/upload-manager/article","newTab":true},"session":"bilibili"}'
sleep 5
```

**⚠️ 关键**：必须用 `/platform/upload-manager/article`，不能用 `/platform/content-manager/video`（会重定向到首页）。

### 步骤2：evaluate提取当前页数据

```js
(() => {
  var cards = document.querySelectorAll("[class*=article-card]");
  var r = [];
  cards.forEach(function(card) {
    var bv = card.querySelector("a[href*=video]")?.href?.split("/video/")[1]?.replace("/", "") || "";
    var title = card.querySelector("[class*=name]")?.textContent?.trim() || "";
    var date = card.querySelector("span.date")?.textContent?.trim() || "";
    var dur = card.querySelector("[class*=duration]")?.textContent?.trim() || "";
    var s = {};
    card.querySelectorAll("[class*=view-stat]").forEach(function(vs) {
      var label = vs.getAttribute("title") || "";
      var val = vs.querySelector("[class*=icon-text]")?.textContent?.trim() || "0";
      s[label] = parseInt(val.replace(/[^0-9]/g, "")) || 0;
    });
    if (bv && title) r.push([bv, title, date, dur,
      s["播放"]||0, s["点赞"]||0, s["弹幕"]||0,
      s["评论"]||0, s["硬币"]||0, s["收藏"]||0, s["分享"]||0
    ]);
  });
  return JSON.stringify(r);
})()
```

**输出格式**：`[BV号, 标题, 日期, 时长, 播放, 点赞, 弹幕, 评论, 硬币, 收藏, 分享]`

### 步骤3：翻页

```js
document.querySelector(".bcc-pagination-next")?.click()
```

翻页后等待3秒让新页面渲染，再执行步骤2。循环直到"下一页"按钮不可点击或消失。

### 步骤4：日期格式转换

```python
# DOM: "2026年06月12日 21:40:27"
# 目标: "2026-06-12T21:40:27+08:00"
d = date.replace('年','-').replace('月','-').replace('日 ','T').replace('日','T').replace(' ','')
d += '+08:00'
```

### 步骤5：录入工厂

```python
api('POST', '/works', {
    'platform': 'bilibili', 'account_id': bili_id,
    'content_type': 'video', 'title': title[:200],
    'platform_url': 'https://www.bilibili.com/video/' + bv,
    'platform_content_id': bv,
    'published_at': d, 'status': 'published'
})
```

## 踩坑记录

| # | 坑 | 错误做法 | 正确做法 |
|---|-----|---------|---------|
| 1 | **URL重定向** | `/platform/content-manager/video` → 重定向到首页 | 用 `/platform/upload-manager/article` |
| 2 | **`.date`选择器带噪点** | `[class*=date]` 抓到 "2026年...当前字幕:1" | 用 `span.date` 精确选择 |
| 3 | **snapshot看不见Vue渲染内容** | 以为snapshot能拿到article-card | B站用Vue.js，snapshot的accessibility tree不包含动态渲染的卡片；**必须evaluate** |

## 与其他平台的翻页/滚动差异

| 平台 | 渲染/翻页方式 | stats 数量 |
|------|-------------|-----------|
| B站 | 标准翻页，click `.bcc-pagination-next` | 7项(+弹幕/硬币/收藏) |
| 抖音 | 虚拟滚动，scrollBy 触发 | 4项 |
| 小红书 | 滚动 `div.content` | 5项 |
| 知乎 | 虚拟滚动 | 4项 |
