# Multi-Scene Composition: Common Lint Errors and Fixes

When building a single `index.html` with multiple scenes (each a `<div class="scene clip">`
with its own `data-start`/`data-duration`), these lint errors commonly appear.
Each section shows the error, the cause, and the fix.

## overlapping_clips_same_track

**Error:** `Track N: clip ending at Xs overlaps with clip starting at Xs.`

**Cause:** Two clips on the same `data-track-index` share an exact boundary
(e.g., scene6 ends at 193.6s and scene7 starts at 193.6s). The lint requires
non-overlapping ranges.

**Fix:** Add a 0.2–0.5s gap between scene boundaries. Example:

```html
<!-- Scene 6: ends at 157.3 + 36.2 = 193.5 -->
<div id="scene6" data-start="157.3" data-duration="36.2" data-track-index="0">
<!-- Scene 7: starts at 193.7 (0.2s gap) -->
<div id="scene7" data-start="193.7" data-duration="37.7" data-track-index="0">
```

Adjust audio `data-start`/`data-duration` to match, and offset GSAP sceneOut/sceneIn
calls accordingly. The 0.2s gap is imperceptible in playback.

## timed_element_missing_clip_class

**Error:** `<div id="progress"> has timing attributes but no class="clip".`

**Cause:** An element with `data-start`/`data-duration`/`data-track-index` lacks
`class="clip"`. The runtime uses `.clip` for visibility control.

**Fix:** Add `class="clip"` to the element:

```html
<div class="progress-bar clip" id="progress" data-start="0" data-duration="231.4" data-track-index="98"></div>
```

## scene_layer_missing_visibility_kill

**Warning:** `Scene layer "#scene7" exits via opacity tween but has no visibility: hidden hard kill.`

**Cause:** The final scene fades to `opacity:0` but never gets `visibility:hidden`.
During non-linear seeking, the scene may become partially visible again.

**Fix:** Add a hard `tl.set()` kill at the end time:

```js
tl.to("#scene7", { opacity: 0, duration: 1.0, ease: "power2.in" }, 230.4);
tl.set("#scene7", { visibility: "hidden" }, 231.4); // ← hard kill
```

This applies to the LAST scene only (the only one allowed to use exit animations).

## duplicate_audio_track

**Warning:** `Multiple <audio> elements on track 99 overlap.`

**Cause:** Consecutive `<audio>` elements on the same track share a boundary
and are flagged as overlapping. Same root cause as overlapping_clips_same_track.

**Fix:** Same gap fix — adjust audio `data-start`/`data-duration` to match the
gapped scene timings:

```html
<audio id="audio6" data-start="157.3" data-duration="36.2" data-track-index="99" src="assets/scene6.wav"></audio>
<audio id="audio7" data-start="193.7" data-duration="37.7" data-track-index="99" src="assets/scene7.wav"></audio>
```

## timeline_track_too_dense (warning, not error)

**Warning:** `Track 0 has 7 timed elements in this HTML file.`

This is a style suggestion, not a blocking error. It recommends splitting into
sub-compositions under `compositions/`. For simple multi-scene videos with
CSS crossfade transitions, a single-file approach is acceptable. Ignore for
videos with ≤10 scenes.

## CSS Crossfade Transition Pattern

The simplest multi-scene transition that passes lint cleanly:

```js
function sceneIn(id, at) {
  tl.set("#" + id, { opacity: 0, visibility: "visible" }, at);
  tl.to("#" + id, { opacity: 1, duration: 0.6, ease: "power2.inOut" }, at + 0.1);
}
function sceneOut(id, at) {
  tl.to("#" + id, { opacity: 0, duration: 0.5, ease: "power2.in" }, at);
  tl.set("#" + id, { visibility: "hidden" }, at + 0.5);
}
```

Each scene div needs:
```css
.scene { position: absolute; inset: 0; opacity: 0; visibility: hidden; }
```
