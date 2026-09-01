---
name: ios-icon-gen
description: Use when generating PNG icon imagesets (1x/2x/3x plus Contents.json) for Xcode asset catalogs, from SF Symbols (macOS, offline) or the Iconify API (275k+ open-source icons). Covers the bundled generator scripts, Iconify collection prefixes, and common SF Symbol names.
---

# iOS Icon Generator

Generate Xcode-compatible PNG imagesets from two sources. Both produce the same output structure:

```
<output-dir>/<asset-name>.imageset/
  Contents.json
  <asset-name>.png        # 1x (68px default)
  <asset-name>@2x.png     # 2x (136px)
  <asset-name>@3x.png     # 3x (204px)
```

| Source | Icons | Requires | Best for |
|--------|-------|----------|----------|
| Iconify API | 275,000+ from 200+ collections | Internet | Wide selection, specific styles |
| SF Symbols | 5,000+ Apple symbols | macOS only | Apple-native style, offline |

Scripts live in this skill's `scripts/` directory (`$SKILL_DIR` below).

## Workflow

### 1. Match existing style first

Check dimensions/color/weight of icons already in the project:

```bash
sips -g pixelWidth -g pixelHeight path/to/existing@2x.png
```

### 2. Search

Iconify:

```bash
$SKILL_DIR/scripts/iconify_gen.sh search "receipt"
$SKILL_DIR/scripts/iconify_gen.sh search "business card" --prefix mdi
$SKILL_DIR/scripts/iconify_gen.sh collections
```

SF Symbols — browse the SF Symbols app, or common names:

| Use Case | Symbol Name |
|----------|-------------|
| Document | `doc.text`, `doc.fill` |
| Receipt | `doc.text.below.ecg`, `receipt` |
| Person | `person.crop.rectangle`, `person.text.rectangle` |
| Camera | `camera`, `camera.fill` |
| Scan | `doc.viewfinder`, `qrcode.viewfinder` |
| Settings | `gearshape`, `slider.horizontal.3` |

### 3. Preview (optional)

```bash
$SKILL_DIR/scripts/iconify_gen.sh preview mdi:receipt-text-outline
```

### 4. Generate

Iconify:

```bash
$SKILL_DIR/scripts/iconify_gen.sh mdi:receipt-text-outline editTool_expenseReport
$SKILL_DIR/scripts/iconify_gen.sh mdi:receipt-text-outline myIcon --color 007AFF --output ./Assets.xcassets/icons
```

Options: `--size <pt>` (default 68), `--color <hex>` (default 8E8E93), `--output <dir>` (default /tmp/icons)

SF Symbols:

```bash
swift $SKILL_DIR/scripts/generate_icons.swift doc.text.below.ecg editTool_expenseReport
swift $SKILL_DIR/scripts/generate_icons.swift person.crop.rectangle myIcon --color 007AFF --weight regular --output ./Assets.xcassets/icons
```

Options: `--size <pt>` (default 68), `--color <hex>` (default 8E8E93), `--weight <name>` (default thin), `--output <dir>` (default /tmp/icons)

### 5. Verify and integrate

1. Read the generated @2x PNG to verify visually.
2. Copy into the asset catalog if not generated there directly:
   ```bash
   cp -r /tmp/icons/<name>.imageset path/to/Assets.xcassets/<group>/
   ```
3. Build the project to confirm Xcode picks up the assets.

## Popular Iconify Collections

| Prefix | Name | Count | Style |
|--------|------|-------|-------|
| `mdi` | Material Design Icons | 7400+ | Filled + outline variants |
| `ph` | Phosphor | 9000+ | 6 weights per icon |
| `solar` | Solar | 7400+ | Bold, linear, outline |
| `tabler` | Tabler Icons | 6000+ | Consistent stroke width |
| `lucide` | Lucide | 1700+ | Clean, minimal |
| `ri` | Remix Icon | 3100+ | Filled + line variants |
| `carbon` | Carbon | 2400+ | IBM design language |
| `heroicons` | HeroIcons | 1200+ | Tailwind CSS companion |

Browse all: https://icon-sets.iconify.design/ (Iconify API base: https://api.iconify.design)

## Anti-Patterns

- Generating without checking the existing project icon style (size, color, weight)
- Using default colors when the project has a defined palette
- Committing generated icons without visually verifying the @2x PNG
