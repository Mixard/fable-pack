---
name: wcag22-reference
description: Use when implementing or auditing accessibility on Web, iOS, or Android. Covers WCAG 2.2 success criteria (numbers, names, levels), contrast ratios, target sizes, and the cross-platform mapping for labels, hints, roles, and live regions.
---

# WCAG 2.2 Reference

## Key Success Criteria and Thresholds

| SC | Name | Level | Threshold / rule |
|----|------|-------|------------------|
| 1.4.3 | Contrast (Minimum) | AA | Text 4.5:1; large text (18pt / 14pt bold and up) 3:1 |
| 1.4.11 | Non-text Contrast | AA | UI components and graphical objects 3:1 |
| 1.4.10 | Reflow | AA | Content usable at 400% zoom (320 CSS px width) without 2D scrolling |
| 2.1.2 | No Keyboard Trap | A | Focus must be escapable (Escape key or explicit close) |
| 2.5.7 | Dragging Movements | AA | Every drag action needs a single-pointer alternative |
| 2.5.8 | Target Size (Minimum) | AA | 24x24 CSS px minimum (new in 2.2); platform HIGs recommend 44x44pt (iOS) / 48x48dp (Android) |
| 3.2.6 | Consistent Help | A | Help mechanisms appear in the same relative order across pages (new in 2.2) |
| 3.3.3 | Error Suggestion | AA | Errors described in text with correction suggestions |
| 3.3.7 | Redundant Entry | A | Do not ask for the same data twice in one process (new in 2.2) |
| 3.3.8 | Accessible Authentication (Minimum) | AA | No cognitive test (e.g. transcription, puzzle) without alternative (new in 2.2) |
| 4.1.2 | Name, Role, Value | A | Custom controls expose name, role, state to the accessibility tree |

Focus-related criteria new in 2.2: 2.4.11 Focus Not Obscured (Minimum, AA), 2.4.12 Focus Not Obscured (Enhanced, AAA), 2.4.13 Focus Appearance (AAA). Note: 4.1.1 Parsing was removed in WCAG 2.2.

## Cross-Platform Mapping

| Feature | Web (HTML/ARIA) | iOS (SwiftUI) | Android (Compose) |
|---------|-----------------|---------------|-------------------|
| Primary label | `aria-label` / `<label>` | `.accessibilityLabel()` | `contentDescription` |
| Secondary hint | `aria-describedby` | `.accessibilityHint()` | `Modifier.semantics { stateDescription = ... }` |
| Action role | `role="button"` | `.accessibilityAddTraits(.isButton)` | `Modifier.semantics { role = Role.Button }` |
| Live updates | `aria-live="polite"` | `.accessibilityLiveRegion(.polite)` | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` |

## Platform Snippets

Web icon-only button inside a search form:

```html
<form role="search">
  <label for="q" class="sr-only">Search products</label>
  <input type="search" id="q" />
  <button type="submit" aria-label="Submit search">
    <svg aria-hidden="true">...</svg>
  </button>
</form>
```

iOS:

```swift
Button(action: deleteItem) { Image(systemName: "trash") }
    .accessibilityLabel("Delete item")
    .accessibilityHint("Permanently removes this item from your list")
```

Android:

```kotlin
Switch(
    checked = isEnabled,
    onCheckedChange = { onToggle() },
    modifier = Modifier.semantics { contentDescription = "Enable notifications" }
)
```

## Gotchas

- Div-buttons: a `<div>` with a click handler needs `role="button"`, `tabindex="0"`, and Enter/Space key handling; prefer `<button>`.
- Color-only meaning fails 1.4.1: pair color changes (e.g. red border) with text or an icon.
- Modals: trap focus while open, release to the trigger element on close; dropdowns and menus likewise restore focus to their trigger.
- Alt text: never prefix with "Image of" or "Picture of" -- screen readers already announce the role.
- Focus indicators need 3:1 contrast against adjacent colors (1.4.11 applies to focus rings).
