# Captions: transcription, SRT import, display

Package: `@remotion/captions` (`npx remotion add @remotion/captions`). All utilities operate on its `Caption` type.

## Transcription options

- `@remotion/install-whisper-cpp` — Whisper.cpp on a server. Fast, free, needs server infrastructure. https://remotion.dev/docs/install-whisper-cpp
- `@remotion/whisper-web` — Whisper via WebAssembly in the browser. No server, free, slower. https://remotion.dev/docs/whisper-web
- `@remotion/openai-whisper` — OpenAI Whisper API. Fast, no server, paid. https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions

## Importing .srt files

Parse with `parseSrt()`; gate rendering on the async load with `useDelayRender`:

```tsx
import {useState, useEffect, useCallback} from 'react';
import {AbsoluteFill, staticFile, useDelayRender} from 'remotion';
import {parseSrt} from '@remotion/captions';
import type {Caption} from '@remotion/captions';

export const MyComponent: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const {delayRender, continueRender, cancelRender} = useDelayRender();
  const [handle] = useState(() => delayRender());

  const fetchCaptions = useCallback(async () => {
    try {
      const response = await fetch(staticFile('subtitles.srt'));
      const text = await response.text();
      const {captions: parsed} = parseSrt({input: text});
      setCaptions(parsed);
      continueRender(handle);
    } catch (e) {
      cancelRender(e);
    }
  }, [continueRender, cancelRender, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  if (!captions) {
    return null;
  }

  return <AbsoluteFill>{/* use captions */}</AbsoluteFill>;
};
```

Remote `.srt` files can be fetched by URL instead of `staticFile()`.

## Grouping into pages

`createTikTokStyleCaptions()` groups captions into pages. `combineTokensWithinMilliseconds` controls words per page (higher = more words at once, lower = word-by-word):

```tsx
import {useMemo} from 'react';
import {createTikTokStyleCaptions} from '@remotion/captions';

const SWITCH_CAPTIONS_EVERY_MS = 1200;

const {pages} = useMemo(() => {
  return createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
  });
}, [captions]);
```

## Rendering pages with Sequences

```tsx
import {Sequence, useVideoConfig, AbsoluteFill} from 'remotion';
import type {TikTokPage} from '@remotion/captions';

const CaptionedContent: React.FC = () => {
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill>
      {pages.map((page, index) => {
        const nextPage = pages[index + 1] ?? null;
        const startFrame = (page.startMs / 1000) * fps;
        const endFrame = Math.min(
          nextPage ? (nextPage.startMs / 1000) * fps : Infinity,
          startFrame + (SWITCH_CAPTIONS_EVERY_MS / 1000) * fps,
        );
        const durationInFrames = endFrame - startFrame;

        if (durationInFrames <= 0) {
          return null;
        }

        return (
          <Sequence key={index} from={startFrame} durationInFrames={durationInFrames}>
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Word highlighting

Each `TikTokPage` has `tokens` with `fromMs`/`toMs`. Since `useCurrentFrame()` is local inside the Sequence, add `page.startMs` to get absolute time:

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {TikTokPage} from '@remotion/captions';

const HIGHLIGHT_COLOR = '#39E508';

const CaptionPage: React.FC<{page: TikTokPage}> = ({page}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const currentTimeMs = (frame / fps) * 1000;
  const absoluteTimeMs = page.startMs + currentTimeMs;

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontSize: 80, fontWeight: 'bold', whiteSpace: 'pre'}}>
        {page.tokens.map((token) => {
          const isActive = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
          return (
            <span key={token.fromMs} style={{color: isActive ? HIGHLIGHT_COLOR : 'white'}}>
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```
