# Hermes Setup: zenmux-image-generation

Key learnings from the initial install session (2026-05-13).

## Installation

```bash
# Clone the skill repo
GIT_SSL_NO_VERIFY=1 git clone --depth 1 https://github.com/ZenMux/skills.git /tmp/zenmux-skills

# Copy to Hermes
cp -r /tmp/zenmux-skills/skills/zenmux-image-generation ~/.hermes/skills/creative/zenmux-image-generation

# Install Python deps
cd ~/.hermes/skills/creative/zenmux-image-generation
uv sync --project .
```

## API Key Configuration

Add to `~/.hermes/.env`:
```
ZENMUX_API_KEY=sk-ai-v1-...
```

Or use:
```bash
hermes config set ZENMUX_API_KEY "sk-ai-v1-..."
```

## 403 Protocol Trap

The most important lesson from this session: gpt-image-2 on ZenMux uses **Vertex AI protocol** by default, NOT OpenAI Images protocol.

| What | Endpoint | Result |
|------|----------|--------|
| OpenAI Images protocol (`/api/v1/images/generations`) | `https://zenmux.ai/api/v1/images/generations` | 403 even with valid key |
| Vertex AI protocol | `https://zenmux.ai/api/vertex-ai` | Works |

**Always prefer `scripts/generate_gemini.py` for gpt-image-2.** Only use `scripts/generate_openai.py` when the user explicitly requests OpenAI Images protocol.

## Key Validity Check

The old key `sk-mg-v1-...` could list models but couldn't call any models (text or image — all 403). The new key `sk-ai-v1-...` works for both text and image. Diagnostic: if models list succeeds but all calls 403, the key lacks execution permissions — user needs to check ZenMux dashboard.

## Script Invocation Pattern

All paths must be absolute for Hermes terminal() calls:

```bash
export ZENMUX_API_KEY="sk-ai-v1-..."
uv run --project ~/.hermes/skills/creative/zenmux-image-generation python \
  ~/.hermes/skills/creative/zenmux-image-generation/scripts/generate_gemini.py \
  --model "openai/gpt-image-2" \
  --prompt-file /path/to/prompt.md \
  --n 1 --size "1024x1024" --quality medium \
  --output-dir /tmp/zenmux-output
```

## Available Image Models

As of 2026-05-13, 12 models via Vertex AI:
- openai/gpt-image-2 (default)
- openai/gpt-image-1.5
- google/gemini-3-pro-image-preview
- google/gemini-3.1-flash-image-preview
- google/gemini-2.5-flash-image
- qwen/qwen-image-2.0-pro / qwen/qwen-image-2.0
- bytedance/doubao-seedream-5.0-lite
- baidu/ernie-image-turbo
- z-ai/glm-image
- tencent/hy-image-v3.0
- klingai/kling-v2
