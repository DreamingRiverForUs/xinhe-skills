# 小红书内容采集器

从 `https://creator.xiaohongshu.com/new/note-manager` 采集全部笔记作品。

## 核心原理

小红书创作平台使用滚动加载，**滚动容器是 `div.content` 而非 `window`**。stats无文字标签，仅通过SVG图标区分，按固定顺序映射。

## 提取方法

### 步骤1：导航

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://creator.xiaohongshu.com/new/note-manager","newTab":true},"session":"xhs"}'
sleep 5
```

### 步骤2：滚动加载（关键！）

**⚠️ 必须滚动 `div.content`，不是 window/document.body！**

```bash
for i in $(seq 1 15); do
  curl -s -X POST http://127.0.0.1:10086/command \
    -H 'Content-Type: application/json' \
    -d '{"action":"evaluate","args":{"code":"var el=document.querySelector(\"div.content\");if(el)el.scrollTo(0,el.scrollTop+400)"},"session":"xhs"}' > /dev/null
  sleep 0.8
done
```

### 步骤3：evaluate提取

```js
(() => {
  var cards = document.querySelectorAll(".note-card");
  var seen = new Set();
  var r = [];
  cards.forEach(function(card) {
    var title = card.querySelector(".note-card__title")?.textContent?.trim() || "";
    if (!title || seen.has(title.substring(0, 40))) return;
    seen.add(title.substring(0, 40));

    var date = card.querySelector(".note-card__time")?.textContent?.trim() || "";
    
    // noteId 在 data-impression JSON 属性中
    var noteId = "";
    try {
      var imp = JSON.parse(card.getAttribute("data-impression") || "{}");
      noteId = imp.noteTarget?.value?.noteId || "";
    } catch(e) {}

    // Stats: 无文字标签，仅SVG图标。顺序固定：
    // [0]=观看(eye) [1]=评论(comment) [2]=点赞(heart) [3]=收藏(star) [4]=分享(share)
    var stats = [];
    card.querySelectorAll(".note-card__stat span").forEach(function(s) {
      stats.push(parseInt(s.textContent.trim().replace(/[^0-9]/g, "")) || 0);
    });
    
    r.push([noteId, title, date,
      stats[0]||0, stats[1]||0, stats[2]||0, stats[3]||0, stats[4]||0
    ]);
  });
  return JSON.stringify(r);
})()
```

**输出格式**：`[noteId, 标题, 日期, 观看, 评论, 点赞, 收藏, 分享]`

### 步骤4：日期格式转换

```python
# DOM: "2026-06-12 20:40"
# 目标: "2026-06-12T20:40:00+08:00"
d = date.replace(' ', 'T') + ':00+08:00'
```

### 步骤5：录入工厂

```python
api('POST', '/works', {
    'platform': 'xiaohongshu', 'account_id': xhs_id,
    'content_type': 'image_text', 'title': title[:200],
    'platform_content_id': noteId,
    'published_at': d, 'status': 'published'
})
# metrics: view_count=观看, like_count=点赞, comment_count=评论, favorite_count=收藏, share_count=分享
```

## 踩坑记录

| # | 坑 | 错误做法 | 正确做法 |
|---|-----|---------|---------|
| 1 | **URL不对** | `/new/manage/notes` → 404; `/new/home` → 首页不是笔记列表 | 用 `/new/note-manager` |
| 2 | **滚动容器不是window** | `window.scrollBy/scrollingElement.scrollTo` → 不加载新内容 | 找到 `div.content`(overflow:scroll, scrollHeight>clientHeight)，用 `el.scrollTo(0,el.scrollTop+400)` |
| 3 | **stats无文字标签** | 试图找 `评论`/`点赞` 等文字标签 → 不存在 | 按SVG图标顺序固定映射: [0]=观看 [1]=评论 [2]=点赞 [3]=收藏 [4]=分享 |

## 与其他平台的滚动差异

| 平台 | 滚动容器 | 触发方式 |
|------|---------|---------|
| 抖音 | `document.scrollingElement` | `el.scrollTo(0, el.scrollTop+700)` |
| B站 | 无滚动（标准翻页） | `click .bcc-pagination-next` |
| 知乎 | `document.scrollingElement` | `el.scrollTo(0, el.scrollTop+800)` |
| **小红书** | **`div.content`** | **`el.scrollTo(0, el.scrollTop+400)`** |
