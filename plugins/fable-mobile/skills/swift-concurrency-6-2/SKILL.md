---
name: swift-concurrency-6-2
description: Use when writing or migrating Swift 6.2 concurrency code. Covers SE-0461/SE-0466 semantics (async stays on the caller, MainActor default inference), @concurrent offloading, isolated conformances, and Xcode 26 build settings.
---

# Swift 6.2 Approachable Concurrency

Swift 6.2 changes the default execution model: code is single-threaded by default and concurrency is introduced explicitly. Two proposals define the version-specific behavior:

- **SE-0461 (NonisolatedNonsendingByDefault)**: nonisolated async functions run on the caller's actor instead of being implicitly offloaded to the concurrent pool.
- **SE-0466 (MainActor default isolation)**: an opt-in mode where declarations in a module are inferred `@MainActor` unless marked otherwise. Recommended for apps, scripts, and other executable targets.

Both are opt-in build settings; without them, pre-6.2 offloading semantics apply.

## Async stays on the calling actor

In Swift 6.1 and earlier, async functions could be implicitly offloaded to background threads, producing data-race errors in seemingly safe code:

```swift
@MainActor
final class StickerModel {
    let photoProcessor = PhotoProcessor()

    func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
        guard let data = try await item.loadTransferable(type: Data.self) else { return nil }
        // Swift 6.1: error — "Sending 'self.photoProcessor' risks causing data races"
        // Swift 6.2: OK — the async call stays on MainActor
        return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
    }
}
```

Consequence: do not assume async code runs in the background. Under 6.2 defaults it runs wherever the caller is isolated, unless marked `@concurrent`.

## Isolated conformances

MainActor types can conform to non-isolated protocols by isolating the conformance itself:

```swift
protocol Exportable {
    func export()
}

// Swift 6.1: error — crosses into main actor-isolated code
// Swift 6.2: OK
extension StickerModel: @MainActor Exportable {
    func export() {
        photoProcessor.exportAsPNG()
    }
}
```

The compiler restricts use of the conformance to the matching actor:

```swift
@MainActor
struct ImageExporter {
    var items: [any Exportable]
    mutating func add(_ item: StickerModel) {
        items.append(item)  // OK: same isolation
    }
}

nonisolated struct ImageExporter {
    var items: [any Exportable]
    mutating func add(_ item: StickerModel) {
        items.append(item)  // error: main actor-isolated conformance cannot be used here
    }
}
```

Prefer isolated conformances over `nonisolated` workarounds or `@Sendable` wrappers.

## Global and static state

Global/static mutable state of non-Sendable types needs actor isolation:

```swift
// Swift 6.1: error — non-Sendable type may have shared mutable state
final class StickerLibrary {
    static let shared: StickerLibrary = .init()
}

// Fix
@MainActor
final class StickerLibrary {
    static let shared: StickerLibrary = .init()
}
```

With SE-0466 (MainActor default inference) enabled, the annotation is unnecessary — classes, their stored properties, and their protocol conformances in the module are implicitly `@MainActor`.

## @concurrent for background work

`@concurrent` explicitly opts a function into the concurrent thread pool. Reserve it for CPU-intensive work (image processing, compression, heavy computation); profile before offloading.

```swift
nonisolated final class PhotoProcessor {
    private var cachedStickers: [String: Sticker] = [:]

    func extractSticker(data: Data, with id: String) async -> Sticker {
        if let sticker = cachedStickers[id] { return sticker }
        let sticker = await Self.extractSubject(from: data)
        cachedStickers[id] = sticker
        return sticker
    }

    @concurrent
    static func extractSubject(from data: Data) async -> Sticker { /* ... */ }
}

let processor = PhotoProcessor()
processedPhotos[item.id] = await processor.extractSticker(data: data, with: item.id)
```

Requirements for `@concurrent`:
1. The containing type is `nonisolated`
2. The function is `async`
3. Call sites `await`

Version-specific gotcha: this example is only safe with SE-0461 and SE-0466 enabled — then `extractSticker` stays on the caller's actor and the mutable `cachedStickers` access is serialized. Without those settings the same code has a data race, and the compiler flags it.

## Enabling in Xcode 26 / SPM

- Xcode 26: Build Settings > Swift Compiler > Concurrency section — enable Approachable Concurrency features (SE-0461, SE-0466) individually; incremental adoption is the intended path.
- SPM: enable via the `SwiftSettings` API in `Package.swift` (upcoming feature flags).
- Migration tooling for automatic code changes: swift.org/migration.

## Notes

- The compiler is the source of truth: a reported data race is a real isolation issue, not noise to suppress with `nonisolated`.
- Most async functions do not need `@concurrent`; applying it everywhere reintroduces the offloading 6.2 removed.
- Actors replace most legacy `DispatchQueue` synchronization patterns.
- Data-race issues surface as compile-time errors after migration, so a clean build is meaningful verification.
