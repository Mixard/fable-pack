# Timeline Editing

Non-destructive server-side composition: trim, sequence, and overlay assets, then compile to an HLS stream. Source media is never modified. Assets (video, audio, image) must already be uploaded to a collection; caption overlays additionally require a spoken-word index.

## Two timeline APIs — not interchangeable

| | `videodb.timeline.Timeline` | `videodb.editor.Timeline` (Editor API) |
|---|---|---|
| Import | `from videodb.timeline import Timeline` | `from videodb.editor import Timeline as EditorTimeline` |
| Assets | `VideoAsset`, `AudioAsset`, `ImageAsset`, `TextAsset` | `CaptionAsset`, `Clip`, `Track` |
| Methods | `add_inline()`, `add_overlay()` | `add_track()` with `Track`/`Clip` |
| Best for | Composition, overlays, multi-clip editing | Caption/subtitle styling with animations |

`CaptionAsset` only works with the Editor API; the four standard assets only with `videodb.timeline.Timeline`.

## Timeline (videodb.timeline)

```python
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset, ImageAsset, TextAsset, TextStyle

timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video.id, start=10, end=30))  # sequential main track
timeline.add_overlay(0, TextAsset(text="The End", duration=3, style=TextStyle(fontsize=36)))
stream_url = timeline.generate_stream()
```

- `add_inline(asset)` accepts only `VideoAsset`; clips play sequentially on the main track.
- `add_overlay(start, asset)` accepts `AudioAsset`, `ImageAsset`, `TextAsset` at an absolute timeline timestamp. Overlays do not move when inline clips are rearranged; there is no overlay-to-clip binding.
- Multiple overlays can share a timestamp: audio overlays mix; image/text overlays layer in add order.
- Timestamps are not validated: negative `start` is silently accepted and breaks output. Ensure `start >= 0`, `start < end`, `end <= video.length`.

### VideoAsset

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_id` | `str` | required | Video media ID |
| `start` | `float` | `0` | Trim start (seconds) |
| `end` | `float\|None` | `None` | Trim end (`None` = full) |

### AudioAsset

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_id` | `str` | required | Audio media ID |
| `start` / `end` | `float` / `float\|None` | `0` / `None` | Trim bounds (seconds) |
| `disable_other_tracks` | `bool` | `True` | `True` mutes the video's own audio |
| `fade_in_duration` | `float` | `0` | Seconds, max 5 |
| `fade_out_duration` | `float` | `0` | Seconds, max 5 |

### ImageAsset

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_id` | `str` | required | Image media ID |
| `width` / `height` | `int\|str` | `100` / `100` | Display size |
| `x` / `y` | `int` | `80` / `20` | Position in px from left/top |
| `duration` | `float\|None` | `None` | Display duration (seconds) |

### TextAsset and TextStyle

```python
TextAsset(text="Hello", duration=5, style=TextStyle(fontsize=36, fontcolor="white", boxcolor="black", alpha=0.8))
```

`TextStyle` parameters (use `boxcolor`, not `bgcolor`):

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fontsize` | `int` | `24` | Font size in px |
| `fontcolor` | `str` | `"black"` | CSS name or hex |
| `fontcolor_expr` | `str` | `""` | Dynamic color expression |
| `alpha` | `float` | `1.0` | Opacity 0.0-1.0 |
| `font` | `str` | `"Sans"` | Font family |
| `box` | `bool` | `True` | Background box |
| `boxcolor` | `str` | `"white"` | Box color |
| `boxborderw` | `str` | `"10"` | Box border width |
| `boxw` / `boxh` | `int` | `0` | Box size overrides |
| `line_spacing` | `int` | `0` | |
| `text_align` | `str` | `"T"` | Alignment within box |
| `y_align` | `str` | `"text"` | Vertical alignment reference |
| `borderw` / `bordercolor` | `int` / `str` | `0` / `"black"` | Text border |
| `expansion` | `str` | `"normal"` | Text expansion mode |
| `basetime` | `int` | `0` | Base time for time expressions |
| `fix_bounds` | `bool` | `False` | |
| `text_shaping` | `bool` | `True` | |
| `shadowcolor` / `shadowx` / `shadowy` | `str`/`int`/`int` | `"black"`/`0`/`0` | Shadow |
| `tabsize` | `int` | `4` | |
| `x` | `str` | `"(main_w-text_w)/2"` | Horizontal position expression |
| `y` | `str` | `"(main_h-text_h)/2"` | Vertical position expression |

## Captions

Two routes:

**Simple — burned-in subtitles** (uses `videodb.timeline.Timeline` internally):

```python
from videodb import SubtitleStyle

video.index_spoken_words(force=True)
stream_url = video.add_subtitle()  # or add_subtitle(style=SubtitleStyle(font_name="Arial", font_size=22, primary_colour="&H00FFFFFF", bold=True))
```

**Editor API — styled/animated captions:**

```python
from videodb.editor import (
    CaptionAsset, Clip, Track, Timeline as EditorTimeline,
    FontStyling, BorderAndShadow, Positioning, CaptionAnimation,
)

video.index_spoken_words(force=True)
caption = CaptionAsset(
    src="auto",                              # "auto" or base64 ASS string
    font=FontStyling(name="Clear Sans", size=30),
    primary_color="&H00FFFFFF",              # ASS color format
    back_color="&H00000000",
    border=BorderAndShadow(outline=1),
    position=Positioning(margin_v=30),
    animation=CaptionAnimation.box_highlight,  # also: reveal, karaoke
)
editor_tl = EditorTimeline(conn)
track = Track()
track.add_clip(start=0, clip=Clip(asset=caption, duration=video.length))
editor_tl.add_track(track)
stream_url = editor_tl.generate_stream()
```

`CaptionAsset` defaults: `src="auto"`, `font=FontStyling()`, `primary_color="&H00FFFFFF"`, `secondary_color="&H000000FF"`, `back_color="&H00000000"`, `border=BorderAndShadow()`, `position=Positioning()`, `animation=None`.

## Example: search-driven highlight reel

```python
from videodb import SearchType
from videodb.exceptions import InvalidRequestError

video.index_spoken_words(force=True)
try:
    shots = video.search("product announcement", search_type=SearchType.semantic).get_shots()
except InvalidRequestError as e:
    if "No results found" in str(e):
        shots = []
    else:
        raise

timeline = Timeline(conn)
timeline.add_overlay(0, TextAsset(text="Highlights", duration=4,
                                  style=TextStyle(fontsize=48, fontcolor="white", boxcolor="#1a1a2e")))
offset = 0.0
for shot in shots:
    timeline.add_inline(VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end))
    offset += shot.end - shot.start   # track offset if placing per-clip overlays
stream_url = timeline.generate_stream()
```

Generated media (`coll.generate_music/voice/sound_effect/image`) can be used as timeline assets immediately.

## Limitations

Not supported by the timeline editor (fall back to local tools):

| Limitation | Detail |
|---|---|
| Transitions/effects | No crossfades, wipes, dissolves — all cuts are hard cuts |
| Video-on-video (PiP) | `add_inline()` accepts only `VideoAsset`; no video overlay. Image overlays can fake static PiP |
| Speed control | No slow-mo/fast-forward/reverse; `VideoAsset` has no `speed` parameter |
| Crop/zoom/pan | `video.reframe()` handles aspect ratio only |
| Filters/color grading | No brightness/contrast/saturation adjustments |
| Animated text | `TextAsset` is static; for animated captions use `CaptionAsset` (Editor API) |
| Mixed text styling | One `TextStyle` per `TextAsset` |
| Blank/solid-color clips | Text/image overlays require a `VideoAsset` beneath them on the inline track |
| Audio volume control | No `volume` parameter; audio is full volume or muted via `disable_other_tracks` |
| Keyframe animation | Overlay properties cannot change over time |

Constraints: audio fades capped at 5 s; overlay timestamps are absolute; inline track is video-only.
