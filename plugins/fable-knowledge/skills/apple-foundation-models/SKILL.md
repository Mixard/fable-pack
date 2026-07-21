---
name: apple-foundation-models
description: Use when integrating Apple's on-device LLM via the FoundationModels framework (iOS 26+). Covers SystemLanguageModel availability cases, LanguageModelSession, @Generable/@Guide guided generation, PartiallyGenerated snapshot streaming, tool calling, and the 4096-token context limit.
---

# Apple FoundationModels (on-device LLM, iOS 26+)

The FoundationModels framework runs Apple Intelligence's language model entirely on-device: no network, no data leaving the device. Key constraints: availability depends on device eligibility and user settings, and the context window is 4,096 tokens total (instructions + prompt + output combined) — chunk larger inputs across sessions.

## Availability

Check `SystemLanguageModel.default.availability` before creating a session; every unavailability case is reachable in the field:

```swift
struct GenerativeView: View {
    private var model = SystemLanguageModel.default

    var body: some View {
        switch model.availability {
        case .available:
            ContentView()
        case .unavailable(.deviceNotEligible):
            Text("Device not eligible for Apple Intelligence")
        case .unavailable(.appleIntelligenceNotEnabled):
            Text("Please enable Apple Intelligence in Settings")
        case .unavailable(.modelNotReady):
            Text("Model is downloading or not ready")
        case .unavailable(let other):
            Text("Model unavailable: \(other)")
        }
    }
}
```

## LanguageModelSession

```swift
// Single-turn: new session each time
let session = LanguageModelSession()
let response = try await session.respond(to: "What's a good month to visit Paris?")
print(response.content)

// Multi-turn: reuse the session; it keeps conversation context
let session = LanguageModelSession(instructions: """
    You are a cooking assistant.
    Provide recipe suggestions based on ingredients.
    Keep suggestions brief and practical.
    """)
let first = try await session.respond(to: "I have chicken and rice")
let followUp = try await session.respond(to: "What about a vegetarian option?")
```

- The result is on `response.content` — there is no `.output` property; that is a common wrong guess.
- `instructions` take priority over prompts; use them for role, task, style, and safety framing.
- A session handles one request at a time — check `session.isResponding` before sending another, or create multiple sessions for concurrency.
- `GenerationOptions(temperature:)` tunes creativity (higher = more creative).

## Guided generation with @Generable

Generate typed Swift values instead of parsing strings:

```swift
@Generable(description: "Basic profile information about a cat")
struct CatProfile {
    var name: String

    @Guide(description: "The age of the cat", .range(0...20))
    var age: Int

    @Guide(description: "A one sentence profile about the cat's personality")
    var profile: String
}

let response = try await session.respond(
    to: "Generate a cute rescue cat",
    generating: CatProfile.self
)
print(response.content.name)   // typed access
```

`@Guide` constraints:
- `.range(0...20)` — numeric range
- `.count(3)` — array element count
- `description:` — semantic guidance

The macro also generates a `PartiallyGenerated` companion type used for streaming.

## Snapshot streaming

Streaming yields snapshots, not deltas: each element is a complete partial state of the value, with all properties Optional (`TripIdeas.PartiallyGenerated`).

```swift
@Generable
struct TripIdeas {
    @Guide(description: "Ideas for upcoming trips")
    var ideas: [String]
}

let stream = session.streamResponse(
    to: "What are some exciting trip ideas?",
    generating: TripIdeas.self
)

for try await partial in stream {
    // partial: TripIdeas.PartiallyGenerated
}
```

SwiftUI integration:

```swift
@State private var partialResult: TripIdeas.PartiallyGenerated?
@State private var errorMessage: String?

var body: some View {
    List {
        ForEach(partialResult?.ideas ?? [], id: \.self) { idea in
            Text(idea)
        }
    }
    .task {
        do {
            let stream = session.streamResponse(to: prompt, generating: TripIdeas.self)
            for try await partial in stream {
                partialResult = partial
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
```

## Tool calling

A tool is a struct conforming to `Tool` with `name`, `description`, a `@Generable` `Arguments` type, and `call(arguments:) async throws -> ToolOutput`:

```swift
struct RecipeSearchTool: Tool {
    let name = "recipe_search"
    let description = "Search for recipes matching a given term and return a list of results."

    @Generable
    struct Arguments {
        var searchTerm: String
        var numberOfResults: Int
    }

    func call(arguments: Arguments) async throws -> ToolOutput {
        let recipes = await searchRecipes(term: arguments.searchTerm,
                                          limit: arguments.numberOfResults)
        return .string(recipes.map { "- \($0.name): \($0.description)" }.joined(separator: "\n"))
    }
}

let session = LanguageModelSession(tools: [RecipeSearchTool()])
let response = try await session.respond(to: "Find me some pasta recipes")
```

Tool errors surface as `LanguageModelSession.ToolCallError`, which carries the tool and the underlying error:

```swift
do {
    let answer = try await session.respond(to: "Find a recipe for tomato soup.")
} catch let error as LanguageModelSession.ToolCallError {
    print(error.tool.name)
    if case .databaseIsEmpty = error.underlyingError as? RecipeSearchToolError {
        // handle specific tool failure
    }
}
```

## Practical notes

- Prefer `@Generable` output over parsing free text whenever the result has structure.
- Break complex multi-step tasks into several focused prompts rather than one large one — the 4,096-token budget covers instructions, prompt, and output together.
- Profile request latency with Xcode Instruments.
