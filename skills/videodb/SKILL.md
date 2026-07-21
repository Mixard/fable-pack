---
name: videodb
description: Use when writing code against the VideoDB Python SDK (videodb package) for video upload, transcription, moment search, timeline editing, transcoding, reframing, generative media, RTSP/RTMP live streams, or desktop capture. Covers exact method signatures, enums, exception handling gotchas, and the WebSocket event workflow.
---

# VideoDB Python SDK

Server-side video platform. Upload/ingest media, transcribe and index it, search for moments with timestamps, compose timelines, transcode and reframe, generate media with AI, ingest live streams, and record desktop sessions. Every operation returns HLS stream URLs compiled on demand — no local rendering.

Trimming, concatenation, audio/music overlay, subtitles, text/image overlays, transcoding, resolution and aspect-ratio changes, transcription, and media generation are all handled server-side by VideoDB. Fall back to ffmpeg/local tools only for operations the timeline does not support: transitions, speed changes, crop/zoom, color grading, per-track volume mixing (see `references/editing.md`, Limitations).

## Setup

```bash
pip install "videodb[capture]" python-dotenv
# If the capture extra fails on Linux:
pip install videodb python-dotenv
```

API key: `VIDEO_DB_API_KEY` as an environment variable or in the project `.env` file. Free key at console.videodb.io (50 free uploads). Let the user set the key; do not handle it directly.

```python
from dotenv import load_dotenv
load_dotenv(".env")

import videodb
conn = videodb.connect()      # raises AuthenticationError when key is missing/invalid
coll = conn.get_collection()  # default collection
```

## Core API map

| Task | Call |
|------|------|
| Upload file/URL/YouTube | `coll.upload(url=... \| file_path=...)` -> `Video\|Audio\|Image` |
| Transcript | `video.index_spoken_words(force=True)` then `video.get_transcript_text()` |
| Burned-in subtitles | `video.add_subtitle(style=SubtitleStyle(...))` -> stream URL |
| Search spoken content | `video.search(query, search_type=SearchType.semantic)` |
| Search visuals | `video.index_scenes(...)` then `video.search(..., index_type=IndexType.scene, scene_index_id=...)` |
| Compile search hits to clip | `results.compile()` -> stream URL |
| Trim / combine / overlay | `Timeline(conn)` + `VideoAsset`/`AudioAsset`/`ImageAsset`/`TextAsset` |
| Stream a segment fast | `video.generate_stream(timeline=[(start, end)])` |
| Change resolution/quality | `conn.transcode(source, callback_url, mode, video_config, audio_config)` |
| Change aspect ratio | `video.reframe(start, end, target, mode)` |
| Generate image/video/music/SFX/voice | `coll.generate_image/generate_video/generate_music/generate_sound_effect/generate_voice` |
| LLM over transcript | `coll.generate_text(prompt, model_name)["output"]` |
| Dub to another language | `coll.dub_video(video_id, language_code)` |
| Record a meeting | `coll.record_meeting(meeting_url, bot_name)` |
| Live RTSP/RTMP stream | `coll.connect_rtstream(url, name, store=True)` |
| Desktop capture (macOS only) | `conn.create_capture_session(...)` + `CaptureClient` |

Key enums (all importable from `videodb`): `SearchType` (semantic, keyword, scene, llm), `IndexType` (spoken_word, scene), `SceneExtractionType` (shot_based, time_based, transcript), `TranscodeMode` (economy, lightning), `ResizeMode` (crop, fit, pad), `ReframeMode` (simple, smart), `MediaType`, `Segmenter`, `SegmentationType`, `RTStreamChannelType`, plus `SubtitleStyle`, `TextStyle`, `VideoConfig`, `AudioConfig`.

Exceptions (`videodb.exceptions`): `AuthenticationError`, `InvalidRequestError`, `RequestTimeoutError`, `SearchError`, `VideodbError` (base).

## Gotchas

1. `index_spoken_words()` errors on an already-indexed video ("Spoken word index for video already exists"). Pass `force=True` to make it idempotent.
2. `index_scenes()` has no `force` parameter. When a scene index already exists it raises; recover the existing ID from the message:
   ```python
   import re
   try:
       scene_index_id = video.index_scenes(
           extraction_type=SceneExtractionType.shot_based,
           prompt="Describe the visual content in this scene.",
       )
   except Exception as e:
       m = re.search(r"id\s+([a-f0-9]+)", str(e))
       if m:
           scene_index_id = m.group(1)
       else:
           raise
   ```
3. `video.search()` raises `InvalidRequestError` with message "No results found" when nothing matches. Wrap in try/except and treat that message as an empty result set (`shots = []`); re-raise anything else.
4. `reframe()` is slow server-side work — minutes for long videos, can time out. Limit with `start`/`end`, or pass `callback_url` (then it returns `None` and delivers via webhook).
5. Timeline assets are not validated: negative `start` is silently accepted and produces broken output. Ensure `start >= 0`, `start < end`, `end <= video.length` before building `VideoAsset`.
6. `coll.search()` supports only `SearchType.semantic`; keyword and scene search at collection level raise `NotImplementedError` — use `video.search()` per video.
7. `Image.url` may be `None` for generated images; use `image.generate_url()` for a signed URL.
8. `generate_video()` and `create_collection()` are plan-gated — "Operation not allowed" / "maximum limit" errors mean plan limits, not bugs.
9. For scene search, prefer `SearchType.semantic` with `index_type=IndexType.scene` (works on all plans; `SearchType.scene` may be paid-only) and pass `score_threshold=0.3` or higher to cut noise.

## Desktop capture quick start (macOS only)

`scripts/ws_listener.py` connects a WebSocket and dumps all events to JSONL.

```bash
STATE_DIR="${VIDEODB_EVENTS_DIR:-$HOME/.local/state/videodb}"
VIDEODB_EVENTS_DIR="$STATE_DIR" python scripts/ws_listener.py --clear "$STATE_DIR" &
cat "$STATE_DIR/videodb_ws_id"      # ws_connection_id for capture/AI pipelines
# events accumulate in $STATE_DIR/videodb_events.jsonl
kill "$(cat "$STATE_DIR/videodb_ws_pid")"   # stop listener
```

Use `--clear` for every fresh capture run so stale events do not leak into the new session. Full workflow, event schemas, and `CaptureClient` API: `references/capture.md`.

## References

- `references/api-reference.md` — Connection, Collection, Video/Audio/Image objects, transcode, reframe, Meeting, streaming, enums, exceptions
- `references/search.md` — spoken-word and scene indexing, search types, metadata filters, cross-collection search
- `references/editing.md` — Timeline and asset parameters, captions, the two timeline APIs, hard limitations
- `references/generative.md` — generate_image/video/music/sound_effect/voice/text, dubbing, transcript translation
- `references/rtstream.md` — RTSP/RTMP ingestion, live AI indexing, events, alerts, export
- `references/capture.md` — desktop capture sessions, CaptureClient, WebSocket event schemas, lifecycle
