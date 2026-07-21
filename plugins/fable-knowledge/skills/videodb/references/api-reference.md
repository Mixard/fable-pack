# VideoDB API Reference

## Connection

```python
import videodb

conn = videodb.connect(
    api_key="your-api-key",   # or set VIDEO_DB_API_KEY env var
    base_url=None,            # custom API endpoint (optional)
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `conn.get_collection(collection_id="default")` | `Collection` | Get collection |
| `conn.get_collections()` | `list[Collection]` | List collections |
| `conn.create_collection(name, description, is_public=False)` | `Collection` | Create collection (plan-gated) |
| `conn.update_collection(id, name, description)` | `Collection` | Update collection |
| `conn.check_usage()` | `dict` | Account usage stats |
| `conn.upload(source, media_type, name, ...)` | `Video\|Audio\|Image` | Upload to default collection |
| `conn.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | Record a meeting |
| `conn.create_capture_session(...)` | `CaptureSession` | See capture.md |
| `conn.youtube_search(query, result_threshold, duration)` | `list[dict]` | Search YouTube |
| `conn.transcode(source, callback_url, mode, ...)` | `str` | Transcode (returns job ID) |
| `conn.get_transcode_details(job_id)` | `dict` | Transcode job status |
| `conn.connect_websocket(collection_id)` | `WebSocketConnection` | See capture.md |
| `conn.create_event(event_prompt, label)` | `str` | Detection event (see rtstream.md) |
| `conn.list_events()` | `list` | List detection events |

## Transcode

Server-side transcode from a URL — no local ffmpeg.

```python
from videodb import TranscodeMode, VideoConfig, AudioConfig, ResizeMode

job_id = conn.transcode(
    source="https://example.com/video.mp4",   # required, downloadable URL
    callback_url="https://example.com/webhook",  # required
    mode=TranscodeMode.economy,               # economy | lightning
    video_config=VideoConfig(resolution=720, quality=23, aspect_ratio="16:9"),
    audio_config=AudioConfig(mute=False),
)
details = conn.get_transcode_details(job_id)
```

`VideoConfig` fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `resolution` | `int\|None` | `None` | Target height in px (480, 720, 1080, ...) |
| `quality` | `int` | `23` | Encoding quality (lower = better) |
| `framerate` | `int\|None` | `None` | Target framerate |
| `aspect_ratio` | `str\|None` | `None` | e.g. `"16:9"`, `"9:16"` |
| `resize_mode` | `str` | `ResizeMode.crop` | `crop`, `fit`, or `pad` |

`AudioConfig`: single field `mute: bool = False`.

## Collection

| Method | Returns | Description |
|--------|---------|-------------|
| `coll.get_videos()` / `get_video(id)` | `list[Video]` / `Video` | |
| `coll.get_audios()` / `get_audio(id)` | `list[Audio]` / `Audio` | |
| `coll.get_images()` / `get_image(id)` | `list[Image]` / `Image` | |
| `coll.upload(url=None, file_path=None, media_type=None, name=None, description=None, callback_url=None)` | `Video\|Audio\|Image` | `media_type` auto-detected if omitted; URL, YouTube URL, or local path |
| `coll.search(query, search_type, index_type, score_threshold, namespace, scene_index_id, ...)` | `SearchResult` | Semantic only; keyword/scene raise `NotImplementedError` |
| `coll.generate_image(prompt, aspect_ratio="1:1")` | `Image` | |
| `coll.generate_video(prompt, duration=5)` | `Video` | Plan-gated |
| `coll.generate_music(prompt, duration=5)` | `Audio` | |
| `coll.generate_sound_effect(prompt, duration=2)` | `Audio` | |
| `coll.generate_voice(text, voice_name="Default")` | `Audio` | |
| `coll.generate_text(prompt, model_name="basic", response_type="text")` | `dict` | Result in `["output"]` |
| `coll.dub_video(video_id, language_code)` | `Video` | |
| `coll.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | |
| `coll.create_capture_session(...)` / `get_capture_session(...)` | `CaptureSession` | See capture.md |
| `coll.connect_rtstream(url, name, ...)` | `RTStream` | See rtstream.md |
| `coll.get_rtstream(id)` / `list_rtstreams(...)` | `RTStream` / `list[RTStream]` | See rtstream.md |
| `coll.make_public()` / `make_private()` | `None` | |
| `coll.delete_video(id)` / `delete_audio(id)` / `delete_image(id)` / `delete()` | `None` | |

## Video

Properties: `id`, `collection_id`, `name`, `description`, `length` (float seconds), `stream_url`, `player_url`, `thumbnail_url`.

| Method | Returns | Description |
|--------|---------|-------------|
| `video.generate_stream(timeline=None)` | `str` | Stream URL; `timeline=[(start, end), ...]` streams only those segments |
| `video.play()` | `str` | Open stream in browser, returns player URL |
| `video.index_spoken_words(language_code=None, segmentation_type=SegmentationType.sentence, force=False, callback_url=None)` | `None` | Speech index; `force=True` skips "already exists" error |
| `video.index_scenes(extraction_type, prompt, extraction_config, metadata, model_name, name, scenes, callback_url)` | `str` | Returns `scene_index_id`; no `force` param — see search.md |
| `video.index_visuals(prompt, batch_config, ...)` | `str` | Returns scene_index_id |
| `video.index_audio(prompt, model_name, ...)` | `str` | LLM audio index, returns scene_index_id |
| `video.get_transcript(start=None, end=None)` | `list[dict]` | Timestamped transcript |
| `video.get_transcript_text(start=None, end=None)` | `str` | Plain transcript |
| `video.generate_transcript(force=None)` | `dict` | |
| `video.translate_transcript(language, additional_notes)` | `list[dict]` | |
| `video.search(query, search_type, index_type, filter, **kwargs)` | `SearchResult` | Raises `InvalidRequestError` "No results found" on no match |
| `video.add_subtitle(style=SubtitleStyle())` | `str` | Burned-in subtitles, returns stream URL |
| `video.generate_thumbnail(time=None)` | `str\|Image` | |
| `video.get_thumbnails()` | `list[Image]` | |
| `video.extract_scenes(extraction_type, extraction_config)` | `SceneCollection` | |
| `video.reframe(start, end, target, mode, callback_url)` | `Video\|None` | See below |
| `video.clip(prompt, content_type, model_name)` | `str` | Prompt-generated clip, returns stream URL |
| `video.insert_video(video, timestamp)` | `str` | |
| `video.download(name=None)` | `dict` | |
| `video.delete()` | `None` | |

### Reframe

Slow server-side operation (minutes on long videos, can time out). Limit with `start`/`end` or use `callback_url` for async; for full-length videos, trim on a `Timeline` first and reframe the shorter result.

```python
from videodb import ReframeMode

reframed = video.reframe(start=0, end=60, target="vertical", mode=ReframeMode.smart)
video.reframe(target="vertical", callback_url="https://example.com/webhook")  # async, returns None
reframed = video.reframe(start=0, end=60, target={"width": 1080, "height": 1080})
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start` / `end` | `float\|None` | `None` | Segment bounds in seconds (None = full) |
| `target` | `str\|dict` | `"vertical"` | `"vertical"` (9:16), `"square"` (1:1), `"landscape"` (16:9), or `{"width": int, "height": int}` |
| `mode` | `str` | `ReframeMode.smart` | `"simple"` (center crop) or `"smart"` (object tracking) |
| `callback_url` | `str\|None` | `None` | Async webhook; when set, returns `None` |

## Audio

Properties: `id`, `collection_id`, `name`, `length`.
Methods: `generate_url()` (signed playback URL), `get_transcript(start, end)`, `get_transcript_text(start, end)`, `generate_transcript(force=None)`, `delete()`.

## Image

Properties: `id`, `collection_id`, `name`, `url` (may be `None` for generated images — use `generate_url()`).
Methods: `generate_url()` (signed URL), `delete()`.

## video.search parameters

```python
results = video.search(
    query="your query",
    search_type=SearchType.semantic,     # semantic, keyword, scene, llm
    index_type=IndexType.spoken_word,    # spoken_word or scene
    result_threshold=None,               # max results
    score_threshold=None,                # minimum relevance score
    dynamic_score_percentage=None,
    scene_index_id=None,                 # passed via **kwargs to the API
    filter=[],                           # metadata filters for scene search (named param)
)
```

`filter` is a named parameter; `scene_index_id` goes through `**kwargs`. Raises `InvalidRequestError` "No results found" on no match.

## SearchResult and Shot

`results.get_shots() -> list[Shot]`, `results.compile() -> str` (single stream of all hits), `results.play() -> str`.

Shot properties: `video_id`, `video_length`, `video_title`, `start`, `end`, `text` (matched content), `search_score`.
Shot methods: `generate_stream() -> str`, `play() -> str`.

## Meeting

```python
meeting = coll.record_meeting(
    meeting_url="https://meet.google.com/...",
    bot_name="Bot",
    callback_url=None,
    callback_data=None,     # dict passed through to callbacks
    time_zone="UTC",
)
```

Properties: `id`, `collection_id`, `status`, `video_id` (after completion), `bot_name`, `meeting_title`, `meeting_url`, `speaker_timeline`, `is_active`, `is_completed`.
Methods: `refresh() -> Meeting`, `wait_for_status(target_status, timeout=14400, interval=120) -> bool`.

## Streaming notes

- All stream URLs are HLS manifests (`.m3u8`): native in Safari, hls.js elsewhere.
- Streams compile on demand; first play may lag briefly, repeats are cached. `video.generate_stream()` without args returns the cached URL.
- `video.generate_stream(timeline=[(10, 30), (60, 90)])` is the fastest way to stream specific clips without building a `Timeline` object.
- Audio playback: `audio.generate_url()` returns a signed URL (no `generate_stream` on Audio).

## Enums and constants

```python
from videodb import (
    SearchType,         # semantic, keyword, scene (may need paid plan), llm
    IndexType,          # spoken_word, scene
    SceneExtractionType,  # shot_based, time_based, transcript
    MediaType,          # video, audio, image
    Segmenter,          # word, sentence, time
    SegmentationType,   # sentence, llm
    TranscodeMode,      # economy, lightning
    ResizeMode,         # crop, fit, pad
    ReframeMode,        # simple, smart
    RTStreamChannelType,
    SubtitleStyle, SubtitleAlignment, SubtitleBorderStyle,
    TextStyle,          # also importable from videodb.asset
    VideoConfig, AudioConfig,
)
```

```python
style = SubtitleStyle(
    font_name="Arial",
    font_size=18,
    primary_colour="&H00FFFFFF",   # ASS color format
    bold=False,
)
video.add_subtitle(style=style)
```

## Exceptions

```python
from videodb.exceptions import (
    AuthenticationError,   # missing/invalid VIDEO_DB_API_KEY
    InvalidRequestError,   # bad URL/format/params; also "No results found" on search
    RequestTimeoutError,   # server timeout
    SearchError,           # e.g. searching before indexing
    VideodbError,          # base class; server/network/generic
)
```
