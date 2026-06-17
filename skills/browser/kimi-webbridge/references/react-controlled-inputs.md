# React Controlled Inputs — WebBridge Workaround

## Problem

React's synthetic event system uses internal state tracking for controlled inputs. Direct `el.value = 'x'` followed by `dispatchEvent(new Event('input'))` does NOT update React state. The form submits empty values even though the DOM shows text.

**Diagnosis signal**: Form validation says "请完善必填项" (or equivalent) for fields that visually have values.

## Fix: Native Property Setter

```js
var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(element, newValue);
element.dispatchEvent(new Event('input', {bubbles: true}));
element.dispatchEvent(new Event('change', {bubbles: true}));
```

For textareas, use `HTMLTextAreaElement.prototype`.

## Bulk Fill Pattern

```js
var inpSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
var taSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
var inputs = document.querySelectorAll('input,textarea');
var values = ['url', 'branch', '.', 'name', 'description', 'tags'];
for (var i = 0; i < values.length && i < inputs.length; i++) {
  var el = inputs[i];
  var setter = el.tagName === 'TEXTAREA' ? taSetter : inpSetter;
  setter.call(el, values[i]);
  el.dispatchEvent(new Event('input', {bubbles: true}));
  el.dispatchEvent(new Event('change', {bubbles: true}));
}
```

## Verified On

- 心河Paper (Next.js + Ant Design + React)
- Form validation correctly passes after using this technique
