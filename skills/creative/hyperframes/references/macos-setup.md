# macOS Setup Quirks

## chrome-headless-shell install failures

**Symptom:** `npx puppeteer browsers install chrome-headless-shell` (or `scripts/setup.sh`) fails with:

```
Error: All providers failed for chrome 148.0.7778.97:
  DefaultProvider: The browser folder exists but the executable is missing
```

**Cause:** Corrupted puppeteer cache from a previous interrupted download.

**Fix:**
```bash
# Clear the corrupt cache entry
rm -rf ~/.cache/puppeteer/chrome/mac_arm-148.0.7778.97

# Retry
npx puppeteer browsers install chrome-headless-shell
```

**Skip entirely:** HyperFrames 0.4.2+ auto-detects and falls back to system Chrome screenshot mode. On macOS with `/Applications/Google Chrome.app` present, rendering works without chrome-headless-shell (verified: 0.6.2, 8.6s render for 10s/30fps). Use `--quality draft` for fast iteration.

## setup.sh timeout

On slow connections, the `npx puppeteer browsers install` step in setup.sh can exceed the default 120s timeout. The script sets HYPERFRAMES_CLI_VERSION so the `npm install -g hyperframes` step completes; only the browser install may hang. System Chrome is sufficient — no need to re-run setup.sh.
