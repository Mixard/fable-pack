# Media assets: videos, images, animated images, audio

## Assets and staticFile()

Place assets in `public/` at the project root and reference them with `staticFile()`:

```tsx
import {Img, staticFile} from 'remotion';

<Img src={staticFile('logo.png')} />;
```

`staticFile()` returns an encoded URL that survives deployment to subdirectories; special characters in filenames (`#`, `?`, `&`) are encoded automatically. Remote URLs are used directly, without `staticFile()` (CORS required for remote images/GIFs).

Remotion's media components (`<Img>`, `<Video>`, `<Audio>`, `<AnimatedImage>`) wait until the asset is fully loaded before the frame is rendered — native `<img>`, Next.js `<Image>`, or CSS `background-image` cause flickering and blank frames in the export.

## Videos: `<Video>` from @remotion/media

Requires `@remotion/media` (`npx remotion add @remotion/media`).

```tsx
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';

<Video src={staticFile('video.mp4')} />;
```

### Trimming (values in frames)

```tsx
const {fps} = useVideoConfig();

<Video
  src={staticFile('video.mp4')}
  trimBefore={2 * fps}  // skip first 2 seconds of the file
  trimAfter={10 * fps}  // end at the 10-second mark of the file
/>;
```

### Delaying

Wrap in `<Sequence from={n}>` to start the video later on the timeline:

```tsx
<Sequence from={1 * fps}>
  <Video src={staticFile('video.mp4')} />
</Sequence>
```

### Sizing

Use the `style` prop: `width`, `height`, `position`, `objectFit: 'cover'`, etc.

### Volume

```tsx
<Video src={staticFile('video.mp4')} volume={0.5} />

// Dynamic: callback receives the frame since the media started playing (starts at 0)
<Video
  src={staticFile('video.mp4')}
  volume={(f) => interpolate(f, [0, 1 * fps], [0, 1], {extrapolateRight: 'clamp'})}
/>

<Video src={staticFile('video.mp4')} muted />
```

### Speed, looping, pitch

```tsx
<Video src={staticFile('video.mp4')} playbackRate={2} />   // reverse playback not supported
<Video src={staticFile('video.mp4')} loop />
<Video src={staticFile('video.mp4')} toneFrequency={1.5} /> // pitch, range 0.01-2
```

- `loopVolumeCurveBehavior`: `"repeat"` resets the volume-callback frame count each loop; `"extend"` keeps incrementing (use for fades spanning multiple loops).
- `toneFrequency` (pitch without speed change) only works during server-side rendering — not in Studio preview or `<Player />`.

## Images: `<Img>`

```tsx
import {Img, staticFile} from 'remotion';

<Img src={staticFile('photo.png')} />
```

Dynamic paths via template literals work for image sequences, avatars, conditional icons:

```tsx
<Img src={staticFile(`frames/frame${frame}.png`)} />
<Img src={staticFile(`avatars/${props.userId}.png`)} />
```

Get dimensions with `getImageDimensions()` from `remotion`:

```tsx
import {getImageDimensions, staticFile} from 'remotion';

const {width, height} = await getImageDimensions(staticFile('photo.png'));
```

Useful inside `calculateMetadata` to size the composition to an image.

## Animated images: `<AnimatedImage>` and `<Gif>`

`<AnimatedImage>` (from `remotion`) plays GIF, APNG, AVIF, and WebP synchronized with the timeline:

```tsx
import {AnimatedImage, staticFile} from 'remotion';

<AnimatedImage src={staticFile('animation.gif')} width={500} height={500} />;
```

- `fit`: `"fill"` (default), `"contain"`, `"cover"`.
- `playbackRate`: speed multiplier.
- `loopBehavior`: `"loop"` (default), `"pause-after-finish"`, `"clear-after-finish"`.
- Use `width`/`height` props for sizing; `style` for other CSS.
- Browser support: Chrome and Firefox only. Fallback: `<Gif>` from `@remotion/gif` — same props, GIF files only.

GIF duration:

```tsx
import {getGifDurationInSeconds} from '@remotion/gif';

const duration = await getGifDurationInSeconds(staticFile('animation.gif'));
// In calculateMetadata: durationInFrames: Math.ceil(duration * fps)
```

## Audio: `<Audio>` from @remotion/media

Requires `@remotion/media`.

```tsx
import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';

<Audio src={staticFile('audio.mp3')} />;
```

Plays from composition start, full volume, full length by default. Layer multiple `<Audio>` components for multiple tracks.

Same props as `<Video>`: `trimBefore`/`trimAfter` (frames), `volume` (static or callback; callback frame starts at 0 when the audio starts, not at the composition frame), `playbackRate` (no reverse), `loop` + `loopVolumeCurveBehavior`, `toneFrequency` (0.01-2, server-side rendering only). Delay with `<Sequence from={...}>`.

`muted` can be dynamic:

```tsx
<Audio src={staticFile('audio.mp3')} muted={frame >= 2 * fps && frame <= 4 * fps} />
```

## Fonts as raw files

Prefer `@remotion/fonts` or `@remotion/google-fonts` (see visuals.md). Manual loading:

```tsx
const fontFace = new FontFace('MyFont', `url(${staticFile('font.woff2')})`);
await fontFace.load();
document.fonts.add(fontFace);
```
