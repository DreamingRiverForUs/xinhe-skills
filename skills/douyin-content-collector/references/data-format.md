# 抖音数据格式参考

## DOM结构

每张video-card的结构：

```html
<div class="video-card-zQ02ng video-card-new-pWwRVu">
  <div class="video-card-content-_C7uJe">
    <div class="video-card-cover-xx9wyS">
      <span class="badge-pcgoA6">01:48</span>
      <span class="badge-top-mEOJIK">置顶</span>
    </div>
    <div class="video-card-info-aglKIQ">
      <div class="info-title-text-YTLo9y">标题文本</div>
      <div class="info-time-iAYLF0">2026年04月02日 22:02</div>
      <div class="info-status-AIgxHw">已发布</div>
      <div class="metric-container-Rc61p9">
        <div class="metric-item-u1CAYE">
          <div class="metric-label-AX_5OF">播放</div>
          <div class="metric-value-k4R5P_">3065</div>
        </div>
        <div class="metric-item-u1CAYE">
          <div class="metric-label-AX_5OF">点赞</div>
          <div class="metric-value-k4R5P_">21</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 提取数据格式

evaluate输出格式（每个item是一个数组）：

```json
["标题文本", "2026年04月02日 22:02", "播放=3065", "点赞=21", "评论=2", "分享=2"]
```

## 日期转换

```
输入: "2026年04月02日 22:02"
步骤: replace('年','-') then replace('月','-') then replace('日 ','T')
输出: "2026-04-02T22:02:00+08:00"
陷阱: replace('日','T') 会留下空格变成 "2026-04-02T 22:02" (API 422)
```

## 工厂API

POST /works:
```json
{"platform":"douyin","account_id":"...","content_type":"short_video","title":"...","published_at":"2026-04-02T22:02:00+08:00","status":"published"}
```

POST /works/{id}/metrics:
```json
{"view_count":3065,"like_count":21,"comment_count":2,"share_count":2,"collected_at":"2026-06-16T10:00:00Z"}
```

分页清理（防page_size截断）:
```python
while True:
    r = api('GET', '/works?platform=douyin&page_size=100')
    if not r.get('items'): break
    for w in r['items']: api('DELETE', '/works/' + w['id'])
```
