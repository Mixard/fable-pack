# Animation, timing, sequencing, transitions

## interpolate

```ts
import {interpolate} from 'remotion';

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

Not clamped by default — values extrapolate outside the output range. Clamp with:

```ts
interpolate(frame, [0, 100], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### Easing

```ts
import {Easing, interpolate} from 'remotion';

interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

Default is `Easing.linear`. Combine a convexity with a curve:

- Convexities: `Easing.in` (slow start), `Easing.out` (slow end), `Easing.inOut`.
- Curves, most linear to most curved: `Easing.quad`, `Easing.sin`, `Easing.exp`, `Easing.circle`.
- Cubic bezier: `Easing.bezier(0.8, 0.22, 0.96, 0.65)`.

## spring

```ts
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const scale = spring({frame, fps});
```

Goes from 0 to 1. Default config `{mass: 1, damping: 10, stiffness: 100}` has visible bounce. Common configs:

```ts
const smooth = {damping: 200};                            // no bounce (subtle reveals; recommended default)
const snappy = {damping: 20, stiffness: 200};             // minimal bounce (UI elements)
const bouncy = {damping: 8};                              // playful entrance
const heavy = {damping: 15, stiffness: 80, mass: 2};      // slow, small bounce
```

- Delay: `spring({frame, fps, delay: 20})` or offset the frame: `spring({frame: frame - START, fps})`.
- Fixed duration: `spring({frame, fps, durationInFrames: 40})` stretches the curve; otherwise duration follows the physics.
- Map to other ranges via `interpolate(springProgress, [0, 1], [0, 360])`.
- Springs are plain numbers; combine with math, e.g. in/out animation:

```ts
const inAnimation = spring({frame, fps});
const outAnimation = spring({frame, fps, durationInFrames: 1 * fps, delay: durationInFrames - 1 * fps});
const scale = inAnimation - outAnimation;
```

## Sequence

`<Sequence>` shifts when children appear on the timeline:

```tsx
import {Sequence} from 'remotion';
const {fps} = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
```

- Children are wrapped in an absolute-fill container by default; `layout="none"` disables the wrapper.
- `premountFor={n}` mounts the component n frames early so assets are loaded before it becomes visible — recommended for every `<Sequence>` containing media.
- Inside a Sequence, `useCurrentFrame()` is local: within `<Sequence from={60} durationInFrames={30}>` it returns 0-29, not 60-89.
- Sequences nest; inner `from` values are relative to the outer sequence.

### Trimming animations with negative `from`

A negative `from` shifts time backwards, cutting the start of an animation:

```tsx
<Sequence from={-0.5 * fps}>
  <MyAnimation />  {/* useCurrentFrame() starts at 15 (at 30fps) */}
</Sequence>
```

`durationInFrames` unmounts content after n frames (trims the end). Nest to trim and delay:

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />  {/* first 15 frames trimmed, result delayed by 30 */}
  </Sequence>
</Sequence>
```

## Series

`<Series>` plays items back to back:

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={45}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><MainContent /></Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={30}>
    <Outro />  {/* negative offset: starts 15 frames before the previous ends */}
  </Series.Sequence>
</Series>
```

Same absolute-fill wrapping and `layout="none"` behavior as `<Sequence>`.

## Transitions: @remotion/transitions

Install: `npx remotion add @remotion/transitions`. `<TransitionSeries>` absolutely positions its children.

```tsx
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}><SceneA /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: 15})} />
  <TransitionSeries.Sequence durationInFrames={60}><SceneB /></TransitionSeries.Sequence>
</TransitionSeries>;
```

Presentations (each from its own module):

```tsx
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {flip} from '@remotion/transitions/flip';
import {clockWipe} from '@remotion/transitions/clock-wipe';
```

`slide({direction: 'from-left'})` — directions: `"from-left"`, `"from-right"`, `"from-top"`, `"from-bottom"`.

Timings:

```tsx
import {linearTiming, springTiming} from '@remotion/transitions';

linearTiming({durationInFrames: 20});
springTiming({config: {damping: 200}, durationInFrames: 25});
```

### Duration math

Transitions overlap adjacent scenes, so total length is shorter than the sum of sequence durations: two 60-frame scenes with a 15-frame transition = `60 + 60 - 15 = 105` frames. Get a transition's duration from its timing object:

```tsx
linearTiming({durationInFrames: 20}).getDurationInFrames({fps: 30}); // 20
springTiming({config: {damping: 200}}).getDurationInFrames({fps: 30}); // depends on when the spring settles
```

`springTiming` without an explicit `durationInFrames` depends on `fps`. Total composition duration = sum of scene durations minus sum of transition durations.

## Text animation patterns

- Typewriter: slice the string by frame count (`fullText.slice(0, Math.floor(frame / CHAR_FRAMES))`), not per-character opacity. Full example with blinking cursor and mid-sentence pause: `assets/text-animations-typewriter.tsx`.
- Word highlight (highlighter-pen wipe): absolutely positioned background span scaled with `scaleX` from a spring, `transformOrigin: 'left center'`. Full example: `assets/text-animations-word-highlight.tsx`.
