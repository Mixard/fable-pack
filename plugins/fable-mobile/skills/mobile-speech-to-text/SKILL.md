---
name: mobile-speech-to-text
description: Use when capturing a voice message in Russian, Ukrainian, or another non-English language in an Expo/React Native app and converting it to text on iOS and Android. Covers expo-speech-recognition, SFSpeechRecognizer vs iOS 26 SpeechAnalyzer/SpeechTranscriber, Android SpeechRecognizer/RecognizerIntent on-device models, and Gemini API audio transcription with pricing.
---

# Mobile Speech-to-Text (Expo, iOS, Android, Gemini)

Two independent choices, not one: (1) which engine transcribes — on-device (free, private, capability
varies by device) or cloud (paid, reliable, always covers the language) — and (2) how you capture
audio (`expo-audio`) versus how you recognize it live (`expo-speech-recognition`, which captures
its own audio internally and does not need `expo-audio` unless you also want to save the file).
On-device language coverage for Russian and especially Ukrainian is the crux of every decision below
— never assume support, always check the platform's own capability API at runtime.

## Decision: on-device vs cloud

| Language | Duration | Priority | Recommended path |
|---|---|---|---|
| Russian | < 60s | Free / private / offline | iOS: on-device `SpeechTranscriber` (iOS 26+) or `SFSpeechRecognizer` with `requiresOnDeviceRecognition`. Android: on-device `SpeechRecognizer` if `checkRecognitionSupport()` reports it installed. |
| Ukrainian | any | any | **Default to cloud (Gemini).** No confirmed on-device locale support found on either platform as of 2026-09-01 (see Unverified). Check the runtime capability API first and fall back to cloud when it's absent — don't hardcode "unsupported." |
| Either | > 60s | any | Cloud, or iOS `SpeechTranscriber` (no documented cap), or Android `EXTRA_SEGMENTED_SESSION`. **Never** legacy `SFSpeechRecognizer` server mode — hard ~60s cutoff, see below. |
| Either | any | Lowest cost, high volume | Gemini `gemini-2.5-flash-lite` / `gemini-3.5-flash-lite` — about $0.0006 per 60-second clip (see Cost table). Cheaper than the engineering cost of an on-device fallback path at low-to-medium volume. |
| Either | any | Guaranteed coverage, minimal capability-check code | Cloud (Gemini/OpenAI/ElevenLabs) — skips the on-device locale gamble entirely; multilingual by design. |
| Either | any | Must work with no network | On-device only: iOS `SpeechTranscriber`/`SFSpeechRecognizer` or Android on-device model, pre-downloaded. Accept that ru/uk may be unavailable on some devices and degrade gracefully (queue for later cloud transcription, or block the feature). |

## Expo layer

`expo-speech-recognition` (npm, MIT, maintainer `jamsch`, current `57.0.0`, published 2026-08-30 per
the npm registry's raw `time` field — targets Expo SDK 57 / RN 0.86 — older projects pin `@sdk-54` or
`@sdk-53`) wraps `SFSpeechRecognizer`/`SpeechAnalyzer` on iOS and `SpeechRecognizer`/`RecognizerIntent`
on Android behind one JS API. The config plugin's exact injections (from `app.plugin.js` at the repo
root): iOS `NSSpeechRecognitionUsageDescription` + `NSMicrophoneUsageDescription`; Android
`RECORD_AUDIO` permission plus a `<queries>` block (default package
`com.google.android.googlequicksearchbox`, extendable via `androidSpeechServicePackages`) and an
`android.speech.RecognitionService` intent-action query. Note: on Android 13+ the OS actually gates
availability via the separate `com.google.android.tts` package, not
`com.google.android.googlequicksearchbox` (which only matters on Android 12 and below) — you may need
to add it to `androidSpeechServicePackages`. These keys/permissions are required regardless of the
plugin, because the OS requires them independent of any wrapper.

```ts
ExpoSpeechRecognitionModule.start({
  lang: "ru-RU", // or "uk-UA" — BCP-47, no fixed enum on either platform
  interimResults: true,
  requiresOnDeviceRecognition: false, // true = never leaves the device; fails if unsupported
  addsPunctuation: true,
  continuous: false,
  androidIntentOptions: { EXTRA_PREFER_OFFLINE: true },
  iosTaskHint: "dictation", // "unspecified" | "dictation" | "search" | "confirmation"
});
```

If you record the file yourself (e.g. to also upload it to Gemini), use `expo-audio`, not this
module — it captures its own audio internally. `expo-audio` presets: `HIGH_QUALITY` (`.m4a`, 44.1kHz,
128kbps, stereo) and `LOW_QUALITY` (`.m4a`/`.3gp`, 44.1kHz, 64kbps, stereo). A 60-second recording is
therefore **~0.96MB at HIGH_QUALITY, ~469KB at LOW_QUALITY** (both stereo, computed from the bitrate —
not an official figure); a mono voice-message-tuned encoding (~24–32kbps) would land closer to
90–240KB. Background recording needs the `enableBackgroundRecording: true` plugin option, which adds
Android's `FOREGROUND_SERVICE` + `FOREGROUND_SERVICE_MICROPHONE` + `POST_NOTIFICATIONS` and iOS's
`UIBackgroundModes: ["audio"]`.

## iOS: SFSpeechRecognizer vs SpeechAnalyzer/SpeechTranscriber

| Fact | Value | Verified |
|---|---|---|
| `SFSpeechRecognizer` server-based duration cap | ~60s hard stop — "the framework stops speech recognition tasks that last longer than one minute" | 2026-09-01 |
| `SFSpeechRecognizer` daily/app quota | Enforced, no published number; expect throttling, retry later on fast failures | 2026-09-01 |
| `SFSpeechRecognizer.supportsOnDeviceRecognition` | Bool, since iOS 13; on-device path is not subject to the 60s cap | 2026-09-01 |
| `SpeechTranscriber` (new API) min OS | iOS/iPadOS/macOS/tvOS/visionOS **26.0+** — not watchOS | 2026-09-01 |
| `SpeechTranscriber` network path | None — on-device only, by design (privacy) | 2026-09-01 |
| `SpeechTranscriber` duration cap | None documented (contrast with the 60s SFSpeechRecognizer cap) | 2026-09-01 |
| `SpeechTranscriber` supported locales | **Not published as a static list anywhere** — `supportedLocales`/`installedLocales` are runtime-only properties. Best dated secondary evidence (a 2025-07 blog, WWDC25-beta era): `ru_RU` present, `uk_UA` absent from a 41-locale list. Treat as unconfirmed for today; call `SpeechTranscriber.supportedLocales` at runtime. | secondary, dated |
| iOS 27 | Exists — in developer/public beta (beta 8 / public beta 6 as of 2026-08-31, no stable/GA row published yet in Wikipedia's version-history table). Wikipedia's infobox says GA "September 2026" but its own lead sentence says only "late 2026" — treat the date as unresolved, not settled. No Speech-framework changes found in that source. | secondary |

Language models download via `AssetInventory`:

```swift
if let downloader = try await AssetInventory.assetInstallationRequest(supporting: [transcriber]) {
    try await downloader.downloadAndInstall()
}
```

Purpose strings: `NSSpeechRecognitionUsageDescription` ("A message that tells people why the app is
requesting to send user data to Apple's speech recognition servers" — required whenever you call an
API that can leave the device, i.e. any non-`requiresOnDeviceRecognition` use) and
`NSMicrophoneUsageDescription` ("A message that tells people why the app is requesting access to the
device's microphone" — standard mic-access key, all recording).

## Android: SpeechRecognizer / RecognizerIntent

| Constant | Confirmed | Purpose |
|---|---|---|
| `EXTRA_LANGUAGE` | Yes | BCP-47 tag string, e.g. `"ru-RU"`; no fixed enum |
| `EXTRA_PREFER_OFFLINE` | Yes | Bool — only use an offline recognition engine |
| `EXTRA_ENABLE_LANGUAGE_DETECTION` | Yes (verify before assuming — easy to guess wrong) | Bool — auto-detect spoken language; pair with `EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES` |
| `EXTRA_SEGMENTED_SESSION` | Yes (verify before assuming) | String — segmented/continuous long-dictation mode, combines with `EXTRA_AUDIO_SOURCE`, `EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS`, `EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS` |

On-device model lifecycle: `SpeechRecognizer.checkRecognitionSupport(recognizerIntent, executor,
callback)` is asynchronous (`void`, not a return value) — it delivers a `RecognitionSupport` object to
your `RecognitionSupportCallback`, exposing `getInstalledOnDeviceLanguages()`,
`getPendingOnDeviceLanguages()` (downloading), `getSupportedOnDeviceLanguages()` (available but not yet
downloaded — call `triggerModelDownload()` to fetch), and `getOnlineLanguages()`.
`isRecognitionAvailable()` / `isOnDeviceRecognitionAvailable()` both fail (return `false`) when no
recognition service is installed — in practice this means Google's Speech Services app / Gboard;
behavior on non-GMS OEM devices (Huawei, some Chinese ROMs) is undocumented in primary sources — don't
assume, detect and fall back to cloud.

`RECORD_AUDIO` is required to use `SpeechRecognizer` at all. For background capture, **Android 14
(API 34)+ requires** declaring `android:foregroundServiceType="microphone"` in the manifest, holding
the `FOREGROUND_SERVICE_MICROPHONE` permission, and passing `FOREGROUND_SERVICE_TYPE_MICROPHONE` to
`startForeground()` — `RECORD_AUDIO` alone is not enough once the app leaves the foreground.

Android 17 released 2026-06-16 (Wikipedia; corroborated by developer.android.com showing active
QPR1/QPR2 beta cycles on top of it as of a 2026-07-01 page timestamp) — no speech-recognition-specific
behavior changes were found in the primary pages checked, but the per-version behavior-change
sub-pages were not individually audited; re-check before relying on that absence.

## Cloud: Gemini API audio input

Formats: WAV, MP3, AIFF, AAC, OGG, FLAC, Opus, WebM (non-exhaustive — the live page also lists MPEG,
M4A, L16, ALAW, MULAW). Max **9.5 hours of audio per prompt**.
Token rate for batch transcription (record-then-send, as opposed to the streaming Live API): **32
tokens/second of audio** (60s = 1,920 tokens). As of 2026-09-01 the audio docs page's own code samples
use a newer "Interactions API" (`client.interactions.create`) with zero occurrences of `generateContent`
— verify the current method name in the SDK/reference before hardcoding either one. This is *not* the
same number used elsewhere on the pricing page for the Transcribe/Live-Translate/TTS model family (25
tokens/second, appearing on both real-time and audio-output line items) — don't conflate the two when
reading the pricing page. Inline base64 audio works up to **20MB total request size**; use the Files
API above that.

Gemini model names churn fast — as of 2026-09-01 at least five bare Flash generations coexist on the
live pricing page (2.5, 3, 3.5, 3.6, 3.7); 3.1 has no bare "-flash" tier, only
"-flash-lite"/"-flash-live-preview"/"-flash-image"/"-flash-tts-preview" variants. Verify against the
live pricing page before hardcoding an ID. Cheapest confirmed audio-**input** models today:
`gemini-2.5-flash-lite` and `gemini-3.5-flash-lite`, tied at $0.30 per 1M tokens for input — but their
**output** pricing is not tied ($0.40/1M vs $2.50/1M, 6.25x apart), so for a clip with a non-trivial
transcript `gemini-3.5-flash-lite` costs meaningfully more overall. The cost table below counts input
tokens only.

### Cost table (60-second mono clip, verified 2026-09-01)

| Service | Model | Rate | Cost per 60s clip |
|---|---|---|---|
| Gemini | `gemini-2.5-flash-lite` / `gemini-3.5-flash-lite` | $0.30 / 1M tokens, 32 tok/s | **~$0.0006** |
| OpenAI | `gpt-4o-mini-transcribe` | $0.003 / minute | **$0.003** |
| OpenAI | `gpt-4o-transcribe` / `Whisper` | $0.006 / minute | **$0.006** |
| ElevenLabs | Scribe (pay-as-you-go overage) | $0.22/hour "Extra hour, API" — uniform across Free/Starter/Creator/Pro; a separate on-page FAQ instead quotes a blended "starting from $0.40/hour" headline figure | **~$0.004–$0.007** |

Note: Gemini's separate async Batch API prices this same audio input at $0.15/1M (half of Standard) —
a different "batch" than this skill's record-then-send usage above; don't confuse the two when reading
the pricing page. Whisper is hidden behind an "All models" toggle on the live OpenAI pricing page by
default (present in the page's data, just not shown without expanding) — don't confuse it with the
separate, non-hidden "gpt-realtime-whisper" model, a live/realtime product priced at $0.017/minute.

(`platform.openai.com/docs/pricing` now 301-redirects to `developers.openai.com/api/docs/pricing`.)

## Gotchas

- Apple's own docs never publish a static SpeechTranscriber/SFSpeechRecognizer language list — check
  `supportedLocales` on-device, don't hardcode a list copied from a blog post or from memory.
- `EXTRA_ENABLE_LANGUAGE_DETECTION` and `EXTRA_SEGMENTED_SESSION` are real, current `RecognizerIntent`
  constants (confirmed in AOSP source) — a plausible-sounding guess that they "don't exist" is wrong.
- Android's foreground-service microphone-type requirement (Android 14+) is easy to miss if you only
  tested recording while the app is in the foreground.
- `addsPunctuation` silently produces no punctuation on Android unless on-device recognition is
  enabled — per the package's own README: "Not supported on Android 12 and below. On Android 13+,
  only supported when on-device recognition is enabled."
- Gemini's 32 tok/s batch-audio rate and its 25 tok/s Live-API rate are different products with
  different billing — check which endpoint a quoted price actually applies to.
- `expo-speech-recognition`'s config plugin injects its exact keys from `app.plugin.js`, not spelled
  out in the README's own prose — the OS-required permission keys apply either way, plugin or not.
- iOS 27 and Android 17 both already exist as of this skill's research date (2026-09-01) — don't
  assume "next major version, future/unreleased" when reasoning about either platform this year.

## Unverified

- Ukrainian on-device support (`uk_UA`/`uk-UA`) on iOS `SpeechTranscriber`/`SFSpeechRecognizer` or
  Android `SpeechRecognizer` — no primary source confirms or denies it; only dated (2025-07),
  secondary evidence exists for iOS, and it excludes Ukrainian.
- On-device Android speech recognition availability on non-Google-Mobile-Services devices.
- Any accuracy/WER benchmark for Russian or Ukrainian specifically, on-device vs. cloud, for any
  vendor (Apple, Google, Gemini, OpenAI, ElevenLabs) — none found from a primary or reputable source.

## Sources

- https://github.com/jamsch/expo-speech-recognition (README, package.json, LICENSE)
- https://www.npmjs.com/package/expo-speech-recognition
- https://docs.expo.dev/versions/latest/sdk/audio/
- https://developer.apple.com/documentation/speech/sfspeechrecognizer
- https://developer.apple.com/documentation/speech/speechtranscriber
- https://developer.apple.com/videos/play/wwdc2025/277/ ("Bring advanced speech-to-text to your app with SpeechAnalyzer")
- https://developer.apple.com/documentation/bundleresources/information-property-list
- https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/speech/RecognizerIntent.java
- https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/speech/SpeechRecognizer.java
- https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/speech/RecognitionSupport.java
- https://developer.android.com/develop/background-work/services/fgs/service-types
- https://developer.android.com/about/versions/17
- https://ai.google.dev/gemini-api/docs/audio
- https://ai.google.dev/gemini-api/docs/pricing
- https://developers.openai.com/api/docs/pricing
- https://elevenlabs.io/speech-to-text
- https://en.wikipedia.org/wiki/IOS_27 (secondary)
- https://en.wikipedia.org/wiki/Android_17 (secondary)
- https://antongubarenko.substack.com/p/ios-26-speechanalyzer-guide (secondary, dated 2025-07-28)
