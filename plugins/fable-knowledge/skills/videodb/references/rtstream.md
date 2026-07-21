# RTStream (Live Streams)

Real-time ingestion of RTSP/RTMP feeds and desktop-capture streams: record, index with AI, transcribe, alert, export to permanent video, and search. Typical flow: connect -> `start()` -> start AI pipelines -> monitor WebSocket events -> `stop()` -> `export()` -> index and search the exported video.

## Collection methods

| Method | Returns | Description |
|--------|---------|-------------|
| `coll.connect_rtstream(url, name, ...)` | `RTStream` | Create from RTSP/RTMP URL |
| `coll.get_rtstream(id)` | `RTStream` | Get by ID (e.g. `"rts-xxx"`) |
| `coll.list_rtstreams(limit, offset, status, name, ordering)` | `list[RTStream]` | e.g. `status="connected"`, `ordering="-created_at"` |
| `coll.search(query, namespace="rtstream")` | `RTStreamSearchResult` | Search across all RTStreams |

```python
rtstream = coll.connect_rtstream(
    url="rtmp://your-stream-server/live/stream-key",
    name="My Live Stream",
    media_types=["video"],   # or ["audio", "video"]
    sample_rate=30,          # optional
    store=True,              # enable recording storage; required for export()
    enable_transcript=True,  # optional
    ws_connection_id=ws_id,  # optional, for real-time events
)
```

From a capture session: `session.get_rtstream("mic" | "screen" | "system_audio")` returns `list[RTStream]`, or use `rtstream_id`s from the `capture_session.active` WebSocket event with `coll.get_rtstream()`.

## RTStream methods

| Method | Returns | Description |
|--------|---------|-------------|
| `rtstream.start()` / `stop()` | `None` | Begin / end ingestion |
| `rtstream.generate_stream(start, end)` | `str` | Playback of recorded segment — Unix timestamps, not second offsets |
| `rtstream.export(name=None)` | `RTStreamExportResult` | Export recording to permanent video |
| `rtstream.index_visuals(prompt, batch_config, model_name, name, ws_connection_id)` | `RTStreamSceneIndex` | Live visual AI indexing |
| `rtstream.index_audio(prompt, batch_config, model_name, name, ws_connection_id)` | `RTStreamSceneIndex` | Live audio LLM summarization |
| `rtstream.list_scene_indexes()` | `list[RTStreamSceneIndex]` | |
| `rtstream.get_scene_index(index_id)` | `RTStreamSceneIndex` | |
| `rtstream.search(query, ...)` | `RTStreamSearchResult` | Search indexed content |
| `rtstream.start_transcript(ws_connection_id, engine)` | `dict` | Live transcription (engine defaults to `"assemblyai"`) |
| `rtstream.get_transcript(page, page_size, start, end, since, engine)` | `dict` | Transcript pages; `since` for polling |
| `rtstream.stop_transcript(engine)` | `dict` | |

`RTStreamExportResult` properties: `video_id`, `stream_url` (HLS), `player_url`, `name`, `duration` (seconds).

```python
import time
start_ts = time.time()
rtstream.start()
# ... recording ...
end_ts = time.time()
rtstream.stop()
stream_url = rtstream.generate_stream(start=start_ts, end=end_ts)  # Unix timestamps
export_result = rtstream.export(name="Meeting Recording")
video = coll.get_video(export_result.video_id)   # then index/search like any video
```

## AI pipelines

Results are delivered on WebSocket channels (see capture.md for the listener): `transcript`, `scene_index` (visuals), `audio_index`, `alert`.

### Audio indexing

```python
audio_index = rtstream.index_audio(
    prompt="Summarize what is being discussed",
    batch_config={"type": "word", "value": 50},
    model_name=None,
    name="meeting_audio",
    ws_connection_id=ws_id,
)
```

Audio `batch_config`: `{"type": "word"|"sentence"|"time", "value": N}` — segment every N words / sentences / seconds.

### Visual indexing

```python
scene_index = rtstream.index_visuals(
    prompt="Describe what is happening on screen",
    batch_config={"type": "time", "value": 2, "frame_count": 5},  # 5 frames every 2 s
    model_name="basic",     # "mini" | "basic" | "pro" | "ultra"
    name="screen_monitor",
    ws_connection_id=ws_id,
)
```

Visual `batch_config`: only `type: "time"` is supported; `value` = window seconds, `frame_count` = frames sampled per window.

The prompt supports structured output — ask for a JSON object ("Return only valid JSON") and parse the `text` field of incoming events.

## RTStreamSceneIndex

Returned by `index_audio()` / `index_visuals()`.

Properties: `rtstream_index_id`, `rtstream_id`, `extraction_type` (`time` or `transcript`), `extraction_config`, `prompt`, `name`, `status` (`connected`, `stopped`).

| Method | Returns | Description |
|--------|---------|-------------|
| `index.get_scenes(start, end, page=1, page_size=100)` | `dict` | Keys: `scenes` (each with `start`, `end`, `text`), `next_page` |
| `index.start()` / `stop()` | `None` | Resume / stop indexing |
| `index.create_alert(event_id, callback_url, ws_connection_id)` | `str` | Alert ID |
| `index.list_alerts()` | `list` | |
| `index.enable_alert(alert_id)` / `disable_alert(alert_id)` | `None` | |

## Events and alerts

Events are reusable detection rules; alerts wire an event to a scene index.

```python
event_id = conn.create_event(
    event_prompt="User opened Slack application",
    label="slack_opened",
)
events = conn.list_events()   # dicts with event_id, label

alert_id = scene_index.create_alert(
    event_id=event_id,
    callback_url="https://your-backend.com/alerts",  # required; pass "" if WebSocket-only
    ws_connection_id=ws_id,                          # optional WebSocket delivery
)
```

Delivery: WebSocket (real-time, dashboards) and/or webhook (<1 s, server-to-server).

WebSocket alert event:

```json
{
  "channel": "alert",
  "rtstream_id": "rts-xxx",
  "data": {"event_label": "slack_opened", "timestamp": 1710000012340, "text": "User opened Slack application"}
}
```

Webhook payload:

```json
{
  "event_id": "event-xxx",
  "label": "slack_opened",
  "confidence": 0.95,
  "explanation": "User opened the Slack application",
  "timestamp": "2024-01-15T10:30:45Z",
  "start_time": 1234.5,
  "end_time": 1238.0,
  "stream_url": "https://stream.videodb.io/v3/...",
  "player_url": "https://console.videodb.io/player?url=..."
}
```

`ws_connection_id` is accepted by `start_transcript()`, `index_audio()`, `index_visuals()`, and `create_alert()`. Channel mapping: `transcript` <- start_transcript, `scene_index` <- index_visuals, `audio_index` <- index_audio, `alert` <- create_alert.
