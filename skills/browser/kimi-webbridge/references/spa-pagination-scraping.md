# SPA Pagination Scraping via WebBridge

When a site blocks curl (Cloudflare/ESA 403) and the content is loaded via JavaScript, use WebBridge's `evaluate` to extract data and paginate in minimal API calls.

## Core technique: extract + navigate in one evaluate

The key insight: use `setTimeout` to trigger the Next click AFTER the data is returned, so extracting data and paginating happen in a single `evaluate` call:

```js
(() => {
    // 1. Extract data from current page
    var cards = document.querySelectorAll('a[href*="/template/"]');
    var r = [];
    cards.forEach(function(a) {
        var h = a.querySelector('h2, h3, [class*=title], [class*=name]') || a;
        r.push({name: h.textContent.trim().replace(/\s+/g, ' '), href: a.href});
    });
    
    // 2. Schedule Next click (fires after return, so page navigates AFTER we get data)
    var links = document.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
        if (links[i].textContent.trim() === 'Next') {
            setTimeout(function(){ links[i].click(); }, 200);
            break;
        }
    }
    
    return JSON.stringify(r);
})()
```

## Why this works

- `evaluate` returns synchronously with the data
- `setTimeout(..., 200)` fires after the return, navigating the SPA to the next page
- The next `evaluate` call (after a 2-3s sleep) runs on the new page
- Result: 1 WebBridge call per page instead of 3 (evaluate + snapshot + click)

## Loop pattern (Python via execute_code)

```python
EXTRACT_AND_NEXT = """... JS above ..."""

def wb_eval(code):
    body = {"action": "evaluate", "args": {"code": code}, "session": session}
    write_file("/tmp/wb_body.json", json.dumps(body))
    r = terminal(f"curl -s --max-time 15 -X POST http://127.0.0.1:10086/command -H 'Content-Type: application/json' -d @/tmp/wb_body.json", timeout=20)
    return json.loads(r["output"])

page = 0
while page < MAX_PAGES:
    time.sleep(2.5)  # Wait for previous navigation to settle
    resp = wb_eval(EXTRACT_AND_NEXT)
    if not resp.get("ok"):
        break
    data = json.loads(resp["data"]["value"])
    if len(data) == 0:
        break
    # ... accumulate data ...
    page += 1
```

## Pitfalls

1. **Don't use async/await in evaluate** — SPA navigation kills the script context mid-await. Use synchronous extraction with `setTimeout` for the click.
2. **Don't use WebBridge `click` action for pagination** — it works but requires a separate `snapshot` call to find the `@e` ref, costing 2 extra API calls per page.
3. **Regex for snapshot refs needs `\s*` after colons** — the snapshot JSON has spaces: `"role": "link"`, not `"role":"link"`. Pattern: `r'"role":\s*"link",\s*"name":\s*"Next",\s*"ref":\s*"(@e\d+)"'`
4. **Save intermediate results** — long-running pagination hits tool-call limits. Save to file every N pages so you can resume.
5. **Use `--max-time` on curl** — WebBridge calls can hang if the page is slow; a 15-20s timeout prevents terminal stalls.
