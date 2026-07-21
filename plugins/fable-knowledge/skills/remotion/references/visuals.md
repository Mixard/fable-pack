# Fonts, charts, 3D, Lottie, Tailwind

## Google Fonts: @remotion/google-fonts

Install: `npx remotion add @remotion/google-fonts`. Type-safe; blocks rendering until the font is ready.

```tsx
import {loadFont} from '@remotion/google-fonts/Roboto';

const {fontFamily} = loadFont('normal', {
  weights: ['400', '700'],
  subsets: ['latin'],
});

export const Title = () => <div style={{fontFamily}}>Hello World</div>;
```

Specify only needed weights/subsets to reduce download size. `loadFont()` also returns `waitUntilDone()` — await it before measuring text. Call `loadFont()` at module top level (or in an early-imported file), not inside render.

## Local fonts: @remotion/fonts

Install: `npx remotion add @remotion/fonts`. Put font files in `public/`:

```tsx
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

await loadFont({
  family: 'MyFont',            // required: CSS name
  url: staticFile('MyFont-Regular.woff2'), // required
  format: 'woff2',             // optional, auto-detected from extension
  weight: '400',               // optional
  style: 'normal',             // optional: normal | italic
  display: 'block',            // optional: font-display
});
```

Multiple weights: call `loadFont()` once per file with the same `family` and different `weight`, wrapped in `Promise.all`.

## Charts

Build charts with plain HTML/SVG/D3. Third-party chart libraries with built-in animation cause flicker — disable their animations and drive everything from `useCurrentFrame()`.

Staggered bars (full component: `assets/charts-bar-chart.tsx`):

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const bars = data.map((item, i) => {
  const height = spring({frame, fps, delay: i * STAGGER_DELAY, config: {damping: 200}});
  return <div style={{height: height * item.value}} />;
});
```

Pie chart segments via stroke-dashoffset, rotated to start at 12 o'clock:

```tsx
const progress = interpolate(frame, [0, 100], [0, 1]);
const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle
  r={radius} cx={center} cy={center} fill="none"
  stroke={color} strokeWidth={strokeWidth}
  strokeDasharray={`${segmentLength} ${circumference}`}
  strokeDashoffset={offset}
  transform={`rotate(-90 ${center} ${center})`}
/>;
```

## 3D: @remotion/three

Install: `npx remotion add @remotion/three`. Standard React Three Fiber / Three.js practices apply, plus:

- Wrap 3D content in `<ThreeCanvas>` with explicit `width` and `height` props, and include lighting:

```tsx
import {ThreeCanvas} from '@remotion/three';
import {useVideoConfig} from 'remotion';

const {width, height} = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <ambientLight intensity={0.4} />
  <directionalLight position={[5, 5, 5]} intensity={0.8} />
  <mesh>
    <sphereGeometry args={[1, 32, 32]} />
    <meshStandardMaterial color="red" />
  </mesh>
</ThreeCanvas>;
```

- No self-animating shaders/models and no `useFrame()` from `@react-three/fiber` — both cause flicker during rendering. Derive motion from `useCurrentFrame()`:

```tsx
const frame = useCurrentFrame();
<mesh rotation={[0, frame * 0.02, 0]}>...</mesh>;
```

- Any `<Sequence>` inside `<ThreeCanvas>` must have `layout="none"` (the default div wrapper is not valid inside a Three scene).

## Lottie: @remotion/lottie

Install: `npx remotion add @remotion/lottie`. Fetch the animation JSON, gate rendering with `delayRender`/`continueRender`, then render `<Lottie>`:

```tsx
import {Lottie, LottieAnimationData} from '@remotion/lottie';
import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender} from 'remotion';

export const MyAnimation = () => {
  const [handle] = useState(() => delayRender('Loading Lottie animation'));
  const [animationData, setAnimationData] = useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch('https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json')
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        cancelRender(err);
      });
  }, [handle]);

  if (!animationData) {
    return null;
  }

  return <Lottie animationData={animationData} style={{width: 400, height: 400}} />;
};
```

## TailwindCSS

Tailwind works in Remotion once installed and enabled for the project (setup: https://www.remotion.dev/docs/tailwind). Do not use `transition-*` or `animate-*` classes — they do not render correctly; animate via `useCurrentFrame()` and inline styles instead.
