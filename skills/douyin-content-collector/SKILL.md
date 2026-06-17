---
name: douyin-content-collector
description: 从抖音创作者中心采集全部作品数据(标题+日期+播放/点赞/评论/分享)。使用WebBridge evaluate从video-card DOM直接提取，逐段scrollTo滚动到底。snapshot只用于标题/日期提取，stats数字必须通过evaluate获取。
category: xinhe-paper
---

# 抖音内容采集器

从 `https://creator.douyin.com/creator-micro/content/manage` 采集全部作品数据并录入工厂。

## 提取方法（最终验证版 — 62条全量）

### 核心原理

抖音内容管理页使用**虚拟滚动**，DOM中只保留~12张 `video-card-*` 卡片。需要逐段滚动到底，在顶部和底部分别采集，合并去重。

三个关键发现：

1. **stats在CSS module class中（`metric-value-k4R5P_`）**，不在accessibility tree里。snapshot看不到数字，**必须用evaluate从DOM提取**。
2. **虚拟滚动逐段触发**：`document.scrollingElement.scrollTo(0, scrollTop+700)` 反复执行直到 `atBottom=true`。不能用 `scrollTop=scrollHeight` 一次跳到底（不触发渲染）。
3. **每张卡片数据结构固定**：`.info-title-text-*` 标题、`.info-time-*` 日期、`.metric-item-*` 下的 `.metric-label-*` + `.metric-value-*` 统计。

### 步骤1：导航并逐段滚到底

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://creator.douyin.com/creator-micro/content/manage","newTab":true},"session":"douyin"}'

sleep 5

# 逐段滚动，直到触底
for i in $(seq 1 20); do
  curl -s -X POST http://127.0.0.1:10086/command \
    -H 'Content-Type: application/json' \
    -d '{"action":"evaluate","args":{"code":"var e=document.scrollingElement||document.body;e.scrollTo(0,e.scrollTop+700)"},"session":"douyin"}' > /dev/null
  sleep 0.8
done
sleep 2
```

### 步骤2：底部采集（evaluate提取完整数据）

```js
(() => {
  var seen = new Set(), result = [];
  document.querySelectorAll("[class*=video-card]").forEach(card => {
    var title = card.querySelector("[class*=info-title-text]")?.textContent?.trim() || "";
    if (!title || title.length < 5) return;
    var key = title.substring(0, 40);
    if (seen.has(key)) return;
    seen.add(key);
    var item = [
      title,  // [0] 标题
      card.querySelector("[class*=info-time]")?.textContent?.trim() || ""  // [1] 日期
    ];
    card.querySelectorAll("[class*=metric-item]").forEach(mi => {
      var l = mi.querySelector("[class*=metric-label]")?.textContent?.trim();
      var v = mi.querySelector("[class*=metric-value]")?.textContent?.trim();
      if (l && v) item.push(l + "=" + (parseInt(v.replace(/[^0-9]/g, "")) || 0));
    });
    result.push(item);
  });
  return JSON.stringify(result);
})()
```

### 步骤3：滚回顶部采集

```js
// 滚回顶部
var e = document.scrollingElement || document.body;
e.scrollTo(0, 0);

// 等渲染好，再执行步骤2的evaluate
```

### 步骤4：合并去重

```python
merged = {}
for item in bottom_data + top_data:
    key = item[0][:40]  # 标题前40字符做去重key
    if key not in merged:
        merged[key] = item
```

### 步骤5：日期格式转换（关键！）

```python
# DOM: "2026年04月02日 22:02"
# 目标: "2026-04-02T22:02:00+08:00"
# 陷阱: replace('日','T') 会留下空格变成 "2026-04-02T 22:02"
# 正解:
d = date.replace('年','-').replace('月','-').replace('日 ','T').replace('日','T').replace(' ','')
```

### 步骤6：录入工厂

优先使用 upsert API（`POST /works?upsert=true` + `platform_content_id`），但抖音无content_id，需先清理旧数据再全量录入。用分页遍历DELETE避免page_size截断：

```python
# 分页清理
while True:
    resp = api('GET', '/works?platform=douyin&page_size=100')
    items = resp.get('items', [])
    if not items: break
    for w in items:
        api('DELETE', '/works/' + w['id'])
```

## 踩坑记录（6个已验证的坑）

| # | 坑 | 错误做法 | 正确做法 | 后果 |
|---|-----|---------|---------|------|
| 1 | **snapshot看不到stats** | 以为snapshot能拿到全部数据 | stats在CSS module class(`metric-value-k4R5P_`)里，accessibility tree不包含，**必须evaluate** | 36条作品全部0播放 |
| 2 | **虚拟滚动只渲染~12张** | 一次`scrollTop=scrollHeight`跳到底 | 逐段`scrollTo(0, scrollTop+700)`触发渲染，底部+顶部分别采集，合并去重 | 只拿到12条 |
| 3 | **querySelector不跟随卡片** | `[class*=metric-container]`独立查询导致stats和标题错位 | 从每张`[class*=video-card]`内部用`.info-title-text-*` `.metric-item-*`提取 | 数据完全错乱 |
| 4 | **日期格式多了空格** | `replace('日','T')` → `"2026-04-02T 22:02"` | `replace('日 ','T').replace(' ','')` → `"2026-04-02T22:02"` | API 422全部录入失败 |
| 5 | **删除时不遍历分页** | `while items: break` 只删第一页100条 | 循环检查 `resp.get('total')` 直到为0 | 数据累积到303条 |
| 6 | **反复重跑有bug脚本** | 失败后不改直接重试 | **先诊断根因 → 写bug报告 → 协同修复 → 一次跑通** | 浪费时间+数据污染 |

## 注意事项

- 不要用 `window.scrollBy` — 用 `document.scrollingElement.scrollTo`
- 不要在快照里找数字 — 用 evaluate 读 DOM
- 标题去重用前40字符 — 虚拟滚动会产生重复DOM节点
- 工厂录入前务必先清空旧数据（分页删除）
