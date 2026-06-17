# Snapshot Data Extraction Recipes

Pipe `snapshot` output through these Python one-liners to extract structured data without needing `vision_analyze`.

## Extract all table rows

```bash
curl ... | python3 -c "
import json, sys
data = json.load(sys.stdin)
tree = data['data']['tree']
main = tree[1][1]  # sidebar is tree[0], main content is tree[1][1]

def extract_table(node):
    if isinstance(node, dict):
        if node.get('role') == 'row':
            cells = []
            for child in node.get('children', []):
                if isinstance(child, dict):
                    texts = []
                    for c in child.get('children', []):
                        if isinstance(c, dict) and c.get('role') == 'StaticText':
                            texts.append(c.get('name', ''))
                    cells.append(''.join(texts))
            print(' | '.join(cells))
        for child in node.get('children', []):
            extract_table(child)
    elif isinstance(node, list):
        for item in node:
            extract_table(item)

extract_table(main)
"
```

## Extract all visible text (flattened)

```bash
curl ... | python3 -c "
import json, sys
data = json.load(sys.stdin)
main = data['data']['tree'][1][1]

def extract_texts(node):
    if isinstance(node, dict):
        name = node.get('name','')
        texts = [name] if name and node.get('role')=='StaticText' else []
        for child in node.get('children', []):
            texts.extend(extract_texts(child))
        return texts
    elif isinstance(node, list):
        texts = []
        for item in node:
            texts.extend(extract_texts(item))
        return texts
    return []

for t in extract_texts(main):
    if t.strip():
        print(t, end=' | ')
"
```

## Extract chart axis labels

```bash
curl ... | python3 -c "
import json, sys
tree = json.load(sys.stdin)['data']['tree']
main = tree[1][1]

def find_svg_texts(node):
    if isinstance(node, dict):
        if node.get('role') == 'SvgRoot':
            texts = []
            for child in node.get('children', []):
                if isinstance(child, dict) and child.get('role') == 'StaticText':
                    texts.append(child.get('name', ''))
            return [' | '.join(texts)]
        result = []
        for child in node.get('children', []):
            result.extend(find_svg_texts(child))
        return result
    elif isinstance(node, list):
        result = []
        for item in node:
            result.extend(find_svg_texts(item))
        return result
    return []

for chart_data in find_svg_texts(main):
    print(chart_data)
"
```

## Universal text dump (recommended first pass)

Simplest possible pattern — no tree-index knowledge needed. Works on any page layout:

```bash
curl ... | python3 -c "
import sys, json
data = json.load(sys.stdin)
tree = data.get('data', {}).get('tree', [])
def find_texts(node):
    results = []
    if isinstance(node, dict):
        role = node.get('role', '')
        name = node.get('name', '')
        if role in ('StaticText', 'InlineTextBox') and name:
            results.append(name)
        if 'children' in node:
            for child in node['children']:
                results.extend(find_texts(child))
    elif isinstance(node, list):
        for child in node:
            results.extend(find_texts(child))
    return results
for t in find_texts(tree):
    print(t)
"
```

This dumps every visible text fragment. Pipe through `sort | uniq -c` for frequency analysis, or `grep` for specific keywords.

## Notes

- `tree[0]` is the sidebar, `tree[1][0]` is the top banner, `tree[1][1]` is the main content area. Adjust if the page layout differs. Prefer the universal dump above when unsure of layout.
- Chart data from `SvgRoot` only gives axis labels and legend text — not the bar/line values. For exact values, look for a companion `<table>` element.
- StaticText `name` contains the visible text. `InlineTextBox` children are line-wrapping fragments of the same text. The universal dump deduplicates these naturally because both carry the same `name`.
- `@e` refs appear on interactive elements only — they won't help with data extraction.
- **Admin dashboard pattern**: React SPA dashboards often use nested sidebar menus. Clicking a parent menu item expands its sub-menu but does NOT change the main content. You must then click the sub-item (e.g. "收入报表", "转化报表") to load that page. Always snapshot after a navigation click to confirm the content actually changed — if it didn't, you likely need to click a child menu item.
