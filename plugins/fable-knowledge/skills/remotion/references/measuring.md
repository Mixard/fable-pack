# Measuring: media metadata (Mediabunny), text, DOM nodes

## Mediabunny basics

Mediabunny reads media metadata and decodes frames in browser, Node.js, and Bun. Sources:

- `UrlSource(src, {getRetryDelay: () => null})` — URLs (including `staticFile()` results).
- `FileSource(file)` — `File` objects from input/drag-and-drop.
- `BlobSource(blob)` — blobs.

## Duration of video or audio (seconds)

```tsx
import {Input, ALL_FORMATS, UrlSource} from 'mediabunny';

export const getMediaDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {getRetryDelay: () => null}),
  });
  return input.computeDuration(); // seconds, e.g. 10.5
};
```

Works the same for audio files (`mp3`, `wav`, ...) and with `staticFile('audio.mp3')`.

## Video dimensions

```tsx
export const getVideoDimensions = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {getRetryDelay: () => null}),
  });
  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error('No video track found');
  }
  return {width: videoTrack.displayWidth, height: videoTrack.displayHeight};
};
```

## Sizing a composition to media (calculateMetadata)

```tsx
import {CalculateMetadataFunction} from 'remotion';

const calculateMetadata: CalculateMetadataFunction<Props> = async ({props}) => {
  const [durationInSeconds, dimensions] = await Promise.all([
    getMediaDuration(props.videoSrc),
    getVideoDimensions(props.videoSrc),
  ]);
  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
    width: dimensions.width,
    height: dimensions.height,
  };
};
```

For multiple videos, `Promise.all` the metadata calls and sum the durations. `calculateMetadata` can also return `defaultOutName` (e.g. `` `video-${props.id}.mp4` ``) and `defaultCodec`.

For images use `getImageDimensions()` from `remotion`; for GIFs use `getGifDurationInSeconds()` from `@remotion/gif` (see media.md).

## Checking decodability

```tsx
import {Input, ALL_FORMATS, UrlSource} from 'mediabunny';

export const canDecode = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {getRetryDelay: () => null}),
  });

  try {
    await input.getFormat();
  } catch {
    return false;
  }

  const videoTrack = await input.getPrimaryVideoTrack();
  if (videoTrack && !(await videoTrack.canDecode())) {
    return false;
  }

  const audioTrack = await input.getPrimaryAudioTrack();
  if (audioTrack && !(await audioTrack.canDecode())) {
    return false;
  }

  return true;
};
```

## Extracting frames at timestamps

Useful for thumbnails and filmstrips. Copy-pasteable helper:

```tsx
import {ALL_FORMATS, Input, UrlSource, VideoSample, VideoSampleSink} from 'mediabunny';

type Options = {
  track: {width: number; height: number};
  container: string;
  durationInSeconds: number | null;
};

export type ExtractFramesTimestampsInSecondsFn = (options: Options) => Promise<number[]> | number[];

export type ExtractFramesProps = {
  src: string;
  timestampsInSeconds: number[] | ExtractFramesTimestampsInSecondsFn;
  onVideoSample: (sample: VideoSample) => void;
  signal?: AbortSignal;
};

export async function extractFrames({src, timestampsInSeconds, onVideoSample, signal}: ExtractFramesProps): Promise<void> {
  using input = new Input({formats: ALL_FORMATS, source: new UrlSource(src)});

  const [durationInSeconds, format, videoTrack] = await Promise.all([
    input.computeDuration(),
    input.getFormat(),
    input.getPrimaryVideoTrack(),
  ]);

  if (!videoTrack) {
    throw new Error('No video track found in the input');
  }
  if (signal?.aborted) {
    throw new Error('Aborted');
  }

  const timestamps =
    typeof timestampsInSeconds === 'function'
      ? await timestampsInSeconds({
          track: {width: videoTrack.displayWidth, height: videoTrack.displayHeight},
          container: format.name,
          durationInSeconds,
        })
      : timestampsInSeconds;

  if (timestamps.length === 0) {
    return;
  }
  if (signal?.aborted) {
    throw new Error('Aborted');
  }

  const sink = new VideoSampleSink(videoTrack);

  for await (using videoSample of sink.samplesAtTimestamps(timestamps)) {
    if (signal?.aborted) {
      break;
    }
    if (!videoSample) {
      continue;
    }
    onVideoSample(videoSample);
  }
}
```

Usage — draw each sample to a canvas:

```tsx
await extractFrames({
  src: 'https://remotion.media/video.mp4',
  timestampsInSeconds: [0, 1, 2, 3, 4],
  onVideoSample: (sample) => {
    const canvas = document.createElement('canvas');
    canvas.width = sample.displayWidth;
    canvas.height = sample.displayHeight;
    sample.draw(canvas.getContext('2d')!, 0, 0);
  },
});
```

For a filmstrip, pass a callback as `timestampsInSeconds` and compute evenly spaced timestamps from `track` aspect ratio and `durationInSeconds`. Cancel with an `AbortController` passed as `signal` (optionally combined with `Promise.race` for a timeout).

## Measuring text: @remotion/layout-utils

Install: `npx remotion add @remotion/layout-utils`.

```tsx
import {measureText, fitText, fillTextBox} from '@remotion/layout-utils';

// Dimensions (results are cached)
const {width, height} = measureText({text: 'Hello World', fontFamily: 'Arial', fontSize: 32, fontWeight: 'bold'});

// Optimal font size for a container width
const {fontSize} = fitText({text: 'Hello World', withinWidth: 600, fontFamily: 'Inter', fontWeight: 'bold'});
// Cap it: style={{fontSize: Math.min(fontSize, 80)}}

// Overflow check
const box = fillTextBox({maxBoxWidth: 400, maxLines: 3});
const {exceedsBox} = box.add({text: 'word ', fontFamily: 'Arial', fontSize: 24});
```

Gotchas:

- Measure only after fonts are loaded (`await waitUntilDone()` from the font loader first).
- `validateFontIsLoaded: true` makes `measureText` throw if the font is not loaded.
- Use identical font properties (family, size, weight, letterSpacing) for measuring and rendering — share a style object.
- `border` and `padding` skew measurements; use `outline` instead of `border`.

## Measuring DOM nodes

Remotion scales the video container with a CSS `scale()` transform, which distorts `getBoundingClientRect()`. Divide by `useCurrentScale()`:

```tsx
import {useCurrentScale} from 'remotion';
import {useRef, useEffect, useState} from 'react';

export const MyComponent = () => {
  const ref = useRef<HTMLDivElement>(null);
  const scale = useCurrentScale();
  const [dimensions, setDimensions] = useState({width: 0, height: 0});

  useEffect(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    setDimensions({width: rect.width / scale, height: rect.height / scale});
  }, [scale]);

  return <div ref={ref}>Content to measure</div>;
};
```
