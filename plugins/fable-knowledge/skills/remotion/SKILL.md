---
name: remotion
description: Use when writing or reviewing Remotion code (video creation in React). Covers compositions, frame-driven animation with interpolate/spring, calculateMetadata, media embedding, captions, transitions, Mediabunny metadata/frame extraction, fonts, charts, 3D, Lottie, and Tailwind.
---

# Remotion

Remotion renders videos from React components. A video is a function of the current frame: every visual state derives from `useCurrentFrame()`.

## Core rules

- All animation is driven by `useCurrentFrame()`. CSS transitions/animations and Tailwind `animate-*` / `transition-*` classes do not render correctly (frames are rendered independently, so time-based CSS produces flicker or static output). The same applies to self-animating third-party libraries (chart libs, `useFrame()` from React Three Fiber, Lottie autoplay).
- Express durations in seconds and multiply by `fps` from `useVideoConfig()`.
- Reference files in `public/` via `staticFile()`; remote URLs work directly.

## Composition

A `<Composition>` (usually in `src/Root.tsx`) defines component, `width`, `height`, `fps`, `durationInFrames`:

```tsx
import {Composition} from 'remotion';

export const RemotionRoot = () => (
  <Composition
    id="MyComposition"
    component={MyComposition}
    durationInFrames={100}
    fps={30}
    width={1080}
    height={1080}
    defaultProps={{title: 'Hello'} satisfies MyCompositionProps}
  />
);
```

- `defaultProps` values must be JSON-serializable (`Date`, `Map`, `Set`, and `staticFile()` are supported). Declare prop types with `type`, not `interface`, for `defaultProps` type safety.
- `<Still>` defines a single-frame image; no `durationInFrames`/`fps` needed.
- `<Folder name="...">` groups compositions in the Studio sidebar (names: letters, numbers, hyphens only).

## Basic animation

```tsx
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
  extrapolateRight: 'clamp',
});
```

`interpolate` does not clamp by default; pass `extrapolateLeft`/`extrapolateRight: 'clamp'` to keep values in range.

```tsx
import {spring} from 'remotion';

const scale = spring({frame, fps, config: {damping: 200}});
```

`spring()` goes 0 to 1 with physical motion. `{damping: 200}` gives smooth motion without bounce. Details, easing curves, and common configs: `references/animation.md`.

## calculateMetadata

Pass `calculateMetadata` to `<Composition>` to set duration, dimensions, fps, or props dynamically before rendering:

```tsx
import {CalculateMetadataFunction} from 'remotion';

const calculateMetadata: CalculateMetadataFunction<Props> = async ({props, abortSignal}) => {
  const data = await fetch(props.dataUrl, {signal: abortSignal}).then((r) => r.json());
  return {
    durationInFrames: Math.ceil(data.duration * 30),
    props: {...props, fetchedData: data},
  };
};
```

It runs once before rendering. All return fields are optional and override the `<Composition>` props: `durationInFrames`, `width`, `height`, `fps`, `props`, `defaultOutName`, `defaultCodec`. `abortSignal` cancels stale requests when props change in the Studio. Patterns for sizing to media files: `references/measuring.md`.

## References

- `references/media.md` - Assets and `staticFile()`, `<Video>`, `<Img>`, `<AnimatedImage>`/`<Gif>`, `<Audio>`; trimming, volume, speed, looping, pitch.
- `references/animation.md` - `interpolate` easing, `spring` configs, `<Sequence>`/`<Series>`, `<TransitionSeries>` transitions, trimming animations, text animation patterns.
- `references/captions.md` - Transcription options, `parseSrt()`, `createTikTokStyleCaptions()`, word highlighting.
- `references/measuring.md` - Mediabunny (duration, dimensions, decode check, frame extraction), `getImageDimensions()`, `getGifDurationInSeconds()`, measuring text and DOM nodes, calculateMetadata sizing patterns.
- `references/visuals.md` - Fonts (Google and local), charts, Three.js via `@remotion/three`, Lottie, TailwindCSS.
- `references/assets/` - Complete example components: bar chart, typewriter, word highlight.

Optional packages install via `npx remotion add <package>` (or `bunx`/`yarn`/`pnpm exec` equivalents), e.g. `npx remotion add @remotion/media`.
