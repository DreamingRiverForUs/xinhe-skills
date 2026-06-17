# B站/Chinese Video Content Extraction (no-subtitle fallback)

When asked to summarize a Bilibili or other Chinese-platform video that lacks accessible subtitles, use this multi-source fallback strategy instead of giving up.

## TL;DR fallback chain

1. **Video description** (richest signal on B站 — authors write detailed outlines)
2. **Google search** for blog summaries (什么值得买, 增长黑客AI周报, etc.)
3. **YouTube mirror** check (many creators cross-post)
4. **API metadata** (cid, bvid, stats) for attribution

## Step-by-step

### 1. Open the video page and snapshot

Use WebBridge navigate + snapshot. B站 descriptions are often 500+ chars with numbered section breakdowns — this alone can give 80% of the content structure.

### 2. Try subtitle extraction

**Bilibili API (needs WBI signing — often blocked outside China)**:
```
# This endpoint times out from non-China IPs due to WBI verification
https://api.bilibili.com/x/player/wbi/v2?bvid=<BV>&cid=<CID>
```

**Legacy API (works more often)**:
```
https://api.bilibili.com/x/player/v2?bvid=<BV>&cid=<CID>
```

**Video info API (always works)**:
```
https://api.bilibili.com/x/web-interface/view?bvid=<BV>
```
Returns: title, description, owner, stats, pages (with cid), subtitle availability flag. The `subtitle.list` field being empty means no CC available.

### 3. Extract metadata via evaluate

```js
// Get cid, bvid, aid from __INITIAL_STATE__
window.__INITIAL_STATE__.videoData
// Returns: {cid, bvid, aid, title, pages}
```

### 4. When subtitles are unavailable → Google search fallback

Search for: `"<video title keywords>" 全流程` or `"<bvid>" 总结`

Key sources that often summarize Chinese AI videos:
- **什么值得买** (post.smzdm.com) — tech review posts with detailed tool breakdowns
- **增长黑客AI周报** (zengzhang.ai) — weekly roundups that summarize popular videos
- **知乎** — users often write article versions of their videos
- **CSDN / 掘金** — developer blog mirrors

### 5. YouTube mirror

Many B站 creators cross-post to YouTube. Search: `"<Chinese title>" Tang Spark` or channel name. YouTube may have auto-generated captions even when B站 doesn't.

### 6. Compile summary from all sources

Even without a transcript, the combination of:
- Detailed video description (numbered sections)
- Blog summaries from Google results
- YouTube mirror metadata
- Related video comparisons (sidebar recommendations)

...is usually sufficient for a high-quality summary. The B站 culture of writing long, structured descriptions makes this more effective than it would be for Western platforms.

## Pitfalls

- **Bilibili WBI API blocking**: The `/x/player/wbi/v2` endpoint requires WBI signing parameters that are hard to compute without a browser session. `/x/web-interface/view` is a reliable fallback that doesn't need signing.
- **什么值得买 iframe wrapping**: Content may be inside an iframe that WebBridge snapshot returns empty. The article text is still in the HTML source — try evaluate to extract from the iframe's contentDocument, or move on to another source.
- **YouTube auto-captions not guaranteed**: Small channels may not have auto-generated captions enabled. Check the CC button state in snapshot before investing time.
- **yt-dlp not always installed**: Don't assume it; check with `which` first. If missing, skip to Google search fallback.
