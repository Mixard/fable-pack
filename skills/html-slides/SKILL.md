---
name: html-slides
description: Use when building a self-contained HTML presentation deck. Covers a viewport-safe CSS base with clamp() scaling and short-height breakpoints, slide density limits, a catalog of 12 visual presets (font pairings, palettes, signatures), and the negated-CSS-function gotcha.
---

# HTML Slides

Zero-dependency decks: one HTML file, inline CSS/JS, keyboard/wheel/touch navigation, `prefers-reduced-motion` support. Fonts may come from Google Fonts or Fontshare.

## Viewport Fit

Each slide occupies exactly one viewport height; content that does not fit gets split into more slides, never scrolled or shrunk below readable sizes.

Density limits per slide type:

| Slide type | Maximum content |
|------------|-----------------|
| Title | 1 heading + 1 subtitle + optional tagline |
| Content | 1 heading + 4-6 bullets or 2 paragraphs |
| Feature grid | 6 cards |
| Code | 8-10 lines |
| Quote | 1 quote + attribution |
| Image | 1 image, ideally under 60vh |

## Base CSS

Copy this block into every deck, then theme on top of it. All type and spacing scale with `clamp()`; short-height breakpoints keep landscape phones and small windows usable.

```css
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

:root {
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    .grid {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}
```

## Preset Catalog

| Preset | Fonts | Palette | Signature | Best for |
|--------|-------|---------|-----------|----------|
| Bold Signal | Archivo Black + Space Grotesk | charcoal, hot orange focal card, white | oversized section numbers, high-contrast card on dark | pitch decks, launches |
| Electric Studio | Manrope | black, white, cobalt accent | two-panel split, sharp editorial alignment | client decks, strategy reviews |
| Creative Voltage | Syne + Space Mono | electric blue, neon yellow, deep navy | halftone textures, badges, punchy contrast | creative studios, brand work |
| Dark Botanical | Cormorant + IBM Plex Sans | near-black, ivory, blush, gold, terracotta | blurred abstract circles, fine rules, restrained motion | luxury, premium narratives |
| Notebook Tabs | Bodoni Moda + DM Sans | cream paper on charcoal, pastel tabs | paper sheet, colored side tabs, binder details | reports, structured storytelling |
| Pastel Geometry | Plus Jakarta Sans | pale blue, cream card, pink/mint/lavender | vertical pills, rounded cards, soft shadows | product overviews, onboarding |
| Split Pastel | Outfit | peach + lavender split, mint badges | split backdrop, rounded tags, light grid overlays | agency intros, workshops |
| Vintage Editorial | Fraunces + Work Sans | cream, charcoal, dusty warm accents | geometric accents, bordered callouts, serif headlines | personal brands, opinionated talks |
| Neon Cyber | Clash Display + Satoshi | midnight navy, cyan, magenta | glow, particles, grids, data-radar energy | AI, infra, dev tools |
| Terminal Green | JetBrains Mono | GitHub dark + terminal green | scan lines, CLI framing, monospace rhythm | APIs, CLI tools, engineering demos |
| Swiss Modern | Archivo + Nunito | white, black, signal red | visible grids, asymmetry, geometric discipline | corporate, analytics |
| Paper & Ink | Cormorant Garamond + Source Serif 4 | warm cream, charcoal, crimson accent | pull quotes, drop caps, elegant rules | essays, manifesto decks |

Mood shortcuts: confident/impressed -> Bold Signal, Electric Studio, Dark Botanical; energized -> Creative Voltage, Neon Cyber, Split Pastel; calm/focused -> Notebook Tabs, Paper & Ink, Swiss Modern; inspired -> Dark Botanical, Vintage Editorial, Pastel Geometry.

Motion by feel: cinematic -> slow fades, parallax, large scale-ins; techy -> glow, particles, grid motion, scramble text; playful -> springy easing, floating motion; corporate -> subtle 200-300 ms transitions; minimal -> whitespace-first restraint; editorial -> staggered text/image interplay.

## CSS Gotcha: Negated Functions

A minus sign in front of a CSS function is invalid and browsers drop the declaration silently:

```css
/* silently ignored */
right: -clamp(28px, 3.5vw, 44px);
margin-left: -min(10vw, 100px);

/* correct */
right: calc(-1 * clamp(28px, 3.5vw, 44px));
margin-left: calc(-1 * min(10vw, 100px));
```

## Validation Sizes

Check the deck at 1920x1080, 1280x720, 768x1024, 375x667, and 667x375 (landscape phone). No slide should overflow at any of them; the anti-pattern to catch is a fixed-height content box that breaks on short screens.
