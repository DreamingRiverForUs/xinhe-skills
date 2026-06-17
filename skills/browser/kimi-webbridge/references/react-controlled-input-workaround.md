# React Controlled Input Workaround

When automating form filling on React SPAs via WebBridge `evaluate`, setting `element.value = 'xxx'` and dispatching `input`/`change` events **does NOT update React's internal state**. React hooks into the native value setter on the input prototype, bypassing direct property assignment.

## Symptom

- `element.value` shows the expected value in DOM
- But React form validation says "field is required" or "please fill in required fields"
- Form submission sends empty values

## Solution

Use `Object.getOwnPropertyDescriptor` to get the native setter and call it directly:

```js
var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
nativeSetter.call(element, 'new value');
element.dispatchEvent(new Event('input', {bubbles: true}));
element.dispatchEvent(new Event('change', {bubbles: true}));
```

For textareas, use the TextAreaElement prototype:

```js
var nativeTextareaSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
nativeTextareaSetter.call(textarea, 'new value');
```

## Bulk Fill Pattern

```js
(function(){
var nativeInputSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
var nativeTextareaSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
var vals = ['url', 'branch', 'subdir', 'name', 'description', 'tags'];
var inp = document.querySelectorAll('input,textarea');
for (var i = 0; i < vals.length && i < inp.length; i++) {
  var el = inp[i];
  var v = vals[i];
  if (el.tagName === 'TEXTAREA') nativeTextareaSetter.call(el, v);
  else nativeInputSetter.call(el, v);
  el.dispatchEvent(new Event('input', {bubbles: true}));
  el.dispatchEvent(new Event('change', {bubbles: true}));
}
})()
```

## Verified On

- 心河Paper (paper.huimengxinhe.com) — Next.js + React SPA, template import form (2026-06-14)
- Pattern applies to any React controlled-input form (antd, shadcn/ui, react-hook-form, etc.)
