---
name: fal-ai-media
description: Use when generating images, video, or audio via the fal.ai MCP server. Covers MCP config, the tool set, model app_ids with per-model parameter schemas (Nano Banana, Seedance, Kling, Veo 3, CSM-1B, ThinkSound), and cost-estimate call shapes.
---

# fal.ai Media Generation

## MCP Setup

Add to `~/.claude.json` (API key from fal.ai):

```json
"fal-ai": {
  "command": "npx",
  "args": ["-y", "fal-ai-mcp-server"],
  "env": { "FAL_KEY": "YOUR_FAL_KEY_HERE" }
}
```

MCP tools: `search` (find models by keyword), `find` (model details/parameters), `generate` (run a model), `result` / `status` (async job state), `cancel`, `estimate_cost`, `models` (list popular), `upload` (upload local files for use as inputs).

## Image Models

| app_id | Use for |
|--------|---------|
| `fal-ai/nano-banana-2` | fast iteration, drafts, image editing |
| `fal-ai/nano-banana-pro` | production quality, realism, typography |

```
generate(
  app_id: "fal-ai/nano-banana-2",
  input_data: {
    "prompt": "a futuristic cityscape at sunset, cyberpunk style",
    "image_size": "landscape_16_9",
    "num_images": 1,
    "seed": 42
  }
)
```

Image parameters:

| Param | Type | Values | Notes |
|-------|------|--------|-------|
| `prompt` | string | required | |
| `image_size` | string | `square`, `portrait_4_3`, `landscape_16_9`, `portrait_16_9`, `landscape_4_3` | |
| `num_images` | number | 1-4 | |
| `seed` | number | any integer | reproducibility |
| `guidance_scale` | number | 1-20 | higher = more literal prompt adherence |
| `image_url` | string | URL | source image for editing/style transfer |

Image editing (inpainting, outpainting, style transfer) with Nano Banana 2: `upload(file_path: "/path/to/image.png")` first, then pass the returned URL as `image_url` alongside the prompt.

## Video Models

| app_id | Notes |
|--------|-------|
| `fal-ai/seedance-1-0-pro` | ByteDance; text-to-video and image-to-video, high motion quality |
| `fal-ai/kling-video/v3/pro` | text/image-to-video with native audio generation |
| `fal-ai/veo-3` | Google DeepMind; video with generated sound |

```
generate(
  app_id: "fal-ai/seedance-1-0-pro",
  input_data: {
    "prompt": "a drone flyover of a mountain lake at golden hour, cinematic",
    "duration": "5s",
    "aspect_ratio": "16:9",
    "seed": 42
  }
)
```

Video parameters:

| Param | Type | Values |
|-------|------|--------|
| `prompt` | string | required |
| `duration` | string | `"5s"`, `"10s"` |
| `aspect_ratio` | string | `"16:9"`, `"9:16"`, `"1:1"` |
| `seed` | number | any integer |
| `image_url` | string | source image for image-to-video |

Image-to-video (pass an uploaded `image_url` plus a motion-focused prompt) gives more controlled results than pure text-to-video.

## Audio Models

CSM-1B - conversational text-to-speech:

```
generate(
  app_id: "fal-ai/csm-1b",
  input_data: {
    "text": "Hello, welcome to the demo.",
    "speaker_id": 0
  }
)
```

ThinkSound - video-to-audio (soundtrack/SFX matching video content):

```
generate(
  app_id: "fal-ai/thinksound",
  input_data: {
    "video_url": "<video_url>",
    "prompt": "ambient forest sounds with birds chirping"
  }
)
```

## Cost Estimation

Check before expensive (especially video) generations:

```
estimate_cost(
  estimate_type: "unit_price",
  endpoints: {
    "fal-ai/nano-banana-pro": { "unit_quantity": 1 }
  }
)
```

## Discovery

```
search(query: "text to video")
find(endpoint_ids: ["fal-ai/seedance-1-0-pro"])
models()
```

## Tips

- Fix `seed` while iterating on prompts for comparable results.
- Iterate on the cheap model (`nano-banana-2`), switch to Pro for finals.
- Video prompts: descriptive but concise, focused on motion and scene.
