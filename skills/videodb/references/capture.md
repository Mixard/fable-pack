# Desktop Capture

Real-time screen, microphone, and system-audio recording with live AI processing. Desktop capture supports macOS only. All events (including session lifecycle) arrive over WebSocket — no webhooks or polling needed.

Gotcha: the `CaptureClient` runs the local recorder binary that streams data to VideoDB. If the Python process that created it exits, the recorder is killed and capture stops silently. Run capture code as a long-lived background process (e.g. `nohup python capture_script.py &`) and block on an `asyncio.Event` with `SIGINT`/`SIGTERM` handlers until explicitly stopped.

## ws_listener.py

`scripts/ws_listener.py` connects a WebSocket and appends every event to a JSONL file.

```bash
STATE_DIR="${VIDEODB_EVENTS_DIR:-$HOME/.local/state/videodb}"
python scripts/ws_listener.py --clear "$STATE_DIR" &   # --clear wipes old events; use for each new session
cat "$STATE_DIR/videodb_ws_id"                          # WebSocket connection ID
kill "$(cat "$STATE_DIR/videodb_ws_pid")"               # stop listener
```

- Output dir precedence: positional arg > `VIDEODB_EVENTS_DIR` env > `${XDG_STATE_HOME:-$HOME/.local/state}/videodb`.
- Files: `videodb_events.jsonl` (all events), `videodb_ws_id` (connection ID for `ws_connection_id` params), `videodb_ws_pid` (PID).
- Prints `WS_ID=<connection_id>` on the first line, then listens; auto-reconnects with exponential backoff; graceful shutdown on SIGINT/SIGTERM.

JSONL lines are the raw events plus `ts` (ISO) and `unix_ts` (float) fields:

```json
{"ts": "2026-03-02T10:15:30.123Z", "unix_ts": 1772446530.123, "channel": "visual_index", "data": {"text": "..."}}
```

Reading events:

```python
import json, os, time
from pathlib import Path

events_dir = Path(os.environ.get("VIDEODB_EVENTS_DIR", Path.home() / ".local" / "state" / "videodb"))
events = []
with (events_dir / "videodb_events.jsonl").open(encoding="utf-8") as f:
    for line in f:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

transcripts = [e["data"]["text"] for e in events if e.get("channel") == "transcript"]
cutoff = time.time() - 300
recent_visual = [e for e in events if e.get("channel") == "visual_index" and e["unix_ts"] > cutoff]
```

## Capture workflow

1. Start `ws_listener.py --clear` in the background; wait for `videodb_ws_id` to appear and read it.
2. `conn.create_capture_session(...)` with the ws_id; `conn.generate_client_token()`.
3. Create `CaptureClient(client_token=token)`; request `"microphone"` and `"screen_capture"` permissions.
4. `client.list_channels()`; pick mic/display/system_audio; set `channel.store = True` on channels to persist as video.
5. `client.start_capture_session(...)`.
6. Read events until `capture_session.active` — it carries the `rtstreams[]` array. Save session ID and RTStream IDs to a file so other scripts can use them.
7. Keep the process alive (asyncio.Event + signal handlers); write a PID file, overwritten on every run.
8. Start AI pipelines (`index_audio`, `index_visuals`, `start_transcript` — see rtstream.md) on the RTStreams from a separate script.
9. Process events from the JSONL per use case (keyword alerts on `transcript`, app tracking on `visual_index`, summaries on `audio_index`).
10. To stop: SIGTERM the capture process; its handler calls `client.stop_capture()` then `client.shutdown()`.
11. Wait for `capture_session.exported` in the events file (may take several seconds) — it carries `exported_video_id`, `stream_url`, `player_url`.
12. Only then kill the WebSocket listener; killing it earlier loses the final video URLs.

## WebSocket connection (SDK level)

```python
ws_wrapper = conn.connect_websocket()
ws = await ws_wrapper.connect()
ws_id = ws.connection_id          # pass to AI pipeline methods
# ws.receive() -> AsyncIterator[dict]
```

## CaptureSession

| Method | Returns | Description |
|--------|---------|-------------|
| `conn.create_capture_session(end_user_id, collection_id, ws_connection_id, metadata)` | `CaptureSession` | `end_user_id` is required — any unique string works for testing |
| `conn.get_capture_session(capture_session_id)` | `CaptureSession` | |
| `conn.generate_client_token()` | `str` | Client-side auth token |
| `session.get_rtstream(type)` | `list[RTStream]` | `type`: `"mic"`, `"screen"`, `"system_audio"` |

Property: `session.id`.

## CaptureClient

```python
from videodb.capture import CaptureClient

client = CaptureClient(client_token=token)
await client.request_permission("microphone")
await client.request_permission("screen_capture")

channels = await client.list_channels()
mic = channels.mics.default
display = channels.displays.default
system_audio = channels.system_audio.default
# channel groups: channels.mics / .displays / .system_audio; each has .default and .all()
# channel props: ch.id, ch.type ("mic"|"display"|"system_audio"), ch.name, ch.store (bool)
# Without store=True a stream is processed in real time but not saved.

selected = [c for c in [mic, display, system_audio] if c]
await client.start_capture_session(
    capture_session_id=session.id,
    channels=selected,
    primary_video_channel_id=display.id if display else None,
)
# ... later:
await client.stop_capture()
await client.shutdown()
```

## Event channels and lifecycle

| Channel | Source | Content |
|---------|--------|---------|
| `capture_session` | Session lifecycle | Status changes |
| `transcript` | `start_transcript()` | Speech-to-text |
| `visual_index` / `scene_index` | `index_visuals()` | Visual analysis |
| `audio_index` | `index_audio()` | Audio analysis |
| `alert` | `create_alert()` | Alert notifications |

Lifecycle events: `capture_session.created` -> `.starting` -> `.active` (carries `rtstreams[]`) -> `.stopping` -> `.stopped` -> `.exported` (carries `exported_video_id`, `stream_url`, `player_url`; only when `store=True`). Failure path: `.failed` (carries `error`).

### Event payload shapes

Transcript:

```json
{
  "channel": "transcript",
  "rtstream_id": "rts-xxx",
  "rtstream_name": "mic:default",
  "data": {"text": "Let's schedule the meeting for Thursday", "is_final": true, "start": 1710000001234, "end": 1710000002345}
}
```

Visual index (`rtstream_name` like `"display:1"`) and audio index (`"mic:default"`) share the shape: `data` has `text`, `start`, `end`.

Session active:

```json
{
  "event": "capture_session.active",
  "capture_session_id": "cap-xxx",
  "status": "active",
  "data": {
    "rtstreams": [
      {"rtstream_id": "rts-1", "name": "mic:default", "media_types": ["audio"]},
      {"rtstream_id": "rts-2", "name": "system_audio:default", "media_types": ["audio"]},
      {"rtstream_id": "rts-3", "name": "display:1", "media_types": ["video"]}
    ]
  }
}
```

Session exported:

```json
{
  "event": "capture_session.exported",
  "capture_session_id": "cap-xxx",
  "status": "exported",
  "data": {
    "exported_video_id": "v_xyz789",
    "stream_url": "https://stream.videodb.io/...",
    "player_url": "https://console.videodb.io/player?url=..."
  }
}
```
