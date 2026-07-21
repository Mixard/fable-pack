---
name: ffmpeg-media-recipes
description: Use when cutting, reframing, or preprocessing video/audio with FFmpeg, or generating voiceover via the ElevenLabs API. Covers segment extraction, concat, loudnorm parameters, scene and silence detection, aspect-ratio crop formulas, and the ElevenLabs TTS endpoint.
---

# FFmpeg Media Recipes

## Cutting and Assembly

Extract a segment by timestamp (stream copy, no re-encode; cuts snap to keyframes):

```bash
ffmpeg -i raw.mp4 -ss 00:12:30 -to 00:15:45 -c copy segment_01.mp4
```

Batch cut from an edit decision list (`cuts.txt` lines: `start,end,label`):

```bash
while IFS=, read -r start end label; do
  ffmpeg -i raw.mp4 -ss "$start" -to "$end" -c copy "segments/${label}.mp4"
done < cuts.txt
```

Concatenate segments (same codec/params required for `-c copy`):

```bash
for f in segments/*.mp4; do echo "file '$f'"; done > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy assembled.mp4
```

## Preprocessing

Proxy for faster editing:

```bash
ffmpeg -i raw.mp4 -vf "scale=960:-2" -c:v libx264 -preset ultrafast -crf 28 proxy.mp4
```

Extract audio for transcription (16 kHz mono-friendly PCM):

```bash
ffmpeg -i raw.mp4 -vn -acodec pcm_s16le -ar 16000 audio.wav
```

Loudness normalization (EBU R128; `I` target integrated loudness in LUFS, `TP` true peak in dBTP, `LRA` loudness range):

```bash
ffmpeg -i segment.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy normalized.mp4
```

`I=-16` suits spoken-word/podcast delivery; streaming platforms commonly target -14.

## Aspect-Ratio Reframing

| Platform | Aspect | Resolution |
|----------|--------|------------|
| YouTube | 16:9 | 1920x1080 |
| TikTok / Reels / Shorts | 9:16 | 1080x1920 |
| Instagram feed | 1:1 | 1080x1080 |
| X / Twitter | 16:9 or 1:1 | 1280x720 or 720x720 |

Center crops (crop expressions are relative to input height `ih`):

```bash
# 16:9 -> 9:16
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" vertical.mp4

# 16:9 -> 1:1
ffmpeg -i input.mp4 -vf "crop=ih:ih,scale=1080:1080" square.mp4
```

Center crop keeps the middle of the frame; subjects off-center need an x-offset in `crop=w:h:x:y` or AI-guided reframing.

## Detection

Scene changes (threshold 0.3 = moderate sensitivity; timestamps appear in `showinfo` output on stderr):

```bash
ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr -f null - 2>&1 | grep showinfo
```

Silence (segments quieter than -30 dB lasting at least 2 s; useful for cutting dead air):

```bash
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=2 -f null - 2>&1 | grep silence
```

## ElevenLabs Voiceover

Endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`, auth header `xi-api-key`. The response body is raw MP3 bytes.

```python
import os, requests

resp = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={
        "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
        "Content-Type": "application/json",
    },
    json={
        "text": "Your narration text here",
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    },
)
with open("voiceover.mp3", "wb") as f:
    f.write(resp.content)
```

`eleven_turbo_v2_5` is the low-latency multilingual model; `stability` and `similarity_boost` range 0-1.
