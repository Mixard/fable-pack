---
name: manim-explainers
description: Use when building short animated technical explainers (graphs, architectures, system diagrams) with Manim. Covers render commands and quality flags, scene structure notes, and a reusable network-graph scene starter.
---

# Manim Explainers

Manim suits technical explainers where motion, structure, and clarity matter more than photorealism: graphs, workflows, architectures, metric progressions.

## Render Commands

```bash
# Low-quality smoke test (480p15) - iterate here first
manim -ql scripts/network_graph_scene.py NetworkGraphExplainer

# Final render (1080p60)
manim -qh scripts/network_graph_scene.py NetworkGraphExplainer

# Save the last frame as a PNG (thumbnail/poster)
manim -s -qh scripts/network_graph_scene.py NetworkGraphExplainer
```

Quality flags: `-ql` 480p15, `-qm` 720p30, `-qh` 1080p60, `-qk` 4K60. `-p` opens the result after rendering. Output lands under `media/videos/<script_name>/<quality>/`.

Render low-quality until composition and timing are stable; only then switch to `-qh`. Default to 16:9 landscape unless vertical is requested.

## Scene Structure

A scene is a class deriving from `Scene` with a `construct(self)` method: build mobjects (`Text`, `Circle`, `CurvedArrow`, `VGroup`), then animate with `self.play(...)` and pause with `self.wait(seconds)`. Multiple animations passed to one `self.play` call run simultaneously.

Notes that keep explainers readable:

- One idea per scene beat; prefer progressive reveal over a full diagram appearing at once.
- Use motion to show state change (nodes pruned, edges added), not to keep the screen busy.
- Group related mobjects in a `VGroup` so a final reposition (`group.animate.shift(...)`) moves them together.
- Labels placed with `.move_to(shape.get_center())` stay attached only if animated together with the shape.
- Show the "before" state, then transform to the "after" state - the contrast carries the explanation.

## Starter Scene

`scripts/network_graph_scene.py` is a working before/after network-graph explainer: a "You" node with gray low-signal edges and green bridge/target edges; the low-signal nodes fade out and a new target node is added. Adapt colors, labels, and layout per topic.
