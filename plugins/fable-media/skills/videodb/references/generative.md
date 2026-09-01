# Generative Media

All generation methods live on the `Collection` object. Generated media is persisted in the collection and usable immediately as timeline assets or search targets.

## Image

```python
image = coll.generate_image(prompt="a futuristic cityscape at sunset", aspect_ratio="16:9")
url = image.generate_url()   # signed URL; image.url may be None for generated images
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | required | |
| `aspect_ratio` | `str` | `"1:1"` | `"1:1"`, `"9:16"`, `"16:9"`, `"4:3"`, `"3:4"` |
| `callback_url` | `str\|None` | `None` | Async webhook |

Note: `Video` uses `.generate_stream()`; `Image` uses `.generate_url()`. `image.url` is populated only for some image types (e.g. thumbnails).

## Video

```python
video = coll.generate_video(prompt="a timelapse of a flower blooming", duration=5)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | required | |
| `duration` | `int` | `5` | Integer seconds, range 5-8 |
| `callback_url` | `str\|None` | `None` | |

Plan-gated ("Operation not allowed" on free tier).

## Audio — three separate methods, no unified generate_audio()

```python
music = coll.generate_music(prompt="upbeat electronic, driving beat", duration=30)   # default duration=5
sfx = coll.generate_sound_effect(prompt="thunderstorm with heavy rain", duration=10) # default duration=2, extra: config={}
voice = coll.generate_voice(text="Welcome to the demo.", voice_name="Default")       # extra: config={}
```

All accept `callback_url` and return `Audio` (`.id`, `.name`, `.length`, `.collection_id`).

## Text (LLM)

Collection-level; it has no automatic access to video content — fetch the transcript and put it in the prompt.

```python
transcript_text = video.get_transcript_text()
result = coll.generate_text(
    prompt=f"Summarize the key points:\n{transcript_text}",
    model_name="pro",          # "basic" (fast) | "pro" (balanced) | "ultra" (best)
    response_type="text",      # "text" -> output is str; "json" -> output is dict
)
print(result["output"])        # result is a dict; actual content under "output"
```

Structured output: instruct JSON shape in the prompt and set `response_type="json"`; `result["output"]` is then a dict.

## Dubbing and translation

```python
dubbed = coll.dub_video(video_id=video.id, language_code="es")   # returns Video; also accepts callback_url

translated = video.translate_transcript(language="Spanish", additional_notes="Use formal tone")
# returns list[dict]; no dubbing
```

Supported language codes include `en`, `es`, `fr`, `de`, `it`, `pt`, `ja`, `ko`, `zh`, `hi`, `ar`.

## Example: video plus generated music

```python
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset

music = coll.generate_music(prompt="calm ambient background for a tutorial", duration=60)
timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video.id))
timeline.add_overlay(0, AudioAsset(asset_id=music.id, disable_other_tracks=False))
stream_url = timeline.generate_stream()
```
