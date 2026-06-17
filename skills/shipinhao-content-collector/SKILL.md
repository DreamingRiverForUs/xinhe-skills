---
name: shipinhao-content-collector
description: 从微信视频号助手采集全部视频数据(标题+日期+播放/点赞/评论/分享/收藏)。内容在iframe中，需通过contentDocument访问。底部翻页，每页20条。
category: xinhe-paper
---

# 视频号内容采集器

从 `https://channels.weixin.qq.com/platform/post/list` 采集全部视频作品。

## 核心原理

视频号助手页面将内容渲染在**iframe**中，所有DOM操作必须通过 `iframe.contentDocument` 访问。底部翻页，每页20条。

## 提取方法

### 步骤1：导航并关闭弹窗

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://channels.weixin.qq.com/platform/post/list","newTab":true},"session":"wx"}'
sleep 5

# 关闭可能出现的账号切换弹窗
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"var btns=document.querySelectorAll(\"button,span,div\");for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()===\"取消\"){btns[i].click();break}}"},"session":"wx"}'
sleep 2
```

### 步骤2：通过iframe提取当前页

**⚠️ 关键：所有DOM查询必须通过 `iframe.contentDocument`！**

```js
(() => {
  var doc = document.querySelector("iframe").contentDocument;
  var titles = doc.querySelectorAll(".post-title");
  var items = [];
  var seen = new Set();
  titles.forEach(function(t) {
    var text = t.textContent.trim();
    var key = text.substring(0, 40);
    if (seen.has(key)) return;
    seen.add(key);
    
    // 找到父级卡片
    var card = t.closest("div");
    while (card && !card.querySelector(".post-data")) card = card.parentElement;
    
    var date = card?.querySelector(".post-time span")?.textContent?.trim() || "";
    var counts = card?.querySelectorAll(".data-item .count");
    var stats = [];
    counts?.forEach(function(c) {
      stats.push(parseInt(c.textContent.trim().replace(/[^0-9]/g, "")) || 0);
    });
    
    // stats顺序: [0]=播放(eyes-on) [1]=点赞(like) [2]=评论(comment) [3]=分享(share) [4]=收藏(thumb)
    items.push([text.replace(/\n/g, " "), date,
      stats[0]||0, stats[1]||0, stats[2]||0, stats[3]||0, stats[4]||0
    ]);
  });
  return JSON.stringify(items);
})()
```

### 步骤3：翻页（已验证）

**⚠️ 翻页按钮在iframe内！当在第2页时，"下一页"和"上一页"同时存在，必须精确匹配 textContent！**

```js
var doc = document.querySelector("iframe").contentDocument;
// 必须精确匹配 textContent === "下一页"，不能用 first-match
var btns = doc.querySelectorAll(".weui-desktop-btn");
for (var i = 0; i < btns.length; i++) {
  if (btns[i].textContent.trim() === "下一页") {
    btns[i].click();
    break;
  }
}
// 翻页后等待2-3秒渲染
```

**翻页按钮信息**：
- 页码导航：`span.weui-desktop-pagination__nav` → "1  2  3 下一页"
- 下一页按钮：`a.weui-desktop-btn.weui-desktop-btn_default` + textContent==="下一页"
- 上一页按钮：同class + textContent==="上一页"
- 总页数：3页（20+20+3=43条）

### 步骤4：日期格式转换

```python
# DOM: "2026年06月12日 21:42"
# 目标: "2026-06-12T21:42:00+08:00"
d = date.replace('年','-').replace('月','-').replace('日 ','T').replace('日','T').replace(' ','')
d += ':00+08:00'
```

## 踩坑记录（3个已验证 + 1个待验证）

| # | 坑 | 错误做法 | 正确做法 |
|---|-----|---------|---------|
| 1 | **内容在iframe中** | `document.querySelector(".post-title")` → 0结果 | 通过 `document.querySelector("iframe").contentDocument` 访问 |
| 2 | **账号切换弹窗** | 导航后直接查询 → 弹窗遮挡渲染 | 先click "取消"关闭弹窗 |
| 3 | **evaluate报错但snapshot有数据** | 以为数据拿不到 | 数据在iframe的DOM中，evaluate可以访问；snapshot显示无障碍树有标题但evaluate查不到是因为没进iframe |
| 4 | **翻页按钮有两个** | 用`.weui-desktop-btn:first` → 页面2时点到"上一页"而不是"下一页" | 遍历所有button，精确匹配 `textContent.trim()==="下一页"` |

## 各平台滚动/翻页对比

| 平台 | 方式 | 容器 | 每页条数 |
|------|------|------|---------|
| 抖音 | 虚拟滚动 | `document.scrollingElement` | ~12 DOM |
| B站 | 标准翻页 | `click .bcc-pagination-next` | 10 |
| 知乎 | 虚拟滚动 | `document.scrollingElement` | ~20 DOM |
| 小红书 | 容器内滚动 | `div.content` | 按需加载 |
| **视频号** | **iframe内翻页** | **`iframe.contentDocument`** | **20** |
