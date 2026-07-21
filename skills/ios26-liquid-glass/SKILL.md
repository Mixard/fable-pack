---
name: ios26-liquid-glass
description: Use when implementing the iOS 26 Liquid Glass material in SwiftUI, UIKit, or WidgetKit. Covers glassEffect variants, GlassEffectContainer, glassEffectID/glassEffectUnion morphing, UIGlassEffect/UIGlassContainerEffect, scroll edge effects, and widget accented rendering.
---

# iOS 26 Liquid Glass

Liquid Glass is the iOS 26 dynamic material: it blurs content behind it, reflects surrounding color and light, and can react to touch and pointer interaction. APIs exist for SwiftUI, UIKit, and WidgetKit.

## SwiftUI

### glassEffect

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()  // default: .regular variant, capsule shape
```

Customized:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.tint(.orange).interactive(), in: .rect(cornerRadius: 16.0))
```

- `.regular` — standard glass
- `.tint(Color)` — color tint for prominence
- `.interactive()` — reacts to touch/pointer; opt-in, use only on elements that respond to interaction
- Shapes: `.capsule` (default), `.rect(cornerRadius:)`, `.circle`

Apply `.glassEffect()` after other appearance modifiers (frame, font, padding).

### Button styles

```swift
Button("Click Me") { }.buttonStyle(.glass)
Button("Important") { }.buttonStyle(.glassProminent)
```

### GlassEffectContainer

Wrap multiple sibling glass views in a container — it improves rendering performance and enables shape merging and morphing. Multiple standalone `.glassEffect()` siblings without a container is the main performance mistake.

```swift
GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()

        Image(systemName: "eraser.fill")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()
    }
}
```

`spacing` controls merge distance: elements closer than the spacing blend their glass shapes together.

### glassEffectUnion

Combines multiple views into a single glass shape by group id:

```swift
@Namespace private var namespace

GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        ForEach(symbolSet.indices, id: \.self) { item in
            Image(systemName: symbolSet[item])
                .frame(width: 80.0, height: 80.0)
                .glassEffect()
                .glassEffectUnion(id: item < 2 ? "group1" : "group2", namespace: namespace)
        }
    }
}
```

### Morphing with glassEffectID

Glass elements morph between each other when views appear/disappear inside a container, keyed by `glassEffectID` in a shared `@Namespace`. Wrap the state change in `withAnimation` or the morph does not animate.

```swift
@State private var isExpanded = false
@Namespace private var namespace

GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .glassEffect()
            .glassEffectID("pencil", in: namespace)

        if isExpanded {
            Image(systemName: "eraser.fill")
                .frame(width: 80.0, height: 80.0)
                .glassEffect()
                .glassEffectID("eraser", in: namespace)
        }
    }
}

Button("Toggle") {
    withAnimation { isExpanded.toggle() }
}
.buttonStyle(.glass)
```

### Scrolling under sidebar/inspector

No dedicated modifier: when a horizontal `ScrollView`'s content reaches the leading/trailing container edges, the system handles under-sidebar scrolling automatically.

## UIKit

### UIGlassEffect

```swift
let glassEffect = UIGlassEffect()
glassEffect.tintColor = UIColor.systemBlue.withAlphaComponent(0.3)
glassEffect.isInteractive = true

let visualEffectView = UIVisualEffectView(effect: glassEffect)
visualEffectView.layer.cornerRadius = 20
visualEffectView.clipsToBounds = true  // required with corner radius

// Content goes into contentView, not the effect view itself
visualEffectView.contentView.addSubview(label)
```

### UIGlassContainerEffect

Same container concept as SwiftUI's `GlassEffectContainer`:

```swift
let containerEffect = UIGlassContainerEffect()
containerEffect.spacing = 40.0

let containerView = UIVisualEffectView(effect: containerEffect)
let firstGlass = UIVisualEffectView(effect: UIGlassEffect())
let secondGlass = UIVisualEffectView(effect: UIGlassEffect())
containerView.contentView.addSubview(firstGlass)
containerView.contentView.addSubview(secondGlass)
```

### Scroll edge effects

```swift
scrollView.topEdgeEffect.style = .automatic
scrollView.bottomEdgeEffect.style = .hard
scrollView.leftEdgeEffect.isHidden = true
```

### Toolbar items

```swift
let favoriteButton = UIBarButtonItem(image: UIImage(systemName: "heart"),
                                     style: .plain, target: self, action: #selector(favoriteAction))
favoriteButton.hidesSharedBackground = true  // opt out of the shared glass background
```

## WidgetKit

When the user selects a tinted Home Screen, widgets render in accented mode (white-tinted content on themed glass). Ignoring this mode breaks the tinted appearance.

```swift
struct MyWidgetView: View {
    @Environment(\.widgetRenderingMode) var renderingMode

    var body: some View {
        if renderingMode == .accented {
            // tinted mode
        } else {
            // full color mode
        }
    }
}
```

Accent groups — views marked `.widgetAccentable()` join the accent group; unmarked views stay in the primary group:

```swift
HStack {
    VStack(alignment: .leading) {
        Text("Title").widgetAccentable()
        Text("Subtitle")  // primary group (default)
    }
    Image(systemName: "star.fill").widgetAccentable()
}
```

Images in accented mode:

```swift
Image("myImage")
    .widgetAccentedRenderingMode(.monochrome)
```

Container background:

```swift
VStack { /* content */ }
    .containerBackground(for: .widget) {
        Color.blue.opacity(0.2)
    }
```

## Gotchas

- An opaque background behind glass defeats the translucency; glass needs visible content behind it.
- Nested glass effects degrade performance and visual clarity — reserve glass for interactive elements, toolbars, and cards, not every view.
- Test light, dark, and accented/tinted appearances; text on glass needs sufficient contrast.
- UIKit: forgetting `clipsToBounds = true` with `layer.cornerRadius` leaves square corners on the effect view.
