# Testing Chrome Extension Content Scripts via WebBridge

> Use WebBridge `evaluate` to test DOM injection logic against real platform pages before deploying the extension.

## When to use

- Building a Chrome extension that injects content into platform editors
- Need to verify DOM selectors work on the LIVE version of a site (not a mock)
- The extension isn't loaded yet and you want fast feedback on injection logic
- End-to-end testing of the full extension pipeline (options page → distribute → verify injection)

## Before you start: find the extension ID

For unpacked dev extensions, the ID is **not** in `~/Library/.../Extensions/` (that's for store-installed extensions). Try these methods in order:

### Method 1: Secure Preferences (most reliable)

```bash
python3 -c "
import json, os
path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Secure Preferences')
with open(path) as f:
    data = json.load(f)
for eid, s in data.get('extensions',{}).get('settings',{}).items():
    name = s.get('manifest',{}).get('name','?')
    if 'your-keyword' in name:
        print(f'{eid}: {name}  path={s.get(\"path\")}')
"
```

Replace `your-keyword` with part of the extension name (e.g. `心河`, `DEV`). If nothing shows up, the extension is **not loaded** — the user must load it from `chrome://extensions/` first.

### Method 2: Compute from build path (unpacked only)

For unpacked extensions loaded via "Load unpacked", Chrome derives the ID from the directory path:

```python
import hashlib, os
build_path = "/absolute/path/to/build/dir"
norm = os.path.normpath(build_path).lower()
h = hashlib.sha256(norm.encode()).digest()
ext_id = ''.join(chr(ord('a')+(b&0x0f))+chr(ord('a')+((b>>4)&0x0f)) for b in h[:16])
print(ext_id)
```

Verify this ID exists in `~/Library/Application Support/Google/Chrome/Default/Local Extension Settings/<id>/`. If the directory doesn't exist, the extension isn't loaded or Chrome re-generated the ID.

### Limitation: WebBridge can't open chrome-extension:// pages of other extensions

WebBridge returns `"Cannot access a chrome-extension:// URL of different extension"`. To interact with the extension's own pages (options.html, sidepanel.html), either:
- Ask the user to open the page manually, then use `find_tab` to attach
- Use osascript (only if Chrome's "Allow JavaScript from Apple Events" is enabled in View → Developer menu)

## Workflow A: Test content script injection directly (no extension UI needed)

### A1. Navigate to the target page

```bash
# Open the platform's editor page
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://editor.csdn.net/md","newTab":true},"session":"test"}'
```

### A2. Wait for load and probe DOM

```bash
sleep 5  # Wait for SPA to render

# Probe via evaluate
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"...JS to find editor elements..."},"session":"test"}'
```

Key things to check:
- Does the page have `textarea`, `contenteditable`, `.CodeMirror`, `.ProseMirror`, `.ql-editor`?
- What class names does the actual editor use?
- Is the editor inside an iframe?

### A3. Test injection

```js
// Simple test: set textContent on the editor and dispatch events
var pre = document.querySelector("pre.editor__inner");
pre.textContent = "# Test Title\n\nTest content...";
pre.dispatchEvent(new Event("input", {bubbles: true}));
pre.dispatchEvent(new Event("change", {bubbles: true}));
```

### A4. Test title injection

```js
var inp = document.querySelector("input[placeholder*='文章标题']");
inp.value = "Test Title";
inp.dispatchEvent(new Event("input", {bubbles: true}));
inp.dispatchEvent(new Event("change", {bubbles: true}));
```

### A5. Update content script selectors, rebuild, commit

## Workflow B: End-to-end extension pipeline test

Test the full extension distribution pipeline: open options page → fill content → distribute to platform → verify content lands in editor.

### B1. Ensure extension is loaded

Use Method 1 from "Before you start" to verify. If not loaded, ask user to load it from `chrome://extensions/`.

### B2. Open the extension's options page

WebBridge **cannot** navigate to `chrome-extension://<id>/options.html` directly. Workarounds:
- Ask user to manually click the extension icon → open options page, then use `find_tab` to attach
- If on macOS with "Allow JavaScript from Apple Events" enabled, use osascript
- Test individual content scripts directly (Workflow A) as fallback

### B3. Interact with the extension UI

Once attached to the options page via `find_tab`, use `snapshot` to find form fields, `fill` to enter test content, `click` to trigger distribution.

### B4. Verify injection on platform

After distribution triggers, the extension opens the platform editor in a new tab. Use `find_tab` (with `active:true`) to attach, then `snapshot` or `screenshot` to verify content landed correctly.

## Pitfalls

### WebBridge evaluate runs in a different context than content scripts
- `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set` fails in WebBridge evaluate (Illegal invocation) but works in real content scripts
- Simple `.value = val` + dispatchEvent works in both contexts

### Login-gated pages
- Some platforms redirect to login (e.g., 简书 writer page). The content script should detect this and return `login_required` so the background worker can skip retries.

### Complex JS quoting
- When passing JS with nested quotes via curl, save the code to a temp file first, or use single quotes with careful escaping
- For large JS blocks, use `execute_code` in Python to construct the JSON payload

### Platform DOM changes between sessions
- What worked today may break tomorrow. Each test session should re-probe the DOM rather than assuming previous selectors are still valid.

## Real Example: CSDN Editor (2025-06)

```
Expected: <textarea> or .CodeMirror
Actual:   <pre class="editor__inner markdown-highlighting" contenteditable="true">
Fix:      Target "pre.editor__inner" instead of textarea/CodeMirror
```

## Related

- Plasmo pitfall: files in `src/contents/` are auto-injected as content scripts. Put shared utilities in `src/lib/` instead.
