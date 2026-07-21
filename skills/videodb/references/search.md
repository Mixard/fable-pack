# Search and Indexing

Videos must be indexed before search. Indexing is one-time per video per index type; searches afterwards are fast.

## Spoken word index

```python
video.index_spoken_words(force=True)   # force=True = idempotent, skips "already exists" error
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language_code` | `str\|None` | `None` | Language of the video |
| `segmentation_type` | `SegmentationType` | `SegmentationType.sentence` | `sentence` or `llm` |
| `force` | `bool` | `False` | Skip if already indexed |
| `callback_url` | `str\|None` | `None` | Async webhook |

Required for both semantic and keyword search over speech.

## Scene index

No `force` parameter — raises if a scene index already exists ("Scene index with id XXXX already exists"). Recover the ID from the error:

```python
import re
from videodb import SceneExtractionType

try:
    scene_index_id = video.index_scenes(
        extraction_type=SceneExtractionType.shot_based,
        prompt="Describe the visual content, objects, actions, and setting in this scene.",
    )
except Exception as e:
    m = re.search(r"id\s+([a-f0-9]+)", str(e))
    if m:
        scene_index_id = m.group(1)
    else:
        raise
```

Extraction types:

| Type | Splits on | Best for |
|------|-----------|----------|
| `SceneExtractionType.shot_based` | Visual shot boundaries | General purpose, action content |
| `SceneExtractionType.time_based` | Fixed intervals | Uniform sampling, long static content |
| `SceneExtractionType.transcript` | Transcript segments | Speech-driven boundaries |

`time_based` config:

```python
video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 5, "select_frames": ["first", "last"]},
    prompt="Describe what is happening in this scene.",
)
```

Multiple scene indexes per video are allowed (different prompts/extraction types); target one with `scene_index_id`, or omit it to search all.

## Search types

All searches can raise `InvalidRequestError` "No results found" — always wrap:

```python
from videodb import SearchType, IndexType
from videodb.exceptions import InvalidRequestError

try:
    results = video.search("product demo", search_type=SearchType.semantic)
    shots = results.get_shots()
except InvalidRequestError as e:
    if "No results found" in str(e):
        shots = []
    else:
        raise
```

- **Semantic** (`SearchType.semantic`): natural-language matching over spoken content. Works best with descriptive phrases, not single keywords.
- **Keyword** (`SearchType.keyword`): exact term/phrase matching in the transcript.
- **Scene**: use `SearchType.semantic` with `index_type=IndexType.scene` — the reliable combination on all plans. `SearchType.scene` exists but may be unavailable on the free tier. Pass `score_threshold=0.3` or higher to filter low-relevance noise.

```python
results = video.search(
    query="person writing on a whiteboard",
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    scene_index_id=scene_index_id,
    score_threshold=0.3,
)
```

### Scene search with metadata filters

When scenes were indexed with custom metadata:

```python
results = video.search(
    query="a skillful chasing scene",
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    scene_index_id=scene_index_id,
    filter=[{"camera_view": "road_ahead"}, {"action_type": "chasing"}],
)
```

## Working with results

```python
for shot in results.get_shots():
    print(shot.video_id, shot.start, shot.end, shot.text)

stream_url = results.compile()        # all hits as one stream
results.play()                        # open compiled stream in browser
clip_url = results.get_shots()[0].generate_stream()  # single hit
```

## Cross-collection search

```python
results = coll.search(query="product demo", search_type=SearchType.semantic)
```

Collection-level search supports only `SearchType.semantic`; `keyword` or `scene` raise `NotImplementedError`. Use `video.search()` per video for those.
