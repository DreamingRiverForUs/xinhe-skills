# AI Information Source Research Pattern

## When to use this

When the user asks you to research and compile information sources (X accounts, subreddits, Discord servers, etc.) via browser.

## CRITICAL: Always use isolated sessions for parallel research

**Each independent research query needs its own session.** Sessions are separate browser tab groups. Without distinct sessions, tabs collide and snapshots return wrong pages. The user will correct you if you don't do this.

```
# Parallel research — three sessions, no interference
{"session": "ai-discord"}  → search Discord servers
{"session": "ai-reddit"}   → search subreddits  
{"session": "search-2"}    → search X accounts
```

Close all sessions at the end with `close_session`.

## The pattern: Google → Reddit, not Google → blogs

### Step 1: Search Google for the topic

Use WebBridge to navigate to Google and search for "[topic] list 2026 best". Example searches:
- `best AI X Twitter accounts follow 2026 list`
- `best AI subreddits 2026 list`
- `best AI Discord servers developers 2026`

### Step 2: Scan search results via snapshot

Use `snapshot` to read the accessibility tree. Google result snippets are rich — they contain actual account names and descriptions even before opening the link. Extract text from the snapshot to identify promising sources.

### Step 3: Skip blog listicles — they're mostly 404

Blog listicle articles (pasqualepillitteri.it, amperly.com, softwarethug.com, tweetstorm.ai, braiviq.com, mediafast.ai, promptquest.ai) are frequently dead links. Don't waste time navigating to them. If you must try one, verify with a quick evaluate of `document.body.innerText` before committing to extraction.

### Step 4: Go to Reddit directly

The reliable source pattern: **community-curated Reddit posts stay alive**. The workflow:
1. Navigate to `reddit.com/r/[relevant-sub]/search/?q=[topic]+list+2026&sort=relevance`
2. Snapshot to find the top Reddit post
3. Click into the post → evaluate `document.body.innerText` to extract the full list

For example, r/ArtificialInteligence has a comprehensive "List of the best AI subreddits" post by u/JensPetrus from ~4mo ago that's still live and covers 64 subreddits.

### Step 5: For Discord servers, skip Disboard

Disboard (disboard.org) has Cloudflare anti-bot protection. Instead, use known invite links (discord.gg/anthropic, discord.gg/nousresearch, huggingface.co/join/discord) or search Reddit for "AI Discord servers list".

## X (Twitter) account verification

### Step A: Batch-verify handles via curl (fast, no browser needed)

Before using WebBridge, batch-check likely handles with a shell loop. X returns 200 for existing profiles, 404 for non-existent, 403 for private/suspended:

```bash
for handle in AnthropicAI OpenAI karpathy sama deepseek_ai; do
  code=$(curl -sI -o /dev/null -w "%{http_code}" --max-time 5 "https://x.com/$handle" 2>&1)
  echo "$code https://x.com/$handle"
done
```

Run with 30-50 handles at once. Only navigate to 200-returning handles with WebBridge.

### Step B: Verify profile identity via WebBridge snapshot

After `navigate` to the X profile, use `snapshot` (NOT `evaluate` — X profiles may not load innerText due to login walls). The accessibility tree captures the display name, bio text, and recent posts. This is sufficient to distinguish the real account from impostors.

Key signals in snapshot:
- Display name matches expected (e.g., "Kimi.ai" not "kimi aulia")
- Bio contains relevant keywords (e.g., "Moonshot", "AI", "Baichuan")
- Post count and content align with official use
- "Verified account" badge appears in the tree

### Pitfall: X profile evaluate often returns empty

`evaluate` with `document.body.innerText` on X profiles frequently returns only the sidebar navigation — not the profile content. This is likely due to X's dynamic rendering. **Always use `snapshot` as the primary reading method for X profiles.** The accessibility tree reliably captures profile bio, display name, and post text.

### Step C: For Chinese AI figures, expect low hit rate

Many Chinese AI founders (王小川, 杨植麟) do not maintain public English X accounts. Try 5-10 common handle patterns, and if all fail with 404, mark as "not found on X" and move on. Their company accounts (@BaichuanAI, @Kimi_Moonshot) are more likely to exist.

### Step D: X search for account discovery

Use X's own search with `f=user` filter to find accounts by display name:
```
https://x.com/search?q=[URL-encoded-name]&src=typed_query&f=user
```

This is more reliable than Google for finding specific X accounts, but may return empty results for accounts with low X presence.
