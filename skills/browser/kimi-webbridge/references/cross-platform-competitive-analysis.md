# Cross-Platform Competitive Intelligence Analysis

Pattern: search the same keyword across multiple social platforms simultaneously, then compare search relevance, content volume, engagement metrics, and publisher types to diagnose platform-level suppression vs. content quality issues.

## When to use

- Suspected platform-level content suppression or shadow-banning
- Competitive landscape analysis for a keyword/category
- Validating whether low traffic is due to your content quality vs. platform policy
- Pre-competition window reconnaissance

## Workflow

### 1. Open all platforms simultaneously

Use `navigate` with distinct session names per platform:

```
hermes-douyin    → https://www.douyin.com/search/{keyword}?type=video
hermes-xhs       → https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51
hermes-bilibili  → https://search.bilibili.com/all?keyword={keyword}
hermes-zhihu     → https://www.zhihu.com/search?type=content&q={keyword}
```

Use `newTab:true` on first call. Wait 3-5s for render.

### 2. Collect data via snapshot

For each platform, call `snapshot` and parse the accessibility tree. **The raw output can be 50-100KB per platform** — always pipe through Python to extract only the relevant result items, not the full page chrome (footer links, navigation, etc.).

Target extraction: search result list items only. In the tree, these are typically `<listitem>` elements inside a `<list>` under the main content area. Strip navigation bars, footers, and sidebar noise.

Key data points to extract:

- **Search relevance**: How many results are semantically on-topic? (e.g., "2026中青杯" returning 2026 World Cup content = search keyword hijacking)
- **Content volume**: Raw result count indicators (e.g., Bilibili's "99+" badge)
- **Engagement metrics**: Likes/plays/comments per result
- **Publisher types**: Are results from organic users, institutional accounts, or spam farms?
- **Timing**: Post recency relative to the event window

### 3. Diagnose suppression patterns

| Symptom | Diagnosis |
|---------|-----------|
| Search results are mostly off-topic (keyword being generic-matched) | **Search-level hijacking** — keyword is being decomposed and remapped to unrelated content |
| Results are on-topic but engagement near-zero | **Recommendation suppression** — content exists and is searchable but not pushed to feeds |
| Content removed/deleted | **Content moderation** — actual takedowns for policy violations |
| Some competitors visible but not you | **Account-level action** — shadowban or category trust-score penalty |

### 4. Cross-reference

The pattern that matters is the **difference between platforms**. If the same keyword returns relevant results on Bilibili but not Douyin, the issue is platform-specific policy, not content quality.

## Limitations

- `snapshot` accessibility trees can be very large (50-100KB per platform). Pipe through Python for extraction.
- Non-Chinese platforms may require different search URL patterns.
- `vision_analyze` may fail with non-vision models (e.g., deepseek) — rely on snapshot text extraction instead.
- Login state matters: the user should be logged into all target platforms in their real browser.
- Bilibili search URLs must use `search.bilibili.com/all?keyword=...` (NOT the main site URL) — the main site search bar redirects but doesn't work reliably with `navigate`.

## URL encoding

Chinese keywords must be URL-encoded. Use Python for one-shot encoding:

```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('中青杯'))"
# → %E4%B8%AD%E9%9D%92%E6%9D%AF
```
