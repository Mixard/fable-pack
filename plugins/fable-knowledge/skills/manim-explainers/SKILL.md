---
name: manim-explainers
description: Use when building short animated technical explainers (graphs, architectures, system diagrams) with Manim. Covers render commands and quality flags, output paths, and a reusable network-graph scene starter.
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

## Starter Scene

`scripts/network_graph_scene.py` is a working before/after network-graph explainer: a "You" node with gray low-signal edges and green bridge/target edges; the low-signal nodes fade out and a new target node is added. Adapt colors, labels, and layout per topic.
