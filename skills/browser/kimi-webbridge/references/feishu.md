# Feishu (飞书) Web Client Interaction Patterns

## Navigation

- Marketing site: `https://www.feishu.cn/` — not the web client
- The "网页版" link on the marketing site may open a popup; prefer direct navigation
- Web client URL: `https://www.feishu.cn/messenger/` → redirects to `https://<workspace>.feishu.cn/next/messenger/`
- After `close_session`, a fresh `navigate` with `newTab:true` works reliably

## Chat List Navigation

- **Chat items do NOT have accessible @e refs** in the Feishu DOM — the accessibility tree shows them as `StaticText` in groups without clickable roles
- **Workaround**: Use `document.createTreeWalker` to find text nodes, locate the target name, and click the nearest clickable parent element:

```javascript
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
let node;
while (node = walker.nextNode()) {
  if (node.textContent.trim() === "刘琪") {
    // Walk up to find a clickable container
    let el = node.parentElement;
    while (el && el !== document.body) {
      if (el.closest("[class*=list]") || el.closest("[class*=chat]") || 
          el.closest("[class*=conversation]")) {
        el.click();
        break;
      }
      el = el.parentElement;
    }
    break;
  }
}
```

## Typing Messages

- **`fill` action FAILS** on Feishu's `div[contenteditable=true]` — returns `"extension_error: fill: Uncaught"`
- **Workaround**: Set `textContent` directly and dispatch `InputEvent`:

```javascript
const editable = document.querySelector("div[contenteditable=true]");
editable.focus();
editable.textContent = "your message here";
editable.dispatchEvent(new InputEvent("input", {
  bubbles: true, inputType: "insertText", data: "your message here"
}));
editable.dispatchEvent(new Event("change", {bubbles: true}));
```

## Sending Messages

- Press **Enter** on the contenteditable div (Shift+Enter for newline):

```javascript
editable.dispatchEvent(new KeyboardEvent("keydown", {
  key: "Enter", code: "Enter", keyCode: 13, which: 13,
  bubbles: true, cancelable: true
}));
```

## Uploading Images

- **No `<input type="file">` elements** exist in Feishu's DOM — Feishu uses a custom upload pipeline
- **Reliable method**: Clipboard paste via `DataTransfer`:

```javascript
// 1. Get image data (from fetch, embedded base64, or local server)
// 2. Create File object
const blob = new Blob([byteArray], {type: "image/png"});
const file = new File([blob], "screenshot.png", {type: "image/png"});

// 3. Create DataTransfer and add file
const dt = new DataTransfer();
dt.items.add(file);

// 4. Focus editable area and dispatch paste
const editable = document.querySelector("div[contenteditable=true]");
editable.focus();
editable.dispatchEvent(new ClipboardEvent("paste", {
  bubbles: true, cancelable: true, clipboardData: dt
}));

// 5. Wait for upload to process (~3s), then send
await new Promise(r => setTimeout(r, 3000));
```

### Getting image data into the browser

**Preferred: Embed base64 in evaluate** — evaluate calls handle payloads up to ~230KB:
```python
with open('screenshot.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
# Build JS with b64 string embedded in the code
```

**Fallback: Local HTTP server** — HTTPS pages block `fetch` to HTTP origins:
```bash
cd /tmp && python3 -m http.server 9876  # background
```
Note: Feishu is HTTPS → browser blocks `fetch("http://127.0.0.1:9876/...")` as mixed content. Embed base64 directly instead.

### Sending the pasted image

After paste, Feishu shows an upload preview with a title field (`textbox` role, name="无标题"). The send button appears in the toolbar. Press Enter on the editable area to send, or click the send button in the toolbar group (typically the last button among @e36-@e39).

## Pitfalls

- **Don't use `fill` on Feishu** — always use JavaScript textContent + InputEvent
- **Don't rely on @e refs for chat items** — use TreeWalker text search
- **Don't try HTTP fetches from HTTPS Feishu** — mixed content blocked; embed base64
- **After paste, wait ~3s** for Feishu to process the image before sending
- **`close_session` before `navigate`** avoids stale tab reference errors
