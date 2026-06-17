# Screenshot-to-Video Tutorial Workflow

Full pipeline for creating narrated tutorial/product-demo videos from browser screenshots + TTS + HyperFrames. Proven with 心河Paper tutorial (77.5s, 10 scenes, 8.1MB final).

## Phase 1: Capture Screenshots

Use Kimi WebBridge to navigate through the product workflow and capture each step:

```bash
# Health check
~/.kimi-webbridge/bin/kimi-webbridge status

# Screenshot at each step
bash /path/to/screenshot.sh -s hermes -o screenshots/stepN-description.png
```

Key principle: **screenshot at every screen state change**, even "loading" or "initializing" states — they become scenes. Don't skip transient states; they add authenticity.

Capture areas:
- Full page for broad context scenes (homepage, template selection)
- Consider cropping or zoom annotations for detail scenes (specific button, input field)
- If the same screenshot serves two scenes, vary with CSS `transform: scale()` to focus different regions

## Phase 2: Script + TTS

Write scene-by-scene narration script (SCRIPT.md), then generate TTS per scene:

```bash
# Chinese TTS (Edge-TTS — no espeak-ng needed)
python3 -m edge_tts --voice zh-CN-XiaoxiaoNeural --rate=-5% \
  --text "旁白文字" --write-media audio/sceneN_name.wav

# Get exact duration
ffprobe -v error -show_entries format=duration \
  -of default=nw=1:nk=1 audio/sceneN_name.wav
```

Use per-scene audio files (not one long file) — this gives exact duration for each scene's `data-duration` and allows independent scene editing.

## Phase 3: Timeline Math

Build the timeline from TTS durations. Round to 0.01s precision with a 0.01s gap between adjacent clips to avoid HyperFrames floating-point overlap errors:

```
Scene 1: 0      → 11.79  (11.79s TTS)
Scene 2: 11.80  → 18.59  (6.79s  TTS)
Scene 3: 18.60  → 25.99  (7.39s  TTS)
...
```

Each scene's `data-duration` = TTS_duration - 0.01. Next scene's `data-start` = previous end + 0.01.

## Phase 4: HyperFrames Composition

Single `index.html` with all scenes on track 0, audio on track 1, transition overlay on track 2.

Template structure for each scene:
```html
<div id="sN" class="clip" data-start="X" data-duration="Y" data-track-index="0">
  <div class="scene">
    <div id="sN-step" class="scene-step">Step N</div>
    <img id="sN-img" src="assets/stepN.png" />
    <div id="sN-label" class="scene-label">描述文字</div>
  </div>
</div>
```

Crossfade transition pattern:
```js
const boundaries = [11.79, 18.59, ...];  // scene boundaries
const fadeDur = 0.3;
boundaries.forEach(function(t) {
  tl.to("#trans", { opacity: 1, duration: fadeDur }, t - fadeDur);
  tl.to("#trans", { opacity: 0, duration: fadeDur }, t + fadeDur);
});
```

Entrance animations per scene (staggered 0.3s apart, using varied eases):
```js
tl.from("#sN-step", { opacity: 0, x: -30, duration: 0.6, ease: "power2.out" }, boundary + 0.2);
tl.from("#sN-img",  { opacity: 0, scale: 0.95, duration: 0.8, ease: "power3.out" }, boundary + 0.2);
tl.from("#sN-label",{ opacity: 0, y: 15, duration: 0.6, ease: "power2.out" }, boundary + 0.5);
```

## Phase 5: Render

```bash
# Fast iteration
npx hyperframes render --quality draft --output draft.mp4

# Final delivery
npx hyperframes render --quality high --output final.mp4
```

## Pitfalls Specific to This Workflow

1. **Font mapping**: Chinese system fonts ("PingFang SC", "Microsoft YaHei") aren't in HyperFrames' deterministic font registry. Use "Noto Sans SC" which is supported and auto-fetched from Google Fonts. Add "PingFang SC", "Microsoft YaHei" as fallbacks in the CSS font-family stack for local preview, but expect the compiler warning.
2. **TTS timing precision**: Edge-TTS durations vary slightly per run. Generate all audio once, measure with ffprobe, and lock the timeline to those exact values.
3. **Duplicate image warning**: Using the same screenshot in adjacent scenes (e.g., search result + template selection) triggers `duplicate_media_discovery_risk`. This is cosmetic — accept the warning or use CSS `object-position` to show different regions of the same image.
4. **Track density warning**: 10+ clips on a single track triggers `timeline_track_too_dense`. Acceptable for simple tutorial videos under 20 scenes. For larger projects, split into sub-compositions.
