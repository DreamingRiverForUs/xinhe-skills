---
name: zhihu-content-collector
description: 从知乎创作中心采集文章数据(标题+URL+日期+阅读/赞同/评论/收藏/喜欢)。虚拟滚动，需scrollTo加载。只采集文章类型，过滤非2026年内容。
category: xinhe-paper
---

# 知乎内容采集器

从 `https://www.zhihu.com/creator/manage/creation/all` 采集文章类型作品。

## 核心原理

知乎创作中心使用虚拟滚动，卡片类型混合（文章/回答/想法）。需要：
1. 逐段scrollTo加载所有卡片
2. 按类型`div[class*=hh4w84]` === "文章" 过滤
3. 只采集2026年内容

## 提取方法

### 步骤1：导航

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://www.zhihu.com/creator/manage/creation/all","newTab":true},"session":"zhihu"}'
sleep 5
```

### 步骤2：滚动加载

```bash
for i in $(seq 1 10); do
  curl -s -X POST http://127.0.0.1:10086/command \
    -H 'Content-Type: application/json' \
    -d '{"action":"evaluate","args":{"code":"var e=document.scrollingElement||document.body;e.scrollTo(0,e.scrollTop+800)"},"session":"zhihu"}' > /dev/null
  sleep 0.8
done
```

### 步骤3：evaluate提取

```js
(() => {
  var cards = document.querySelectorAll("div[class*=CreationCard]");
  var r = [];
  var seen = new Set();
  cards.forEach(function(card) {
    // 只采集"文章"类型
    var typeEl = card.querySelector("div[class*=hh4w84]");
    if (!typeEl || typeEl.textContent.trim() !== "文章") return;
    
    // 必须包含zhuanlan链接
    var link = card.querySelector("a[href*=zhuanlan]");
    if (!link) return;
    
    var pid = link.href.split("/p/")[1]?.split("?")[0] || "";
    if (seen.has(pid)) return;
    seen.add(pid);
    
    var title = card.querySelector("span")?.textContent?.trim() || "";
    var date = card.querySelector("div[class*=zzavo4]")?.textContent?.trim() || "";
    
    // Stats: 1mj4fzq = 数字, 1jw9fry = 标签(阅读/赞同/评论/收藏/喜欢)
    var s = {};
    var divs = card.querySelectorAll("div");
    for (var i = 0; i < divs.length; i++) {
      var d = divs[i];
      if (d.className.indexOf("1mj4fzq") > -1) {
        var n = parseInt(d.textContent.trim().replace(/[^0-9]/g, "")) || 0;
        var next = d.nextElementSibling;
        var l = next && next.className.indexOf("1jw9fry") > -1 ? next.textContent.trim() : "";
        if (l) s[l] = n;
      }
    }
    
    r.push([pid, title, date,
      s["阅读"]||0, s["赞同"]||0, s["评论"]||0, s["收藏"]||0, s["喜欢"]||0
    ]);
  });
  return JSON.stringify(r);
})()
```

**输出格式**：`[pid, 标题, 日期, 阅读, 赞同, 评论, 收藏, 喜欢]`

### 步骤4：过滤2026+内容

```python
import re

for item in items:
    pid, title, date, reading, agree, comment, fav, like = item
    
    # 跳过含4位数年份且不是2026的
    year_match = re.search(r'(\d{4})', date)
    if year_match and int(year_match.group(1)) != 2026:
        continue
    
    # "编辑于 06-04" → "2026-06-04T00:00:00+08:00"
    mmdd = re.search(r'(\d{2})-(\d{2})', date)
    if not mmdd: continue
    pub_date = f'2026-{mmdd.group(1)}-{mmdd.group(2)}T00:00:00+08:00'
    
    url = f'https://zhuanlan.zhihu.com/p/{pid}'
```

### 步骤5：录入工厂

```python
api('POST', '/works', {
    'platform': 'zhihu', 'account_id': zh_id,
    'content_type': 'article', 'title': title[:200],
    'platform_url': url, 'platform_content_id': pid,
    'published_at': pub_date, 'status': 'published'
})
# metrics: view_count=reading, like_count=agree, comment_count=comment, favorite_count=fav
```

## 踩坑记录（4个已验证的坑）

| # | 坑 | 错误做法 | 正确做法 |
|---|-----|---------|---------|
| 1 | **CSS class以数字开头** | `[class*=150duks]` → InvalidSelectorError | 用 `d.className.indexOf("1mj4fzq")` JS判断 |
| 2 | **卡片类型混合** | 不区分类型全部提取 | 检查 `div[class*=hh4w84]` textContent === "文章" |
| 3 | **日期无年份** | "编辑于 06-04" 无法直接用 | 正则匹配：无4位年份=当前年(2026)，有年份需校验 |
| 4 | **旧文章混入** | 2021-2025年PaddleSpeech/TVM文章也被采集 | 过滤 `year_match and year != 2026` |

## 与其他平台的差异

| 特性 | 抖音 | B站 | 知乎 |
|------|------|-----|------|
| 渲染方式 | 虚拟滚动 | 标准翻页 | 虚拟滚动 |
| 内容类型 | 视频+图文混合 | 纯视频 | 文章+回答+想法混合 |
| stats数量 | 4项 | 7项 | 5项(阅读/赞同/评论/收藏/喜欢) |
| 日期格式 | 完整年月日时分 | 完整年月日时分秒 | "编辑于MM-DD"(无年份) |
| URL | 无(SPA) | BV号在href | pid在zhuanlan URL |
