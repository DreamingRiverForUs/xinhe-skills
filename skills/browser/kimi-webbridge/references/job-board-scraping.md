# Scraping Job Board SPAs (mokahr.com & similar)

## Problem

Job board SPAs like `app.mokahr.com` render job descriptions **inline within the list page** — each position is an `<a>` element whose `textContent` contains the full JD (title, location, description, requirements, bonuses). The `snapshot()` accessibility tree captures this text but the output is enormous (200k+ chars for 30 positions) and gets truncated. Clicking each position to open a detail view is slow and fragile.

## Solution: evaluate + textContent extraction

### Step 1: Get all position titles (fast scan)

```js
(()=>{
  var texts=[];
  document.querySelectorAll("a").forEach(function(a){
    var t=a.textContent.trim();
    if(t.startsWith("Agent") || t.startsWith("产品经理")){
      texts.push(t.substring(0,3000))
    }
  });
  return JSON.stringify(texts)
})()
```

This returns full JDs from the list page in one call. The `substring(0,3000)` is important — JDs can be 4000+ chars and the response may get truncated without it. Adjust the filter keywords per target role.

### Step 2: Extract a specific position by title prefix

After identifying target positions from Step 1, extract full details:

```js
(()=>{
  var as=document.querySelectorAll("a");
  for(var i=0;i<as.length;i++){
    var t=as[i].textContent.trim();
    if(t.startsWith("Agent Harness 研发")) return t.substring(0,4000);
  }
  return "not found"
})()
```

### Step 3: Get position offsets for scrolling

When positions are below the fold, find their scroll positions first:

```js
(()=>{
  var r=[];
  var as=document.querySelectorAll("a");
  for(var i=0;i<as.length;i++){
    var t=as[i].textContent.trim();
    if(t.startsWith("Agent")) r.push({idx:i,title:t.substring(0,50),offset:as[i].getBoundingClientRect().top})
  }
  return JSON.stringify(r)
})()
```

Then scroll: `window.scrollTo(0, OFFSET-50);"ok"`

## Why this beats snapshot for this use case

| Approach | Pros | Cons |
|----------|------|------|
| `snapshot()` | Full accessibility tree, `@e` refs preserved | Huge output (200k+ chars), truncation, needs Python parsing |
| `evaluate` + `textContent` | Fast, targeted, one call per position | No `@e` refs (but not needed for data extraction) |

## Platform quirks

- **mokahr.com**: Positions are rendered as `<a>` links with `href` containing the job path. Full JD text is in `textContent`. No separate detail page — clicking just scrolls to an expanded section. The pagination is client-side (no URL change).
- **Filtering**: The search box `@e2` and filter checkboxes support narrowing by location/type. Use these before extracting to reduce result count.
- **Pagination**: 30 per page. Page buttons are at the bottom. Use `snapshot` to get pagination `@e` refs, click page 2, then re-run `evaluate`.

## Workflow template

1. Navigate to the job listing URL
2. Optional: apply filters (location, type) to reduce results
3. Run Step 1 `evaluate` to get all matching position JDs
4. For positions below the fold, use Step 3 to get offsets, scroll, and extract
5. For multi-page results, click pagination, re-run Step 1
6. Close session when done
