---
name: csdn-content-collector
description: 从CSDN创作中心采集全部文章数据(标题+URL+日期+阅读/点赞/评论/收藏)。无翻页，直接提取。注意CSS选择器不能含'/'(如a[href*=article/details]会报错)。
category: xinhe-paper
---

# CSDN内容采集器

从 `https://mp.csdn.net/mp_blog/manage/article` 采集全部已发布文章。

## 核心原理

CSDN创作中心无翻页、无滚动加载——所有文章直接渲染在DOM中。使用 `article-list-item-mp` 卡片结构。

## 提取方法

### 步骤1：导航

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://mp.csdn.net/mp_blog/manage/article","newTab":true},"session":"csdn"}'
sleep 5
```

### 步骤2：evaluate提取

```js
(() => {
  var cards = document.querySelectorAll(".article-list-item-mp");
  var items = [];
  cards.forEach(function(card) {
    var title = card.querySelector(".article-list-item-txt a")?.textContent?.trim() || "";
    if (!title) return;
    
    var date = card.querySelector(".article-list-item-time")?.textContent?.trim() || "";
    
    // Stats: .article-list-item-readComment → [阅读, 点赞, 评论, 收藏]
    var stats = [];
    card.querySelectorAll(".article-list-item-readComment").forEach(function(s) {
      stats.push(parseInt(s.textContent.trim().replace(/[^0-9]/g, "")) || 0);
    });
    
    // 公网URL: 遍历所有a标签找 blog.csdn.net
    var pubUrl = "";
    var allLinks = card.querySelectorAll("a");
    for (var i = 0; i < allLinks.length; i++) {
      if (allLinks[i].href.indexOf("blog.csdn.net") > -1) {
        pubUrl = allLinks[i].href;
        break;
      }
    }
    
    items.push({
      title: title, date: date, url: pubUrl,
      stats: stats
    });
  });
  return JSON.stringify(items);
})()
```

**输出格式**：`[{title, date, url, stats: [阅读, 点赞, 评论, 收藏]}]`

### 步骤3：日期格式转换

```python
# DOM: "2026-06-04 20:24:52"
# 目标: "2026-06-04T20:24:52+08:00"
d = date.replace(' ', 'T') + '+08:00'
```

### 步骤4：录入工厂

```python
api('POST', '/works', {
    'platform': 'csdn', 'account_id': csdn_id,
    'content_type': 'article', 'title': title[:200],
    'platform_url': url, 'platform_content_id': url.split('/details/')[1],
    'published_at': d, 'status': 'published'
})
# metrics: view_count=stats[0], like_count=stats[1], comment_count=stats[2], favorite_count=stats[3]
```

## 踩坑记录（1个已验证的坑）

| # | 坑 | 错误做法 | 正确做法 |
|---|-----|---------|---------|
| 1 | **CSS选择器含`/`报错** | `a[href*=article/details]` → InvalidSelectorError | 用JS循环遍历所有a标签，`if(href.indexOf("blog.csdn.net")>-1)`判断 |
